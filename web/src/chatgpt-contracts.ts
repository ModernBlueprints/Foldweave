import type {
  FolderPlanMemberChange,
  FolderPlanPreviewCounts,
  FolderPlanPreviewV1,
  FolderPlanTreeMember,
  Journey,
  ReviewDisplayStatus,
} from "./contracts";
import { assertPreview } from "./contracts";

export type HostedReviewLifecycle =
  | "reviewing"
  | "revision_failed"
  | "executing"
  | "verified";

export type HostedJobLifecycle =
  | "matching"
  | "planning"
  | "awaiting_clarification"
  | "reviewing"
  | "revising"
  | "revision_failed"
  | "executing"
  | "verified"
  | "stale"
  | "blocked";

export type HostedPlanningBasis = "fresh" | "derivative" | "none";
export type HostedModelTransport =
  | "chatgpt_hosted"
  | "codex_hosted"
  | "none";
export type HostedExecutionOrigin =
  | "gpt_planned"
  | "gpt_revised_from_change_file"
  | "capsule_applied"
  | "none";

export type HostedReviewStatus = ReviewDisplayStatus & {
  lifecycle: HostedReviewLifecycle;
  authorization_context_fingerprint: string;
  planning_basis: HostedPlanningBasis;
  model_transport: HostedModelTransport;
  execution_origin: HostedExecutionOrigin;
  direct_api_used: false;
  direct_budget_reserved: false;
};

export interface HostedVerifiedResult {
  verification: "verified";
  source_unchanged: true;
  complete_file_count: number;
  changed_path_count: number;
  organized_tree_commitment: string;
  change_file_fingerprint: string | null;
}

export interface FoldweaveChatGptReviewV1 {
  schema_version: "foldweave-chatgpt-review.v1";
  state_version: number;
  journey: Journey;
  preview: FolderPlanPreviewV1;
  status: HostedReviewStatus;
  result: HostedVerifiedResult | null;
}

export interface FoldweaveHostedJobStatusV1 {
  schema_version: "foldweave-hosted-job-status.v1";
  job_id: string;
  lifecycle: HostedJobLifecycle;
  job_revision: number;
  proposal_revision: number;
  source_commitment: string;
  request_fingerprint: string;
  planning_basis: HostedPlanningBasis;
  model_transport: HostedModelTransport;
  execution_origin: HostedExecutionOrigin;
  direct_api_used: false;
  direct_budget_reserved: false;
  has_preview: boolean;
  candidate_fingerprint: string | null;
  preview_fingerprint: string | null;
  clarification_question: string | null;
  clarification_question_fingerprint: string | null;
  revision_attempts_remaining: number;
  revision_failure_code: string | null;
  blocker_code: string | null;
}

export interface FoldweaveVerificationResultV1 {
  schema_version: "foldweave-verification-result.v1";
  verification: "verified";
  job_id: string;
  receipt_fingerprint: string;
  organized_tree_commitment: string;
  failed_check_ids: [];
}

export interface FoldweaveOpaqueLocalItemV1 {
  schema_version: "foldweave-local-item-handle.v1";
  handle: string;
  role: "change_file" | "restore_destination";
  display_name: string;
  expires_at: string;
}

export interface FoldweaveChangeFileResultV1 {
  schema_version: "foldweave-change-file-result.v1";
  job_id: string;
  item: FoldweaveOpaqueLocalItemV1 & { role: "change_file" };
  change_file_fingerprint: string;
  originating_receipt_fingerprint: string;
}

export interface FoldweaveReconstructionResultV1 {
  schema_version: "foldweave-reconstruction-result.v1";
  job_id: string;
  item: FoldweaveOpaqueLocalItemV1 & { role: "restore_destination" };
  receipt_fingerprint: string;
  source_commitment: string;
  restored_file_count: number;
  restored_bytes: number;
  restored_empty_directory_count: number;
}

const SHA256 = /^[a-f0-9]{64}$/;
const JOB_ID = /^[a-f0-9]{32}$/;
const OPAQUE_LOCAL_HANDLE = /^fw_[A-Za-z0-9_-]{43}$/;
const OFFSET_TIMESTAMP = /(?:Z|[+-]\d{2}:\d{2})$/;
const PUBLIC_CODE = /^[a-z0-9_:-]{1,128}$/;
const POSIX_ABSOLUTE_PATH = /(?:^|[\s"'(])\/(?!\/)[^\s"')]+/;
const HOME_ABSOLUTE_PATH = /(?:^|[\s"'(])~\//;
const WINDOWS_ABSOLUTE_PATH = /(?:^|[\s"'(])[a-zA-Z]:[\\/]/;
const UNC_ABSOLUTE_PATH = /(?:^|[\s"'(])\\\\[^\\\s]+\\/;
const SECRET_VALUE = /(?:\bsk-(?:proj-)?[a-zA-Z0-9_-]{8,}|\bBearer\s+[a-zA-Z0-9._~-]{8,}|\bfwjc_[a-zA-Z0-9_-]{8,})/;
const COMMON_LOCAL_PATH = /(?:^|[\s"'(])\/(?:Users|Volumes|private|tmp|home)\//;
const FILE_URL = /\bfile:\/{1,3}/i;
const SECRET_KEYS = new Set([
  "apikey",
  "accesstoken",
  "refreshtoken",
  "password",
  "clientsecret",
  "credential",
  "authorizationheader",
  "capabilityid",
  "capabilityexpiresat",
]);
const MAX_BOUNDARY_NODES = 50_000;
const MAX_BOUNDARY_DEPTH = 64;

export function parseHostedReviewEnvelope(value: unknown): FoldweaveChatGptReviewV1 {
  assertNoSensitiveBoundaryData(value);
  const normalized = normalizeHostedReviewEnvelope(value);
  if (
    !isRecord(normalized) ||
    normalized.schema_version !== "foldweave-chatgpt-review.v1"
  ) {
    throw new Error("ChatGPT did not provide a Foldweave review snapshot.");
  }
  if (
    !Number.isInteger(normalized.state_version) ||
    (normalized.state_version as number) < 0 ||
    (normalized.journey !== "organize" && normalized.journey !== "apply") ||
    !isRecord(normalized.status) ||
    !isRecord(normalized.preview)
  ) {
    throw new Error("The Foldweave review snapshot is incomplete.");
  }

  const status = normalized.status;
  if (typeof status.job_id !== "string" || !JOB_ID.test(status.job_id)) {
    throw new Error("The Foldweave review snapshot has no valid job identity.");
  }
  assertPreview(normalized.preview, status.job_id);
  assertHostedPreviewDetails(normalized.preview);
  assertHostedStatus(status, normalized.preview);
  if (normalized.state_version !== status.job_revision) {
    throw new Error("The Foldweave review version differs from its durable job revision.");
  }
  assertHostedResult(normalized.result, status.lifecycle, normalized.preview);
  return normalized as unknown as FoldweaveChatGptReviewV1;
}

export function parseHostedJobStatus(
  value: unknown,
  expectedJobId?: string,
): FoldweaveHostedJobStatusV1 {
  assertNoSensitiveBoundaryData(value);
  const normalized = normalizeHostedJobStatus(value);
  const actualJobId = isRecord(normalized) ? normalized.job_id : undefined;
  if (
    !isRecord(normalized) ||
    normalized.schema_version !== "foldweave-hosted-job-status.v1" ||
    typeof actualJobId !== "string" ||
    !JOB_ID.test(actualJobId) ||
    (expectedJobId !== undefined && actualJobId !== expectedJobId) ||
    !isHostedJobLifecycle(normalized.lifecycle) ||
    !isNonnegativeInteger(normalized.job_revision) ||
    !isNonnegativeInteger(normalized.proposal_revision) ||
    (normalized.proposal_revision as number) > 2 ||
    !isSha256(normalized.source_commitment) ||
    !isSha256(normalized.request_fingerprint) ||
    !isHostedPlanningBasis(normalized.planning_basis) ||
    !isHostedModelTransport(normalized.model_transport) ||
    !isHostedExecutionOrigin(normalized.execution_origin) ||
    !isConsistentHostedProvenance(
      normalized.planning_basis,
      normalized.model_transport,
      normalized.execution_origin,
    ) ||
    normalized.direct_api_used !== false ||
    normalized.direct_budget_reserved !== false ||
    typeof normalized.has_preview !== "boolean" ||
    !isNullableSha256(normalized.candidate_fingerprint) ||
    !isNullableSha256(normalized.preview_fingerprint) ||
    !isNullableBoundedString(normalized.clarification_question, 1_000) ||
    !isNullableSha256(normalized.clarification_question_fingerprint) ||
    !isNonnegativeInteger(normalized.revision_attempts_remaining) ||
    (normalized.revision_attempts_remaining as number) > 2 ||
    !isNullablePublicCode(normalized.revision_failure_code) ||
    !isNullablePublicCode(normalized.blocker_code)
  ) {
    throw new Error("Foldweave did not return a valid durable hosted status.");
  }
  if (
    normalized.has_preview !== (normalized.preview_fingerprint !== null) ||
    normalized.has_preview !== (normalized.candidate_fingerprint !== null) ||
    (normalized.clarification_question === null) !==
      (normalized.clarification_question_fingerprint === null)
  ) {
    throw new Error("Foldweave returned a contradictory durable hosted status.");
  }
  return normalized as unknown as FoldweaveHostedJobStatusV1;
}

function normalizeHostedReviewEnvelope(value: unknown): unknown {
  if (!isRecord(value) || value.schema_version !== "foldweave-chatgpt-review.v1") {
    return value;
  }
  const normalized = withMissingNullFields(value, ["result"]);
  if (isRecord(value.preview)) {
    normalized.preview = withMissingNullFields(value.preview, [
      "imported_change_file_fingerprint",
      "match_report_fingerprint",
      "immediate_parent_candidate_fingerprint",
    ]);
  }
  if (isRecord(value.status)) {
    normalized.status = withMissingNullFields(value.status, ["revision_failure"]);
  }
  if (isRecord(value.result)) {
    normalized.result = withMissingNullFields(value.result, [
      "change_file_fingerprint",
    ]);
  }
  return normalized;
}

function normalizeHostedJobStatus(value: unknown): unknown {
  if (!isRecord(value) || value.schema_version !== "foldweave-hosted-job-status.v1") {
    return value;
  }
  return withMissingNullFields(value, [
    "candidate_fingerprint",
    "preview_fingerprint",
    "clarification_question",
    "clarification_question_fingerprint",
    "revision_failure_code",
    "blocker_code",
  ]);
}

function withMissingNullFields(
  value: Record<string, unknown>,
  fields: readonly string[],
): Record<string, unknown> {
  const normalized = { ...value };
  for (const field of fields) {
    if (!Object.prototype.hasOwnProperty.call(normalized, field)) {
      normalized[field] = null;
    }
  }
  return normalized;
}

export function parseHostedVerificationResult(
  value: unknown,
  expectedJobId: string,
  expectedOrganizedTreeCommitment: string,
): FoldweaveVerificationResultV1 {
  assertNoSensitiveBoundaryData(value);
  if (
    !isRecord(value) ||
    value.schema_version !== "foldweave-verification-result.v1" ||
    value.verification !== "verified" ||
    value.job_id !== expectedJobId ||
    !JOB_ID.test(expectedJobId) ||
    !isSha256(value.receipt_fingerprint) ||
    value.organized_tree_commitment !== expectedOrganizedTreeCommitment ||
    !SHA256.test(expectedOrganizedTreeCommitment) ||
    !Array.isArray(value.failed_check_ids) ||
    value.failed_check_ids.length !== 0
  ) {
    throw new Error("Foldweave did not return matching verification evidence.");
  }
  return value as unknown as FoldweaveVerificationResultV1;
}

export function parseHostedChangeFileResult(
  value: unknown,
  expectedJobId: string,
  expectedChangeFileFingerprint: string,
): FoldweaveChangeFileResultV1 {
  assertNoSensitiveBoundaryData(value);
  if (
    !isRecord(value) ||
    value.schema_version !== "foldweave-change-file-result.v1" ||
    value.job_id !== expectedJobId ||
    !JOB_ID.test(expectedJobId) ||
    value.change_file_fingerprint !== expectedChangeFileFingerprint ||
    !isSha256(expectedChangeFileFingerprint) ||
    !isSha256(value.originating_receipt_fingerprint) ||
    !isOpaqueLocalItem(value.item, "change_file")
  ) {
    throw new Error("Foldweave did not return the verified Change File identity.");
  }
  return value as unknown as FoldweaveChangeFileResultV1;
}

export function parseHostedReconstructionResult(
  value: unknown,
  expectedJobId: string,
  expectedSourceCommitment: string,
  expectedFileCount: number,
): FoldweaveReconstructionResultV1 {
  assertNoSensitiveBoundaryData(value);
  if (
    !isRecord(value) ||
    value.schema_version !== "foldweave-reconstruction-result.v1" ||
    value.job_id !== expectedJobId ||
    !JOB_ID.test(expectedJobId) ||
    !isOpaqueLocalItem(value.item, "restore_destination") ||
    !isSha256(value.receipt_fingerprint) ||
    value.source_commitment !== expectedSourceCommitment ||
    !isSha256(expectedSourceCommitment) ||
    value.restored_file_count !== expectedFileCount ||
    !Number.isInteger(expectedFileCount) ||
    expectedFileCount < 1 ||
    !isNonnegativeInteger(value.restored_bytes) ||
    !isNonnegativeInteger(value.restored_empty_directory_count)
  ) {
    throw new Error("Foldweave did not return verified reconstruction evidence.");
  }
  return value as unknown as FoldweaveReconstructionResultV1;
}

function isOpaqueLocalItem(
  value: unknown,
  expectedRole: FoldweaveOpaqueLocalItemV1["role"],
): value is FoldweaveOpaqueLocalItemV1 {
  if (
    !isRecord(value) ||
    value.schema_version !== "foldweave-local-item-handle.v1" ||
    !OPAQUE_LOCAL_HANDLE.test(String(value.handle)) ||
    value.role !== expectedRole ||
    typeof value.display_name !== "string" ||
    value.display_name.length < 1 ||
    value.display_name.length > 255 ||
    typeof value.expires_at !== "string" ||
    !OFFSET_TIMESTAMP.test(value.expires_at) ||
    !Number.isFinite(Date.parse(value.expires_at))
  ) {
    return false;
  }
  return true;
}

export function assertNoSensitiveBoundaryData(value: unknown): void {
  const visited = new WeakSet<object>();
  let visitedNodes = 0;

  const inspect = (candidate: unknown, depth: number): void => {
    visitedNodes += 1;
    if (visitedNodes > MAX_BOUNDARY_NODES || depth > MAX_BOUNDARY_DEPTH) {
      throw new Error("The ChatGPT review payload exceeds Foldweave's safe display bounds.");
    }
    if (typeof candidate === "string") {
      if (
        POSIX_ABSOLUTE_PATH.test(candidate) ||
        HOME_ABSOLUTE_PATH.test(candidate) ||
        UNC_ABSOLUTE_PATH.test(candidate) ||
        WINDOWS_ABSOLUTE_PATH.test(candidate) ||
        COMMON_LOCAL_PATH.test(candidate) ||
        FILE_URL.test(candidate)
      ) {
        throw new Error("Foldweave blocked a local absolute path at the ChatGPT boundary.");
      }
      if (SECRET_VALUE.test(candidate)) {
        throw new Error("Foldweave blocked credential-like data at the ChatGPT boundary.");
      }
      return;
    }
    if (typeof candidate !== "object" || candidate === null) {
      return;
    }
    if (visited.has(candidate)) {
      throw new Error("The ChatGPT review payload contains an unsupported object cycle.");
    }
    visited.add(candidate);
    if (Array.isArray(candidate)) {
      candidate.forEach((item) => inspect(item, depth + 1));
      return;
    }
    for (const [key, item] of Object.entries(candidate)) {
      const normalizedKey = key.toLocaleLowerCase().replace(/[^a-z0-9]/g, "");
      if (SECRET_KEYS.has(normalizedKey)) {
        throw new Error("Foldweave blocked a credential field at the ChatGPT boundary.");
      }
      inspect(item, depth + 1);
    }
  };

  inspect(value, 0);
}

function assertHostedStatus(
  value: Record<string, unknown>,
  preview: FolderPlanPreviewV1,
): asserts value is Record<string, unknown> & HostedReviewStatus {
  const lifecycle = value.lifecycle;
  if (
    lifecycle !== "reviewing" &&
    lifecycle !== "revision_failed" &&
    lifecycle !== "executing" &&
    lifecycle !== "verified"
  ) {
    throw new Error("The Foldweave review has an unsupported lifecycle state.");
  }
  if (
    !Number.isInteger(value.job_revision) ||
    !Number.isInteger(value.proposal_revision) ||
    value.proposal_revision !== preview.proposal_revision ||
    value.candidate_fingerprint !== preview.compiled_candidate_fingerprint ||
    value.preview_fingerprint !== preview.preview_fingerprint ||
    typeof value.authorization_context_fingerprint !== "string" ||
    !SHA256.test(value.authorization_context_fingerprint) ||
    !isHostedPlanningBasis(value.planning_basis) ||
    !isHostedModelTransport(value.model_transport) ||
    !isHostedExecutionOrigin(value.execution_origin) ||
    !isConsistentHostedProvenance(
      value.planning_basis,
      value.model_transport,
      value.execution_origin,
    ) ||
    value.direct_api_used !== false ||
    value.direct_budget_reserved !== false ||
    typeof value.revision_available !== "boolean" ||
    !Number.isInteger(value.revision_attempts_remaining) ||
    (value.revision_attempts_remaining as number) < 0 ||
    (value.revision_attempts_remaining as number) > 2 ||
    (value.revision_failure !== null &&
      typeof value.revision_failure !== "string")
  ) {
    throw new Error("The Foldweave review status does not match its exact preview.");
  }
  if (
    (lifecycle === "reviewing" || lifecycle === "revision_failed") &&
    value.job_revision !== preview.expected_job_revision
  ) {
    throw new Error("The reviewable Foldweave job revision differs from its preview.");
  }
  if (
    (lifecycle === "executing" || lifecycle === "verified") &&
    (value.job_revision as number) <= preview.expected_job_revision
  ) {
    throw new Error("The executed Foldweave job did not advance beyond authorization.");
  }
  if (
    (lifecycle === "executing" || lifecycle === "verified") &&
    value.revision_available !== false
  ) {
    throw new Error("A non-reviewing Foldweave job cannot advertise another revision.");
  }
  const reviewable = lifecycle === "reviewing" || lifecycle === "revision_failed";
  const expectedRevisionAvailable =
    reviewable && (value.revision_attempts_remaining as number) > 0;
  if (value.revision_available !== expectedRevisionAvailable) {
    throw new Error("The Foldweave revision allowance contradicts the durable state.");
  }
  if ((lifecycle === "revision_failed") !== (value.revision_failure !== null)) {
    throw new Error("The Foldweave revision-failure state is incomplete.");
  }
}

function assertHostedResult(
  value: unknown,
  lifecycle: HostedReviewLifecycle,
  preview: FolderPlanPreviewV1,
): void {
  if (lifecycle !== "verified") {
    if (value !== null) {
      throw new Error("An unverified Foldweave job cannot expose a verified result.");
    }
    return;
  }
  if (
    !isRecord(value) ||
    value.verification !== "verified" ||
    value.source_unchanged !== true ||
    !isNonnegativeInteger(value.complete_file_count) ||
    !isNonnegativeInteger(value.changed_path_count) ||
    value.complete_file_count !== preview.counts.file_count ||
    value.changed_path_count !== preview.counts.changed_path_count ||
    typeof value.organized_tree_commitment !== "string" ||
    !SHA256.test(value.organized_tree_commitment) ||
    (value.change_file_fingerprint !== null &&
      (typeof value.change_file_fingerprint !== "string" ||
        !SHA256.test(value.change_file_fingerprint)))
  ) {
    throw new Error("The verified Foldweave result summary is incomplete.");
  }
}

function assertHostedPreviewDetails(preview: FolderPlanPreviewV1): void {
  if (
    !preview.current_tree_members.every(isTreeMember) ||
    !preview.proposed_tree_members.every(isTreeMember) ||
    !preview.member_changes.every(isMemberChange) ||
    !preview.supported_link_effects.every(isLinkEffect) ||
    !preview.collision_findings.every((finding) => isFinding(finding, "collision")) ||
    !preview.blocker_findings.every((finding) => isFinding(finding, "blocker")) ||
    !isPreviewCounts(preview.counts)
  ) {
    throw new Error("The Foldweave preview contains an invalid member or link record.");
  }

  const currentById = new Map(
    preview.current_tree_members.map((member) => [member.member_id, member]),
  );
  const proposedById = new Map(
    preview.proposed_tree_members.map((member) => [member.member_id, member]),
  );
  const changeById = new Map(
    preview.member_changes.map((change) => [change.member_id, change]),
  );
  const currentPaths = new Set(
    preview.current_tree_members.map((member) => member.relative_path),
  );
  const proposedPaths = new Set(
    preview.proposed_tree_members.map((member) => member.relative_path),
  );
  if (
    currentById.size !== preview.current_tree_members.length ||
    proposedById.size !== preview.proposed_tree_members.length ||
    changeById.size !== preview.member_changes.length ||
    currentPaths.size !== preview.current_tree_members.length ||
    proposedPaths.size !== preview.proposed_tree_members.length ||
    currentById.size !== proposedById.size ||
    currentById.size !== changeById.size ||
    [...currentById].some(
      ([memberId]) => !proposedById.has(memberId) || !changeById.has(memberId),
    )
  ) {
    throw new Error("The Foldweave preview does not account for every member exactly once.");
  }

  if (
    !isOrderedBy(preview.current_tree_members, (member) => member.relative_path) ||
    !isOrderedBy(preview.proposed_tree_members, (member) => member.relative_path) ||
    !isOrderedBy(preview.member_changes, (change) => change.current_relative_path) ||
    !isOrderedBy(
      preview.supported_link_effects,
      (effect) => `${effect.current_source_path}\u0000${effect.reference_id}`,
    )
  ) {
    throw new Error("The Foldweave preview is not deterministically ordered.");
  }

  for (const [memberId, change] of changeById) {
    const current = currentById.get(memberId)!;
    const proposed = proposedById.get(memberId)!;
    if (
      current.member_kind !== change.member_kind ||
      proposed.member_kind !== change.member_kind ||
      current.relative_path !== change.current_relative_path ||
      proposed.relative_path !== change.proposed_relative_path ||
      current.protected !== change.protected ||
      proposed.protected !== change.protected ||
      !sameStrings(current.directory_prefixes, directoryPrefixes(current.relative_path)) ||
      !sameStrings(proposed.directory_prefixes, directoryPrefixes(proposed.relative_path))
    ) {
      throw new Error("The Foldweave preview does not reconcile both structure views.");
    }
    const expectedClassification = classifyChange(change);
    if (change.change_classification !== expectedClassification) {
      throw new Error("A Foldweave change classification differs from its exact paths.");
    }
    if (
      change.member_kind === "empty_directory" &&
      (!change.protected ||
        change.authority_source !== "protected" ||
        change.current_relative_path !== change.proposed_relative_path)
    ) {
      throw new Error("Explicit empty directories must remain protected and unchanged.");
    }
    if (change.protected !== (change.authority_source === "protected")) {
      throw new Error("Foldweave protection and member authority disagree.");
    }
  }

  const effectsBySource = new Map<string, typeof preview.supported_link_effects>();
  const effectIds = new Set<string>();
  for (const effect of preview.supported_link_effects) {
    if (effectIds.has(effect.reference_id)) {
      throw new Error("Foldweave link effects must have unique identities.");
    }
    effectIds.add(effect.reference_id);
    const sourceCurrent = currentById.get(effect.source_member_id);
    const sourceProposed = proposedById.get(effect.source_member_id);
    const targetCurrent = currentById.get(effect.target_member_id);
    const targetProposed = proposedById.get(effect.target_member_id);
    if (
      sourceCurrent === undefined ||
      sourceProposed === undefined ||
      targetCurrent === undefined ||
      targetProposed === undefined ||
      effect.current_source_path !== sourceCurrent.relative_path ||
      effect.proposed_source_path !== sourceProposed.relative_path ||
      effect.current_target_path !== targetCurrent.relative_path ||
      effect.proposed_target_path !== targetProposed.relative_path
    ) {
      throw new Error("A Foldweave link effect does not reconcile both structures.");
    }
    effectsBySource.set(effect.source_member_id, [
      ...(effectsBySource.get(effect.source_member_id) ?? []),
      effect,
    ]);
  }

  for (const [memberId, change] of changeById) {
    const outgoing = effectsBySource.get(memberId) ?? [];
    const expectedIds = outgoing.map((effect) => effect.reference_id).sort(compareStrings);
    if (
      !sameStrings(change.supported_link_effect_ids, expectedIds) ||
      change.link_updated !== outgoing.some((effect) => effect.status === "rewritten")
    ) {
      throw new Error("A Foldweave member link summary is incomplete.");
    }
  }

  for (const finding of [
    ...preview.collision_findings,
    ...preview.blocker_findings,
  ]) {
    if (finding.member_ids.some((memberId) => !currentById.has(memberId))) {
      throw new Error("A Foldweave finding refers to a member outside the preview.");
    }
  }

  const regularChanges = preview.member_changes.filter(
    (change) => change.member_kind === "regular_file",
  );
  const changed = regularChanges.filter(
    (change) => change.current_relative_path !== change.proposed_relative_path,
  );
  const expectedCounts: FolderPlanPreviewCounts = {
    file_count: regularChanges.length,
    empty_directory_count: preview.member_changes.length - regularChanges.length,
    changed_path_count: changed.length,
    renamed_count: changed.filter(
      (change) => basename(change.current_relative_path) !== basename(change.proposed_relative_path),
    ).length,
    moved_count: changed.filter(
      (change) => parentPath(change.current_relative_path) !== parentPath(change.proposed_relative_path),
    ).length,
    link_count: preview.supported_link_effects.length,
    link_updated_count: preview.supported_link_effects.filter(
      (effect) => effect.status === "rewritten",
    ).length,
    protected_count: regularChanges.filter((change) => change.protected).length,
    blocker_count: preview.blocker_findings.length,
  };
  if (
    (Object.keys(expectedCounts) as Array<keyof FolderPlanPreviewCounts>).some(
      (key) => preview.counts[key] !== expectedCounts[key],
    )
  ) {
    throw new Error("The Foldweave preview counts differ from its complete contents.");
  }
}

function isTreeMember(value: unknown): value is FolderPlanTreeMember {
  return (
    isRecord(value) &&
    typeof value.member_id === "string" &&
    SHA256.test(value.member_id) &&
    (value.member_kind === "regular_file" || value.member_kind === "empty_directory") &&
    isSafeRelativePath(value.relative_path) &&
    Array.isArray(value.directory_prefixes) &&
    value.directory_prefixes.every(isSafeRelativePath) &&
    typeof value.protected === "boolean"
  );
}

function isMemberChange(value: unknown): value is FolderPlanMemberChange {
  return (
    isRecord(value) &&
    typeof value.member_id === "string" &&
    SHA256.test(value.member_id) &&
    (value.member_kind === "regular_file" || value.member_kind === "empty_directory") &&
    isSafeRelativePath(value.current_relative_path) &&
    isSafeRelativePath(value.proposed_relative_path) &&
    (value.change_classification === "unchanged" ||
      value.change_classification === "renamed" ||
      value.change_classification === "moved" ||
      value.change_classification === "moved_and_renamed" ||
      value.change_classification === "protected" ||
      value.change_classification === "empty_directory") &&
    typeof value.protected === "boolean" &&
    (value.authority_source === "gpt_plan" ||
      value.authority_source === "change_file" ||
      value.authority_source === "protected") &&
    typeof value.rationale === "string" &&
    value.rationale.length > 0 &&
    value.rationale.length <= 1_000 &&
    typeof value.link_updated === "boolean" &&
    Array.isArray(value.supported_link_effect_ids) &&
    value.supported_link_effect_ids.every(
      (item) => typeof item === "string" && SHA256.test(item),
    )
  );
}

function isLinkEffect(value: unknown): value is FolderPlanPreviewV1["supported_link_effects"][number] {
  return (
    isRecord(value) &&
    isSha256(value.reference_id) &&
    isSha256(value.source_member_id) &&
    isSha256(value.target_member_id) &&
    isSafeRelativePath(value.current_source_path) &&
    isSafeRelativePath(value.current_target_path) &&
    isSafeRelativePath(value.proposed_source_path) &&
    isSafeRelativePath(value.proposed_target_path) &&
    typeof value.original_destination === "string" &&
    value.original_destination.length > 0 &&
    value.original_destination.length <= 8_192 &&
    typeof value.proposed_destination === "string" &&
    value.proposed_destination.length > 0 &&
    value.proposed_destination.length <= 8_192 &&
    (value.status === "unchanged" || value.status === "rewritten")
  );
}

function isFinding(
  value: unknown,
  severity: "collision" | "blocker",
): boolean {
  return (
    isRecord(value) &&
    typeof value.finding_id === "string" &&
    PUBLIC_CODE.test(value.finding_id) &&
    value.severity === severity &&
    typeof value.detail === "string" &&
    value.detail.length > 0 &&
    value.detail.length <= 2_000 &&
    Array.isArray(value.member_ids) &&
    value.member_ids.every(isSha256)
  );
}

function isPreviewCounts(value: unknown): value is FolderPlanPreviewCounts {
  if (!isRecord(value)) {
    return false;
  }
  const keys: Array<keyof FolderPlanPreviewCounts> = [
    "file_count",
    "empty_directory_count",
    "changed_path_count",
    "renamed_count",
    "moved_count",
    "link_count",
    "link_updated_count",
    "protected_count",
    "blocker_count",
  ];
  return (
    keys.every((key) => isNonnegativeInteger(value[key])) &&
    (value.file_count as number) >= 1 &&
    (value.file_count as number) <= 500 &&
    (value.empty_directory_count as number) <= 1_000 &&
    (value.changed_path_count as number) <= 500 &&
    (value.renamed_count as number) <= 500 &&
    (value.moved_count as number) <= 500 &&
    (value.protected_count as number) <= 500
  );
}

function isSafeRelativePath(value: unknown): value is string {
  if (
    typeof value !== "string" ||
    value.length === 0 ||
    value.length > 4_096 ||
    value.includes("\0")
  ) {
    return false;
  }
  const parts = value.split("/");
  return parts.every((part) => part.length > 0 && part !== "." && part !== "..");
}

function classifyChange(change: FolderPlanMemberChange): FolderPlanMemberChange["change_classification"] {
  if (change.member_kind === "empty_directory") {
    return "empty_directory";
  }
  if (change.protected) {
    return "protected";
  }
  if (change.current_relative_path === change.proposed_relative_path) {
    return "unchanged";
  }
  const renamed = basename(change.current_relative_path) !== basename(change.proposed_relative_path);
  const moved = parentPath(change.current_relative_path) !== parentPath(change.proposed_relative_path);
  if (renamed && moved) {
    return "moved_and_renamed";
  }
  return renamed ? "renamed" : "moved";
}

function directoryPrefixes(relativePath: string): string[] {
  const parts = relativePath.split("/").slice(0, -1);
  return parts.map((_, index) => parts.slice(0, index + 1).join("/"));
}

function basename(relativePath: string): string {
  return relativePath.split("/").at(-1) ?? relativePath;
}

function parentPath(relativePath: string): string {
  return relativePath.split("/").slice(0, -1).join("/");
}

function sameStrings(left: readonly string[], right: readonly string[]): boolean {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function isOrderedBy<T>(items: readonly T[], selector: (item: T) => string): boolean {
  return items.every(
    (item, index) => index === 0 || compareStrings(selector(items[index - 1]!), selector(item)) <= 0,
  );
}

function compareStrings(left: string, right: string): number {
  const leftCodePoints = Array.from(left, (value) => value.codePointAt(0)!);
  const rightCodePoints = Array.from(right, (value) => value.codePointAt(0)!);
  const count = Math.min(leftCodePoints.length, rightCodePoints.length);
  for (let index = 0; index < count; index += 1) {
    if (leftCodePoints[index] !== rightCodePoints[index]) {
      return leftCodePoints[index]! - rightCodePoints[index]!;
    }
  }
  return leftCodePoints.length - rightCodePoints.length;
}

function isHostedPlanningBasis(value: unknown): value is HostedPlanningBasis {
  return value === "fresh" || value === "derivative" || value === "none";
}

function isHostedModelTransport(value: unknown): value is HostedModelTransport {
  return (
    value === "chatgpt_hosted" || value === "codex_hosted" || value === "none"
  );
}

function isHostedExecutionOrigin(value: unknown): value is HostedExecutionOrigin {
  return (
    value === "gpt_planned" ||
    value === "gpt_revised_from_change_file" ||
    value === "capsule_applied" ||
    value === "none"
  );
}

function isConsistentHostedProvenance(
  planningBasis: HostedPlanningBasis,
  modelTransport: HostedModelTransport,
  executionOrigin: HostedExecutionOrigin,
): boolean {
  if (planningBasis === "none") {
    return modelTransport === "none" && executionOrigin === "capsule_applied";
  }
  if (modelTransport === "none") {
    return false;
  }
  if (planningBasis === "fresh") {
    return executionOrigin === "none" || executionOrigin === "gpt_planned";
  }
  return (
    executionOrigin === "none" ||
    executionOrigin === "gpt_revised_from_change_file"
  );
}

function isHostedJobLifecycle(value: unknown): value is HostedJobLifecycle {
  return (
    value === "matching" ||
    value === "planning" ||
    value === "awaiting_clarification" ||
    value === "reviewing" ||
    value === "revising" ||
    value === "revision_failed" ||
    value === "executing" ||
    value === "verified" ||
    value === "stale" ||
    value === "blocked"
  );
}

function isSha256(value: unknown): value is string {
  return typeof value === "string" && SHA256.test(value);
}

function isNullableSha256(value: unknown): value is string | null {
  return value === null || isSha256(value);
}

function isNullablePublicCode(value: unknown): value is string | null {
  return value === null || (typeof value === "string" && PUBLIC_CODE.test(value));
}

function isNullableBoundedString(value: unknown, maxLength: number): value is string | null {
  return value === null ||
    (typeof value === "string" && value.length > 0 && value.length <= maxLength);
}

function isNonnegativeInteger(value: unknown): value is number {
  return Number.isInteger(value) && (value as number) >= 0;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

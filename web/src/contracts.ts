export type Journey = "organize" | "apply";
export type ViewSide = "current" | "proposed";

export type MemberKind = "regular_file" | "empty_directory";

export type ChangeClassification =
  | "unchanged"
  | "renamed"
  | "moved"
  | "moved_and_renamed"
  | "protected"
  | "empty_directory";

export interface FolderPlanTreeMember {
  member_id: string;
  member_kind: MemberKind;
  relative_path: string;
  directory_prefixes: string[];
  protected: boolean;
}

export interface FolderPlanLinkEffect {
  reference_id: string;
  source_member_id: string;
  target_member_id: string;
  current_source_path: string;
  current_target_path: string;
  proposed_source_path: string;
  proposed_target_path: string;
  original_destination: string;
  proposed_destination: string;
  status: "unchanged" | "rewritten";
}

export interface FolderPlanMemberChange {
  member_id: string;
  member_kind: MemberKind;
  current_relative_path: string;
  proposed_relative_path: string;
  change_classification: ChangeClassification;
  protected: boolean;
  authority_source: "gpt_plan" | "change_file" | "protected";
  rationale: string;
  link_updated: boolean;
  supported_link_effect_ids: string[];
}

export interface FolderPlanFinding {
  finding_id: string;
  severity: "collision" | "blocker";
  detail: string;
  member_ids: string[];
}

export interface FolderPlanPreviewCounts {
  file_count: number;
  empty_directory_count: number;
  changed_path_count: number;
  renamed_count: number;
  moved_count: number;
  link_count: number;
  link_updated_count: number;
  protected_count: number;
  blocker_count: number;
}

export interface FolderPlanPreviewV1 {
  schema_version: "folder-plan-preview.v1";
  job_id: string;
  expected_job_revision: number;
  proposal_revision: number;
  proposal_basis:
    | "fresh_gpt_plan"
    | "imported_change_file"
    | "gpt_derivative";
  source_commitment: string;
  imported_change_file_fingerprint: string | null;
  match_report_fingerprint: string | null;
  immediate_parent_candidate_fingerprint: string | null;
  current_tree_members: FolderPlanTreeMember[];
  proposed_tree_members: FolderPlanTreeMember[];
  member_changes: FolderPlanMemberChange[];
  supported_link_effects: FolderPlanLinkEffect[];
  collision_findings: FolderPlanFinding[];
  blocker_findings: FolderPlanFinding[];
  counts: FolderPlanPreviewCounts;
  compiled_candidate_fingerprint: string;
  preview_fingerprint: string;
}

export interface ReviewStatus {
  job_id: string;
  lifecycle: string;
  job_revision: number;
  proposal_revision: number;
  candidate_fingerprint: string;
  preview_fingerprint: string;
  output_parent: string;
  result_folder_name: string;
  revision_available: boolean;
  revision_attempts_remaining: number;
  revision_failure: string | null;
  done_url: string | null;
}

export interface AcceptancePayload {
  candidate_fingerprint: string;
  expected_revision: number;
  idempotency_key: string;
  output_parent: string;
  preview_fingerprint: string;
  result_folder_name: string;
}

export interface RevisionPayload {
  candidate_fingerprint: string;
  expected_revision: number;
  idempotency_key: string;
  instruction: string;
  preview_fingerprint: string;
}

export interface KeepProposalPayload {
  candidate_fingerprint: string;
  expected_revision: number;
  idempotency_key: string;
  preview_fingerprint: string;
}

const SHA256 = /^[a-f0-9]{64}$/;
const JOB_ID = /^[a-f0-9]{32}$/;

export function assertPreview(
  value: unknown,
  expectedJobId: string,
): asserts value is FolderPlanPreviewV1 {
  if (!isRecord(value)) {
    throw new Error("Foldweave returned an invalid preview object.");
  }
  if (
    value.schema_version !== "folder-plan-preview.v1" ||
    value.job_id !== expectedJobId ||
    !matchesPattern(value.job_id, JOB_ID) ||
    !matchesPattern(value.source_commitment, SHA256) ||
    !matchesPattern(value.compiled_candidate_fingerprint, SHA256) ||
    !matchesPattern(value.preview_fingerprint, SHA256) ||
    !Number.isInteger(value.expected_job_revision) ||
    !Number.isInteger(value.proposal_revision) ||
    !Array.isArray(value.current_tree_members) ||
    !Array.isArray(value.proposed_tree_members) ||
    !Array.isArray(value.member_changes) ||
    !Array.isArray(value.supported_link_effects) ||
    !isRecord(value.counts)
  ) {
    throw new Error("Foldweave returned an incomplete preview contract.");
  }
}

export function assertStatus(
  value: unknown,
  expectedJobId: string,
): asserts value is ReviewStatus {
  if (!isRecord(value)) {
    throw new Error("Foldweave returned an invalid review status.");
  }
  if (
    value.job_id !== expectedJobId ||
    !matchesPattern(value.job_id, JOB_ID) ||
    value.lifecycle !== "reviewing" ||
    !Number.isInteger(value.job_revision) ||
    !Number.isInteger(value.proposal_revision) ||
    !matchesPattern(value.candidate_fingerprint, SHA256) ||
    !matchesPattern(value.preview_fingerprint, SHA256) ||
    typeof value.output_parent !== "string" ||
    value.output_parent.length === 0 ||
    typeof value.result_folder_name !== "string" ||
    value.result_folder_name.length === 0 ||
    typeof value.revision_available !== "boolean" ||
    typeof value.revision_attempts_remaining !== "number" ||
    !Number.isInteger(value.revision_attempts_remaining) ||
    value.revision_attempts_remaining < 0 ||
    value.revision_attempts_remaining > 2 ||
    (value.revision_failure !== null &&
      typeof value.revision_failure !== "string")
  ) {
    throw new Error("Foldweave returned an incomplete review status.");
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function matchesPattern(value: unknown, pattern: RegExp): value is string {
  return typeof value === "string" && pattern.test(value);
}

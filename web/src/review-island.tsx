import {
  Button,
  ButtonGroup,
  Card,
  Checkbox,
  Icon,
  InputGroup,
  Spinner,
  Tag,
} from "@blueprintjs/core";
import {
  type CSSProperties,
  type KeyboardEvent,
  type ReactElement,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";

import type {
  AcceptancePayload,
  ChangeClassification,
  FolderPlanMemberChange,
  FolderPlanPreviewV1,
  FolderPlanTreeMember,
  Journey,
  KeepProposalPayload,
  RevisionPayload,
  ReviewStatus,
  ViewSide,
} from "./contracts";

type FilterKey =
  | "moved"
  | "renamed"
  | "link_updated"
  | "protected"
  | "unchanged"
  | "empty_directory";

interface TreeNode {
  key: string;
  label: string;
  path: string;
  depth: number;
  kind: "directory" | "file";
  memberId: string | null;
  explicitEmptyDirectory: boolean;
  children: TreeNode[];
}

interface PendingMutationKey {
  requestFingerprint: string;
  idempotencyKey: string;
}

export interface ReviewIslandProps {
  preview: FolderPlanPreviewV1;
  status: ReviewStatus;
  journey: Journey;
  acceptPlan: (payload: AcceptancePayload) => Promise<void>;
  revisePlan: (payload: RevisionPayload) => Promise<void>;
  keepPrevious: (payload: KeepProposalPayload) => Promise<void>;
  idempotencyKeyFactory?: () => string;
}

const FILTERS: ReadonlyArray<{ key: FilterKey; label: string }> = [
  { key: "moved", label: "Moved" },
  { key: "renamed", label: "Renamed" },
  { key: "link_updated", label: "Link updated" },
  { key: "protected", label: "Protected" },
  { key: "unchanged", label: "Unchanged" },
  { key: "empty_directory", label: "Empty directory" },
];

const CLASS_LABELS: Record<ChangeClassification, string> = {
  unchanged: "Unchanged",
  renamed: "Renamed",
  moved: "Moved",
  moved_and_renamed: "Moved + renamed",
  protected: "Protected",
  empty_directory: "Empty directory",
};

export function ReviewIsland({
  preview,
  status,
  journey,
  acceptPlan,
  revisePlan,
  keepPrevious,
  idempotencyKeyFactory = createIdempotencyKey,
}: ReviewIslandProps): ReactElement {
  const [side, setSide] = useState<ViewSide>("proposed");
  const [changedOnly, setChangedOnly] = useState(true);
  const [activeFilters, setActiveFilters] = useState<Set<FilterKey>>(new Set());
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(
    preview.member_changes.find(isChanged)?.member_id ??
      preview.member_changes[0]?.member_id ??
      null,
  );
  const [expanded, setExpanded] = useState<Set<string>>(() =>
    initialExpandedPaths(preview),
  );
  const [revisionInstruction, setRevisionInstruction] = useState("");
  const [accepting, setAccepting] = useState(false);
  const [acceptanceError, setAcceptanceError] = useState<string | null>(null);
  const [revisionBusy, setRevisionBusy] = useState(false);
  const [revisionError, setRevisionError] = useState<string | null>(null);
  const [revisionDelta, setRevisionDelta] = useState<string | null>(null);
  const priorPreview = useRef(preview);
  const acceptanceMutation = useRef<PendingMutationKey | null>(null);
  const revisionMutation = useRef<PendingMutationKey | null>(null);
  const keepMutation = useRef<PendingMutationKey | null>(null);
  const revisionInput = useRef<HTMLTextAreaElement | null>(null);
  const treeItemRefs = useRef<Array<HTMLButtonElement | null>>([]);

  const changeById = useMemo(
    () => new Map(preview.member_changes.map((change) => [change.member_id, change])),
    [preview.member_changes],
  );
  const members = side === "current" ? preview.current_tree_members : preview.proposed_tree_members;
  const visibleMembers = useMemo(
    () =>
      members.filter((member) => {
        const change = changeById.get(member.member_id);
        if (!change) {
          return false;
        }
        const normalizedQuery = query.trim().toLocaleLowerCase();
        const matchesQuery =
          normalizedQuery.length === 0 ||
          change.current_relative_path.toLocaleLowerCase().includes(normalizedQuery) ||
          change.proposed_relative_path.toLocaleLowerCase().includes(normalizedQuery);
        if (!matchesQuery) {
          return false;
        }
        if (activeFilters.size > 0) {
          return [...activeFilters].some((filter) => matchesFilter(change, filter));
        }
        return !changedOnly || isChanged(change);
      }),
    [activeFilters, changeById, changedOnly, members, query],
  );
  const tree = useMemo(() => buildTree(visibleMembers), [visibleMembers]);
  const flatTree = useMemo(() => flattenVisibleTree(tree, expanded), [expanded, tree]);
  const selected = selectedId === null ? undefined : changeById.get(selectedId);
  const selectedLinks = useMemo(
    () =>
      selected === undefined
        ? []
        : preview.supported_link_effects.filter(
            (effect) =>
              effect.source_member_id === selected.member_id ||
              effect.target_member_id === selected.member_id,
          ),
    [preview.supported_link_effects, selected],
  );

  useEffect(() => {
    if (selectedId !== null && visibleMembers.some((item) => item.member_id === selectedId)) {
      return;
    }
    setSelectedId(visibleMembers[0]?.member_id ?? null);
  }, [selectedId, visibleMembers]);

  useEffect(() => {
    const previous = priorPreview.current;
    if (previous.preview_fingerprint === preview.preview_fingerprint) {
      return;
    }
    const previousPaths = new Map(
      previous.member_changes.map((change) => [
        change.member_id,
        change.proposed_relative_path,
      ]),
    );
    const changedMappings = preview.member_changes.filter(
      (change) => previousPaths.get(change.member_id) !== change.proposed_relative_path,
    ).length;
    setRevisionDelta(
      `${changedMappings} ${changedMappings === 1 ? "mapping" : "mappings"} changed from the previous proposal.`,
    );
    priorPreview.current = preview;
  }, [preview]);

  const toggleFilter = (filter: FilterKey): void => {
    setChangedOnly(false);
    setActiveFilters((current) => {
      const next = new Set(current);
      if (next.has(filter)) {
        next.delete(filter);
      } else {
        next.add(filter);
      }
      return next;
    });
  };

  const handleTreeKey = (
    event: KeyboardEvent<HTMLButtonElement>,
    index: number,
    node: TreeNode,
  ): void => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      const nextIndex = event.key === "ArrowDown" ? index + 1 : index - 1;
      treeItemRefs.current[nextIndex]?.focus();
      return;
    }
    if (node.kind === "directory" && event.key === "ArrowRight") {
      event.preventDefault();
      setExpanded((current) => new Set(current).add(node.path));
    }
    if (node.kind === "directory" && event.key === "ArrowLeft") {
      event.preventDefault();
      setExpanded((current) => {
        const next = new Set(current);
        next.delete(node.path);
        return next;
      });
    }
  };

  const submitAcceptance = async (): Promise<void> => {
    if (
      accepting ||
      revisionBusy ||
      status.revision_failure !== null ||
      preview.counts.blocker_count > 0
    ) {
      return;
    }
    setAccepting(true);
    setAcceptanceError(null);
    const requestFingerprint = JSON.stringify([
      preview.expected_job_revision,
      preview.compiled_candidate_fingerprint,
      preview.preview_fingerprint,
      status.output_parent,
      status.result_folder_name,
    ]);
    const idempotencyKey = mutationIdempotencyKey(
      acceptanceMutation,
      requestFingerprint,
      idempotencyKeyFactory,
    );
    try {
      await acceptPlan({
        candidate_fingerprint: preview.compiled_candidate_fingerprint,
        expected_revision: preview.expected_job_revision,
        idempotency_key: idempotencyKey,
        output_parent: status.output_parent,
        preview_fingerprint: preview.preview_fingerprint,
        result_folder_name: status.result_folder_name,
      });
      acceptanceMutation.current = null;
    } catch (error) {
      setAcceptanceError(error instanceof Error ? error.message : "Acceptance was blocked.");
      setAccepting(false);
    }
  };

  const submitRevision = async (): Promise<void> => {
    const instruction = revisionInstruction.trim();
    if (
      revisionBusy ||
      accepting ||
      !status.revision_available ||
      instruction.length === 0
    ) {
      return;
    }
    setRevisionBusy(true);
    setRevisionError(null);
    const requestFingerprint = JSON.stringify([
      preview.expected_job_revision,
      preview.compiled_candidate_fingerprint,
      preview.preview_fingerprint,
      instruction,
    ]);
    const idempotencyKey = mutationIdempotencyKey(
      revisionMutation,
      requestFingerprint,
      idempotencyKeyFactory,
    );
    try {
      await revisePlan({
        candidate_fingerprint: preview.compiled_candidate_fingerprint,
        expected_revision: preview.expected_job_revision,
        idempotency_key: idempotencyKey,
        instruction,
        preview_fingerprint: preview.preview_fingerprint,
      });
      revisionMutation.current = null;
      setRevisionInstruction("");
    } catch (error) {
      setRevisionError(error instanceof Error ? error.message : "Revision was blocked.");
    } finally {
      setRevisionBusy(false);
    }
  };

  const submitKeepPrevious = async (): Promise<void> => {
    if (revisionBusy || status.revision_failure === null) {
      return;
    }
    setRevisionBusy(true);
    setRevisionError(null);
    const requestFingerprint = JSON.stringify([
      preview.expected_job_revision,
      preview.compiled_candidate_fingerprint,
      preview.preview_fingerprint,
    ]);
    const idempotencyKey = mutationIdempotencyKey(
      keepMutation,
      requestFingerprint,
      idempotencyKeyFactory,
    );
    try {
      await keepPrevious({
        candidate_fingerprint: preview.compiled_candidate_fingerprint,
        expected_revision: preview.expected_job_revision,
        idempotency_key: idempotencyKey,
        preview_fingerprint: preview.preview_fingerprint,
      });
      keepMutation.current = null;
    } catch (error) {
      setRevisionError(
        error instanceof Error ? error.message : "The prior proposal could not be kept.",
      );
    } finally {
      setRevisionBusy(false);
    }
  };

  const currentLabel = journey === "apply" ? "Your current folder" : "Original structure";
  const proposedLabel = journey === "apply" ? "Shared proposal" : "Proposed structure";

  return (
    <div className="fw-review bp6-dark">
      <section className="fw-trust-strip" aria-label="Plan trust summary">
        <TrustItem icon="lock" label="Source unchanged" value="No output yet" />
        <TrustItem icon="tick-circle" label="Complete accounting" value={`${preview.counts.file_count} files`} />
        <TrustItem icon="shield" label="Protected" value={`${preview.counts.protected_count} fixed`} />
        <TrustItem icon="link" label="Supported links" value={`${preview.counts.link_updated_count} updates`} />
        <TrustItem icon="folder-new" label="Output" value="Created only after accept" />
      </section>

      <div className="fw-toolbar">
        <ButtonGroup aria-label="Structure view">
          <Button
            aria-pressed={side === "current"}
            intent={side === "current" ? "primary" : "none"}
            onClick={() => setSide("current")}
          >
            {currentLabel}
          </Button>
          <Button
            aria-pressed={side === "proposed"}
            intent={side === "proposed" ? "primary" : "none"}
            onClick={() => setSide("proposed")}
          >
            {proposedLabel}
          </Button>
        </ButtonGroup>
        <div className="fw-toolbar-spacer" />
        <InputGroup
          aria-label="Search current and proposed paths"
          leftIcon="search"
          onChange={(event) => setQuery(event.currentTarget.value)}
          placeholder="Search paths"
          value={query}
        />
        <Checkbox
          checked={changedOnly}
          label="Changed only"
          onChange={(event) => {
            setChangedOnly(event.currentTarget.checked);
            if (event.currentTarget.checked) {
              setActiveFilters(new Set());
            }
          }}
        />
      </div>

      <div className="fw-filter-row" role="group" aria-label="Member filters">
        {FILTERS.map(({ key, label }) => (
          <Checkbox
            checked={activeFilters.has(key)}
            inline
            key={key}
            label={label}
            onChange={() => toggleFilter(key)}
          />
        ))}
      </div>

      <div className="fw-main-grid">
        <Card className="fw-tree-panel" compact>
          <header className="fw-panel-heading">
            <div>
              <span className="fw-eyebrow">{side === "current" ? "CURRENT" : "PROPOSED"}</span>
              <h2>{side === "current" ? currentLabel : proposedLabel}</h2>
            </div>
            <Tag minimal>{visibleMembers.length} shown</Tag>
          </header>
          <div className="fw-tree" role="tree" aria-label={`${side === "current" ? currentLabel : proposedLabel} folder tree`}>
            {flatTree.length === 0 ? (
              <div className="fw-empty-state">No members match these filters.</div>
            ) : (
              flatTree.map((node, index) => {
                const change = node.memberId === null ? undefined : changeById.get(node.memberId);
                const isDirectory = node.kind === "directory";
                const isExpanded = expanded.has(node.path);
                return (
                  <button
                    aria-label={treeItemLabel(node, change)}
                    aria-expanded={isDirectory ? isExpanded : undefined}
                    aria-level={node.depth + 1}
                    aria-selected={node.memberId !== null && selectedId === node.memberId}
                    className={`fw-tree-row ${node.memberId !== null && selectedId === node.memberId ? "is-selected" : ""}`}
                    key={node.key}
                    onClick={() => {
                      if (isDirectory) {
                        setExpanded((current) => toggleSetValue(current, node.path));
                      }
                      if (node.memberId !== null) {
                        setSelectedId(node.memberId);
                      }
                    }}
                    onKeyDown={(event) => handleTreeKey(event, index, node)}
                    ref={(element) => {
                      treeItemRefs.current[index] = element;
                    }}
                    role="treeitem"
                    style={{ "--fw-depth": node.depth } as CSSProperties}
                    type="button"
                  >
                    <span className="fw-disclosure" aria-hidden="true">
                      {isDirectory ? (isExpanded ? "⌄" : "›") : ""}
                    </span>
                    <Icon icon={isDirectory ? "folder-close" : "document"} aria-hidden="true" />
                    <span className="fw-tree-label">{node.label}</span>
                    {change && <StatusSignals change={change} />}
                  </button>
                );
              })
            )}
          </div>
        </Card>

        <Card className="fw-detail-panel" compact>
          {selected ? (
            <>
              <div className="fw-detail-heading">
                <div>
                  <span className="fw-eyebrow">SELECTED MEMBER</span>
                  <h2>{side === "current" ? selected.current_relative_path : selected.proposed_relative_path}</h2>
                </div>
                <Tag intent={intentForChange(selected)}>{CLASS_LABELS[selected.change_classification]}</Tag>
              </div>
              <dl className="fw-details">
                <div><dt>Current</dt><dd>{selected.current_relative_path}</dd></div>
                <div><dt>Proposed</dt><dd>{selected.proposed_relative_path}</dd></div>
                <div><dt>Authority</dt><dd>{authorityLabel(selected)}</dd></div>
                <div><dt>Reason</dt><dd>{selected.rationale}</dd></div>
              </dl>
              <section className="fw-link-section" aria-labelledby="link-effects-title">
                <h3 id="link-effects-title">Supported link effects</h3>
                {selectedLinks.length === 0 ? (
                  <p>No supported links originate from this member.</p>
                ) : (
                  <ul>
                    {selectedLinks.map((effect) => (
                      <li key={effect.reference_id}>
                        <Tag intent={effect.status === "rewritten" ? "warning" : "success"} minimal>
                          {effect.status === "rewritten" ? "Rewritten" : "Still valid"}
                        </Tag>
                        <code>{effect.original_destination}</code>
                        <span aria-hidden="true">→</span>
                        <code>{effect.proposed_destination}</code>
                      </li>
                    ))}
                  </ul>
                )}
              </section>
            </>
          ) : (
            <div className="fw-empty-state">Select a member to inspect its exact change.</div>
          )}
        </Card>
      </div>

      <section className="fw-decision-panel" aria-labelledby="decision-title">
        <div className="fw-accept-row">
          <div>
            <span className="fw-eyebrow">EXACT AUTHORIZATION</span>
            <h2 id="decision-title">Create a separate, verified copy</h2>
            <p>The source stays unchanged. Acceptance is bound to this exact preview.</p>
          </div>
          <Button
            className="fw-accept-button"
            disabled={
              preview.counts.blocker_count > 0 ||
              accepting ||
              revisionBusy ||
              status.revision_failure !== null
            }
            intent="success"
            loading={accepting}
            onClick={() => void submitAcceptance()}
            rightIcon="arrow-right"
          >
            Accept this structure and create copy
          </Button>
        </div>
        {acceptanceError && <div className="fw-error" role="alert">{acceptanceError}</div>}
        {revisionDelta && <div className="fw-revision-delta" role="status">{revisionDelta}</div>}
        {status.revision_failure && (
          <div className="fw-error" role="alert">
            <strong>The replacement proposal did not pass Foldweave checks.</strong>
            <span>{status.revision_failure}</span>
            <div className="fw-revision-actions">
              <Button
                disabled={!status.revision_available || revisionBusy}
                onClick={() => revisionInput.current?.focus()}
              >
                Try another change
              </Button>
              <Button
                disabled={revisionBusy}
                onClick={() => void submitKeepPrevious()}
              >
                Keep previous proposal
              </Button>
            </div>
          </div>
        )}
        {revisionError && <div className="fw-error" role="alert">{revisionError}</div>}
        <div className="fw-revision-divider" />
        <label className="fw-revision-label" htmlFor="foldweave-revision">
          Describe a change to this proposal
        </label>
        <textarea
          id="foldweave-revision"
          onChange={(event) => setRevisionInstruction(event.currentTarget.value)}
          placeholder="For example: keep the meeting notes together, and move the final brief into Delivery."
          ref={revisionInput}
          rows={3}
          value={revisionInstruction}
        />
        <div className="fw-revision-footer">
          <span>
            {status.revision_available
              ? `${status.revision_attempts_remaining} revision ${status.revision_attempts_remaining === 1 ? "attempt" : "attempts"} remaining.`
              : "Start a new job to request another revision."}
          </span>
          <Button
            disabled={
              !status.revision_available ||
              revisionInstruction.trim().length === 0 ||
              revisionBusy ||
              accepting
            }
            intent="primary"
            loading={revisionBusy}
            onClick={() => void submitRevision()}
            rightIcon="send-message"
          >
            Send changes
          </Button>
        </div>
      </section>
    </div>
  );
}

function mutationIdempotencyKey(
  reference: { current: PendingMutationKey | null },
  requestFingerprint: string,
  factory: () => string,
): string {
  if (reference.current?.requestFingerprint === requestFingerprint) {
    return reference.current.idempotencyKey;
  }
  const idempotencyKey = factory();
  reference.current = { requestFingerprint, idempotencyKey };
  return idempotencyKey;
}

function TrustItem({ icon, label, value }: { icon: React.ComponentProps<typeof Icon>["icon"]; label: string; value: string }): ReactElement {
  return (
    <div className="fw-trust-item">
      <Icon icon={icon} aria-hidden="true" />
      <span><strong>{label}</strong><small>{value}</small></span>
    </div>
  );
}

function StatusSignals({ change }: { change: FolderPlanMemberChange }): ReactElement {
  return (
    <span className="fw-status-signals">
      {change.protected && <span className="fw-signal is-protected">Protected</span>}
      {change.link_updated && <span className="fw-signal is-link">Link</span>}
      {!change.protected && change.change_classification !== "unchanged" && (
        <span className={`fw-signal is-${change.change_classification}`}>{CLASS_LABELS[change.change_classification]}</span>
      )}
      {change.change_classification === "unchanged" && <span className="fw-signal is-unchanged">Unchanged</span>}
    </span>
  );
}

function treeItemLabel(
  node: TreeNode,
  change: FolderPlanMemberChange | undefined,
): string {
  if (!change) {
    return node.label;
  }
  const signals = [CLASS_LABELS[change.change_classification]];
  if (change.link_updated) {
    signals.push("supported link updated");
  }
  return `${node.label}, ${signals.join(", ")}`;
}

function buildTree(members: FolderPlanTreeMember[]): TreeNode[] {
  const root: TreeNode = {
    key: "root",
    label: "",
    path: "",
    depth: -1,
    kind: "directory",
    memberId: null,
    explicitEmptyDirectory: false,
    children: [],
  };
  const directories = new Map<string, TreeNode>([["", root]]);

  for (const member of members) {
    const pathParts = member.relative_path.split("/");
    const directoryPartCount = member.member_kind === "empty_directory" ? pathParts.length : pathParts.length - 1;
    let parent = root;
    for (let index = 0; index < directoryPartCount; index += 1) {
      const directoryPath = pathParts.slice(0, index + 1).join("/");
      let directory = directories.get(directoryPath);
      if (!directory) {
        directory = {
          key: `directory:${directoryPath}`,
          label: pathParts[index],
          path: directoryPath,
          depth: index,
          kind: "directory",
          memberId: null,
          explicitEmptyDirectory: false,
          children: [],
        };
        directories.set(directoryPath, directory);
        parent.children.push(directory);
      }
      if (member.member_kind === "empty_directory" && index === pathParts.length - 1) {
        directory.memberId = member.member_id;
        directory.explicitEmptyDirectory = true;
      }
      parent = directory;
    }
    if (member.member_kind === "regular_file") {
      parent.children.push({
        key: `file:${member.member_id}`,
        label: pathParts.at(-1) ?? member.relative_path,
        path: member.relative_path,
        depth: pathParts.length - 1,
        kind: "file",
        memberId: member.member_id,
        explicitEmptyDirectory: false,
        children: [],
      });
    }
  }

  sortTree(root);
  return root.children;
}

function sortTree(node: TreeNode): void {
  node.children.sort((left, right) => {
    if (left.kind !== right.kind) {
      return left.kind === "directory" ? -1 : 1;
    }
    return left.label.localeCompare(right.label);
  });
  node.children.forEach(sortTree);
}

function flattenVisibleTree(nodes: TreeNode[], expanded: Set<string>): TreeNode[] {
  const output: TreeNode[] = [];
  for (const node of nodes) {
    output.push(node);
    if (node.kind === "directory" && expanded.has(node.path)) {
      output.push(...flattenVisibleTree(node.children, expanded));
    }
  }
  return output;
}

function initialExpandedPaths(preview: FolderPlanPreviewV1): Set<string> {
  const paths = new Set<string>();
  for (const change of preview.member_changes.filter(isChanged)) {
    for (const path of [change.current_relative_path, change.proposed_relative_path]) {
      const parts = path.split("/");
      const count = change.member_kind === "empty_directory" ? parts.length : parts.length - 1;
      for (let index = 1; index <= count; index += 1) {
        paths.add(parts.slice(0, index).join("/"));
      }
    }
  }
  return paths;
}

function matchesFilter(change: FolderPlanMemberChange, filter: FilterKey): boolean {
  switch (filter) {
    case "moved":
      return change.change_classification === "moved" || change.change_classification === "moved_and_renamed";
    case "renamed":
      return change.change_classification === "renamed" || change.change_classification === "moved_and_renamed";
    case "link_updated":
      return change.link_updated;
    case "protected":
      return change.protected;
    case "unchanged":
      return change.change_classification === "unchanged";
    case "empty_directory":
      return change.member_kind === "empty_directory";
  }
}

function isChanged(change: FolderPlanMemberChange): boolean {
  return change.current_relative_path !== change.proposed_relative_path || change.link_updated;
}

function authorityLabel(change: FolderPlanMemberChange): string {
  if (change.authority_source === "change_file") {
    return "Imported Foldweave Change File";
  }
  if (change.authority_source === "gpt_plan") {
    return "Planning proposal, checked by deterministic code";
  }
  return "Protected by deterministic policy";
}

function intentForChange(change: FolderPlanMemberChange): "none" | "primary" | "warning" | "success" {
  if (change.protected || change.change_classification === "unchanged") {
    return "none";
  }
  if (change.link_updated) {
    return "warning";
  }
  return "primary";
}

function toggleSetValue(current: Set<string>, value: string): Set<string> {
  const next = new Set(current);
  if (next.has(value)) {
    next.delete(value);
  } else {
    next.add(value);
  }
  return next;
}

function createIdempotencyKey(): string {
  if (typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  return Array.from(bytes, (value) => value.toString(16).padStart(2, "0")).join("");
}

export function ReviewLoading(): ReactElement {
  return <div className="fw-loading"><Spinner size={24} /><span>Loading the verified preview…</span></div>;
}

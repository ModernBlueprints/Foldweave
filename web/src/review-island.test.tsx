import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";

import type {
  AcceptanceBindingPayload,
  FolderPlanPreviewV1,
  ReviewStatus,
  RevisionPayload,
} from "./contracts";
import { ReviewIsland } from "./review-island";

const A = "a".repeat(64);
const B = "b".repeat(64);
const C = "c".repeat(64);
const D = "d".repeat(64);
const E = "e".repeat(64);
const JOB_ID = "1".repeat(32);

const preview: FolderPlanPreviewV1 = {
  schema_version: "folder-plan-preview.v1",
  job_id: JOB_ID,
  expected_job_revision: 3,
  proposal_revision: 0,
  proposal_basis: "fresh_gpt_plan",
  source_commitment: A,
  imported_change_file_fingerprint: null,
  match_report_fingerprint: null,
  immediate_parent_candidate_fingerprint: null,
  current_tree_members: [
    { member_id: A, member_kind: "regular_file", relative_path: ".env.local", directory_prefixes: [], protected: true },
    { member_id: D, member_kind: "empty_directory", relative_path: "archive/empty", directory_prefixes: ["archive"], protected: true },
    { member_id: C, member_kind: "regular_file", relative_path: "assets/logo.png", directory_prefixes: ["assets"], protected: false },
    { member_id: B, member_kind: "regular_file", relative_path: "notes/brief.md", directory_prefixes: ["notes"], protected: false },
  ],
  proposed_tree_members: [
    { member_id: A, member_kind: "regular_file", relative_path: ".env.local", directory_prefixes: [], protected: true },
    { member_id: C, member_kind: "regular_file", relative_path: "Delivery/brand/logo.png", directory_prefixes: ["Delivery", "Delivery/brand"], protected: false },
    { member_id: B, member_kind: "regular_file", relative_path: "Delivery/final-brief.md", directory_prefixes: ["Delivery"], protected: false },
    { member_id: D, member_kind: "empty_directory", relative_path: "archive/empty", directory_prefixes: ["archive"], protected: true },
  ],
  member_changes: [
    {
      member_id: A,
      member_kind: "regular_file",
      current_relative_path: ".env.local",
      proposed_relative_path: ".env.local",
      change_classification: "protected",
      protected: true,
      authority_source: "protected",
      rationale: "Keep this protected file at its exact source path.",
      link_updated: false,
      supported_link_effect_ids: [],
    },
    {
      member_id: D,
      member_kind: "empty_directory",
      current_relative_path: "archive/empty",
      proposed_relative_path: "archive/empty",
      change_classification: "empty_directory",
      protected: true,
      authority_source: "protected",
      rationale: "Keep this explicit empty directory unchanged.",
      link_updated: false,
      supported_link_effect_ids: [],
    },
    {
      member_id: C,
      member_kind: "regular_file",
      current_relative_path: "assets/logo.png",
      proposed_relative_path: "Delivery/brand/logo.png",
      change_classification: "moved",
      protected: false,
      authority_source: "gpt_plan",
      rationale: "Move the identity asset into delivery.",
      link_updated: false,
      supported_link_effect_ids: [],
    },
    {
      member_id: B,
      member_kind: "regular_file",
      current_relative_path: "notes/brief.md",
      proposed_relative_path: "Delivery/final-brief.md",
      change_classification: "moved_and_renamed",
      protected: false,
      authority_source: "gpt_plan",
      rationale: "Put the final brief in Delivery.",
      link_updated: true,
      supported_link_effect_ids: [A],
    },
  ],
  supported_link_effects: [
    {
      reference_id: A,
      source_member_id: B,
      target_member_id: C,
      current_source_path: "notes/brief.md",
      current_target_path: "assets/logo.png",
      proposed_source_path: "Delivery/final-brief.md",
      proposed_target_path: "Delivery/brand/logo.png",
      original_destination: "../assets/logo.png",
      proposed_destination: "brand/logo.png",
      status: "rewritten",
    },
  ],
  collision_findings: [],
  blocker_findings: [],
  counts: {
    file_count: 3,
    empty_directory_count: 1,
    changed_path_count: 2,
    renamed_count: 1,
    moved_count: 2,
    link_count: 1,
    link_updated_count: 1,
    protected_count: 1,
    blocker_count: 0,
  },
  compiled_candidate_fingerprint: B,
  preview_fingerprint: C,
};

const status: ReviewStatus = {
  job_id: JOB_ID,
  lifecycle: "reviewing",
  job_revision: 3,
  proposal_revision: 0,
  candidate_fingerprint: B,
  preview_fingerprint: C,
  output_parent: "/tmp/foldweave-output",
  result_folder_name: "northstar-organized",
  revision_available: true,
  revision_attempts_remaining: 2,
  revision_failure: null,
  done_url: null,
};

function renderReview(journey: "organize" | "apply" = "organize") {
  const acceptPlan = vi.fn(async () => undefined);
  const revisePlan = vi.fn(async () => undefined);
  const keepPrevious = vi.fn(async () => undefined);
  render(
    <ReviewIsland
      acceptPlan={acceptPlan}
      idempotencyKeyFactory={() => "test-idempotency-key"}
      journey={journey}
      keepPrevious={keepPrevious}
      preview={preview}
      revisePlan={revisePlan}
      status={status}
    />,
  );
  return { acceptPlan, keepPrevious, revisePlan };
}

function makeReceiverPreview(): FolderPlanPreviewV1 {
  return {
    ...preview,
    proposal_basis: "imported_change_file",
    imported_change_file_fingerprint: D,
    match_report_fingerprint: E,
    member_changes: preview.member_changes.map((change) => ({
      ...change,
      authority_source: change.protected ? "protected" : "change_file",
    })),
  };
}

function makeMaximumShapePreview(): FolderPlanPreviewV1 {
  const currentTreeMembers: FolderPlanPreviewV1["current_tree_members"] = [];
  const proposedTreeMembers: FolderPlanPreviewV1["proposed_tree_members"] = [];
  const memberChanges: FolderPlanPreviewV1["member_changes"] = [];

  for (let index = 0; index < 500; index += 1) {
    const memberId = hexId(index + 1);
    const protectedMember = index % 100 === 0;
    const currentPath = `source/bucket-${String(index % 10).padStart(2, "0")}/file-${String(index).padStart(4, "0")}.md`;
    const proposedPath = protectedMember
      ? currentPath
      : `organized/bucket-${String(index % 10).padStart(2, "0")}/item-${String(index).padStart(4, "0")}.md`;
    currentTreeMembers.push({
      member_id: memberId,
      member_kind: "regular_file",
      relative_path: currentPath,
      directory_prefixes: directoryPrefixes(currentPath),
      protected: protectedMember,
    });
    proposedTreeMembers.push({
      member_id: memberId,
      member_kind: "regular_file",
      relative_path: proposedPath,
      directory_prefixes: directoryPrefixes(proposedPath),
      protected: protectedMember,
    });
    memberChanges.push({
      member_id: memberId,
      member_kind: "regular_file",
      current_relative_path: currentPath,
      proposed_relative_path: proposedPath,
      change_classification: protectedMember ? "protected" : "moved_and_renamed",
      protected: protectedMember,
      authority_source: protectedMember ? "protected" : "gpt_plan",
      rationale: protectedMember
        ? "Keep the protected member fixed."
        : "Move this member into the organized tree.",
      link_updated: false,
      supported_link_effect_ids: [],
    });
  }

  for (let index = 0; index < 1_000; index += 1) {
    const memberId = hexId(index + 501);
    const path = `empty/group-${String(index).padStart(4, "0")}`;
    const member = {
      member_id: memberId,
      member_kind: "empty_directory" as const,
      relative_path: path,
      directory_prefixes: ["empty"],
      protected: false,
    };
    currentTreeMembers.push(member);
    proposedTreeMembers.push(member);
    memberChanges.push({
      member_id: memberId,
      member_kind: "empty_directory",
      current_relative_path: path,
      proposed_relative_path: path,
      change_classification: "empty_directory",
      protected: false,
      authority_source: "gpt_plan",
      rationale: "Preserve this explicit empty directory.",
      link_updated: false,
      supported_link_effect_ids: [],
    });
  }

  return {
    ...preview,
    current_tree_members: currentTreeMembers,
    proposed_tree_members: proposedTreeMembers,
    member_changes: memberChanges,
    supported_link_effects: [],
    counts: {
      file_count: 500,
      empty_directory_count: 1_000,
      changed_path_count: 495,
      renamed_count: 495,
      moved_count: 495,
      link_count: 0,
      link_updated_count: 0,
      protected_count: 5,
      blocker_count: 0,
    },
  };
}

function hexId(value: number): string {
  return value.toString(16).padStart(64, "0");
}

function directoryPrefixes(path: string): string[] {
  const parts = path.split("/").slice(0, -1);
  return parts.map((_, index) => parts.slice(0, index + 1).join("/"));
}

afterEach(cleanup);

describe("Foldweave review island", () => {
  it("shows all members by default for a small preview and exact proposal counts", () => {
    renderReview();

    expect(screen.getByRole("checkbox", { name: "Changed only" })).not.toBeChecked();
    expect(screen.getByText("4 shown")).toBeInTheDocument();
    const counts = screen.getByRole("region", { name: "Exact proposal counts" });
    expect(counts).toHaveTextContent("3 files");
    expect(counts).toHaveTextContent("1 explicit empty directory");
    expect(counts).toHaveTextContent("2 changed paths");
    expect(counts).toHaveTextContent("1 updated link");
    expect(counts).toHaveTextContent("1 protected member");
    expect(screen.getByText("No result exists during review")).toBeInTheDocument();
  });

  it("toggles the complete origin labels without losing selected member details", async () => {
    const user = userEvent.setup();
    renderReview();

    expect(screen.getByRole("button", { name: "Proposed structure" })).toHaveAttribute("aria-pressed", "true");
    await user.click(screen.getByRole("treeitem", { name: /final-brief\.md/ }));
    expect(screen.getByText("Delivery/final-brief.md", { selector: "h2" })).toBeInTheDocument();
    expect(screen.getByText("Planning proposal, checked by deterministic code")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Original structure" }));
    expect(screen.getByRole("button", { name: "Original structure" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByText("notes/brief.md", { selector: "h2" })).toBeInTheDocument();
  });

  it("uses receiver-specific current and shared proposal labels", () => {
    const receiverPreview = makeReceiverPreview();
    render(
      <ReviewIsland
        acceptPlan={vi.fn(async () => undefined)}
        journey="apply"
        keepPrevious={vi.fn(async () => undefined)}
        preview={receiverPreview}
        revisePlan={vi.fn(async () => undefined)}
        status={status}
      />,
    );
    expect(screen.getByRole("button", { name: "Your current folder" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Shared proposal" })).toHaveAttribute("aria-pressed", "true");
    const evidence = screen.getByRole("region", { name: "Receiver preparation evidence" });
    expect(within(evidence).getByText("Deterministic receiver match")).toBeInTheDocument();
    expect(within(evidence).getByText(D)).toBeInTheDocument();
    expect(within(evidence).getByText(E)).toBeInTheDocument();
    expect(within(evidence).getByText("0 GPT calls so far")).toBeInTheDocument();
  });

  it("does not invent zero-call evidence for a model-derived receiver proposal", () => {
    render(
      <ReviewIsland
        acceptPlan={vi.fn(async () => undefined)}
        journey="apply"
        keepPrevious={vi.fn(async () => undefined)}
        preview={{
          ...preview,
          proposal_basis: "gpt_derivative",
          imported_change_file_fingerprint: D,
          immediate_parent_candidate_fingerprint: E,
        }}
        revisePlan={vi.fn(async () => undefined)}
        status={status}
      />,
    );

    expect(screen.queryByText("0 GPT calls so far")).not.toBeInTheDocument();
    const evidence = screen.getByRole("region", { name: "Receiver preparation evidence" });
    expect(within(evidence).getByText("Model-derived receiver revision")).toBeInTheDocument();
    expect(within(evidence).getByText("GPT used for this derivative proposal")).toBeInTheDocument();
    expect(within(evidence).getByText(E)).toBeInTheDocument();
  });

  it("shows supported-link impact for both the source and target member", async () => {
    const user = userEvent.setup();
    renderReview();

    await user.click(screen.getByRole("treeitem", { name: /logo\.png/ }));
    expect(screen.getByText("../assets/logo.png")).toBeInTheDocument();
    expect(screen.getByText("brand/logo.png")).toBeInTheDocument();
  });

  it("supports filters and keyboard traversal with visible focus targets", async () => {
    const user = userEvent.setup();
    renderReview();

    await user.click(screen.getByRole("checkbox", { name: "Protected" }));
    expect(screen.getByRole("treeitem", { name: ".env.local, Protected" })).toBeInTheDocument();

    await user.click(screen.getByRole("checkbox", { name: "Protected" }));
    await user.click(screen.getByRole("checkbox", { name: "Changed only" }));
    const tree = screen.getByRole("tree");
    const items = within(tree).getAllByRole("treeitem");
    expect(items[0]).toHaveAttribute("tabindex", "0");
    items.slice(1).forEach((item) => expect(item).toHaveAttribute("tabindex", "-1"));
    items[0].focus();
    fireEvent.keyDown(items[0], { key: "ArrowDown" });
    expect(items[1]).toHaveFocus();
    expect(items[1]).toHaveAttribute("tabindex", "0");
    expect(items[0]).toHaveAttribute("tabindex", "-1");
    fireEvent.keyDown(items[1], { key: "End" });
    expect(items.at(-1)).toHaveFocus();
    fireEvent.keyDown(items.at(-1)!, { key: "Home" });
    expect(items[0]).toHaveFocus();
  });

  it("uses standard left and right tree navigation for parents and children", async () => {
    renderReview();
    const finalBrief = screen.getByRole("treeitem", { name: /final-brief\.md/ });
    finalBrief.focus();

    fireEvent.keyDown(finalBrief, { key: "ArrowLeft" });
    const delivery = screen.getByRole("treeitem", { name: "Delivery" });
    expect(delivery).toHaveFocus();

    fireEvent.keyDown(delivery, { key: "ArrowLeft" });
    expect(delivery).toHaveAttribute("aria-expanded", "false");
    fireEvent.keyDown(delivery, { key: "ArrowRight" });
    expect(delivery).toHaveAttribute("aria-expanded", "true");
    fireEvent.keyDown(delivery, { key: "ArrowRight" });
    expect(screen.getByRole("treeitem", { name: "brand" })).toHaveFocus();
  });

  it("submits the exact fingerprint-bound acceptance only after the explicit click", async () => {
    const user = userEvent.setup();
    const { acceptPlan } = renderReview();
    expect(acceptPlan).not.toHaveBeenCalled();

    await user.click(screen.getByRole("button", { name: "Accept this structure and create copy" }));
    expect(acceptPlan).toHaveBeenCalledTimes(1);
    expect(acceptPlan).toHaveBeenCalledWith({
      candidate_fingerprint: B,
      expected_revision: 3,
      idempotency_key: "test-idempotency-key",
      preview_fingerprint: C,
    });
  });

  it("reuses the exact acceptance key after an uncertain response", async () => {
    const user = userEvent.setup();
    const acceptPlan = vi
      .fn<(payload: AcceptanceBindingPayload) => Promise<void>>()
      .mockRejectedValueOnce(new Error("The response was not observed."))
      .mockResolvedValueOnce(undefined);
    const idempotencyKeyFactory = vi
      .fn<() => string>()
      .mockReturnValueOnce("stable-accept-key")
      .mockReturnValueOnce("must-not-be-used");
    render(
      <ReviewIsland
        acceptPlan={acceptPlan}
        idempotencyKeyFactory={idempotencyKeyFactory}
        journey="organize"
        keepPrevious={vi.fn(async () => undefined)}
        preview={preview}
        revisePlan={vi.fn(async () => undefined)}
        status={status}
      />,
    );

    const accept = screen.getByRole("button", {
      name: "Accept this structure and create copy",
    });
    await user.click(accept);
    expect(await screen.findByText("The response was not observed.")).toBeInTheDocument();
    await user.click(accept);

    expect(acceptPlan).toHaveBeenCalledTimes(2);
    expect(acceptPlan.mock.calls[0]?.[0].idempotency_key).toBe("stable-accept-key");
    expect(acceptPlan.mock.calls[1]?.[0].idempotency_key).toBe("stable-accept-key");
    expect(idempotencyKeyFactory).toHaveBeenCalledTimes(1);
  });

  it("submits one exact bounded revision after nonblank user input", async () => {
    const user = userEvent.setup();
    const { acceptPlan, revisePlan } = renderReview();
    const input = screen.getByLabelText("Describe a change to this proposal");
    expect(screen.getByRole("button", { name: "Send changes" })).toBeDisabled();
    await user.type(input, "Keep the notes together");
    await user.click(screen.getByRole("button", { name: "Send changes" }));
    expect(revisePlan).toHaveBeenCalledWith({
      candidate_fingerprint: B,
      expected_revision: 3,
      idempotency_key: "test-idempotency-key",
      instruction: "Keep the notes together",
      preview_fingerprint: C,
    });
    expect(acceptPlan).not.toHaveBeenCalled();
  });

  it("reuses the exact revision key when the same delivered message is retried", async () => {
    const user = userEvent.setup();
    const revisePlan = vi.fn<(payload: RevisionPayload) => Promise<void>>(
      async () => undefined,
    );
    const idempotencyKeyFactory = vi
      .fn<() => string>()
      .mockReturnValueOnce("stable-revision-key")
      .mockReturnValueOnce("must-not-be-used");
    render(
      <ReviewIsland
        acceptPlan={vi.fn(async () => undefined)}
        idempotencyKeyFactory={idempotencyKeyFactory}
        journey="organize"
        keepPrevious={vi.fn(async () => undefined)}
        preview={preview}
        revisePlan={revisePlan}
        status={status}
      />,
    );

    const input = screen.getByLabelText("Describe a change to this proposal");
    const send = screen.getByRole("button", { name: "Send changes" });
    await user.type(input, "Keep the notes together");
    await user.click(send);
    expect(input).toHaveValue("Keep the notes together");
    await user.click(send);

    expect(revisePlan).toHaveBeenCalledTimes(2);
    expect(revisePlan.mock.calls[0]?.[0].idempotency_key).toBe(
      "stable-revision-key",
    );
    expect(revisePlan.mock.calls[1]?.[0].idempotency_key).toBe(
      "stable-revision-key",
    );
    expect(idempotencyKeyFactory).toHaveBeenCalledTimes(1);
  });

  it("preserves a failed proposal and exposes retry or keep actions", async () => {
    const user = userEvent.setup();
    const keepPrevious = vi.fn(async () => undefined);
    render(
      <ReviewIsland
        acceptPlan={vi.fn(async () => undefined)}
        idempotencyKeyFactory={() => "keep-idempotency-key"}
        journey="organize"
        keepPrevious={keepPrevious}
        preview={preview}
        revisePlan={vi.fn(async () => undefined)}
        status={{
          ...status,
          revision_attempts_remaining: 1,
          revision_failure: "Two files would use the same target path.",
        }}
      />,
    );

    expect(
      screen.getByText("Two files would use the same target path."),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeDisabled();
    await user.click(screen.getByRole("button", { name: "Keep previous proposal" }));
    expect(keepPrevious).toHaveBeenCalledWith({
      candidate_fingerprint: B,
      expected_revision: 3,
      idempotency_key: "keep-idempotency-key",
      preview_fingerprint: C,
    });
  });

  it("preserves tree scroll and shows every changed mapping across preview replacement", async () => {
    const user = userEvent.setup();
    const rendered = render(
      <ReviewIsland
        acceptPlan={vi.fn(async () => undefined)}
        journey="organize"
        keepPrevious={vi.fn(async () => undefined)}
        preview={preview}
        revisePlan={vi.fn(async () => undefined)}
        status={status}
      />,
    );
    const tree = screen.getByRole("tree");
    tree.scrollTop = 173;
    fireEvent.scroll(tree);
    await user.click(screen.getByRole("button", { name: "Original structure" }));
    expect(screen.getByRole("tree").scrollTop).toBe(173);

    const revisedPreview: FolderPlanPreviewV1 = {
      ...preview,
      expected_job_revision: 4,
      proposal_revision: 1,
      proposed_tree_members: preview.proposed_tree_members.map((member) =>
        member.member_id === C
          ? {
              ...member,
              relative_path: "Delivery/final/logo.png",
              directory_prefixes: ["Delivery", "Delivery/final"],
            }
          : member,
      ),
      member_changes: preview.member_changes.map((change) =>
        change.member_id === C
          ? { ...change, proposed_relative_path: "Delivery/final/logo.png" }
          : change,
      ),
      compiled_candidate_fingerprint: D,
      preview_fingerprint: E,
    };
    rendered.rerender(
      <ReviewIsland
        acceptPlan={vi.fn(async () => undefined)}
        journey="organize"
        keepPrevious={vi.fn(async () => undefined)}
        preview={revisedPreview}
        revisePlan={vi.fn(async () => undefined)}
        status={{
          ...status,
          job_revision: 4,
          proposal_revision: 1,
          candidate_fingerprint: D,
          preview_fingerprint: E,
        }}
      />,
    );

    expect(screen.getByRole("tree").scrollTop).toBe(173);
    const delta = await screen.findByRole("status");
    expect(within(delta).getByText("1 mapping changed from the previous proposal.")).toBeInTheDocument();
    expect(within(delta).getByText("Delivery/brand/logo.png")).toBeInTheDocument();
    expect(within(delta).getByText("Delivery/final/logo.png")).toBeInTheDocument();
  });

  it("keeps the bounded 500-file and 1000-directory review usable", async () => {
    const user = userEvent.setup();
    const maximumPreview = makeMaximumShapePreview();
    render(
      <ReviewIsland
        acceptPlan={vi.fn(async () => undefined)}
        journey="organize"
        keepPrevious={vi.fn(async () => undefined)}
        preview={maximumPreview}
        revisePlan={vi.fn(async () => undefined)}
        status={status}
      />,
    );

    expect(screen.getByRole("checkbox", { name: "Changed only" })).toBeChecked();
    expect(screen.getByText("495 shown")).toBeInTheDocument();
    const counts = screen.getByRole("region", { name: "Exact proposal counts" });
    expect(within(counts).getByText("500", { selector: "strong" })).toBeInTheDocument();
    expect(within(counts).getByText("1000", { selector: "strong" })).toBeInTheDocument();
    expect(within(counts).getAllByText("495", { selector: "strong" })).toHaveLength(1);

    const search = screen.getByRole("textbox", {
      name: "Search current and proposed paths",
    });
    await user.type(search, "item-0499");
    expect(screen.getByText("1 shown")).toBeInTheDocument();
    const matchingItem = screen.getByRole("treeitem", { name: /item-0499\.md/ });
    await user.click(matchingItem);
    expect(screen.getByText(/organized\/bucket-09\/item-0499\.md/, { selector: "h2" })).toBeInTheDocument();

    const tree = screen.getByRole("tree");
    tree.scrollTop = 211;
    fireEvent.scroll(tree);
    await user.click(screen.getByRole("button", { name: "Original structure" }));
    expect(screen.getByRole("tree").scrollTop).toBe(211);
    const treeItems = within(screen.getByRole("tree")).getAllByRole("treeitem");
    treeItems[0]!.focus();
    fireEvent.keyDown(treeItems[0]!, { key: "ArrowDown" });
    expect(treeItems[1]).toHaveFocus();

    await user.clear(search);
    await user.click(screen.getByRole("checkbox", { name: "Empty directory" }));
    expect(screen.getByText("1000 shown")).toBeInTheDocument();

    const reviewCss = readFileSync(
      resolve(process.cwd(), "src/review.css"),
      "utf8",
    );
    expect(reviewCss).toMatch(/\.fw-review\s*\{[^}]*overflow-x:\s*clip;/s);
    expect(reviewCss).toMatch(/\.fw-tree\s*\{[^}]*max-width:\s*100%;[^}]*overflow:\s*auto;/s);
    expect(reviewCss).toMatch(/\.fw-tree-row\s*\{[^}]*min-width:\s*0;/s);
  });
});

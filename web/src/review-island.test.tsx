import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type {
  AcceptancePayload,
  FolderPlanPreviewV1,
  ReviewStatus,
} from "./contracts";
import { ReviewIsland } from "./review-island";

const A = "a".repeat(64);
const B = "b".repeat(64);
const C = "c".repeat(64);
const D = "d".repeat(64);
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
    { member_id: B, member_kind: "regular_file", relative_path: "notes/brief.md", directory_prefixes: ["notes"], protected: false },
    { member_id: C, member_kind: "regular_file", relative_path: "assets/logo.png", directory_prefixes: ["assets"], protected: false },
    { member_id: D, member_kind: "empty_directory", relative_path: "archive/empty", directory_prefixes: ["archive", "archive/empty"], protected: true },
  ],
  proposed_tree_members: [
    { member_id: A, member_kind: "regular_file", relative_path: ".env.local", directory_prefixes: [], protected: true },
    { member_id: C, member_kind: "regular_file", relative_path: "Delivery/brand/logo.png", directory_prefixes: ["Delivery", "Delivery/brand"], protected: false },
    { member_id: B, member_kind: "regular_file", relative_path: "Delivery/final-brief.md", directory_prefixes: ["Delivery"], protected: false },
    { member_id: D, member_kind: "empty_directory", relative_path: "archive/empty", directory_prefixes: ["archive", "archive/empty"], protected: true },
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

afterEach(cleanup);

describe("Foldweave review island", () => {
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
    renderReview("apply");
    expect(screen.getByRole("button", { name: "Your current folder" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Shared proposal" })).toHaveAttribute("aria-pressed", "true");
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
    items[0].focus();
    fireEvent.keyDown(items[0], { key: "ArrowDown" });
    expect(items[1]).toHaveFocus();
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
      output_parent: "/tmp/foldweave-output",
      preview_fingerprint: C,
      result_folder_name: "northstar-organized",
    });
  });

  it("reuses the exact acceptance key after an uncertain response", async () => {
    const user = userEvent.setup();
    const acceptPlan = vi
      .fn<(payload: AcceptancePayload) => Promise<void>>()
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
});

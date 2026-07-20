import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { ChatGptHostBridge, HostInterruption } from "./chatgpt-bridge";
import {
  McpAppsHostBridge,
  extractStructuredContent,
} from "./chatgpt-bridge";
import {
  type FoldweaveChatGptReviewV1,
  assertNoSensitiveBoundaryData,
  parseHostedChangeFileResult,
  parseHostedJobStatus,
  parseHostedReconstructionResult,
  parseHostedReviewEnvelope,
} from "./chatgpt-contracts";
import { FoldweaveChatGptWidget } from "./chatgpt-widget";

const A = "a".repeat(64);
const B = "b".repeat(64);
const C = "c".repeat(64);
const D = "d".repeat(64);
const E = "e".repeat(64);
const F = "f".repeat(64);
const ZERO = "0".repeat(64);
const JOB_ID = "1".repeat(32);
const CHILD_JOB_ID = "2".repeat(32);
const RAW_CAPABILITY_ID = `fwjc_${"A".repeat(86)}`;
const CHANGE_FILE_HANDLE = `fw_${"A".repeat(43)}`;
const RESTORE_HANDLE = `fw_${"B".repeat(43)}`;

function changeFileResult() {
  return {
    schema_version: "foldweave-change-file-result.v1",
    job_id: JOB_ID,
    item: {
      schema_version: "foldweave-local-item-handle.v1",
      handle: CHANGE_FILE_HANDLE,
      role: "change_file",
      display_name: "northstar.foldweave-change.json",
      expires_at: "2026-07-20T06:00:00+02:00",
    },
    change_file_fingerprint: B,
    originating_receipt_fingerprint: ZERO,
  };
}

function reconstructionResult() {
  return {
    schema_version: "foldweave-reconstruction-result.v1",
    job_id: JOB_ID,
    item: {
      schema_version: "foldweave-local-item-handle.v1",
      handle: RESTORE_HANDLE,
      role: "restore_destination",
      display_name: "northstar-original-layout",
      expires_at: "2026-07-20T06:00:00+02:00",
    },
    receipt_fingerprint: ZERO,
    source_commitment: A,
    restored_file_count: 1,
    restored_bytes: 128,
    restored_empty_directory_count: 0,
  };
}

const reviewingSnapshot: FoldweaveChatGptReviewV1 = {
  schema_version: "foldweave-chatgpt-review.v1",
  state_version: 3,
  journey: "organize",
  preview: {
    schema_version: "folder-plan-preview.v1",
    job_id: JOB_ID,
    expected_job_revision: 3,
    proposal_revision: 1,
    proposal_basis: "fresh_gpt_plan",
    source_commitment: A,
    imported_change_file_fingerprint: null,
    match_report_fingerprint: null,
    immediate_parent_candidate_fingerprint: null,
    current_tree_members: [
      {
        member_id: B,
        member_kind: "regular_file",
        relative_path: "notes/brief.md",
        directory_prefixes: ["notes"],
        protected: false,
      },
    ],
    proposed_tree_members: [
      {
        member_id: B,
        member_kind: "regular_file",
        relative_path: "Delivery/brief.md",
        directory_prefixes: ["Delivery"],
        protected: false,
      },
    ],
    member_changes: [
      {
        member_id: B,
        member_kind: "regular_file",
        current_relative_path: "notes/brief.md",
        proposed_relative_path: "Delivery/brief.md",
        change_classification: "moved",
        protected: false,
        authority_source: "gpt_plan",
        rationale: "Group the final brief with delivery materials.",
        link_updated: false,
        supported_link_effect_ids: [],
      },
    ],
    supported_link_effects: [],
    collision_findings: [],
    blocker_findings: [],
    counts: {
      file_count: 1,
      empty_directory_count: 0,
      changed_path_count: 1,
      renamed_count: 0,
      moved_count: 1,
      link_count: 0,
      link_updated_count: 0,
      protected_count: 0,
      blocker_count: 0,
    },
    compiled_candidate_fingerprint: C,
    preview_fingerprint: D,
  },
  status: {
    job_id: JOB_ID,
    lifecycle: "reviewing",
    job_revision: 3,
    proposal_revision: 1,
    candidate_fingerprint: C,
    preview_fingerprint: D,
    revision_available: true,
    revision_attempts_remaining: 1,
    revision_failure: null,
    authorization_context_fingerprint: E,
    planning_basis: "fresh",
    model_transport: "chatgpt_hosted",
    execution_origin: "none",
    direct_api_used: false,
    direct_budget_reserved: false,
  },
  result: null,
};

function verifiedSnapshot(): FoldweaveChatGptReviewV1 {
  return {
    ...reviewingSnapshot,
    state_version: 5,
    status: {
      ...reviewingSnapshot.status,
      lifecycle: "verified",
      job_revision: 5,
      revision_available: false,
      revision_attempts_remaining: 0,
    },
    result: {
      verification: "verified",
      source_unchanged: true,
      complete_file_count: 1,
      changed_path_count: 1,
      organized_tree_commitment: A,
      change_file_fingerprint: B,
    },
  };
}

function revisedSnapshot(): FoldweaveChatGptReviewV1 {
  return {
    ...reviewingSnapshot,
    state_version: 4,
    preview: {
      ...reviewingSnapshot.preview,
      expected_job_revision: 4,
      proposal_revision: 2,
      proposed_tree_members: [
        {
          ...reviewingSnapshot.preview.proposed_tree_members[0]!,
          relative_path: "Client/brief.md",
          directory_prefixes: ["Client"],
        },
      ],
      member_changes: [
        {
          ...reviewingSnapshot.preview.member_changes[0]!,
          proposed_relative_path: "Client/brief.md",
          rationale: "Keep the brief with the client delivery.",
        },
      ],
      compiled_candidate_fingerprint: F,
      preview_fingerprint: ZERO,
    },
    status: {
      ...reviewingSnapshot.status,
      job_revision: 4,
      proposal_revision: 2,
      candidate_fingerprint: F,
      preview_fingerprint: ZERO,
      authorization_context_fingerprint: B,
      revision_available: false,
      revision_attempts_remaining: 0,
    },
  };
}

function revisionFailedSnapshot(): FoldweaveChatGptReviewV1 {
  return {
    ...reviewingSnapshot,
    state_version: 4,
    preview: {
      ...reviewingSnapshot.preview,
      expected_job_revision: 4,
    },
    status: {
      ...reviewingSnapshot.status,
      lifecycle: "revision_failed",
      job_revision: 4,
      authorization_context_fingerprint: B,
      revision_failure: "The proposed replacement did not compile.",
    },
  };
}

function restoredPreviousSnapshot(): FoldweaveChatGptReviewV1 {
  return {
    ...reviewingSnapshot,
    state_version: 5,
    preview: {
      ...reviewingSnapshot.preview,
      expected_job_revision: 5,
    },
    status: {
      ...reviewingSnapshot.status,
      job_revision: 5,
      authorization_context_fingerprint: ZERO,
    },
  };
}

function durableStatus(
  snapshot: FoldweaveChatGptReviewV1,
  lifecycle: string = snapshot.status.lifecycle,
): Record<string, unknown> {
  return {
    schema_version: "foldweave-hosted-job-status.v1",
    job_id: snapshot.status.job_id,
    lifecycle,
    job_revision: snapshot.status.job_revision,
    proposal_revision: snapshot.status.proposal_revision,
    source_commitment: snapshot.preview.source_commitment,
    request_fingerprint: F,
    planning_basis: snapshot.status.planning_basis,
    model_transport: snapshot.status.model_transport,
    execution_origin: snapshot.status.execution_origin,
    direct_api_used: false,
    direct_budget_reserved: false,
    has_preview: true,
    candidate_fingerprint: snapshot.preview.compiled_candidate_fingerprint,
    preview_fingerprint: snapshot.preview.preview_fingerprint,
    clarification_question: null,
    clarification_question_fingerprint: null,
    revision_attempts_remaining: snapshot.status.revision_attempts_remaining,
    revision_failure_code: null,
    blocker_code: lifecycle === "blocked" ? "host_plan_blocked" : null,
  };
}

function receiverSnapshot(): FoldweaveChatGptReviewV1 {
  const snapshot = structuredClone(reviewingSnapshot);
  return {
    ...snapshot,
    journey: "apply",
    preview: {
      ...snapshot.preview,
      proposal_basis: "imported_change_file",
      imported_change_file_fingerprint: B,
      match_report_fingerprint: E,
    },
    status: {
      ...snapshot.status,
      planning_basis: "none",
      model_transport: "none",
      execution_origin: "capsule_applied",
    },
  };
}

function derivativePendingStatus(
  parent: FoldweaveChatGptReviewV1,
): Record<string, unknown> {
  return {
    ...durableStatus(parent),
    job_id: CHILD_JOB_ID,
    lifecycle: "revising",
    job_revision: 0,
    proposal_revision: 0,
    planning_basis: "derivative",
    model_transport: "chatgpt_hosted",
    execution_origin: "none",
    has_preview: false,
    candidate_fingerprint: null,
    preview_fingerprint: null,
  };
}

function derivativeReview(
  parent: FoldweaveChatGptReviewV1,
): FoldweaveChatGptReviewV1 {
  return {
    ...structuredClone(parent),
    state_version: 1,
    preview: {
      ...structuredClone(parent.preview),
      job_id: CHILD_JOB_ID,
      expected_job_revision: 1,
      proposal_revision: 1,
      proposal_basis: "gpt_derivative",
      match_report_fingerprint: null,
      immediate_parent_candidate_fingerprint:
        parent.preview.compiled_candidate_fingerprint,
      compiled_candidate_fingerprint: F,
      preview_fingerprint: ZERO,
    },
    status: {
      ...structuredClone(parent.status),
      job_id: CHILD_JOB_ID,
      lifecycle: "reviewing",
      job_revision: 1,
      proposal_revision: 1,
      candidate_fingerprint: F,
      preview_fingerprint: ZERO,
      authorization_context_fingerprint: B,
      planning_basis: "derivative",
      model_transport: "chatgpt_hosted",
      execution_origin: "none",
    },
  };
}

function expectNoRawCapability(value: unknown): void {
  const serialized = JSON.stringify(value);
  expect(serialized).not.toMatch(/capability(?:_id|_expires_at)?/i);
  expect(serialized).not.toContain("fwjc_");
}

class FakeBridge implements ChatGptHostBridge {
  readonly calls: Array<{ name: string; argumentsValue: Record<string, unknown> }> = [];
  readonly prompts: string[] = [];
  private readonly listeners = new Set<(value: unknown) => void>();
  private readonly interruptionListeners = new Set<
    (interruption: HostInterruption) => void
  >();
  callResult: unknown = undefined;
  callResults: unknown[] = [];
  connectCalls = 0;

  constructor(private readonly initial: unknown = reviewingSnapshot) {}

  async connect(): Promise<void> {
    this.connectCalls += 1;
  }

  getInitialStructuredContent(): unknown {
    return this.initial;
  }

  subscribeToolResults(listener: (structuredContent: unknown) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  subscribeInterruptions(
    listener: (interruption: HostInterruption) => void,
  ): () => void {
    this.interruptionListeners.add(listener);
    return () => this.interruptionListeners.delete(listener);
  }

  async callTool(
    name: string,
    argumentsValue: Record<string, unknown>,
  ): Promise<unknown> {
    this.calls.push({ name, argumentsValue });
    return this.callResults.length > 0 ? this.callResults.shift() : this.callResult;
  }

  async sendFollowUpMessage(prompt: string): Promise<void> {
    this.prompts.push(prompt);
  }

  emit(snapshot: FoldweaveChatGptReviewV1): void {
    this.listeners.forEach((listener) => listener(snapshot));
  }

  emitRaw(value: unknown): void {
    this.listeners.forEach((listener) => listener(value));
  }

  interrupt(interruption: HostInterruption): void {
    this.interruptionListeners.forEach((listener) => listener(interruption));
  }
}

afterEach(() => {
  cleanup();
  delete window.openai;
  vi.restoreAllMocks();
});

describe("Foldweave ChatGPT review widget", () => {
  it("renders the complete initial structured-content preview", async () => {
    render(<FoldweaveChatGptWidget bridge={new FakeBridge()} />);

    expect(await screen.findByText("Review the weave")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Proposed structure" })).toHaveAttribute(
      "aria-pressed",
      "true",
    );
    expect(screen.getByText("Delivery/brief.md", { selector: "h2" })).toBeInTheDocument();
    expect(screen.getByText("No direct API key used")).toBeInTheDocument();
  });

  it("rejects raw per-job capability material at every ChatGPT input boundary", () => {
    const reviewWithCapability = structuredClone(
      reviewingSnapshot,
    ) as unknown as Record<string, unknown>;
    (reviewWithCapability.status as Record<string, unknown>).capability_id =
      RAW_CAPABILITY_ID;
    (reviewWithCapability.status as Record<string, unknown>).capability_expires_at =
      1_800_000_000_000;
    expect(() => parseHostedReviewEnvelope(reviewWithCapability)).toThrow(
      /credential field/i,
    );

    const statusWithCapability = durableStatus(reviewingSnapshot);
    statusWithCapability.capability_id = RAW_CAPABILITY_ID;
    statusWithCapability.capability_expires_at = 1_800_000_000_000;
    expect(() => parseHostedJobStatus(statusWithCapability, JOB_ID)).toThrow(
      /credential field/i,
    );

    const reviewWithCapabilityValue = structuredClone(reviewingSnapshot);
    reviewWithCapabilityValue.preview.member_changes[0]!.rationale =
      RAW_CAPABILITY_ID;
    expect(() => parseHostedReviewEnvelope(reviewWithCapabilityValue)).toThrow(
      /credential-like data/i,
    );
  });

  it("keeps raw capability material out of tools, prompts, rendering, and persistence", async () => {
    const setWidgetState = vi.fn();
    window.openai = { setWidgetState } as unknown as OpenAIWidgetRuntime;
    const storageWrite = vi.spyOn(Storage.prototype, "setItem");
    const bridge = new FakeBridge(reviewingSnapshot);
    bridge.callResults = [
      { structuredContent: durableStatus(reviewingSnapshot) },
      { structuredContent: reviewingSnapshot },
    ];
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await screen.findByText("Review the weave");
    expectNoRawCapability(document.documentElement.innerHTML);
    expect(setWidgetState).not.toHaveBeenCalled();
    expect(storageWrite).not.toHaveBeenCalled();

    await user.click(screen.getByRole("button", { name: "Refresh" }));
    expectNoRawCapability(bridge.calls);

    await user.type(
      screen.getByLabelText("Describe a change to this proposal"),
      "Keep the brief nearby",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));
    expect(bridge.prompts).toHaveLength(1);
    expectNoRawCapability(bridge.prompts);
    expectNoRawCapability(document.body.textContent);
    expect(setWidgetState).not.toHaveBeenCalled();
    expect(storageWrite).not.toHaveBeenCalled();
  });

  it("sends revisions through the host model loop and keeps execution tools untouched", async () => {
    const bridge = new FakeBridge();
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.type(
      screen.getByLabelText("Describe a change to this proposal"),
      "Keep the brief under Client delivery",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));

    expect(bridge.prompts).toHaveLength(1);
    expect(bridge.prompts[0]).toContain("Use the Foldweave host-planning tools");
    expect(bridge.prompts[0]).toContain(
      'set every sparse entry evidence_ids exactly to ["initial_inventory"]',
    );
    expect(bridge.prompts[0]).toContain(
      "Do not call evidence tools after revise_plan",
    );
    expect(bridge.prompts[0]).toContain("Keep the brief under Client delivery");
    expect(bridge.prompts[0]).toContain(C);
    expect(bridge.prompts[0]).toContain(D);
    expect(bridge.calls).toHaveLength(0);
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeDisabled();
    expect(screen.getByRole("button", { name: "Send changes" })).toBeDisabled();
  });

  it("dispatches only one host turn for two same-tick revision clicks", async () => {
    const bridge = new FakeBridge();
    let releaseFollowUp: (() => void) | undefined;
    const pendingFollowUp = new Promise<void>((resolve) => {
      releaseFollowUp = resolve;
    });
    const sendFollowUp = vi
      .spyOn(bridge, "sendFollowUpMessage")
      .mockImplementation(async (prompt: string) => {
        bridge.prompts.push(prompt);
        await pendingFollowUp;
      });
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.type(
      screen.getByLabelText("Describe a change to this proposal"),
      "Keep the brief under Client delivery",
    );
    const send = screen.getByRole("button", { name: "Send changes" });
    await act(async () => {
      send.click();
      send.click();
      await Promise.resolve();
    });

    expect(sendFollowUp).toHaveBeenCalledTimes(1);
    expect(bridge.prompts).toHaveLength(1);
    releaseFollowUp?.();
    await act(async () => pendingFollowUp);
  });

  it("calls exact acceptance without emitting a local path or credential", async () => {
    const bridge = new FakeBridge();
    bridge.callResult = {
      structuredContent: {
        ...reviewingSnapshot,
        state_version: 4,
        status: {
          ...reviewingSnapshot.status,
          lifecycle: "executing",
          job_revision: 4,
          revision_available: false,
        },
      },
    };
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(
      await screen.findByRole("button", {
        name: "Accept this structure and create copy",
      }),
    );

    expect(bridge.calls).toHaveLength(1);
    expect(bridge.calls[0]?.name).toBe("accept_plan_and_create_copy");
    expect(bridge.calls[0]?.argumentsValue).toMatchObject({
      job_id: JOB_ID,
      expected_revision: 3,
      proposal_revision: 1,
      candidate_fingerprint: C,
      preview_fingerprint: D,
      source_commitment: A,
      authorization_context_fingerprint: E,
    });
    expect(bridge.calls[0]?.argumentsValue).not.toHaveProperty("channel");
    expect(bridge.calls[0]?.argumentsValue).not.toHaveProperty("output_parent");
    expect(bridge.calls[0]?.argumentsValue).not.toHaveProperty("result_folder_name");
    expect(JSON.stringify(bridge.calls[0]?.argumentsValue)).not.toMatch(
      /(?:\/Users\/|sk-(?:proj-)?)/,
    );
    expect(await screen.findByText("Creating the separate copy")).toBeInTheDocument();
  });

  it("keeps the previous proposal without caller-supplied profile metadata", async () => {
    const bridge = new FakeBridge(revisionFailedSnapshot());
    bridge.callResult = { structuredContent: restoredPreviousSnapshot() };
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(
      await screen.findByRole("button", { name: "Keep previous proposal" }),
    );

    expect(bridge.calls).toHaveLength(1);
    expect(bridge.calls[0]?.name).toBe("keep_previous_proposal");
    expect(bridge.calls[0]?.argumentsValue).toMatchObject({
      job_id: JOB_ID,
      expected_revision: 4,
      proposal_revision: 1,
      candidate_fingerprint: C,
      preview_fingerprint: D,
      source_commitment: A,
      authorization_context_fingerprint: B,
    });
    expect(bridge.calls[0]?.argumentsValue).not.toHaveProperty("channel");
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeEnabled();
  });

  it("refreshes the mounted widget from a complete tool result", async () => {
    const bridge = new FakeBridge();
    bridge.callResults = [
      { structuredContent: durableStatus(verifiedSnapshot()) },
      { structuredContent: verifiedSnapshot() },
    ];
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(await screen.findByRole("button", { name: "Refresh" }));

    expect(bridge.calls.map((call) => call.name)).toEqual([
      "job_status",
      "get_plan_preview",
    ]);
    expect(bridge.calls[0]?.argumentsValue).toEqual({ job_id: JOB_ID });
    expect(bridge.calls[1]?.argumentsValue).toEqual({
      job_id: JOB_ID,
      expected_revision: 5,
      preview_fingerprint: D,
    });
    expect(await screen.findByText("Your new folder is ready")).toBeInTheDocument();
  });

  it("binds refresh calls only to the durable job and exact preview", async () => {
    const bridge = new FakeBridge(reviewingSnapshot);
    bridge.callResults = [
      { structuredContent: durableStatus(reviewingSnapshot) },
      { structuredContent: reviewingSnapshot },
    ];
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(await screen.findByRole("button", { name: "Refresh" }));

    expect(bridge.calls).toEqual([
      {
        name: "job_status",
        argumentsValue: {
          job_id: JOB_ID,
        },
      },
      {
        name: "get_plan_preview",
        argumentsValue: {
          job_id: JOB_ID,
          expected_revision: 3,
          preview_fingerprint: D,
        },
      },
    ]);
    expectNoRawCapability(bridge.calls);
  });

  it("atomically replaces parent job authority with one bound derivative child", async () => {
    const parent = receiverSnapshot();
    const child = derivativeReview(parent);
    expect(() => parseHostedJobStatus(derivativePendingStatus(parent))).not.toThrow();
    expect(() => parseHostedReviewEnvelope(child)).not.toThrow();
    const executingChild = {
      ...child,
      state_version: 2,
      status: {
        ...child.status,
        lifecycle: "executing" as const,
        job_revision: 2,
        revision_available: false,
      },
    };
    const bridge = new FakeBridge(parent);
    bridge.callResult = { structuredContent: executingChild };
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.type(
      await screen.findByLabelText("Describe a change to this proposal"),
      "Use this shared structure as the next proposal",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));
    act(() => bridge.emitRaw(derivativePendingStatus(parent)));
    act(() => bridge.emitRaw(child));

    await user.click(
      await screen.findByRole("button", {
        name: "Accept this structure and create copy",
      }),
    );

    expect(bridge.calls).toHaveLength(1);
    expect(bridge.calls[0]?.name).toBe("accept_plan_and_create_copy");
    expect(bridge.calls[0]?.argumentsValue).toMatchObject({
      job_id: CHILD_JOB_ID,
      expected_revision: 1,
      candidate_fingerprint: F,
      preview_fingerprint: ZERO,
    });
    expectNoRawCapability(bridge.calls[0]?.argumentsValue);
    expect(await screen.findByText("Creating the separate copy")).toBeInTheDocument();
  });

  it("rejects a derivative child that is not bound to the visible parent candidate", async () => {
    const parent = receiverSnapshot();
    const child = derivativeReview(parent);
    child.preview.immediate_parent_candidate_fingerprint = ZERO;
    const bridge = new FakeBridge(parent);
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.type(
      await screen.findByLabelText("Describe a change to this proposal"),
      "Try a derivative structure",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));
    act(() => bridge.emitRaw(derivativePendingStatus(parent)));
    act(() => bridge.emitRaw(child));

    expect(
      await screen.findByText(/different job from replacing this review/i),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeDisabled();
    expect(bridge.calls).toHaveLength(0);
  });

  it("invokes source-free verification from the verified state", async () => {
    const bridge = new FakeBridge(verifiedSnapshot());
    bridge.callResult = {
      structuredContent: {
        schema_version: "foldweave-verification-result.v1",
        verification: "verified",
        job_id: JOB_ID,
        receipt_fingerprint: ZERO,
        organized_tree_commitment: A,
        failed_check_ids: [],
      },
    };
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(await screen.findByRole("button", { name: "Verify again" }));

    expect(bridge.calls[0]).toEqual({
      name: "verify_result",
      argumentsValue: {
        job_id: JOB_ID,
        organized_tree_commitment: A,
      },
    });
    expect(await screen.findByText("Independent verification passed again.")).toBeInTheDocument();
  });

  it("retrieves the verified Change File through one path-free widget tool call", async () => {
    const bridge = new FakeBridge(verifiedSnapshot());
    bridge.callResult = { structuredContent: changeFileResult() };
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(await screen.findByRole("button", { name: "Get Change File" }));

    expect(bridge.calls).toEqual([
      {
        name: "get_change_file",
        argumentsValue: { job_id: JOB_ID },
      },
    ]);
    expect(await screen.findByText("Foldweave Change File ready")).toBeInTheDocument();
    expect(screen.getByText(CHANGE_FILE_HANDLE)).toBeInTheDocument();
    expect(screen.getByText("northstar.foldweave-change.json")).toBeInTheDocument();
    expect(document.body.textContent).not.toContain("/Users/");
  });

  it("recreates and reverifies the fixed original using only immutable job authority", async () => {
    const bridge = new FakeBridge(verifiedSnapshot());
    bridge.callResult = { structuredContent: reconstructionResult() };
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    const recreate = await screen.findByRole("button", { name: "Recreate original" });
    await user.click(recreate);
    expect(await screen.findByText("Original layout recreated and verified")).toBeInTheDocument();
    await user.click(recreate);

    expect(bridge.calls).toEqual([
      { name: "recreate_original", argumentsValue: { job_id: JOB_ID } },
      { name: "recreate_original", argumentsValue: { job_id: JOB_ID } },
    ]);
    expect(screen.getByText(RESTORE_HANDLE)).toBeInTheDocument();
    expect(screen.getByText("northstar-original-layout")).toBeInTheDocument();
    expect(document.body.textContent).not.toContain("idempotency");
    expect(document.body.textContent).not.toContain("/Users/");
  });

  it("blocks sensitive Change File and reconstruction tool results", async () => {
    const unsafeChangeFile = changeFileResult();
    unsafeChangeFile.item.display_name = "/Users/example/private.foldweave-change.json";
    expect(() =>
      parseHostedChangeFileResult(unsafeChangeFile, JOB_ID, B),
    ).toThrow(/local absolute path/i);

    const unsafeReconstruction = reconstructionResult();
    unsafeReconstruction.item.display_name = "/private/tmp/restored-original";
    expect(() =>
      parseHostedReconstructionResult(unsafeReconstruction, JOB_ID, A, 1),
    ).toThrow(/local absolute path/i);
  });

  it("never reports verification success when the host omits proof evidence", async () => {
    const bridge = new FakeBridge(verifiedSnapshot());
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(await screen.findByRole("button", { name: "Verify again" }));

    expect(
      await screen.findByText(/did not return independent verification evidence/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Independent verification passed again."),
    ).not.toBeInTheDocument();
  });

  it("reconciles a same-version job after a host revision produces no tool call", async () => {
    const bridge = new FakeBridge();
    bridge.callResults = [
      { structuredContent: durableStatus(reviewingSnapshot) },
      { structuredContent: reviewingSnapshot },
    ];
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} hostRecoveryMs={10} />);

    await user.type(
      await screen.findByLabelText("Describe a change to this proposal"),
      "Keep the brief nearby",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));

    await waitFor(() =>
      expect(bridge.calls.map((call) => call.name)).toEqual([
        "job_status",
        "get_plan_preview",
      ]),
    );
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeEnabled();
    expect(
      screen.getByLabelText("Describe a change to this proposal"),
    ).toHaveValue("Keep the brief nearby");
    expect(screen.getByRole("button", { name: "Send changes" })).toBeEnabled();
  });

  it("recovers a newer durable preview when its host notification is missing", async () => {
    const bridge = new FakeBridge();
    const revised = revisedSnapshot();
    bridge.callResults = [
      { structuredContent: durableStatus(revised) },
      { structuredContent: revised },
    ];
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} hostRecoveryMs={10} />);

    await user.type(
      await screen.findByLabelText("Describe a change to this proposal"),
      "Keep the brief with the client delivery",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));

    expect(
      await screen.findByText("Client/brief.md", { selector: "h2" }),
    ).toBeInTheDocument();
    expect(screen.getByText(/1 mapping changed from the previous proposal/i)).toBeInTheDocument();
  });

  it("reconciles the durable preview after the host cancels a revision", async () => {
    const bridge = new FakeBridge();
    bridge.callResults = [
      { structuredContent: durableStatus(reviewingSnapshot) },
      { structuredContent: reviewingSnapshot },
    ];
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} hostRecoveryMs={5_000} />);

    await user.type(
      await screen.findByLabelText("Describe a change to this proposal"),
      "Try another grouping",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));
    bridge.interrupt("tool_cancelled");

    await waitFor(() => expect(bridge.calls.at(-1)?.name).toBe("get_plan_preview"));
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeEnabled();
  });

  it("quarantines conflicting state until a complete durable refresh succeeds", async () => {
    const bridge = new FakeBridge();
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);
    await screen.findByText("Review the weave");

    bridge.emitRaw({
      ...reviewingSnapshot,
      status: {
        ...reviewingSnapshot.status,
        authorization_context_fingerprint: F,
      },
    });

    expect(await screen.findByText(/conflicting data for the same review version/i)).toBeInTheDocument();
    const accept = screen.getByRole("button", {
      name: "Accept this structure and create copy",
    });
    expect(accept).toBeDisabled();

    bridge.callResults = [
      { structuredContent: durableStatus(reviewingSnapshot) },
      { structuredContent: reviewingSnapshot },
    ];
    await user.click(screen.getByRole("button", { name: "Refresh" }));
    await waitFor(() => expect(accept).toBeEnabled());
  });

  it("quarantines a complete snapshot belonging to a different job", async () => {
    const bridge = new FakeBridge();
    render(<FoldweaveChatGptWidget bridge={bridge} />);
    await screen.findByText("Review the weave");
    const otherJob = structuredClone(reviewingSnapshot);
    otherJob.preview.job_id = "2".repeat(32);
    otherJob.status.job_id = "2".repeat(32);

    bridge.emitRaw(otherJob);

    expect(await screen.findByText(/different job from replacing this review/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeDisabled();
  });

  it("quarantines an invalid newer preview instead of leaving old actions active", async () => {
    const bridge = new FakeBridge();
    render(<FoldweaveChatGptWidget bridge={bridge} />);
    await screen.findByText("Review the weave");
    const invalid = structuredClone(reviewingSnapshot);
    invalid.state_version = 4;
    invalid.status.job_revision = 4;
    invalid.preview.expected_job_revision = 4;
    invalid.preview.proposed_tree_members[0]!.relative_path = "Wrong/brief.md";

    bridge.emitRaw(invalid);

    expect(await screen.findByText(/does not reconcile both structure views/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeDisabled();
  });

  it("quarantines a job that durable status reports as stale", async () => {
    const bridge = new FakeBridge();
    bridge.callResult = {
      structuredContent: durableStatus(reviewingSnapshot, "stale"),
    };
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(await screen.findByRole("button", { name: "Refresh" }));

    expect(await screen.findByText(/marked this job stale/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeDisabled();
  });

  it("rejects path-inconsistent, count-inconsistent, and incomplete preview DTOs", () => {
    const pathMismatch = structuredClone(reviewingSnapshot);
    pathMismatch.preview.proposed_tree_members[0]!.relative_path = "Other/brief.md";
    expect(() => parseHostedReviewEnvelope(pathMismatch)).toThrow(
      "does not reconcile both structure views",
    );

    const countMismatch = structuredClone(reviewingSnapshot);
    countMismatch.preview.counts.changed_path_count = 0;
    expect(() => parseHostedReviewEnvelope(countMismatch)).toThrow(
      "counts differ",
    );

    const incomplete = structuredClone(reviewingSnapshot) as unknown as Record<
      string,
      unknown
    >;
    delete (incomplete.preview as Record<string, unknown>).blocker_findings;
    expect(() => parseHostedReviewEnvelope(incomplete)).toThrow(
      "incomplete preview contract",
    );
  });

  it("normalizes only omitted nullable fields from the ChatGPT transport", () => {
    const omittedReviewNulls = structuredClone(reviewingSnapshot) as unknown as Record<
      string,
      unknown
    >;
    const preview = omittedReviewNulls.preview as Record<string, unknown>;
    const status = omittedReviewNulls.status as Record<string, unknown>;
    delete preview.imported_change_file_fingerprint;
    delete preview.match_report_fingerprint;
    delete preview.immediate_parent_candidate_fingerprint;
    delete status.revision_failure;
    delete omittedReviewNulls.result;

    const parsedReview = parseHostedReviewEnvelope(omittedReviewNulls);
    expect(parsedReview.preview.imported_change_file_fingerprint).toBeNull();
    expect(parsedReview.preview.match_report_fingerprint).toBeNull();
    expect(parsedReview.preview.immediate_parent_candidate_fingerprint).toBeNull();
    expect(parsedReview.status.revision_failure).toBeNull();
    expect(parsedReview.result).toBeNull();

    const omittedStatusNulls = durableStatus(reviewingSnapshot);
    delete omittedStatusNulls.clarification_question;
    delete omittedStatusNulls.clarification_question_fingerprint;
    delete omittedStatusNulls.revision_failure_code;
    delete omittedStatusNulls.blocker_code;
    const parsedStatus = parseHostedJobStatus(omittedStatusNulls, JOB_ID);
    expect(parsedStatus.clarification_question).toBeNull();
    expect(parsedStatus.clarification_question_fingerprint).toBeNull();
    expect(parsedStatus.revision_failure_code).toBeNull();
    expect(parsedStatus.blocker_code).toBeNull();

    const invalidRequiredField = structuredClone(omittedReviewNulls) as Record<
      string,
      unknown
    >;
    delete (invalidRequiredField.preview as Record<string, unknown>).blocker_findings;
    expect(() => parseHostedReviewEnvelope(invalidRequiredField)).toThrow(
      "incomplete preview contract",
    );
  });

  it("accepts truthful server-owned provenance for Codex and model-free receiver review", () => {
    const codexReview = structuredClone(reviewingSnapshot);
    codexReview.status.model_transport = "codex_hosted";
    expect(parseHostedReviewEnvelope(codexReview).status).toMatchObject({
      planning_basis: "fresh",
      model_transport: "codex_hosted",
      execution_origin: "none",
    });

    const receiverReview = structuredClone(reviewingSnapshot);
    receiverReview.journey = "apply";
    receiverReview.preview.proposal_basis = "imported_change_file";
    receiverReview.preview.imported_change_file_fingerprint = B;
    receiverReview.preview.match_report_fingerprint = E;
    receiverReview.status.planning_basis = "none";
    receiverReview.status.model_transport = "none";
    receiverReview.status.execution_origin = "capsule_applied";
    expect(parseHostedReviewEnvelope(receiverReview).status).toMatchObject({
      planning_basis: "none",
      model_transport: "none",
      execution_origin: "capsule_applied",
    });

    const derivativeStatus = durableStatus(codexReview);
    derivativeStatus.planning_basis = "derivative";
    derivativeStatus.execution_origin = "gpt_revised_from_change_file";
    expect(parseHostedJobStatus(derivativeStatus, JOB_ID)).toMatchObject({
      planning_basis: "derivative",
      model_transport: "codex_hosted",
      execution_origin: "gpt_revised_from_change_file",
    });

    const receiverStatus = durableStatus(receiverReview);
    expect(parseHostedJobStatus(receiverStatus, JOB_ID)).toMatchObject({
      planning_basis: "none",
      model_transport: "none",
      execution_origin: "capsule_applied",
    });
  });

  it("rejects contradictory host provenance combinations", () => {
    const invalidReview = structuredClone(reviewingSnapshot) as unknown as Record<
      string,
      unknown
    >;
    const status = invalidReview.status as Record<string, unknown>;
    status.planning_basis = "none";
    status.model_transport = "chatgpt_hosted";
    status.execution_origin = "capsule_applied";
    expect(() => parseHostedReviewEnvelope(invalidReview)).toThrow(
      "status does not match its exact preview",
    );

    const invalidStatus = durableStatus(reviewingSnapshot);
    invalidStatus.planning_basis = "derivative";
    invalidStatus.execution_origin = "gpt_planned";
    expect(() => parseHostedJobStatus(invalidStatus, JOB_ID)).toThrow(
      "valid durable hosted status",
    );
  });

  it("blocks absolute paths and credential fields before rendering or sending", async () => {
    const unsafeSnapshot = structuredClone(reviewingSnapshot) as unknown as Record<
      string,
      unknown
    >;
    unsafeSnapshot.api_key = "sk-proj-not-allowed";
    expect(() => parseHostedReviewEnvelope(unsafeSnapshot)).toThrow(
      "credential field",
    );

    const bridge = new FakeBridge();
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);
    await user.type(
      await screen.findByLabelText("Describe a change to this proposal"),
      "/Users/example/private should move",
    );
    await user.click(screen.getByRole("button", { name: "Send changes" }));

    expect(bridge.prompts).toHaveLength(0);
    expect(await screen.findByText(/blocked a local absolute path/i)).toBeInTheDocument();
  });

  it("allows relative project paths containing a tmp directory", () => {
    expect(() =>
      assertNoSensitiveBoundaryData({
        relative_path: "drafts/tmp/layout.bin",
        original_destination: "../drafts/tmp/layout.bin",
      }),
    ).not.toThrow();
  });
});

describe("MCP Apps host bridge", () => {
  it("normalizes only bounded known Foldweave tool-result wrappers", () => {
    const status = durableStatus(reviewingSnapshot);

    expect(extractStructuredContent({ structuredContent: status })).toEqual(status);
    expect(extractStructuredContent({ structured_content: status })).toEqual(status);
    expect(
      extractStructuredContent({ result: { structuredContent: status } }),
    ).toEqual(status);
    expect(
      extractStructuredContent({
        structuredContent: { structuredContent: status },
      }),
    ).toEqual(status);
    expect(
      extractStructuredContent({
        structuredContent: { result: { structuredContent: status } },
      }),
    ).toEqual(status);
    expect(extractStructuredContent(status)).toEqual(status);
    expect(
      extractStructuredContent({
        structuredContent: {
          structuredContent: {
            structuredContent: { structuredContent: status },
          },
        },
      }),
    ).toBeUndefined();
    expect(
      extractStructuredContent({
        structuredContent: status,
        isError: true,
      }),
    ).toBeUndefined();
    expect(
      extractStructuredContent({ schema_version: "unknown.v1" }),
    ).toBeUndefined();
  });

  it("does not treat status or verification notifications as review snapshots", async () => {
    const bridge = new FakeBridge();
    render(<FoldweaveChatGptWidget bridge={bridge} />);
    const accept = await screen.findByRole("button", {
      name: "Accept this structure and create copy",
    });

    bridge.emitRaw(durableStatus(reviewingSnapshot));
    bridge.emitRaw({
      schema_version: "foldweave-verification-result.v1",
      verification: "verified",
      job_id: JOB_ID,
      receipt_fingerprint: ZERO,
      organized_tree_commitment: A,
      failed_check_ids: [],
    });

    await waitFor(() => expect(accept).toBeEnabled());
    expect(screen.queryByText(/valid durable hosted status/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/review snapshot/i)).not.toBeInTheDocument();
  });

  it("refreshes through the additional live-host result wrappers", async () => {
    const bridge = new FakeBridge();
    bridge.callResults = [
      {
        structuredContent: {
          result: { structuredContent: durableStatus(reviewingSnapshot) },
        },
      },
      {
        structuredContent: {
          result: { structuredContent: reviewingSnapshot },
        },
      },
    ];
    const user = userEvent.setup();
    render(<FoldweaveChatGptWidget bridge={bridge} />);

    await user.click(await screen.findByRole("button", { name: "Refresh" }));

    expect(bridge.calls.map((call) => call.name)).toEqual([
      "job_status",
      "get_plan_preview",
    ]);
    expect(
      screen.getByRole("button", { name: "Accept this structure and create copy" }),
    ).toBeEnabled();
    expect(screen.queryByText(/valid durable hosted status/i)).not.toBeInTheDocument();
  });

  it("initializes JSON-RPC, calls tools, receives results, and notifies ui/message", async () => {
    const postMessage = vi.spyOn(window.parent, "postMessage").mockImplementation(() => undefined);
    const bridge = new McpAppsHostBridge(window, 2_000);
    const received: unknown[] = [];
    bridge.subscribeToolResults((value) => received.push(value));

    const connectPromise = bridge.connect();
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(1));
    const initialize = postMessage.mock.calls[0]?.[0] as Record<string, unknown>;
    expect(initialize.method).toBe("ui/initialize");
    dispatchRpc({
      jsonrpc: "2.0",
      id: initialize.id,
      result: { hostCapabilities: {} },
    });
    await connectPromise;

    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(2));
    expect((postMessage.mock.calls[1]?.[0] as Record<string, unknown>).method).toBe(
      "ui/notifications/initialized",
    );
    const toolPromise = bridge.callTool("get_plan_preview", { job_id: JOB_ID });
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(3));
    const toolCall = postMessage.mock.calls[2]?.[0] as Record<string, unknown>;
    expect(toolCall).toMatchObject({ method: "tools/call" });
    dispatchRpc({
      jsonrpc: "2.0",
      id: toolCall.id,
      result: { structuredContent: reviewingSnapshot },
    });
    await expect(toolPromise).resolves.toEqual({
      structuredContent: reviewingSnapshot,
    });

    dispatchRpc({
      jsonrpc: "2.0",
      method: "ui/notifications/tool-result",
      params: { structuredContent: verifiedSnapshot() },
    });
    expect(received).toEqual([verifiedSnapshot()]);

    await bridge.sendFollowUpMessage("Revise this proposal.");
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(4));
    const followUp = postMessage.mock.calls.at(-1)?.[0] as Record<string, unknown>;
    expect(followUp).toMatchObject({
      method: "ui/message",
      params: {
        role: "user",
        content: [{ type: "text", text: "Revise this proposal." }],
      },
    });
    expect(followUp).not.toHaveProperty("id");
    bridge.dispose();
  });

  it("submits an MCP Apps follow-up without a nonstandard capability gate", async () => {
    const postMessage = vi
      .spyOn(window.parent, "postMessage")
      .mockImplementation(() => undefined);
    const bridge = new McpAppsHostBridge(window, 2_000);

    const connectPromise = bridge.connect();
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(1));
    const initialize = postMessage.mock.calls[0]?.[0] as Record<string, unknown>;
    dispatchRpc({
      jsonrpc: "2.0",
      id: initialize.id,
      result: { hostCapabilities: {} },
    });
    await connectPromise;

    await bridge.sendFollowUpMessage("Revise this proposal.");
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(3));
    const followUp = postMessage.mock.calls.at(-1)?.[0] as Record<string, unknown>;
    expect(followUp).toMatchObject({
      method: "ui/message",
      params: {
        role: "user",
        content: [{ type: "text", text: "Revise this proposal." }],
      },
    });
    expect(followUp).not.toHaveProperty("id");
    bridge.dispose();
  });

  it("receives delayed window.openai globals and host cancellation", async () => {
    const postMessage = vi.spyOn(window.parent, "postMessage").mockImplementation(() => undefined);
    const bridge = new McpAppsHostBridge(window, 2_000);
    const received: unknown[] = [];
    const interruptions: HostInterruption[] = [];
    bridge.subscribeToolResults((value) => received.push(value));
    bridge.subscribeInterruptions((value) => interruptions.push(value));

    const connectPromise = bridge.connect();
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(1));
    const initialize = postMessage.mock.calls[0]?.[0] as Record<string, unknown>;
    window.dispatchEvent(
      new CustomEvent("openai:set_globals", {
        detail: { globals: { toolOutput: reviewingSnapshot } },
      }),
    );
    dispatchRpc({ jsonrpc: "2.0", id: initialize.id, result: {} });
    await connectPromise;
    dispatchRpc({
      jsonrpc: "2.0",
      method: "ui/notifications/tool-cancelled",
      params: { reason: "cancelled" },
    });

    expect(received).toEqual([reviewingSnapshot]);
    expect(interruptions).toEqual(["tool_cancelled"]);
    bridge.dispose();
  });

  it("keeps tools/call standard while preferring the ChatGPT follow-up extension", async () => {
    const postMessage = vi
      .spyOn(window.parent, "postMessage")
      .mockImplementation(() => undefined);
    const callTool = vi.fn(async () => ({ structuredContent: reviewingSnapshot }));
    const sendFollowUpMessage = vi.fn(async () => undefined);
    window.openai = { callTool, sendFollowUpMessage };
    const bridge = new McpAppsHostBridge(window, 2_000);

    const connectPromise = bridge.connect();
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(1));
    const initialize = postMessage.mock.calls[0]?.[0] as Record<string, unknown>;
    dispatchRpc({ jsonrpc: "2.0", id: initialize.id, result: { hostCapabilities: {} } });
    await connectPromise;

    const toolPromise = bridge.callTool("get_plan_preview", { job_id: JOB_ID });
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(3));
    const toolCall = postMessage.mock.calls.at(-1)?.[0] as Record<string, unknown>;
    dispatchRpc({
      jsonrpc: "2.0",
      id: toolCall.id,
      result: { structuredContent: reviewingSnapshot },
    });
    await expect(toolPromise).resolves.toEqual({
      structuredContent: reviewingSnapshot,
    });

    await bridge.sendFollowUpMessage("Revise this proposal.");
    expect(sendFollowUpMessage).toHaveBeenCalledOnce();
    expect(sendFollowUpMessage).toHaveBeenCalledWith({
      prompt: "Revise this proposal.",
      scrollToBottom: true,
    });
    expect(postMessage).toHaveBeenCalledTimes(3);

    expect(callTool).not.toHaveBeenCalled();
    bridge.dispose();
  });

  it("uses the ChatGPT follow-up extension without initializing the standard bridge", async () => {
    const postMessage = vi
      .spyOn(window.parent, "postMessage")
      .mockImplementation(() => undefined);
    const sendFollowUpMessage = vi.fn(async () => undefined);
    window.openai = { sendFollowUpMessage };
    const bridge = new McpAppsHostBridge(window, 2_000);

    await bridge.sendFollowUpMessage("Revise this proposal.");

    expect(sendFollowUpMessage).toHaveBeenCalledWith({
      prompt: "Revise this proposal.",
      scrollToBottom: true,
    });
    expect(postMessage).not.toHaveBeenCalled();
    bridge.dispose();
  });

  it("uses a ChatGPT follow-up extension that appears during standard initialization", async () => {
    const postMessage = vi
      .spyOn(window.parent, "postMessage")
      .mockImplementation(() => undefined);
    const sendFollowUpMessage = vi.fn(async () => undefined);
    const bridge = new McpAppsHostBridge(window, 2_000);

    const followUpPromise = bridge.sendFollowUpMessage("Revise this proposal.");
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(1));
    const initialize = postMessage.mock.calls[0]?.[0] as Record<string, unknown>;
    window.openai = { sendFollowUpMessage };
    dispatchRpc({ jsonrpc: "2.0", id: initialize.id, result: { hostCapabilities: {} } });
    await followUpPromise;

    expect(sendFollowUpMessage).toHaveBeenCalledOnce();
    expect(sendFollowUpMessage).toHaveBeenCalledWith({
      prompt: "Revise this proposal.",
      scrollToBottom: true,
    });
    expect(
      postMessage.mock.calls.some(
        ([message]) =>
          (message as Record<string, unknown>).method === "ui/message",
      ),
    ).toBe(false);
    bridge.dispose();
  });

  it("never sends ui/message after the ChatGPT follow-up extension succeeds", async () => {
    const postMessage = vi
      .spyOn(window.parent, "postMessage")
      .mockImplementation(() => undefined);
    const sendFollowUpMessage = vi.fn(async () => undefined);
    window.openai = { sendFollowUpMessage };
    const bridge = new McpAppsHostBridge(window, 20);

    const connectPromise = bridge.connect();
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(1));
    const initialize = postMessage.mock.calls[0]?.[0] as Record<string, unknown>;
    dispatchRpc({ jsonrpc: "2.0", id: initialize.id, result: { hostCapabilities: {} } });
    await connectPromise;

    await bridge.sendFollowUpMessage("Revise this proposal.");
    expect(sendFollowUpMessage).toHaveBeenCalledOnce();
    expect(postMessage).toHaveBeenCalledTimes(2);
    expect(
      postMessage.mock.calls.some(
        ([message]) =>
          (message as Record<string, unknown>).method === "ui/message",
      ),
    ).toBe(false);
    bridge.dispose();
  });

  it("does not retry through ui/message when the ChatGPT extension rejects", async () => {
    const postMessage = vi
      .spyOn(window.parent, "postMessage")
      .mockImplementation(() => undefined);
    const rejection = new Error("The host rejected the follow-up.");
    const sendFollowUpMessage = vi.fn(async () => {
      throw rejection;
    });
    window.openai = { sendFollowUpMessage };
    const bridge = new McpAppsHostBridge(window, 2_000);

    const connectPromise = bridge.connect();
    await waitFor(() => expect(postMessage).toHaveBeenCalledTimes(1));
    const initialize = postMessage.mock.calls[0]?.[0] as Record<string, unknown>;
    dispatchRpc({ jsonrpc: "2.0", id: initialize.id, result: { hostCapabilities: {} } });
    await connectPromise;

    await expect(
      bridge.sendFollowUpMessage("Revise this proposal."),
    ).rejects.toBe(rejection);
    expect(sendFollowUpMessage).toHaveBeenCalledOnce();
    expect(postMessage).toHaveBeenCalledTimes(2);
    expect(
      postMessage.mock.calls.some(
        ([message]) =>
          (message as Record<string, unknown>).method === "ui/message",
      ),
    ).toBe(false);
    bridge.dispose();
  });
});

function dispatchRpc(data: Record<string, unknown>): void {
  window.dispatchEvent(new MessageEvent("message", { data, source: window }));
}

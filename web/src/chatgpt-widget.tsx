import "@blueprintjs/core/lib/css/blueprint.css";
import "./chatgpt-widget.css";

import {
  Button,
  Callout,
  Card,
  NonIdealState,
  Spinner,
  Tag,
} from "@blueprintjs/core";
import {
  StrictMode,
  type ReactElement,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { createRoot } from "react-dom/client";

import {
  type ChatGptHostBridge,
  type HostInterruption,
  McpAppsHostBridge,
  extractStructuredContent,
  foldweaveStructuredSchema,
} from "./chatgpt-bridge";
import {
  type FoldweaveChangeFileResultV1,
  type FoldweaveChatGptReviewV1,
  type FoldweaveHostedJobStatusV1,
  type FoldweaveReconstructionResultV1,
  assertNoSensitiveBoundaryData,
  parseHostedChangeFileResult,
  parseHostedJobStatus,
  parseHostedReconstructionResult,
  parseHostedReviewEnvelope,
  parseHostedVerificationResult,
} from "./chatgpt-contracts";
import type {
  AcceptanceBindingPayload,
  KeepProposalPayload,
  RevisionPayload,
} from "./contracts";
import { ReviewIsland } from "./review-island";

type PendingAction = "accept" | "revision" | "keep" | null;
type TerminalAction = "verify" | "change_file" | "reconstruct" | null;
type ApplyOutcome = "applied" | "unchanged" | "older" | "rejected";

interface PendingRevisionContext {
  parentJobId: string;
  parentCandidateFingerprint: string;
  parentPreviewFingerprint: string;
  sourceCommitment: string;
}

const DEFAULT_HOST_RECOVERY_MS = 60_000;

export interface FoldweaveChatGptWidgetProps {
  bridge: ChatGptHostBridge;
  hostRecoveryMs?: number;
}

export function FoldweaveChatGptWidget({
  bridge,
  hostRecoveryMs = DEFAULT_HOST_RECOVERY_MS,
}: FoldweaveChatGptWidgetProps): ReactElement {
  const [snapshot, setSnapshot] = useState<FoldweaveChatGptReviewV1 | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pendingAction, setPendingAction] = useState<PendingAction>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [requiresRefresh, setRequiresRefresh] = useState(false);
  const [reconcileRequest, setReconcileRequest] = useState(0);
  const [verificationNotice, setVerificationNotice] = useState<string | null>(null);
  const [terminalAction, setTerminalAction] = useState<TerminalAction>(null);
  const [changeFileEvidence, setChangeFileEvidence] =
    useState<FoldweaveChangeFileResultV1 | null>(null);
  const [reconstructionEvidence, setReconstructionEvidence] =
    useState<FoldweaveReconstructionResultV1 | null>(null);
  const snapshotRef = useRef<FoldweaveChatGptReviewV1 | null>(null);
  const activeJobIdRef = useRef<string | null>(null);
  const pendingRevisionContextRef = useRef<PendingRevisionContext | null>(null);
  const pendingActionRef = useRef<PendingAction>(null);
  const recoveryTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const refreshingRef = useRef(false);
  const reconciledRequestRef = useRef(0);

  const clearRecoveryTimer = useCallback((): void => {
    if (recoveryTimerRef.current !== null) {
      clearTimeout(recoveryTimerRef.current);
      recoveryTimerRef.current = null;
    }
  }, []);

  const clearPendingAction = useCallback((): void => {
    clearRecoveryTimer();
    pendingActionRef.current = null;
    setPendingAction(null);
  }, [clearRecoveryTimer]);

  const beginPendingAction = useCallback(
    (action: Exclude<PendingAction, null>): void => {
      clearRecoveryTimer();
      pendingActionRef.current = action;
      setPendingAction(action);
      recoveryTimerRef.current = setTimeout(() => {
        if (pendingActionRef.current !== action) {
          return;
        }
        pendingActionRef.current = null;
        setPendingAction(null);
        setRequiresRefresh(true);
        setError(
          action === "revision"
            ? "ChatGPT did not return a revised preview in time. Refresh to reconcile the durable job before continuing."
            : "Foldweave did not return the completed action in time. Refresh to reconcile the durable job before continuing.",
        );
        setReconcileRequest((current) => current + 1);
      }, hostRecoveryMs);
    },
    [clearRecoveryTimer, hostRecoveryMs],
  );

  const abandonPendingRevision = useCallback((): void => {
    pendingRevisionContextRef.current = null;
    const current = snapshotRef.current;
    if (current !== null) {
      activeJobIdRef.current = current.status.job_id;
    }
  }, []);

  const applyStructuredContent = useCallback(
    (value: unknown, reconcileSameVersion = false): ApplyOutcome => {
      try {
        const next = parseHostedReviewEnvelope(value);
        const current = snapshotRef.current;
        const activeJobId = activeJobIdRef.current;
        const sameJob = current?.status.job_id === next.status.job_id;
        if (current && !sameJob) {
          const revisionContext = pendingRevisionContextRef.current;
          if (!isBoundDerivativeReview(current, next, revisionContext)) {
            throw new Error("Foldweave blocked a different job from replacing this review.");
          }
          if (
            activeJobId !== null &&
            activeJobId !== current.status.job_id &&
            activeJobId !== next.status.job_id
          ) {
            throw new Error("Foldweave blocked an unrelated derivative job response.");
          }
        } else if (activeJobId !== null && activeJobId !== next.status.job_id) {
          throw new Error("Foldweave blocked a stale hosted job response.");
        }
        if (current && sameJob && next.state_version < current.state_version) {
          return "older";
        }
        if (
          current &&
          sameJob &&
          next.state_version === current.state_version &&
          (next.preview.preview_fingerprint !== current.preview.preview_fingerprint ||
            next.status.lifecycle !== current.status.lifecycle ||
            next.status.authorization_context_fingerprint !==
              current.status.authorization_context_fingerprint)
        ) {
          throw new Error("Foldweave blocked conflicting data for the same review version.");
        }
        if (current && sameJob && next.state_version === current.state_version) {
          if (reconcileSameVersion) {
            pendingRevisionContextRef.current = null;
            setError(null);
            setRequiresRefresh(false);
            clearPendingAction();
          }
          return "unchanged";
        }
        activeJobIdRef.current = next.status.job_id;
        snapshotRef.current = next;
        pendingRevisionContextRef.current = null;
        setSnapshot(next);
        setError(null);
        setRequiresRefresh(false);
        setVerificationNotice(null);
        setChangeFileEvidence(null);
        setReconstructionEvidence(null);
        clearPendingAction();
        return "applied";
      } catch (caught) {
        setError(publicError(caught));
        setRequiresRefresh(snapshotRef.current !== null);
        clearPendingAction();
        return "rejected";
      }
    },
    [clearPendingAction],
  );

  useEffect(() => {
    const unsubscribeResults = bridge.subscribeToolResults((value) => {
      const structuredContent = extractStructuredContent(value);
      const schema = foldweaveStructuredSchema(structuredContent);
      if (schema === "foldweave-chatgpt-review.v1") {
        applyStructuredContent(structuredContent);
      } else if (schema === "foldweave-hosted-job-status.v1") {
        try {
          const status = parseHostedJobStatus(structuredContent);
          const current = snapshotRef.current;
          const activeJobId = activeJobIdRef.current;
          if (current === null || activeJobId === null) {
            return;
          }
          if (status.job_id === activeJobId) {
            return;
          }
          if (
            !isBoundDerivativeStatus(
              current,
              status,
              pendingRevisionContextRef.current,
            )
          ) {
            throw new Error("Foldweave blocked an unrelated derivative job response.");
          }
          activeJobIdRef.current = status.job_id;
        } catch (caught) {
          setError(publicError(caught));
          setRequiresRefresh(snapshotRef.current !== null);
          clearPendingAction();
        }
      }
    });
    const unsubscribeInterruptions = bridge.subscribeInterruptions(
      (interruption: HostInterruption) => {
        abandonPendingRevision();
        clearPendingAction();
        const hasSnapshot = snapshotRef.current !== null;
        setRequiresRefresh(hasSnapshot);
        setError(interruptionMessage(interruption, hasSnapshot));
        if (hasSnapshot && interruption === "tool_cancelled") {
          setReconcileRequest((current) => current + 1);
        }
      },
    );
    const initial = bridge.getInitialStructuredContent();
    if (initial !== undefined && initial !== null) {
      const structuredContent = extractStructuredContent(initial);
      if (
        foldweaveStructuredSchema(structuredContent) ===
        "foldweave-chatgpt-review.v1"
      ) {
        applyStructuredContent(structuredContent);
      }
    }
    void bridge.connect().catch((caught: unknown) => {
      if (snapshotRef.current === null) {
        setError(publicError(caught));
      }
    });
    return () => {
      unsubscribeResults();
      unsubscribeInterruptions();
    };
  }, [
    abandonPendingRevision,
    applyStructuredContent,
    bridge,
    clearPendingAction,
  ]);

  useEffect(() => clearRecoveryTimer, [clearRecoveryTimer]);

  const applyToolResponse = useCallback(
    (response: unknown, reconcileSameVersion = false): ApplyOutcome | "missing" => {
      const structuredContent = extractStructuredContent(response);
      if (structuredContent === undefined) {
        return "missing";
      }
      return applyStructuredContent(structuredContent, reconcileSameVersion);
    },
    [applyStructuredContent],
  );

  const callJobBoundTool = useCallback(
    async (
      name: string,
      expectedJobId: string,
      argumentsValue: Record<string, unknown>,
    ): Promise<unknown> => {
      const activeJobId = activeJobIdRef.current;
      if (activeJobId === null || activeJobId !== expectedJobId) {
        throw new Error("Foldweave blocked a stale hosted job action.");
      }
      const boundArguments = bindHostedJobToolArguments(
        activeJobId,
        argumentsValue,
      );
      assertNoSensitiveBoundaryData(boundArguments);
      try {
        return await bridge.callTool(name, boundArguments);
      } catch (caught) {
        throw new Error(publicError(caught));
      }
    },
    [bridge],
  );

  const reconcileDurableJob = useCallback(async (): Promise<void> => {
    const current = snapshotRef.current;
    const activeJobId = activeJobIdRef.current;
    if (current === null || activeJobId === null || refreshingRef.current) {
      return;
    }
    refreshingRef.current = true;
    setRefreshing(true);
    setVerificationNotice(null);
    try {
      const statusResponse = await callJobBoundTool(
        "job_status",
        activeJobId,
        {},
      );
      const statusContent = extractStructuredContent(statusResponse);
      if (statusContent === undefined) {
        throw new Error("Foldweave did not return its durable hosted status.");
      }
      const durableStatus = parseHostedJobStatus(
        statusContent,
        activeJobId,
      );
      if (durableStatus.source_commitment !== current.preview.source_commitment) {
        throw new Error("Foldweave blocked a durable status for a different source.");
      }
      if (durableStatus.lifecycle === "stale") {
        throw new Error(
          "Foldweave marked this job stale because its source or Change File changed. Start a fresh job.",
        );
      }
      if (durableStatus.lifecycle === "blocked") {
        throw new Error("Foldweave marked this hosted job blocked. Start a fresh job.");
      }
      if (
        !durableStatus.has_preview ||
        durableStatus.preview_fingerprint === null ||
        durableStatus.candidate_fingerprint === null ||
        (durableStatus.lifecycle !== "reviewing" &&
          durableStatus.lifecycle !== "revision_failed" &&
          durableStatus.lifecycle !== "executing" &&
          durableStatus.lifecycle !== "verified")
      ) {
        throw new Error(
          "Foldweave is still waiting for a complete reviewable proposal. Refresh again after ChatGPT finishes.",
        );
      }
      const previewResponse = await callJobBoundTool(
        "get_plan_preview",
        durableStatus.job_id,
        {
          expected_revision: durableStatus.job_revision,
          preview_fingerprint: durableStatus.preview_fingerprint,
        },
      );
      const outcome = applyToolResponse(previewResponse, true);
      if (outcome !== "applied" && outcome !== "unchanged") {
        throw new Error("Foldweave did not return a complete reconciled preview.");
      }
    } catch (caught) {
      clearPendingAction();
      setRequiresRefresh(true);
      setError(publicError(caught));
    } finally {
      refreshingRef.current = false;
      setRefreshing(false);
    }
  }, [applyToolResponse, callJobBoundTool, clearPendingAction]);

  useEffect(() => {
    if (reconcileRequest === reconciledRequestRef.current) {
      return;
    }
    reconciledRequestRef.current = reconcileRequest;
    void reconcileDurableJob();
  }, [reconcileDurableJob, reconcileRequest]);

  const acceptPlan = useCallback(
    async (binding: AcceptanceBindingPayload): Promise<void> => {
      if (!snapshot) {
        throw new Error("Foldweave has no exact preview to accept.");
      }
      pendingRevisionContextRef.current = null;
      beginPendingAction("accept");
      const response = await callJobBoundTool(
        "accept_plan_and_create_copy",
        snapshot.status.job_id,
        {
          ...exactPreviewBinding(snapshot),
          ...binding,
        },
      ).catch((caught: unknown) => {
        clearPendingAction();
        setRequiresRefresh(true);
        throw caught;
      });
      const outcome = applyToolResponse(response);
      if (outcome !== "applied") {
        clearPendingAction();
        setRequiresRefresh(true);
        throw new Error(
          "Foldweave did not return the completed exact acceptance. Refresh before continuing.",
        );
      }
    },
    [
      applyToolResponse,
      beginPendingAction,
      callJobBoundTool,
      clearPendingAction,
      snapshot,
    ],
  );

  const revisePlan = useCallback(
    async (payload: RevisionPayload): Promise<void> => {
      if (pendingActionRef.current !== null) {
        return;
      }
      if (!snapshot) {
        throw new Error("Foldweave has no exact preview to revise.");
      }
      if (payload.instruction.length > 2_000) {
        throw new Error("Foldweave revision instructions are limited to 2,000 characters.");
      }
      assertNoSensitiveBoundaryData(payload);
      const prompt = createRevisionPrompt(snapshot, payload);
      assertNoSensitiveBoundaryData(prompt);
      pendingRevisionContextRef.current = {
        parentJobId: snapshot.status.job_id,
        parentCandidateFingerprint: snapshot.preview.compiled_candidate_fingerprint,
        parentPreviewFingerprint: snapshot.preview.preview_fingerprint,
        sourceCommitment: snapshot.preview.source_commitment,
      };
      beginPendingAction("revision");
      try {
        await bridge.sendFollowUpMessage(prompt);
      } catch (caught) {
        abandonPendingRevision();
        clearPendingAction();
        throw new Error(publicError(caught));
      }
    },
    [
      abandonPendingRevision,
      beginPendingAction,
      bridge,
      clearPendingAction,
      snapshot,
    ],
  );

  const keepPrevious = useCallback(
    async (payload: KeepProposalPayload): Promise<void> => {
      if (!snapshot) {
        throw new Error("Foldweave has no previous proposal to keep.");
      }
      pendingRevisionContextRef.current = null;
      beginPendingAction("keep");
      const response = await callJobBoundTool(
        "keep_previous_proposal",
        snapshot.status.job_id,
        {
          ...exactPreviewBinding(snapshot),
          ...payload,
        },
      ).catch((caught: unknown) => {
        clearPendingAction();
        setRequiresRefresh(true);
        throw caught;
      });
      if (applyToolResponse(response) !== "applied") {
        clearPendingAction();
        setRequiresRefresh(true);
        throw new Error("Foldweave did not return the preserved proposal.");
      }
    },
    [
      applyToolResponse,
      beginPendingAction,
      callJobBoundTool,
      clearPendingAction,
      snapshot,
    ],
  );

  const refresh = useCallback(async (): Promise<void> => {
    await reconcileDurableJob();
  }, [reconcileDurableJob]);

  const verifyResult = useCallback(async (): Promise<void> => {
    if (!snapshot || snapshot.status.lifecycle !== "verified") {
      return;
    }
    if (refreshingRef.current) {
      return;
    }
    refreshingRef.current = true;
    setRefreshing(true);
    setTerminalAction("verify");
    setVerificationNotice(null);
    setError(null);
    try {
      const response = await callJobBoundTool(
        "verify_result",
        snapshot.status.job_id,
        {
          organized_tree_commitment: snapshot.result!.organized_tree_commitment,
        },
      );
      const structuredContent = extractStructuredContent(response);
      if (structuredContent === undefined) {
        throw new Error("Foldweave did not return independent verification evidence.");
      }
      parseHostedVerificationResult(
        structuredContent,
        snapshot.status.job_id,
        snapshot.result!.organized_tree_commitment,
      );
      setVerificationNotice("Independent verification passed again.");
    } catch (caught) {
      setError(publicError(caught));
    } finally {
      refreshingRef.current = false;
      setRefreshing(false);
      setTerminalAction(null);
    }
  }, [callJobBoundTool, snapshot]);

  const getChangeFile = useCallback(async (): Promise<void> => {
    if (
      !snapshot ||
      snapshot.status.lifecycle !== "verified" ||
      snapshot.result?.change_file_fingerprint === null ||
      snapshot.result?.change_file_fingerprint === undefined ||
      refreshingRef.current
    ) {
      return;
    }
    refreshingRef.current = true;
    setRefreshing(true);
    setTerminalAction("change_file");
    setError(null);
    try {
      const response = await callJobBoundTool(
        "get_change_file",
        snapshot.status.job_id,
        {},
      );
      const structuredContent = extractStructuredContent(response);
      if (structuredContent === undefined) {
        throw new Error("Foldweave did not return the verified Change File identity.");
      }
      const evidence = parseHostedChangeFileResult(
        structuredContent,
        snapshot.status.job_id,
        snapshot.result.change_file_fingerprint,
      );
      setChangeFileEvidence(evidence);
    } catch (caught) {
      setError(publicError(caught));
    } finally {
      refreshingRef.current = false;
      setRefreshing(false);
      setTerminalAction(null);
    }
  }, [callJobBoundTool, snapshot]);

  const recreateOriginal = useCallback(async (): Promise<void> => {
    if (!snapshot || snapshot.status.lifecycle !== "verified" || refreshingRef.current) {
      return;
    }
    refreshingRef.current = true;
    setRefreshing(true);
    setTerminalAction("reconstruct");
    setError(null);
    try {
      const response = await callJobBoundTool(
        "recreate_original",
        snapshot.status.job_id,
        {},
      );
      const structuredContent = extractStructuredContent(response);
      if (structuredContent === undefined) {
        throw new Error("Foldweave did not return verified reconstruction evidence.");
      }
      const evidence = parseHostedReconstructionResult(
        structuredContent,
        snapshot.status.job_id,
        snapshot.preview.source_commitment,
        snapshot.result!.complete_file_count,
      );
      setReconstructionEvidence(evidence);
    } catch (caught) {
      setError(publicError(caught));
    } finally {
      refreshingRef.current = false;
      setRefreshing(false);
      setTerminalAction(null);
    }
  }, [callJobBoundTool, snapshot]);

  const hostStatus = useMemo(() => {
    if (pendingAction === "revision") {
      return "Revision request sent to ChatGPT; waiting for a revised preview.";
    }
    if (pendingAction === "accept") {
      return "The paired Foldweave app is creating and verifying the separate copy.";
    }
    if (pendingAction === "keep") {
      return "Foldweave is restoring the previous valid proposal.";
    }
    return null;
  }, [pendingAction]);

  if (!snapshot) {
    if (error) {
      return (
        <WidgetShell>
          <NonIdealState icon="error" title="Review unavailable" description={error} />
        </WidgetShell>
      );
    }
    return (
      <WidgetShell>
        <div className="fw-chatgpt-loading">
          <Spinner size={24} />
          <span>Waiting for the complete Foldweave preview…</span>
        </div>
      </WidgetShell>
    );
  }

  return (
    <WidgetShell>
      <header className="fw-chatgpt-header">
        <div>
          <span className="fw-eyebrow">CHATGPT-HOSTED PLANNING</span>
          <h1>Review the weave</h1>
          <p>The host model proposes. Your paired Foldweave app checks and executes.</p>
        </div>
        <div className="fw-chatgpt-header-actions">
          <Tag intent="success">No direct API key used</Tag>
          <Button
            disabled={refreshing}
            loading={refreshing}
            onClick={() => void refresh()}
            small
          >
            Refresh
          </Button>
        </div>
      </header>
      {error && (
        <Callout intent="danger" role="alert">
          {error}
          {requiresRefresh && " Review actions remain locked until Refresh reconciles the durable job."}
        </Callout>
      )}
      {hostStatus && <Callout intent="primary" role="status">{hostStatus}</Callout>}
      {snapshot.status.lifecycle === "executing" ? (
        <Card className="fw-chatgpt-terminal-state">
          <Spinner size={28} />
          <h2>Creating the separate copy</h2>
          <p>The exact accepted preview is executing in the paired local app.</p>
        </Card>
      ) : snapshot.status.lifecycle === "verified" ? (
        <VerifiedResult
          changeFileEvidence={changeFileEvidence}
          notice={verificationNotice}
          onGetChangeFile={() => void getChangeFile()}
          onRecreateOriginal={() => void recreateOriginal()}
          onVerify={() => void verifyResult()}
          reconstructionEvidence={reconstructionEvidence}
          refreshing={refreshing}
          snapshot={snapshot}
          terminalAction={terminalAction}
        />
      ) : (
        <ReviewIsland
          acceptanceScopeFingerprint={
            snapshot.status.authorization_context_fingerprint
          }
          acceptPlan={acceptPlan}
          actionsDisabled={pendingAction !== null || requiresRefresh}
          journey={snapshot.journey}
          keepPrevious={keepPrevious}
          preview={snapshot.preview}
          revisePlan={revisePlan}
          status={snapshot.status}
        />
      )}
    </WidgetShell>
  );
}

function VerifiedResult({
  snapshot,
  refreshing,
  notice,
  changeFileEvidence,
  reconstructionEvidence,
  onVerify,
  onGetChangeFile,
  onRecreateOriginal,
  terminalAction,
}: {
  snapshot: FoldweaveChatGptReviewV1;
  refreshing: boolean;
  notice: string | null;
  changeFileEvidence: FoldweaveChangeFileResultV1 | null;
  reconstructionEvidence: FoldweaveReconstructionResultV1 | null;
  onVerify: () => void;
  onGetChangeFile: () => void;
  onRecreateOriginal: () => void;
  terminalAction: TerminalAction;
}): ReactElement {
  const result = snapshot.result!;
  return (
    <Card className="fw-chatgpt-terminal-state is-verified">
      <Tag intent="success" large>Verified</Tag>
      <h2>Your new folder is ready</h2>
      <p>
        {result.complete_file_count} files accounted for; {result.changed_path_count} paths
        changed. The selected source remained unchanged.
      </p>
      {notice && <Callout intent="success" role="status">{notice}</Callout>}
      {changeFileEvidence && (
        <Callout intent="primary" role="status" title="Foldweave Change File ready">
          <p>
            Opaque local item <code>{changeFileEvidence.item.handle}</code> identifies{" "}
            <strong>{changeFileEvidence.item.display_name}</strong>.
          </p>
          <p>
            Change File <code>{changeFileEvidence.change_file_fingerprint}</code>; receipt{" "}
            <code>{changeFileEvidence.originating_receipt_fingerprint}</code>.
          </p>
        </Callout>
      )}
      {reconstructionEvidence && (
        <Callout intent="success" role="status" title="Original layout recreated and verified">
          <p>
            Opaque local item <code>{reconstructionEvidence.item.handle}</code> identifies{" "}
            <strong>{reconstructionEvidence.item.display_name}</strong>.
          </p>
          <p>
            {reconstructionEvidence.restored_file_count} files and{" "}
            {reconstructionEvidence.restored_empty_directory_count} empty directories restored;
            receipt <code>{reconstructionEvidence.receipt_fingerprint}</code>.
          </p>
        </Callout>
      )}
      <div className="fw-chatgpt-terminal-actions">
        <Button
          disabled={refreshing}
          loading={terminalAction === "verify"}
          onClick={onVerify}
        >
          Verify again
        </Button>
        <Button
          disabled={refreshing || result.change_file_fingerprint === null}
          loading={terminalAction === "change_file"}
          onClick={onGetChangeFile}
        >
          Get Change File
        </Button>
        <Button
          disabled={refreshing}
          loading={terminalAction === "reconstruct"}
          onClick={onRecreateOriginal}
        >
          Recreate original
        </Button>
      </div>
    </Card>
  );
}

function WidgetShell({ children }: { children: React.ReactNode }): ReactElement {
  return <main className="fw-chatgpt-widget bp6-dark">{children}</main>;
}

function bindHostedJobToolArguments(
  jobId: string,
  argumentsValue: Record<string, unknown>,
): Record<string, unknown> {
  if ("job_id" in argumentsValue) {
    throw new Error("Foldweave blocked a caller-supplied hosted job identity.");
  }
  return { job_id: jobId, ...argumentsValue };
}

function isCurrentRevisionParent(
  current: FoldweaveChatGptReviewV1,
  revisionContext: PendingRevisionContext | null,
): revisionContext is PendingRevisionContext {
  return (
    revisionContext !== null &&
    current.status.job_id === revisionContext.parentJobId &&
    current.preview.compiled_candidate_fingerprint ===
      revisionContext.parentCandidateFingerprint &&
    current.preview.preview_fingerprint === revisionContext.parentPreviewFingerprint &&
    current.preview.source_commitment === revisionContext.sourceCommitment
  );
}

function isBoundDerivativeStatus(
  current: FoldweaveChatGptReviewV1,
  status: FoldweaveHostedJobStatusV1,
  revisionContext: PendingRevisionContext | null,
): boolean {
  return (
    isCurrentRevisionParent(current, revisionContext) &&
    current.journey === "apply" &&
    status.job_id !== revisionContext.parentJobId &&
    status.lifecycle === "revising" &&
    status.planning_basis === "derivative" &&
    status.model_transport === "chatgpt_hosted" &&
    status.execution_origin === "none" &&
    status.source_commitment === revisionContext.sourceCommitment &&
    status.has_preview === false &&
    status.candidate_fingerprint === null &&
    status.preview_fingerprint === null
  );
}

function isBoundDerivativeReview(
  current: FoldweaveChatGptReviewV1,
  next: FoldweaveChatGptReviewV1,
  revisionContext: PendingRevisionContext | null,
): boolean {
  return (
    isCurrentRevisionParent(current, revisionContext) &&
    current.journey === "apply" &&
    next.journey === "apply" &&
    next.status.job_id !== revisionContext.parentJobId &&
    next.status.planning_basis === "derivative" &&
    next.status.model_transport === "chatgpt_hosted" &&
    next.status.execution_origin === "none" &&
    next.preview.proposal_basis === "gpt_derivative" &&
    next.preview.immediate_parent_candidate_fingerprint ===
      revisionContext.parentCandidateFingerprint &&
    next.preview.source_commitment === revisionContext.sourceCommitment &&
    next.preview.imported_change_file_fingerprint ===
      current.preview.imported_change_file_fingerprint
  );
}

function exactPreviewBinding(
  snapshot: FoldweaveChatGptReviewV1,
): Record<string, unknown> {
  return {
    proposal_revision: snapshot.preview.proposal_revision,
    source_commitment: snapshot.preview.source_commitment,
    imported_change_file_fingerprint:
      snapshot.preview.imported_change_file_fingerprint,
    match_report_fingerprint: snapshot.preview.match_report_fingerprint,
    authorization_context_fingerprint:
      snapshot.status.authorization_context_fingerprint,
  };
}

function createRevisionPrompt(
  snapshot: FoldweaveChatGptReviewV1,
  payload: RevisionPayload,
): string {
  return [
    `Revise Foldweave planning job ${snapshot.status.job_id}.`,
    `Use the Foldweave host-planning tools and bind the replacement to job revision ${payload.expected_revision}, candidate ${payload.candidate_fingerprint}, and preview ${payload.preview_fingerprint}.`,
    `Reuse this exact idempotency key: ${payload.idempotency_key}.`,
    "Submit one complete mechanically checked replacement preview; do not execute it and do not call the Foldweave direct Responses API.",
    'For this path-only revision, set every sparse entry evidence_ids exactly to ["initial_inventory"]. Do not call evidence tools after revise_plan; they are unavailable while the exact revision is reserved.',
    `The user's requested change is: ${JSON.stringify(payload.instruction)}.`,
  ].join("\n");
}

function interruptionMessage(
  interruption: HostInterruption,
  hasSnapshot: boolean,
): string {
  if (interruption === "resource_teardown") {
    return "The ChatGPT host closed this Foldweave review surface.";
  }
  return hasSnapshot
    ? "The ChatGPT host cancelled the active Foldweave operation."
    : "The ChatGPT host cancelled the Foldweave review before a complete preview arrived.";
}

function publicError(caught: unknown): string {
  const fallback = "Foldweave could not complete the ChatGPT-hosted action.";
  if (!(caught instanceof Error) || caught.message.length === 0) {
    return fallback;
  }
  try {
    assertNoSensitiveBoundaryData(caught.message);
  } catch {
    return fallback;
  }
  return caught.message.startsWith("Foldweave") ||
    caught.message.startsWith("The Foldweave") ||
    caught.message.startsWith("The ChatGPT")
    ? caught.message
    : fallback;
}

const mount = document.getElementById("foldweave-chatgpt-widget-root");
if (mount) {
  createRoot(mount).render(
    <StrictMode>
      <FoldweaveChatGptWidget bridge={new McpAppsHostBridge()} />
    </StrictMode>,
  );
}

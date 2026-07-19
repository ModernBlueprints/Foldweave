import "@blueprintjs/core/lib/css/blueprint.css";
import "./review.css";

import { NonIdealState } from "@blueprintjs/core";
import { StrictMode, type ReactElement, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import {
  type AcceptancePayload,
  type FolderPlanPreviewV1,
  type Journey,
  type ReviewStatus,
  assertPreview,
  assertStatus,
} from "./contracts";
import { ReviewIsland, ReviewLoading } from "./review-island";

interface Bootstrap {
  jobId: string;
  csrfToken: string;
  journey: Journey;
}

function ReviewEntry({ bootstrap }: { bootstrap: Bootstrap }): ReactElement {
  const [preview, setPreview] = useState<FolderPlanPreviewV1 | null>(null);
  const [status, setStatus] = useState<ReviewStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    void Promise.all([
      fetchJson(`/api/jobs/${encodeURIComponent(bootstrap.jobId)}/preview`, controller.signal),
      fetchJson(`/api/jobs/${encodeURIComponent(bootstrap.jobId)}/status`, controller.signal),
    ])
      .then(([previewValue, statusValue]) => {
        assertPreview(previewValue, bootstrap.jobId);
        assertStatus(statusValue, bootstrap.jobId);
        if (
          previewValue.expected_job_revision !== statusValue.job_revision ||
          previewValue.compiled_candidate_fingerprint !== statusValue.candidate_fingerprint ||
          previewValue.preview_fingerprint !== statusValue.preview_fingerprint
        ) {
          throw new Error("The visible preview no longer matches the durable job.");
        }
        setPreview(previewValue);
        setStatus(statusValue);
      })
      .catch((caught: unknown) => {
        if (!controller.signal.aborted) {
          setError(caught instanceof Error ? caught.message : "The preview could not be loaded.");
        }
      });
    return () => controller.abort();
  }, [bootstrap.jobId]);

  if (error) {
    return <NonIdealState icon="error" title="Review unavailable" description={error} />;
  }
  if (!preview || !status) {
    return <ReviewLoading />;
  }

  const acceptPlan = async (payload: AcceptancePayload): Promise<void> => {
    const response = await fetch(`/api/jobs/${encodeURIComponent(bootstrap.jobId)}/accept`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "content-type": "application/json",
        "x-foldweave-csrf": bootstrap.csrfToken,
      },
      body: JSON.stringify(payload),
    });
    const value: unknown = await response.json();
    if (!response.ok) {
      throw new Error(extractError(value));
    }
    if (!isRecord(value) || value.lifecycle !== "verified" || typeof value.done_url !== "string") {
      throw new Error("Foldweave did not return a verified result destination.");
    }
    window.location.assign(value.done_url);
  };

  return (
    <ReviewIsland
      acceptPlan={acceptPlan}
      journey={bootstrap.journey}
      preview={preview}
      status={status}
    />
  );
}

async function fetchJson(url: string, signal: AbortSignal): Promise<unknown> {
  const response = await fetch(url, {
    credentials: "same-origin",
    headers: { accept: "application/json" },
    signal,
  });
  const value: unknown = await response.json();
  if (!response.ok) {
    throw new Error(extractError(value));
  }
  return value;
}

function extractError(value: unknown): string {
  if (isRecord(value) && typeof value.detail === "string" && value.detail.length > 0) {
    return value.detail;
  }
  return "Foldweave could not complete this request.";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function readBootstrap(element: HTMLElement): Bootstrap {
  const { jobId, csrfToken, journey } = element.dataset;
  if (!jobId || !/^[a-f0-9]{32}$/.test(jobId)) {
    throw new Error("The review mount is missing its job identity.");
  }
  if (!csrfToken || csrfToken.length < 16) {
    throw new Error("The review mount is missing its local authorization token.");
  }
  if (journey !== "organize" && journey !== "apply") {
    throw new Error("The review mount has an unsupported journey.");
  }
  return { jobId, csrfToken, journey };
}

const mount = document.getElementById("foldweave-review-root");
if (mount) {
  try {
    const bootstrap = readBootstrap(mount);
    createRoot(mount).render(
      <StrictMode>
        <ReviewEntry bootstrap={bootstrap} />
      </StrictMode>,
    );
  } catch (error) {
    mount.textContent = error instanceof Error ? error.message : "Foldweave review could not start.";
  }
}

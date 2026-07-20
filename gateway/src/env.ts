import type { OAuthHelpers } from "@cloudflare/workers-oauth-provider";

export interface Env {
  DEVICE_SESSIONS: DurableObjectNamespace;
  OAUTH_KV: KVNamespace;
  OAUTH_PROVIDER: OAuthHelpers;
  PAIRING_DIRECTORY: DurableObjectNamespace;
}

export interface OAuthProps {
  authorizedAt: number;
  deviceId: string;
  schemaVersion: "foldweave-oauth-props.v1";
  scopes: string[];
  sessionId: string;
}

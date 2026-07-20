import { OAuthProvider } from "@cloudflare/workers-oauth-provider";

import {
  ACCESS_TOKEN_TTL_SECONDS,
  CLIENT_REGISTRATION_TTL_SECONDS,
  REFRESH_TOKEN_TTL_SECONDS,
  SUPPORTED_SCOPES,
} from "./constants";
import { DeviceSession } from "./device-session";
import type { Env } from "./env";
import {
  defaultHandler,
  McpApiHandler,
  validateClientRegistration,
} from "./gateway";
import { PairingDirectory } from "./pairing-directory";

export { DeviceSession, PairingDirectory };

export default new OAuthProvider<Env>({
  accessTokenTTL: ACCESS_TOKEN_TTL_SECONDS,
  allowImplicitFlow: false,
  allowPlainPKCE: false,
  allowTokenExchangeGrant: false,
  apiHandler: McpApiHandler,
  apiRoute: "/mcp",
  authorizeEndpoint: "/authorize",
  clientIdMetadataDocumentEnabled: true,
  clientRegistrationCallback: validateClientRegistration,
  clientRegistrationEndpoint: "/oauth/register",
  clientRegistrationTTL: CLIENT_REGISTRATION_TTL_SECONDS,
  defaultHandler,
  disallowPublicClientRegistration: false,
  refreshTokenTTL: REFRESH_TOKEN_TTL_SECONDS,
  resourceMetadata: {
    bearer_methods_supported: ["header"],
    resource_name: "Foldweave",
    scopes_supported: [...SUPPORTED_SCOPES],
  },
  scopesSupported: [...SUPPORTED_SCOPES],
  tokenEndpoint: "/oauth/token",
});

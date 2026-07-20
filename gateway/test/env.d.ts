import type { Env as GatewayEnv } from "../src/env";

declare global {
  namespace Cloudflare {
    interface Env extends GatewayEnv {}
  }
}

export {};

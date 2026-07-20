import { readFileSync } from "node:fs";

import { cloudflarePool } from "@cloudflare/vitest-pool-workers";
import { defineConfig } from "vitest/config";

const widgetAssetRoot = new URL(
  "../src/name_atlas/assets/chatgpt-widget/",
  import.meta.url,
);

export default defineConfig({
  define: {
    __FOLDWEAVE_WIDGET_CSS__: JSON.stringify(
      readFileSync(new URL("foldweave-chatgpt-widget.css", widgetAssetRoot), "utf-8"),
    ),
    __FOLDWEAVE_WIDGET_JAVASCRIPT__: JSON.stringify(
      readFileSync(new URL("foldweave-chatgpt-widget.js", widgetAssetRoot), "utf-8"),
    ),
  },
  test: {
    pool: cloudflarePool({
      wrangler: {
        configPath: "./wrangler.jsonc",
      },
    }),
  },
});

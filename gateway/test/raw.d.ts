declare const __FOLDWEAVE_WIDGET_CSS__: string;
declare const __FOLDWEAVE_WIDGET_JAVASCRIPT__: string;

declare module "node:fs" {
  export function readFileSync(path: URL, encoding: "utf-8"): string;
}

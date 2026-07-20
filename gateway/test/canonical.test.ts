import { describe, expect, it } from "vitest";

import {
  base64UrlToBytes,
  bytesToBase64Url,
  canonicalJson,
  canonicalSha256,
  constantTimeEqual,
} from "../src/canonical";
import { generatePairingCode } from "../src/pairing-code";
import { normalizePairingCode } from "../src/contracts";

describe("canonical JSON and transport helpers", () => {
  it("sorts keys recursively and preserves explicit null", () => {
    expect(
      canonicalJson({ z: 1, a: { y: null, b: [3, "ø", false] } }),
    ).toBe('{"a":{"b":[3,"ø",false],"y":null},"z":1}');
  });

  it("rejects non-finite values", () => {
    expect(() => canonicalJson(Number.NaN)).toThrow(/non-finite/u);
    expect(() => canonicalJson(Number.POSITIVE_INFINITY)).toThrow(/non-finite/u);
  });

  it("computes a stable canonical SHA-256", async () => {
    await expect(canonicalSha256({ b: 2, a: 1 })).resolves.toBe(
      "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
    );
  });

  it("round-trips unpadded base64url", () => {
    const bytes = Uint8Array.from([0, 1, 2, 253, 254, 255]);
    const encoded = bytesToBase64Url(bytes);
    expect(encoded).toBe("AAEC_f7_");
    expect(base64UrlToBytes(encoded)).toEqual(bytes);
  });

  it("compares strings without an early-exit branch", () => {
    expect(constantTimeEqual("same", "same")).toBe(true);
    expect(constantTimeEqual("same", "sand")).toBe(false);
    expect(constantTimeEqual("same", "same-longer")).toBe(false);
  });
});
describe("pairing code", () => {
  it("maps ten random bytes onto the exact Crockford alphabet", () => {
    expect(generatePairingCode(Uint8Array.from([0, 1, 2, 3, 4, 5, 6, 7, 30, 31]))).toBe(
      "01234567YZ",
    );
  });

  it("normalizes lowercase separators but rejects ambiguous characters", () => {
    expect(normalizePairingCode("01234-567yz")).toBe("01234567YZ");
    expect(() => normalizePairingCode("01234I67YZ")).toThrow(/invalid/u);
  });
});

import {
  PAIRING_CODE_MAX_FAILURES,
  PAIRING_IP_MAX_ATTEMPTS,
  PAIRING_IP_WINDOW_MS,
} from "./constants";
import {
  isPlainRecord,
  requireExactKeys,
  requireSessionId,
  requireSha256,
  type PairingDirectoryRecord,
} from "./contracts";
import type { Env } from "./env";
import { errorResponse, HttpError, jsonResponse, readJsonBody } from "./http";

interface RateRecord {
  attempts: number[];
  expiresAt: number;
}

interface MissingCodeFailures {
  count: number;
  expiresAt: number;
}

function requireTimestamp(value: unknown, label: string): number {
  if (!Number.isSafeInteger(value) || Number(value) <= 0) {
    throw new HttpError(400, `${label}_invalid`, `${label} is invalid.`);
  }
  return Number(value);
}

function pairKey(codeHash: string): string {
  return `pair:${codeHash}`;
}

function missingCodeKey(codeHash: string): string {
  return `missing:${codeHash}`;
}

function rateKey(ipHash: string): string {
  return `rate:${ipHash}`;
}

export class PairingDirectory implements DurableObject {
  private readonly state: DurableObjectState;

  public constructor(state: DurableObjectState, _env: Env) {
    this.state = state;
  }

  public async fetch(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      if (request.method === "POST" && url.pathname === "/register") {
        return await this.register(request);
      }
      if (request.method === "POST" && url.pathname === "/approve") {
        return await this.approve(request);
      }
      if (request.method === "POST" && url.pathname === "/authorize") {
        return await this.authorize(request);
      }
      if (request.method === "POST" && url.pathname === "/revoke") {
        return await this.revoke(request);
      }
      return jsonResponse({ error: "not_found" }, { status: 404 });
    } catch (error) {
      return errorResponse(error);
    }
  }

  public async alarm(): Promise<void> {
    const now = Date.now();
    const pairs = await this.state.storage.list<PairingDirectoryRecord>({
      prefix: "pair:",
    });
    const missing = await this.state.storage.list<MissingCodeFailures>({
      prefix: "missing:",
    });
    const rates = await this.state.storage.list<RateRecord>({ prefix: "rate:" });
    const expiredKeys = [
      ...[...pairs.entries()]
        .filter(([, record]) =>
          record.expiresAt <= now || record.consumedAt !== null || record.revokedAt !== null,
        )
        .map(([key]) => key),
      ...[...missing.entries()]
        .filter(([, record]) => record.expiresAt <= now)
        .map(([key]) => key),
      ...[...rates.entries()]
        .filter(([, record]) => record.expiresAt <= now)
        .map(([key]) => key),
    ];
    if (expiredKeys.length > 0) {
      await this.state.storage.delete(expiredKeys);
    }
    const remainingExpiries = [
      ...[...pairs.values()]
        .filter((record) => record.expiresAt > now && record.consumedAt === null && record.revokedAt === null)
        .map((record) => record.expiresAt),
      ...[...missing.values()]
        .filter((record) => record.expiresAt > now)
        .map((record) => record.expiresAt),
      ...[...rates.values()]
        .filter((record) => record.expiresAt > now)
        .map((record) => record.expiresAt),
    ];
    if (remainingExpiries.length > 0) {
      await this.state.storage.setAlarm(Math.min(...remainingExpiries));
    }
  }

  private async register(request: Request): Promise<Response> {
    const body = await readJsonBody(request);
    if (!isPlainRecord(body)) {
      throw new HttpError(400, "directory_registration_invalid", "Directory registration is invalid.");
    }
    requireExactKeys(body, ["codeHash", "expiresAt", "sessionId"], "directory_registration");
    const codeHash = requireSha256(body.codeHash, "code_hash");
    const sessionId = requireSessionId(body.sessionId);
    const expiresAt = requireTimestamp(body.expiresAt, "expires_at");
    const now = Date.now();
    if (expiresAt <= now) {
      throw new HttpError(400, "pairing_code_expired", "Pairing code is already expired.");
    }
    const record: PairingDirectoryRecord = {
      codeHash,
      consumedAt: null,
      expiresAt,
      failedAttempts: 0,
      localApprovedAt: null,
      revokedAt: null,
      sessionId,
    };
    const created = await this.state.storage.transaction(async (transaction) => {
      const existing = await transaction.get<PairingDirectoryRecord>(pairKey(codeHash));
      if (existing !== undefined) {
        return false;
      }
      await transaction.put(pairKey(codeHash), record);
      return true;
    });
    if (!created) {
      throw new HttpError(409, "pairing_code_collision", "Pairing code collision; register again.");
    }
    await this.scheduleCleanup(expiresAt);
    return jsonResponse({ registered: true });
  }

  private async approve(request: Request): Promise<Response> {
    const body = await readJsonBody(request);
    if (!isPlainRecord(body)) {
      throw new HttpError(400, "pairing_approval_invalid", "Pairing approval is invalid.");
    }
    requireExactKeys(body, ["approvedAt", "codeHash", "sessionId"], "pairing_approval");
    const codeHash = requireSha256(body.codeHash, "code_hash");
    const sessionId = requireSessionId(body.sessionId);
    const approvedAt = requireTimestamp(body.approvedAt, "approved_at");
    const approved = await this.state.storage.transaction(async (transaction) => {
      const record = await transaction.get<PairingDirectoryRecord>(pairKey(codeHash));
      if (
        record === undefined ||
        record.sessionId !== sessionId ||
        record.expiresAt <= approvedAt ||
        record.revokedAt !== null ||
        record.consumedAt !== null
      ) {
        return false;
      }
      record.localApprovedAt = approvedAt;
      await transaction.put(pairKey(codeHash), record);
      return true;
    });
    if (!approved) {
      throw new HttpError(409, "pairing_approval_rejected", "Pairing approval is no longer valid.");
    }
    return jsonResponse({ approved: true });
  }

  private async authorize(request: Request): Promise<Response> {
    const body = await readJsonBody(request);
    if (!isPlainRecord(body)) {
      throw new HttpError(400, "pairing_attempt_invalid", "Pairing attempt is invalid.");
    }
    requireExactKeys(body, ["attemptedAt", "codeHash", "ipHash"], "pairing_attempt");
    const codeHash = requireSha256(body.codeHash, "code_hash");
    const ipHash = requireSha256(body.ipHash, "ip_hash");
    const attemptedAt = requireTimestamp(body.attemptedAt, "attempted_at");

    const outcome = await this.state.storage.transaction(async (transaction) => {
      const ipKey = rateKey(ipHash);
      const rate = (await transaction.get<RateRecord>(ipKey)) ?? {
        attempts: [],
        expiresAt: attemptedAt + PAIRING_IP_WINDOW_MS,
      };
      rate.attempts = rate.attempts.filter(
        (timestamp) => attemptedAt - timestamp < PAIRING_IP_WINDOW_MS,
      );
      if (rate.attempts.length >= PAIRING_IP_MAX_ATTEMPTS) {
        return { kind: "rate_limited" as const };
      }
      rate.attempts.push(attemptedAt);
      rate.expiresAt = attemptedAt + PAIRING_IP_WINDOW_MS;
      await transaction.put(ipKey, rate);

      const key = pairKey(codeHash);
      const record = await transaction.get<PairingDirectoryRecord>(key);
      if (record === undefined) {
        const missingKey = missingCodeKey(codeHash);
        const existingFailures = await transaction.get<MissingCodeFailures>(missingKey);
        const failures =
          existingFailures === undefined || existingFailures.expiresAt <= attemptedAt
            ? {
            count: 0,
            expiresAt: attemptedAt + PAIRING_IP_WINDOW_MS,
              }
            : existingFailures;
        if (failures.count >= PAIRING_CODE_MAX_FAILURES) {
          return { kind: "code_locked" as const };
        }
        failures.count += 1;
        await transaction.put(missingKey, failures);
        return {
          kind:
            failures.count >= PAIRING_CODE_MAX_FAILURES
              ? ("code_locked" as const)
              : ("invalid" as const),
        };
      }

      if (record.failedAttempts >= PAIRING_CODE_MAX_FAILURES) {
        return { kind: "code_locked" as const };
      }
      if (
        record.expiresAt <= attemptedAt ||
        record.revokedAt !== null ||
        record.consumedAt !== null ||
        record.localApprovedAt === null
      ) {
        record.failedAttempts += 1;
        await transaction.put(key, record);
        return {
          kind:
            record.failedAttempts >= PAIRING_CODE_MAX_FAILURES
              ? ("code_locked" as const)
              : ("invalid" as const),
        };
      }

      await transaction.delete(key);
      return { kind: "authorized" as const, sessionId: record.sessionId };
    });

    await this.scheduleCleanup(attemptedAt + PAIRING_IP_WINDOW_MS);

    if (outcome.kind === "rate_limited") {
      throw new HttpError(429, "pairing_rate_limited", "Too many pairing attempts.");
    }
    if (outcome.kind === "code_locked") {
      throw new HttpError(429, "pairing_code_locked", "Pairing code is locked.");
    }
    if (outcome.kind === "invalid") {
      throw new HttpError(400, "pairing_code_invalid", "Pairing code is invalid or unavailable.");
    }
    return jsonResponse({
      authorized: true,
      sessionId: requireSessionId(outcome.sessionId),
    });
  }

  private async revoke(request: Request): Promise<Response> {
    const body = await readJsonBody(request);
    if (!isPlainRecord(body)) {
      throw new HttpError(400, "pairing_revocation_invalid", "Pairing revocation is invalid.");
    }
    requireExactKeys(body, ["codeHash", "revokedAt", "sessionId"], "pairing_revocation");
    const codeHash = requireSha256(body.codeHash, "code_hash");
    const sessionId = requireSessionId(body.sessionId);
    const revokedAt = requireTimestamp(body.revokedAt, "revoked_at");
    await this.state.storage.transaction(async (transaction) => {
      const key = pairKey(codeHash);
      const record = await transaction.get<PairingDirectoryRecord>(key);
      if (record !== undefined && record.sessionId === sessionId) {
        await transaction.delete(key);
      }
    });
    return jsonResponse({ revoked: true });
  }

  private async scheduleCleanup(at: number): Promise<void> {
    const existing = await this.state.storage.getAlarm();
    if (existing === null || at < existing) {
      await this.state.storage.setAlarm(at);
    }
  }
}

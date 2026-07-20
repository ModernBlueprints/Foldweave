import { PAIRING_CODE_LENGTH } from "./constants";

export const CROCKFORD_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";

export function generatePairingCode(randomBytes?: Uint8Array): string {
  const bytes = randomBytes ?? crypto.getRandomValues(new Uint8Array(PAIRING_CODE_LENGTH));
  if (bytes.byteLength < PAIRING_CODE_LENGTH) {
    throw new TypeError(`At least ${PAIRING_CODE_LENGTH} random bytes are required.`);
  }
  let code = "";
  for (let index = 0; index < PAIRING_CODE_LENGTH; index += 1) {
    code += CROCKFORD_ALPHABET[bytes[index]! & 31];
  }
  return code;
}

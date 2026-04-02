// /index.js

import {
  v1 as uuidv1,
  v3 as uuidv3,
  v4 as uuidv4,
  v5 as uuidv5,
  v6 as uuidv6,
  v7 as uuidv7
} from "uuid";

/**
 * Generate UUID values
 * @param {Object} options
 * @param {number} options.count - number of UUIDs (min 1, max 10)
 * @param {string} options.version - "v1","v3","v4","v5","v6","v7"
 * @param {string} [options.name] - required for v3/v5
 * @param {string} [options.namespace] - required for v3/v5
 * @returns {Object}
 */
export function generateUUID({
  count = 1,
  version = "v7",
  name,
  namespace
} = {}) {
  // ===============================
  // VALIDATE COUNT
  // ===============================
  let safeCount = Number(count);
  if (isNaN(safeCount) || safeCount < 1) safeCount = 1;
  if (safeCount > 10) safeCount = 10;

  // ===============================
  // NORMALIZE VERSION
  // ===============================
  const normalizedVersion = String(version || "v7").toLowerCase();

  const allowedVersions = ["v1", "v3", "v4", "v5", "v6", "v7"];
  const finalVersion = allowedVersions.includes(normalizedVersion)
    ? normalizedVersion
    : "v7";

  // ===============================
  // GENERATOR MAP
  // ===============================
  const generators = {
    v1: () => uuidv1(),

    v3: () => {
      if (!name || !namespace) {
        throw new Error("v3 requires 'name' and 'namespace'");
      }
      return uuidv3(name, namespace);
    },

    v4: () => uuidv4(),

    v5: () => {
      if (!name || !namespace) {
        throw new Error("v5 requires 'name' and 'namespace'");
      }
      return uuidv5(name, namespace);
    },

    v6: () => uuidv6(),

    v7: () => uuidv7()
  };

  const generator = generators[finalVersion];

  // ===============================
  // GENERATE UUIDS
  // ===============================
  const list = [];

  for (let i = 0; i < safeCount; i++) {
    list.push(generator());
  }

  return {
    count: safeCount,
    version: finalVersion,
    position: {
      first: list[0] || null,
      last: list[list.length - 1] || null
    },
    list
  };
}
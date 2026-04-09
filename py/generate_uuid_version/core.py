# py/generate_uuid_version/core.py

import importlib
import uuid

_uuid7_fn = None

try:
    uuid6_module = importlib.import_module("uuid6")
    _uuid7_fn = uuid6_module.uuid7
    HAS_UUID7 = True
except Exception:
    HAS_UUID7 = False


def generate_uuid(count=1, version="v7"):
    """
    Generate UUID values

    :param count: number of UUIDs (min 1, max 10)
    :param version: "v4" or "v7"
    :return: dict
    """

    # ===============================
    # VALIDATE COUNT
    # ===============================
    try:
        safe_count = int(count)
    except Exception:
        safe_count = 1

    if safe_count < 1:
        safe_count = 1
    if safe_count > 10:
        safe_count = 10

    # ===============================
    # NORMALIZE VERSION
    # ===============================
    normalized_version = str(version or "v7").lower()
    final_version = "v4" if normalized_version == "v4" else "v7"

    # ===============================
    # GENERATORS
    # ===============================
    def generate_v4():
        return str(uuid.uuid4())

    def generate_v7():
        if HAS_UUID7 and _uuid7_fn:
            return str(_uuid7_fn())
        # fallback if uuid7 not available
        return str(uuid.uuid4())

    generators = {
        "v4": generate_v4,
        "v7": generate_v7
    }

    generator = generators[final_version]

    # ===============================
    # GENERATE
    # ===============================
    items = [generator() for _ in range(safe_count)]

    return {
        "version": final_version,
        "count": safe_count,
        "items": items
    }
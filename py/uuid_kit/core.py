# py/uuid_kit/core.py

import importlib
import uuid
from datetime import datetime, timezone

_uuid7_fn = None

try:
    uuid6_module = importlib.import_module("uuid6")
    _uuid7_fn = uuid6_module.uuid7
    HAS_UUID7 = True
except Exception:
    HAS_UUID7 = False


ALLOWED_FORMATS = (
    "standard",
    "compact",
    "uppercase",
    "uppercase-compact"
)

ALLOWED_VERSIONS = (
    "v4",
    "v7"
)

ALLOWED_OUTPUT_AS = (
    "array",
    "object",
    "string"
)


def _generate_v4():
    return str(uuid.uuid4())


def _generate_v7():
    if HAS_UUID7 and _uuid7_fn:
        return str(_uuid7_fn())
    return str(uuid.uuid4())


def extract_timestamp_v7(uuid_value):
    hex_value = uuid_value.replace("-", "")[:12]
    ms = int(hex_value, 16)
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)

    return {
        "iso": dt.isoformat().replace("+00:00", "Z"),
        "unix": ms
    }


VERSION_CONFIG = {
    "v4": {
        "generator": _generate_v4,
        "hasTimestamp": False,
        "extractTimestamp": None
    },
    "v7": {
        "generator": _generate_v7,
        "hasTimestamp": True,
        "extractTimestamp": extract_timestamp_v7
    }
}


def generate_uuid(
    count=1,
    version="v7",
    format="standard",
    prefix="",
    suffix="",
    outputAs="array"
):
    """
    Generate UUID values.

    :param count: number of UUIDs (min 1, max 100)
    :param version: "v4" or "v7"
    :param format: "standard", "compact", "uppercase", or "uppercase-compact"
    :param prefix: string to prepend to each UUID
    :param suffix: string to append to each UUID
    :param outputAs: "array", "object", or "string"
    :return: dict
    """

    # ===============================
    # VALIDATE COUNT
    # ===============================
    try:
        safe_count = float(count)
    except Exception:
        safe_count = 1

    if safe_count != safe_count or safe_count < 0:
        safe_count = 1
    if safe_count > 100:
        safe_count = 100

    safe_count = int(safe_count)

    # ===============================
    # VALIDATE VERSION
    # ===============================
    normalized_version = str(version or "v7").lower()
    final_version = normalized_version if normalized_version in ALLOWED_VERSIONS else "v7"

    # ===============================
    # VALIDATE FORMAT
    # ===============================
    normalized_format = str(format or "standard").lower()
    final_format = normalized_format if normalized_format in ALLOWED_FORMATS else "standard"

    # ===============================
    # VALIDATE OUTPUT SHAPE
    # ===============================
    normalized_output_as = str(outputAs or "array").lower()
    final_output_as = normalized_output_as if normalized_output_as in ALLOWED_OUTPUT_AS else "array"

    generator = VERSION_CONFIG[final_version]["generator"]
    has_timestamp = VERSION_CONFIG[final_version]["hasTimestamp"]
    extract_timestamp = VERSION_CONFIG[final_version]["extractTimestamp"]

    # Precompute format and affix behavior for the hot loop.
    use_compact = final_format in ("compact", "uppercase-compact")
    use_upper = final_format in ("uppercase", "uppercase-compact")
    prefix_str = str(prefix) if prefix else ""
    suffix_str = str(suffix) if suffix else ""

    # ===============================
    # GENERATE (optimized)
    # ===============================
    needs_object = final_output_as == "object"

    values = None if needs_object else [None] * safe_count
    objects = [None] * safe_count if needs_object else None

    for i in range(safe_count):
        raw = generator()
        value = raw

        if use_compact:
            value = value.replace("-", "")
        if use_upper:
            value = value.upper()
        if prefix_str or suffix_str:
            value = prefix_str + value + suffix_str

        if needs_object:
            obj = {
                "uuid": value,
                "raw": raw,
                "index": i
            }

            if has_timestamp and extract_timestamp:
                try:
                    obj["timestamp"] = extract_timestamp(raw)
                except Exception:
                    pass

            objects[i] = obj
        else:
            values[i] = value

    # ===============================
    # SHAPE OUTPUT
    # ===============================
    if final_output_as == "object":
        items = objects
    elif final_output_as == "string":
        items = "\n".join(values)
    else:
        items = values

    return {
        "version": final_version,
        "format": final_format,
        "output_as": final_output_as,
        "count": safe_count,
        "items": items
    }
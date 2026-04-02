# generate-uuid-version

Generate UUID values (v4, v7) with simple controls in both JavaScript and Python.

---

## Packages

This repo contains two versions of the same utility:

- JavaScript package for npm in `./js`
- Python package for PyPI in `./py`

---

## JavaScript / npm

### Install

```bash
npm install generate-uuid-version
```

### Usage

```js
import { generateUUID } from "generate-uuid-version";

const result = generateUUID({
  count: 3,
  version: "v7"
});

console.log(result);
```

### Package Location

```text
./js
```

---

## Python / PyPI

### Install

```bash
pip install generate-uuid-version
```

### Usage

```python
from generate_uuid_version import generate_uuid

result = generate_uuid(
    count=3,
    version="v7"
)

print(result)
```

### Package Location

```text
./py
```

---

## Output

```json
{
  "count": 3,
  "version": "v7",
  "items": {
    "first": "uuid-1",
    "last": "uuid-3"
  },
  "list": ["uuid-1", "uuid-2", "uuid-3"]
}
```

---

## Options

| Field | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| count | number / int | No | 1 | Number of UUIDs to generate (min 1, max 10) |
| version | string | No | v7 | UUID version: v4 or v7 |

---

## Supported Versions

- v4 = random
- v7 = modern time-based

---

## Behavior

- Invalid or missing `count` defaults to `1`
- Maximum `count` is `10`
- Invalid or missing `version` defaults to `v7`

---

## Repository Structure

```text
generate-uuid-version/
  README.md
  LICENSE
  .gitignore

  js/
    index.js
    LICENSE
    package.json
    README.md

  py/
    LICENSE
    README.md
    pyproject.toml
    generate_uuid_version/
      __init__.py
      core.py
```

---

## Notes

- `js/README.md` is the npm-focused package README
- `py/README.md` is the PyPI-focused package README
- This root `README.md` is the repo overview

---

## License

MIT
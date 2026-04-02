# generate-uuid-version

Generate UUID values (v1, v3, v4, v5, v6, v7) with simple controls.

---

## Install

```bash
npm install generate-uuid-version
```

---

## Usage

```js
import { generateUUID } from "generate-uuid-version";

const result = generateUUID({
  count: 3,
  version: "v7"
});

console.log(result);
```

---

## Output

```json
{
  "count": 3,
  "version": "v7",
  "position": {
    "first": "uuid-1",
    "last": "uuid-3"
  },
  "list": ["uuid-1", "uuid-2", "uuid-3"]
}
```

---

## Options

| Field | Type | Required | Default | Description |
|------|------|----------|--------|------------|
| count | number | No | 1 | Number of UUIDs to generate (min 1, max 10) |
| version | string | No | v7 | UUID version: v1, v3, v4, v5, v6, v7 |
| name | string | No* | - | Required for v3 and v5 |
| namespace | string | No* | - | Required for v3 and v5 |

\* `name` and `namespace` are required when using `v3` or `v5`

---

## Examples

### v4 (random)
```js
generateUUID({ count: 2, version: "v4" });
```

### v7 (time-based, recommended)
```js
generateUUID({ count: 2, version: "v7" });
```

### v5 (deterministic)
```js
generateUUID({
  count: 1,
  version: "v5",
  name: "example.com",
  namespace: "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
});
```

---

## Supported Versions

- v1 → timestamp-based  
- v3 → deterministic (MD5)  
- v4 → random  
- v5 → deterministic (SHA-1)  
- v6 → reordered timestamp  
- v7 → modern time-based (recommended)  

---

## Zapier Usage

If using in a Zapier Code step, add:

- generate-uuid-version  
- uuid@10  

---

## Behavior

- Invalid or missing `count` defaults to 1  
- Maximum `count` is 10  
- Invalid `version` defaults to v7  
- v3 and v5 require `name` and `namespace`  

---

## License

MIT
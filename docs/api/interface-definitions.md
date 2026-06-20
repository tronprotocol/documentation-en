# Machine-readable API definitions

The repository publishes machine-readable API definitions for tooling, SDK generation, and AI agents:

| API surface | Format | File |
|---|---|---|
| HTTP API | OpenAPI 3.1 | [`openapi.yaml`](openapi.yaml) |
| JSON-RPC API | OpenRPC 1.2.6 | [`openrpc.json`](openrpc.json) |

Per-interface generated fragments are also kept for review:

| API surface | Fragment directory |
|---|---|
| HTTP API | [`specs/http/`](specs/http/) |
| JSON-RPC API | [`specs/json-rpc/`](specs/json-rpc/) |

Regenerate them after java-tron API source changes:

```bash
python3 scripts/generate_api_specs.py
```

The generator needs a local java-tron checkout. It looks for `../java-tron` relative to this
documentation repository, or you can set `JAVA_TRON_SOURCE` explicitly:

```bash
JAVA_TRON_SOURCE=/path/to/java-tron python3 scripts/generate_api_specs.py
```

The generated interface list is source-derived:

- HTTP paths, HTTP methods, servlet classes, Solidity endpoint mappings, and request message hints come from the java-tron source tree.
- JSON-RPC method names, Java parameter names/types, return types, and declared error codes come from `TronJsonRpc.java`.
- Markdown API pages are read only for human-facing summaries, descriptions, and external documentation links.

By default the generator keeps the published definitions aligned with the documented API surface. If a documented HTTP path or JSON-RPC method is no longer present in java-tron source, generation fails instead of silently producing stale definitions.

The top-level `openapi.yaml` and `openrpc.json` files are bundled from the generated per-interface fragments so tools can still consume one standard file.

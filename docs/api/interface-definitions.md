# Machine-readable API definitions

The repository publishes machine-readable API definitions for tooling, SDK generation, and AI agents:

| API surface | Format | File |
|---|---|---|
| HTTP API | OpenAPI 3.1 | [`openapi.yaml`](openapi.yaml) |
| JSON-RPC API | OpenRPC 1.2.6 | [`openrpc.json`](openrpc.json) |

Per-interface fragments are also kept for review:

| API surface | Fragment directory |
|---|---|
| HTTP API | [`specs/http/`](https://github.com/tronprotocol/documentation-en/tree/master/docs/api/specs/http) |
| JSON-RPC API | [`specs/json-rpc/`](https://github.com/tronprotocol/documentation-en/tree/master/docs/api/specs/json-rpc) |

The published definitions are source-derived from java-tron API behavior and include links back to the corresponding human-readable API documentation. The top-level `openapi.yaml` and `openrpc.json` files bundle the per-interface fragments so tools can consume one standard file.

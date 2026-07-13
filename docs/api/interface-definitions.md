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

## HTTP in-band error extension

HTTP endpoints can return success or error objects with status 200. The JSON response schema uses `x-tron-in-band-error` to describe how consumers can distinguish those cases.

When present, the `errors` array is the canonical structure for endpoint-specific business errors. Consumers must fall back to `errorSchema`, `discriminatorField`, and top-level `sources` when the array is absent. A business-error entry contains `responsePath`, `discriminatorPath`, `failureCondition`, and `sources`. A Java error entry identifies the `JavaTronError` schema and uses `$.Error` as its discriminator. An operation is a business failure when any business-error entry matches.

Supported `failureCondition` forms are:

- `equals <value>`: the discriminator field exists and equals the JSON scalar or enum token.
- `missing or equals <value>`: the field is absent, or it exists and equals the value. JSON `null` is not considered missing.
- `field exists and is not <value>`: the field exists and differs from the value. An absent proto3 default field does not match.

Discriminator paths use the JSONPath subset `$`, dot-separated object members, and zero-based array indexes such as `[0]`.

All current `x-tron-in-band-error` entries retain `errorSchema`, `discriminatorField`, and top-level `sources`. Entries for operations with endpoint-specific business errors additionally provide `errors`. These legacy fields describe only the `JavaTronError` branch; endpoint-specific business failures are represented only in `errors`.

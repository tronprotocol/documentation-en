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

## HTTP in-band error and catalog extensions

HTTP endpoints can return success or error objects with status 200. The JSON response schema uses `x-tron-in-band-error` to describe how consumers detect those in-band failures. The top-level OpenAPI `x-tron-error-model` is the single source of truth for stable catalog IDs and retry classifications; these classifications document existing wire behavior and do not add an error-code field to java-tron responses.

Every current `x-tron-in-band-error` object provides an `errors` array. A business-error entry contains `kind: business`, `responsePath`, `discriminatorPath`, `failureCondition`, `catalogIds`, and `sources`. A Java error entry contains `kind: java-tron`, the `JavaTronError` schema, the `$.Error` discriminator path, `catalogIds`, and `sources`. An operation is an in-band failure when any entry matches.

Supported `failureCondition` forms are:

- `equals <value>`: the discriminator field exists and equals the JSON scalar or enum token.
- `missing or equals <value>`: the field is absent, or it exists and equals the value. JSON `null` is not considered missing.
- `field exists and is not <value>`: the field exists and differs from the value. An absent proto3 default field does not match.

Discriminator paths use the JSONPath subset `$`, dot-separated object members, and zero-based array indexes such as `[0]`.

Classify an HTTP response in this order:

1. Select the response status and OpenAPI content branch. HTTP 404 and 413 responses, plus known non-JSON HTTP 200 branches such as the lite FullNode rejection, link directly to candidates through `x-tron-errors.catalogIds`.
2. For an application/json HTTP 200 response, evaluate `x-tron-in-band-error.errors` to detect the matching business or Java error branch.
3. Evaluate the top-level catalog entries referenced by that branch's `catalogIds` in order, using their executable `match` constraints such as schema, path, value, operation ID, or media type.
4. If a response is known to be a failure but no referenced catalog entry matches safely, classify it as `UNKNOWN` and do not retry it automatically.

Each catalog entry has a `retryable` boolean and a more precise `retryClass`. `retryable: true` alone permits automatic replay of the same logical operation. Conditional classes such as `AFTER_STATE_CHANGE`, `AFTER_REQUEST_REBUILD`, and `VERIFY_BEFORE_RETRY` remain `retryable: false` until their precondition is satisfied; `UNKNOWN` also disables automatic retry.

All current `x-tron-in-band-error` objects retain `errorSchema`, `discriminatorField`, and top-level `sources` only as compatibility fields for older consumers. Those legacy fields describe the `JavaTronError` branch only; the `errors` array is canonical for both Java and endpoint-specific business failures.

## OpenRPC error catalog extension

The top-level `x-tron-error-model` and each method's `x-tron-error-catalog` add stable error classifications and retry guidance without changing the JSON-RPC wire format or the source-derived OpenRPC `errors` arrays.

Each method-catalog link contains an `errorIndex`. It is a zero-based index into that method's `errors` array; the linked `catalogId` identifies the corresponding entry in `x-tron-error-model.catalog`. An empty method catalog means the method has no source-declared errors, but method-independent failures from `sharedCatalogIds` still apply.

Classify a response in this order:

1. Evaluate executable matches referenced by `sharedCatalogIds`, including protocol/servlet failures and JSON-RPC transport responses outside the normal envelope.
2. If the invoked method is known, restrict candidates using its `x-tron-error-catalog` links and match observable wire fields such as `code` or a documented message prefix.
3. If multiple candidates remain for the same wire response—especially for reused `-32000` and `-32005` codes—use `ambiguousCodeFallback`: `retryable: false` and `retryClass: UNKNOWN`.

`sourceException` and `sourceMessage` are explanatory metadata derived from java-tron source declarations. They are not guaranteed to appear in `error.message`, `error.data`, or any other wire field and must not be used as runtime match conditions. In particular, `<underlying exception message>` is a source-description placeholder, not a literal response value.

`retryable: true` specifically permits automatic retry of the same logical operation. A conditional class such as `AFTER_STATE_CHANGE`, `AFTER_REQUEST_REBUILD`, or `VERIFY_BEFORE_RETRY` remains `retryable: false`; the client may attempt the operation again only after satisfying the class's stated precondition. `UNKNOWN` also disables automatic retry.

The catalog includes stable protocol, servlet, and HTTP responses emitted by java-tron. Connection failures, timeouts, and generic I/O failures without a stable response contract remain client transport errors.

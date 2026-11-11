# /wallet/listnodes

List the peers discovered by this node.

- Source: `framework/src/main/java/org/tron/core/services/http/ListNodesServlet.java`
- Method: `GET` / `POST`
- Alias path: `/net/listnodes`
- Response: `api.NodeList`

## Request parameters

Both GET and POST read these fields from URL query parameters; the servlet does not parse the POST body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `visible` | GET / POST | bool | No | Text field format (only affects `Address.host`): when `true`, valid UTF-8 bytes are returned as text; all other cases use hex |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/listnodes \
     --header 'accept: application/json'
```
## Response

| Field | Type | Description |
|---|---|---|
| `nodes` | repeated Node | Known nodes |
| `nodes[].address.host` | string | IP address; when `visible=true` and the bytes are valid UTF-8, returned as text (e.g. `"176.9.148.236"`); otherwise, hex of the corresponding bytes (e.g. `"3137362e392e3134382e323336"`) |
| `nodes[].address.port` | int32 | Port |

Response example (default; first 3 entries shown — the actual response contains dozens of nodes):

```json
{
  "nodes": [
    { "address": { "host": "3137362e392e3134382e323336", "port": 18888 } },
    { "address": { "host": "35382e3133362e3130332e3833", "port": 18889 } },
    { "address": { "host": "31352e3233352e3233332e313239", "port": 18888 } }
  ]
}
```

Response example (`visible=true`, UTF-8 output for the same nodes):

```json
{
  "nodes": [
    { "address": { "host": "176.9.148.236", "port": 18888 } },
    { "address": { "host": "58.136.103.83", "port": 18889 } },
    { "address": { "host": "15.235.233.129", "port": 18888 } }
  ]
}
```

> For UTF-8 host strings, append `?visible=true` to the URL on either a GET or POST request. The node's servlet ignores the POST JSON body, so setting `visible` only in that body has no effect, including on a self-hosted node.

Returns `{}` when there are no nodes.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error (failed to fetch node list or serialize) | `{"Error": "<exceptionClass> : <message>"}` |

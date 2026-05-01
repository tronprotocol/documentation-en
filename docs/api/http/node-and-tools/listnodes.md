# /wallet/listnodes

List the peers discovered by this node.

- Source: `framework/src/main/java/org/tron/core/services/http/ListNodesServlet.java`
- Method: `GET` / `POST`
- Alias path: `/net/listnodes`
- Response: `api.NodeList`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `visible` | bool | No | Text field format (only affects `Address.host`: `true` outputs UTF-8 IP string, default/`false` outputs hex bytes) |

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
| `nodes[].address.host` | string | IP address; `visible=true` is UTF-8 text (e.g. `"176.9.148.236"`), otherwise hex of the corresponding bytes (e.g. `"3137362e392e3134382e323336"`) |
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

> The public gateway (`nile.trongrid.io`) does not pass through the `visible` field in POST bodies, so `host` is always hex when going through it. To get UTF-8 form, query a self-hosted node directly.

Returns `{}` when there are no nodes.

### Error responses

| Trigger | Response |
|---|---|
| Internal node error (failed to fetch node list or serialize) | `{"Error": "<exceptionClass> : <message>"}` |

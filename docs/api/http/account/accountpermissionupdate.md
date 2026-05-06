# /wallet/accountpermissionupdate

Update an account's owner / witness / active permissions (multi-sig configuration).

- Source: `framework/src/main/java/org/tron/core/services/http/AccountPermissionUpdateServlet.java`
- Method: `POST`
- Contract: `protocol.AccountPermissionUpdateContract` (`account_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Account address |
| `owner` | Permission | Yes | Owner permission (type=Owner, id=0; cannot be empty) |
| `witness` | Permission | No | Witness permission (type=Witness, id=1); only set on SR accounts |
| `actives` | repeated Permission | Yes | Active permission list (type=Active, id starts from 2) |
| `permission_id` | int32 | No | Permission ID used for the current signature |
| `visible` | bool | No | Address format |

`Permission` fields (`Tron.proto`):

| Field | Type | Description |
|---|---|---|
| `type` | enum | `Owner` / `Witness` / `Active` |
| `id` | int32 | Owner=0, Witness=1, Active>=2 |
| `permission_name` | string | Permission name |
| `threshold` | int64 | Trigger threshold (the sum of `keys[i].weight` must reach this value to take effect) |
| `operations` | bytes | Bitmap of contract types this active permission can execute (hex, 32 bytes) |
| `keys` | repeated Key | Signing keys (`{address, weight}`) |

Example (minimal owner permission + 1 active):

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/accountpermissionupdate \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "owner": {
    "type": 0, "id": 0, "permission_name": "owner",
    "threshold": 1,
    "keys": [{ "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }]
  },
  "actives": [{
    "type": 2, "id": 2, "permission_name": "active",
    "threshold": 1,
    "operations": "7fff1fc0033e0100000000000000000000000000000000000000000000000000",
    "keys": [{ "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }]
  }]
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, and `raw_data_hex` vary by the moment of construction):

```json
{
  "visible": false,
  "txID": "beb8e742fc1f345a9eed45456e54cb3eba4ec286845b57a89bc8638e2e6a8dad",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "owner": {
              "permission_name": "owner",
              "threshold": 1,
              "keys": [
                { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
              ]
            },
            "actives": [
              {
                "type": "Active",
                "id": 2,
                "permission_name": "active",
                "threshold": 1,
                "operations": "7fff1fc0033e0100000000000000000000000000000000000000000000000000",
                "keys": [
                  { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
                ]
              }
            ]
          },
          "type_url": "type.googleapis.com/protocol.AccountPermissionUpdateContract"
        },
        "type": "AccountPermissionUpdateContract"
      }
    ],
    "ref_block_bytes": "270b",
    "ref_block_hash": "d95e28e9c4c8af73",
    "expiration": 1777445901000,
    "timestamp": 1777445841729
  },
  "raw_data_hex": "0a02270b2208d95e28e9c4c8af7340c8a5a0c0dd335ad001082e12cb010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e7472616374128a010a1541dd791d6b49e190062d650e6a23c575510d35f2f912241a056f776e657220013a190a1541dd791d6b49e190062d650e6a23c575510d35f2f91001224b080210021a06616374697665200132207fff1fc0033e01000000000000000000000000000000000000000000000000003a190a1541dd791d6b49e190062d650e6a23c575510d35f2f9100170c1d69cc0dd33"
}
```

> Note: `owner.type` and `owner.id` in the response are protocol enum/default values; they are omitted on serialization, equivalent to `Owner`/`0`.

⚠️ Once this takes effect, the previous owner permission is invalidated; always simulate first.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| `AllowMultiSign` proposal not enabled | `{"Error": "class org.tron.core.exception.ContractValidateException : multi sign is not allowed, need to be opened by the committee"}` |
| `owner_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : invalidate ownerAddress"}` |
| `owner_address` does not exist on chain | `{"Error": "class org.tron.core.exception.ContractValidateException : ownerAddress account does not exist"}` |
| Missing `owner` permission | `{"Error": "class org.tron.core.exception.ContractValidateException : owner permission is missed"}` |
| SR account missing `witness` permission | `{"Error": "class org.tron.core.exception.ContractValidateException : witness permission is missed"}` |
| Non-SR account sets a `witness` permission | `{"Error": "class org.tron.core.exception.ContractValidateException : account isn't witness can't set witness permission"}` |
| Missing `actives` permission | `{"Error": "class org.tron.core.exception.ContractValidateException : active permission is missed"}` |
| `actives` count exceeds 8 | `{"Error": "class org.tron.core.exception.ContractValidateException : active permission is too many"}` |
| `owner.type != Owner` | `{"Error": "class org.tron.core.exception.ContractValidateException : owner permission type is error"}` |
| `witness.type != Witness` | `{"Error": "class org.tron.core.exception.ContractValidateException : witness permission type is error"}` |
| `actives[i].type != Active` | `{"Error": "class org.tron.core.exception.ContractValidateException : active permission type is error"}` |
| `Permission.keys` count exceeds `getTotalSignNum()` (default 5) | `{"Error": "class org.tron.core.exception.ContractValidateException : number of keys in permission should not be greater than <N>"}` |
| `Permission.keys` is empty | `{"Error": "class org.tron.core.exception.ContractValidateException : key's count should be greater than 0"}` |
| `witness` permission's keys count is not 1 | `{"Error": "class org.tron.core.exception.ContractValidateException : Witness permission's key count should be 1"}` |
| `Permission.threshold <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : permission's threshold should be greater than 0"}` |
| `Permission.permission_name` exceeds 32 bytes | `{"Error": "class org.tron.core.exception.ContractValidateException : permission's name is too long"}` |
| `Permission.parent_id != 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : permission's parent should be owner"}` |
| Duplicate addresses in `keys` | `{"Error": "class org.tron.core.exception.ContractValidateException : address should be distinct in permission <Owner\|Witness\|Active>"}` |
| `keys[i].address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : key is not a validate address"}` |
| `keys[i].weight <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : key's weight should be greater than 0"}` |
| `Permission.threshold` exceeds the sum of `keys.weight` | `{"Error": "class org.tron.core.exception.ContractValidateException : sum of all key's weight should not be less than threshold in permission <Owner\|Witness\|Active>"}` |
| owner / witness permission has non-empty `operations` | `{"Error": "class org.tron.core.exception.ContractValidateException : <Owner\|Witness> permission needn't operations"}` |
| `active.operations` length is not 32 bytes | `{"Error": "class org.tron.core.exception.ContractValidateException : operations size must 32"}` |
| `active.operations` contains an unregistered contract type bit | `{"Error": "class org.tron.core.exception.ContractValidateException : <i> isn't a validate ContractType"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |

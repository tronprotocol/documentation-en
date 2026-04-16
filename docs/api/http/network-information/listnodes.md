# listnodes

TRON API method that retrieves a list of all nodes in the TRON network, including Super Representative nodes and full nodes.

## HTTP Request

`POST /wallet/listnodes`

## Supported Paths

- `/wallet/listnodes`

## Parameters

This method does not require any parameters.

## Response

- nodes — array of node information objects containing:
  - address — node address information
    - host — node IP address
    - port — node port number

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/listnodes \
  --header 'Content-Type: application/json' \
  --data '{}'
```

### Response

```json
{
  "nodes": [
    {
      "address": {
        "host": "<string>",
        "port": 123
      }
    }
  ]
}
```

## Use Case

- Discovering available nodes in the TRON network
- Building network topology maps and node distribution analysis
- Finding nodes for direct P2P connections
- Monitoring network health and node availability
- Creating decentralized applications that interact with multiple nodes

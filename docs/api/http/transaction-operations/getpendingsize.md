# getpendingsize

TRON API method that returns the current size of the pending transaction pool (mempool). This provides insight into network congestion and the number of unconfirmed transactions awaiting processing.

## HTTP Request

`GET /wallet/getpendingsize`

## Supported Paths

- `/wallet/getpendingsize`

## Parameters

This method requires no parameters. It returns the current size of the pending transaction pool.

## Response

- pendingSize — number representing the current count of pending transactions in the mempool

## Example

### Request

```shell
curl --request GET \
  --url https://api.shasta.trongrid.io/wallet/getpendingsize
```

## Use Case

- Monitoring network congestion by tracking the number of pending transactions.
- Building network analytics dashboards that display mempool statistics.
- Implementing adaptive fee strategies based on current network load.
- Creating alerts for high network congestion periods.
- Optimizing transaction timing for applications based on mempool size.

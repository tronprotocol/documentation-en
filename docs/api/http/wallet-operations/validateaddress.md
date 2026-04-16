# validateaddress

TRON API method that validates whether a given address is a valid TRON address. This method checks the format and structure of the address to ensure it conforms to TRON’s address specifications.

## HTTP Request

`POST /wallet/validateaddress`

## Supported Paths

- `/wallet/validateaddress`

## Parameters

- address — the TRON address to validate. Can be in base58 or hex format.
- visible — optional boolean parameter. When set to true, the address is expected in base58 format (T-address). When false or omitted, hex format is expected. Default is false.

## Response

- result — boolean indicating whether the address is valid (true) or invalid (false).
- message — hexadecimal representation of the address if valid, or error message if invalid.

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/validateaddress \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs",
  "visible": true
}
'
```

### Response

```json
{
  "result": true,
  "message": "<string>"
}
```

## Use Case

- Validating user input before processing transactions to prevent errors.
- Verifying addresses received from external sources or user interfaces.
- Implementing address validation in wallets and DApps to ensure data integrity.
- Checking address format compatibility between base58 and hex representations.

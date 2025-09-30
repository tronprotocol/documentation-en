# Account Permission Management 

The TRON network supports fine-grained control of account permissions. By configuring permissions (owner, witness, active), joint control of accounts, secure delegation, and functional permission separation can be achieved. The following document details the account permission model, contract structure, configuration methods, and common interface calls.



## Function Overview

Account permission management allows:

- Setting permission levels for an account.
- Associating each permission with a group of addresses and weights.
- Implementing permission control through a threshold mechanism.
- Flexibly configuring which addresses can execute which contract types.

For detailed specifications, see [TIP-16: Account Permission Management](https://github.com/tronprotocol/tips/blob/master/tip-16.md).



## Permission Level Concepts

TRON supports three types of permission:

| Permission Type | Description                          |
|-----------------|--------------------------------------|
| owner           | Highest account permission, controls ownership and permission structure |
| witness         | Super Representative permission, used only for block production |
| active          | Custom permission, can specify functional permission combinations |

---

## Permission Structure Definition

### 1. Account Structure: `Account`

```
message Account {
  ...
  Permission owner_permission = 31;
  Permission witness_permission = 32;
  repeated Permission active_permission = 33;
}
```

Explanation:

- `owner_permission`: `owner` permission (only one).
- `witness_permission`: Super Representative permission (only one).
- `active_permission`: `active` permission list, supports up to 8.

### 2. Permission Configuration: `Permission`

```
message Permission {
  enum PermissionType {
    Owner = 0;
    Witness = 1;
    Active = 2;
  }
  PermissionType type = 1;
  int32 id = 2;
  string permission_name = 3;
  int64 threshold = 4;
  int32 parent_id = 5;
  bytes operations = 6;
  repeated Key keys = 7;
}
```

Explanation:

- `type`: Permission type (owner/witness/active).
- `id`: Permission ID, automatically assigned by the system.
  - `owner` = 0, `witness` = 1, `active` starts from 2 and increments.
- `permission_name`: Permission name, maximum 32 bytes.
- `threshold`: Permission threshold, operation is allowed only when the combined weight of the signing key ≥ this value.
- `operations`: Used only for Active permissions, specifies executable contract types.
- `keys`: Addresses and weights with this permission (up to 5).

### 3. Permission Key Structure: `Key`

```
message Key {
  bytes address = 1;
  int64 weight = 2;
}
```

- `address`: Address with permission.
- `weight`: Weight of this address under this permission.

### 4. Permission Update Transaction: `AccountPermissionUpdateContract`

```
message AccountPermissionUpdateContract {
  bytes owner_address = 1;
  Permission owner = 2;
  Permission witness = 3;
  repeated Permission actives = 4;
}
```

- This contract is used to **update all account permission structures at once**.
- Even if only one permission is modified, all other existing permissions must be fully specified in the contract.

### 5. Contract Type Enumeration: `ContractType`

```
enum ContractType {
  AccountCreateContract = 0;
  ...
  AccountPermissionUpdateContract = 46;
}
```

Active permissions configure which `ContractType` can be executed through the `operations` field, for details on how to calculate the value of `operations`, please see [Operations Value Calculation Example](#2-operations-value-calculation-example).

## Explanation of Each Permission Type

### `owner` Permission (Account Master Control)

- Holds full control over the account.
- Can modify any permission structure (including itself).
- Automatically set when creating an account, default threshold is 1, includes the account's own address.
- By default, transactions without a specified permission_id use the Owner permission.

### `witness` Permission (Block Production Permission)

- Available only for Super Representative, Super Representative Partner and Super Representative Candidate accounts.
- Controls block-producing nodes, does not have permissions for fund transfers or other operations.
- Can delegate block production permission to other addresses to enhance account security.

#### Super Representative Node Configuration Example:

```
# config.conf
//localWitnessAccountAddress = TMK5c1jd...m6FXFXEz  # TRON Address
localwitness = [
  xxx  # Private key of TMK5c1jd...m6FXFXEz
]
```

If the `witness` permission is modified, then:

```
localWitnessAccountAddress = TSMC4YzU...PBebBk2E
localwitness = [
  yyy  # Private key of TSMC4YzU...PBebBk2E
]
```

>**Note**: Only one private key is allowed in `localwitness`.

### Active Permission (Functional Permission Combination)

- Can combine contract permissions, assigning sub-permissions to different roles.
- Supports up to 8 `active` permission configurations.
- Permission IDs start from 2 and increment.
- When creating an account by default, one `active` permission is generated, with a default threshold of 1, containing only the account's own address.

## Operation Fees

| Operation                  | Fee Standard |
| -------------------------- | ------------ |
| Modify Account Permission  | 100 TRX      |
| Transaction (2 or more signatures) | Additional 1 TRX |

The above fees can be adjusted through proposals.

## Interfaces and Operation Examples

### 1. Permission Modification Operation Process

1. Use `getaccount` to query the current account permission structure.
2. Construct the new permission configuration.
3. Call `AccountPermissionUpdateContract`.
4. Sign and broadcast the transaction.

#### Example Request:

```
POST http://{{host}}:{{port}}/wallet/accountpermissionupdate

{
  "owner_address": "41ffa946...",
  "owner": {
    "type": 0,
    "id": 0,
    "permission_name": "owner",
    "threshold": 2,
    "keys": [...]
  },
  "witness": {
    "type": 1,
    "id": 1,
    "permission_name": "witness",
    "threshold": 1,
    "keys": [...]
  },
  "actives": [
    {
      "type": 2,
      "id": 2,
      "permission_name": "active0",
      "threshold": 3,
      "operations": "7fff1fc0037e...",
      "keys": [...]
    }
  ]
}
```

### 2. operations Value Calculation Example

`operations` is a 32-byte hexadecimal string (little-endian) representing executable contract permissions.
The following Java example generates permissions for contracts (ID=0-45):

```
Integer[] contractId = {0, 1, 2, ..., 45};
byte[] operations = new byte[32];
for (int id : contractId) {
  operations[id / 8] |= (1 << id % 8);
}
System.out.println(ByteArray.toHexString(operations));
```

### 3. Transaction Execution Process

1. Create the transaction.
2. Set `Permission_id` (default is 0, i.e., `owner` permission).
3. User A signs and forwards to B.
4. User B signs and forwards to C.
5. ...
6. The last user signs and broadcasts.
7. The node verifies if the total signature weight ≥ `threshold`; if yes, accepts the transaction.

>Example code reference: [wallet-cli Example](https://github.com/tronprotocol/wallet-cli/blob/develop/src/main/java/org/tron/common/utils/TransactionUtils.java)

## Auxiliary Interfaces

### Query Signed Addresses

```
POST /wallet/getapprovedlist

rpc GetTransactionApprovedList(Transaction) returns (TransactionApprovedList) {}
```

### Query Signature Weight

```
POST /wallet/getsignweight

rpc GetTransactionSignWeight(Transaction) returns (TransactionSignWeight) {}
```

## References

- [TIP-16 Permission Management Proposal](https://github.com/tronprotocol/tips/blob/master/tip-16.md)
- [Tron.proto Contract Type Definitions](https://github.com/tronprotocol/java-tron/blob/master/protocol/src/main/protos/core/Tron.proto)

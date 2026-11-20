# Account Model

## Introduction

TRON employs an account model for its ledger. All activities on the network, such as transfers, voting, and contract deployment, revolve around accounts.

- **Unique Identifier**: Each account is uniquely identified by its Address, which typically begins with a `T`.
- **Access Control**: Transactions initiated by an account must be signed by one or more private keys authorized by the selected account permission, with the combined signer weight meeting the permission's threshold.
- **Account Assets and Capabilities**: Each account can own and manage various resources, including:

    - **Assets**: TRX, TRC-10, TRC-20, TRC-721/TRC-1155 NFTs, etc.
    - **Network Resources**: Bandwidth and Energy.
    - **Permissions and Activities**: Initiating transactions, deploying and calling smart contracts, participating in Super Representative elections (voting or becoming a candidate), and more.

## How to Create an Account

There are two primary ways to create a new ordinary TRON account. Smart contract accounts are created through contract deployment.

**Method 1: Offline Generation and On-Chain Activation**

- Generate Address: Use a wallet application (like [TronLink](https://www.tronlink.org/)) to generate a new key pair (private key and public key) and derive the address from the public key.
- Activate Account: At this stage, the account exists only conceptually and must be "activated" to be used on the blockchain. Activation is accomplished by sending a positive amount of TRX or a TRC-10 token from an existing account to this new address. Once the transaction is successful, the new account is officially created on the TRON network.

**Method 2: Creation via System Contract**

- Developers can create an account by calling the `AccountCreateContract` system contract.

**Account Creation Cost:**

Creating an account through `AccountCreateContract`, a TRX transfer using `TransferContract`, or a TRC-10 transfer using `TransferAssetContract` incurs an additional account creation fee, paid by the initiating account and burned. This fee is set by the `getCreateNewAccountFeeInSystemContract` network parameter (currently 1 TRX on mainnet).

The transaction also consumes Bandwidth, but daily free Bandwidth cannot be used. If the initiating account has insufficient staked or delegated Bandwidth, the fixed `getCreateAccountFee` (currently 0.1 TRX on mainnet) is burned instead of the usual per-byte Bandwidth fee. Both fee parameters can be changed by committee proposal.

Smart contract execution can also create ordinary accounts, for example through a positive-value TRX or TRC-10 transfer to an unactivated address, or through `SELFDESTRUCT` with a beneficiary address that does not yet exist. `SELFDESTRUCT` can create the beneficiary account even when the contract has a zero balance. These account creation paths incur an additional base cost of 25,000 Energy; the two fixed fees described above do not apply.

## Key Pair Generation Algorithm

TRON's signature algorithm is ECDSA, and the selected curve is SECP256K1. Its private key is a random number, and the public key is a point on the elliptic curve. The generation process is as follows: first, generate a random number `d` as the private key, then calculate `P = d × G` as the public key, where `G` is the base point of the elliptic curve, and the base point is public.

The private key is a 32-byte large number, and the public key consists of two 32-byte large numbers, which are the abscissa and ordinate of the above-mentioned `P` point respectively.



## TRON Address Generation

The following procedure derives an ordinary account address from a public key. Smart contract addresses follow separate derivation rules.

1. Take the public key `P` as input, calculate `SHA3` to get the result `H` (`SHA3` uses Keccak256).
2. Take the last 20 bytes of `H`, and prepend the byte `0x41` to get the `address`.
3. Perform a Base58Check calculation on the `address` to get the final address.

### Base58Check Calculation Process

1. Calculate the checksum

    a. Perform a SHA256 hash operation on `address` to get `h1`.  
    b. Perform a SHA256 operation on `h1` again to get `h2`.  
    c. Take the first 4 bytes of `h2` as the checksum `check`.

2. Splice data: Append `check` to `address` to get `address||check`.
3. Base58 encoding: Perform Base58 encoding on `address||check`. The character table for Base58 is: `"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"`, excluding easily confused characters: `0` (Arabic numeral 0), `O` (uppercase letter O), `I` (uppercase letter I), `l` (lowercase letter L).

### TRON Address Characteristics

The principle of Base58 encoding is to convert a large integer with a base of 256 into a representation with a base of 58, and then map it to the character table. Since the first byte of `address||check` is fixed as `0x41`, its decimal value `N` satisfies: `65 × 256²⁴ ≤ N < 66 × 256²⁴`.

- Length is `34`: Because `58³⁴ > 66 × 256²⁴` indicates that a length of `34` is sufficient, and `58³³ < 65 × 256²⁴` indicates that a length of `33` is insufficient, so the length can only be `34`.
- The first character is `T`: First, the length is determined to be `34`, and since `27 × 58³³ > 66 × 256²⁴` indicates that the index of the first character in the Base58 character table must be less than `27`, and `26 × 58³³ < 65 × 256²⁴` indicates that the index must be greater than or equal to `26`, so the first index can only be `26`, and `26` corresponds to `T` in the Base58 character table (`0` corresponds to `'1'`).

## Signature Specification

Transactions can be signed using the Owner permission (`Permission_id = 0`) or an existing Active permission (`Permission_id ≥ 2`). The Witness permission (`Permission_id = 1`) cannot be used for transaction signing.

### Algorithm

1. Take the `raw_data` of the transaction, convert it to `byte[]` format, and record it as `data` (for example, the `byte[]` type in Java).
2. Perform a `sha256` operation on `data` to get the hash value of the transaction, recorded as `hash`.
3. Use a private key `d` authorized by the account permission selected by the transaction contract's `Permission_id` to sign the `hash`. If multiple signatures are needed to meet the permission's threshold, each signer signs the same `hash` with their own authorized private key. The signature algorithm is the ECDSA algorithm (using the SECP256K1 curve). Each signature result includes three values: `r`, `s`, and `v`:

    * **Calculate the `r` value**: Generate the per-signature nonce `k`. In java-tron, `k` is derived deterministically from the private key `d` and the transaction's `hash` using HMAC-SHA256 (`HMacDSAKCalculator`), rather than sampled randomly for each signature. Calculate the temporary public key `K = k × G` (`G`: curve base point), then `r = K_x mod n`, that is, the abscissa of `K` modulo `n`, where `n` is the curve order (`n` and `G` satisfy `n × G = O`, and `O` is the zero point of the elliptic curve group on the finite field). `r` is 32 bytes.
    * **Calculate the `s` value**: First calculate the modular inverse of the temporary private key `k` with respect to `n`, `k⁻¹`, that is, `k⁻¹` satisfies `k⁻¹ × k = 1 mod n`, then calculate the `s` value through the transaction's `hash`, the user's private key `d`, and the `r` value: `s = (k⁻¹ × (hash + d × r)) mod n`. `s` is 32 bytes.
    * **Calculate the `v` value**: Calculate the `recoveryId` first. Due to the modulo operation on the `r` value and the symmetry of the elliptic curve, if there is only the `r` value, one `r` can recover up to four `K`s. The value range of `recoveryId` is `0, 1, 2, 3`. The calculation of the `v` value depends on `recoveryId`. Historically, to remain consistent with Ethereum, the  `v` value will be `27` added to `recoveryId`, that is, the value range of `v` is `27, 28, 29, 30`. With a determined `v`, the unique `K` can be recovered. `v` is 1 byte.

4. Concatenate the values of `r`, `s`, and `recoveryId` (or `r`, `s`, and `v`) to obtain the complete signature. The concatenation order shall be `r || s || recoveryId` (or `r || s || v`). At present, both the transaction signing in the official client `wallet-cli` and the block signing in `java-tron` (during block production by SRs) adopt the `recoveryId` scheme, i.e., `signature = r || s || recoveryId`.

### Java Code Sample

```java
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    ECDSASignature signature = myKey.sign(hash);
    ByteString bsSign = ByteString.copyFrom(signature.toByteArray());
    transactionBuilderSigned.addSignature(bsSign);
    return transactionBuilderSigned.build();
}
```

## Signature Verification

When a FullNode receives a transaction, it uses the transaction hash and each signature to recover the signer's public key via the ECDSA recovery mechanism (ecrecover), then derives the signer's address. It validates these addresses against the account permission selected by the transaction contract's `Permission_id`. The signers must be authorized by that permission, and their combined weight must meet its threshold. A signer's address does not have to match the transaction's `owner_address`.

### Algorithm

1. Recover the public key point `K`: The temporary public key point `K` can be uniquely recovered through `v` and `r` in the signature.
2. Derive the public key `P`:

    -  Known signature equation: `s = k⁻¹(hash + d × r) mod n`
    -  Multiply both sides by `k`: `s × k = (hash + d × r) mod n`
    -  Multiply both sides by the base point `G` of the curve (using `K = k × G` and `P = d × G`): `s × K = hash × G + r × P`
    -  Since `s`, `K`, `hash`, `G`, and `r` are all known, `P` can be obtained.

3. Generate TRON address: same as [TRON Address Generation](#tron-address-generation).
4. Permission verification: check the recovered signer addresses against the account permission selected by `Permission_id`. Reject duplicate signers and require their combined weight to meet the permission's threshold. For Active permissions, also verify that the transaction type is allowed.

### Example

Signature verification is performed by the FullNode. In java-tron, [`ECKey.signatureToAddress`](https://github.com/tronprotocol/java-tron/blob/master/crypto/src/main/java/org/tron/common/crypto/ECKey.java) recovers the signer's address. [`TransactionCapsule.validateSignature` and `checkWeight`](https://github.com/tronprotocol/java-tron/blob/master/chainbase/src/main/java/org/tron/core/capsule/TransactionCapsule.java) perform the account permission and signature weight checks.

### Signature normalization

ECDSA signatures using the secp256k1 curve are malleable: for a valid signature $(r, s)$, the pair $(r, n - s)$ is also valid for the same public key and message, where $n$ is the curve order.

Ethereum's [EIP-2](https://eips.ethereum.org/EIPS/eip-2) requires transaction signatures to use low-S values, where $s \leq n/2$.

In TRON, the transaction ID is calculated from the serialized `raw_data` and does not include signatures. The java-tron transaction signature validation path does not enforce low-S values. However, both java-tron and wallet-cli normalize signatures to low-S when signing.

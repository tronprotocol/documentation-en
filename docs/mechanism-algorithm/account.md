# Account Model

## Introduction

TRON uses the account model. The address is the unique identifier of an account, and a private key signature is required to operate an account. An account has many attributes, including TRX & TRC10 token balances, bandwidth, energy, Etc. An account can send transactions to increase or reduce its TRX or TRC10 token balances, deploy smart contracts, and trigger the smart contracts released by itself or others. All TRON accounts can apply to be Super Representatives or vote for the elected Super Representatives. Accounts are the basis of all activities on TRON.

## How to Create an Account

1. Use a wallet application([TronLink](https://www.tronlink.org/) is recommended) to generate a pair of address and private key. To active the account, you need to transfer TRX or other token to it.
2. Use an account already existed in TRON network to create an account

If you have enough staked BandWidth Points, creating an account only consume your staked BandWidth Points, otherwise, it burns 0.1 TRX.

## Key Pair Generation Algorithm

TRON's signature algorithm is ECDSA, and the selected curve is SECP256K1. Its private key is a random number, and the public key is a point on the elliptic curve. The generation process is as follows: first, generate a random number `d` as the private key, then calculate `P = d × G` as the public key, where `G` is the base point of the elliptic curve, and the base point is public.

The private key is a 32-byte large number, and the public key consists of two 32-byte large numbers, which are the abscissa and ordinate of the above-mentioned `P` point respectively.

## TRON Address Generation

1. Take the public key `P` as input, calculate SHA3 to get the result `H`, and SHA3 uses Keccak256.
2. Take the last 20 bytes of `H`, and prepend a byte `0x41` to get `address`.
3. Perform base58check calculation on `address` to get the final address.

### Base58Check Calculation Process

1. Calculate the checksum
    1. Perform SHA256 hash operation on `address` to get `h1`
    2. Perform SHA256 operation on `h1` again to get `h2`
    3. Take the first 4 bytes of `h2` as the checksum `check`

2. Splice data
Append `check` to `address` to get `address||check`

3. Base58 encoding
Perform Base58 encoding on `address||check`. The character table for Base58 is: `"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"`, excluding easily confused characters: `0` (Arabic numeral 0), `O` (uppercase letter O), `I` (uppercase letter I), `l` (lowercase letter L).

### TRON Address Characteristics
The principle of Base58 encoding is to convert a large integer with a base of 256 into a representation with a base of 58, and then map it to the character table. Since the first byte of `address||check` is fixed as `0x41`, its decimal value `N` satisfies: `65 × 256²⁴ ≤ N < 66 × 256²⁴`.

- Length is `34`: Because `58³⁴ > 66 × 256²⁴` indicates that length of `34` are sufficient, and `58³³ < 65 × 256²⁴` indicates that length of `33` are insufficient, so the length can only be `34`.
- The first character is `T`: First, the length is determined to be `34`, and since `27 × 58³³ > 66 × 256²⁴` indicates that the index of first character in base58 character table must be less than `27`, and `26 × 58³³ < 65 × 256²⁴` indicates that the index must be greater than or equal to `26`, so the first index can only be `26`, and `26` corresponds to `T` in the base58 character table (`0` corresponds to `1`).

## Signature

### Algorithm
1. Take the rawdata of the transaction, convert it to byte[] format, and record it as `data`.

2. Perform sha256 operation on `data` to get the hash value of the transaction, recorded as `hash`.

3. Use the private key `d` corresponding to the address in the transaction contract to sign `hash`. The signature algorithm is the ECDSA algorithm (using the SECP256K1 curve). The signature result includes three values: `r`, `s`, and `v`:
    1. Calculate the `r` value: randomly generate a temporary private key `k`, calculate the temporary public key `K = k × G` (G: curve base point), `r = K_x mod n`, that is, the abscissa of `K` modulo `n`, where `n` is the curve order (n and G satisfy `n × G = O`, and O is the zero point of the elliptic curve group on the finite field). `r` is 32 bytes.
    2. Calculate the `s` value: first calculate the modular inverse of the temporary private key `k` with respect to n, `k⁻¹`, that is, `k⁻¹` satisfies `k⁻¹ × k = 1 mod n`, then calculate the `s` value through the transaction's `hash`, the user's private key `d`, and the `r` value, `s = (k⁻¹ × (hash + d × r)) mod n`. `s` is 32 bytes.
    3. Calculate the `v` value: the `v` value is the recovery identifier. Due to `r` value undergoes a modulo operation and the symmetry of the elliptic curve, if there is only the `r` value, one `r` can recover up to four `K`s. The value range of `v` is four integers: 0, 1, 2, 3. Historically, to be consistent with Ethereum, the final `v` value will be 27 added to 0, 1, 2, 3, that is, the final value range of `v` is 27, 28, 29, 30. With a determined `v`, the unique `K` can be recovered. `v` is 1 byte.

4. Append the concatenated signature results `r`, `s`, `v` to the transaction, in the order `v || r || s`.

### Example

```
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    ECDSASignature signature = myKey.sign(hash);
    ByteString bsSign = ByteString.copyFrom(signature.toByteArray());
    transactionBuilderSigned.addSignature(bsSign);
}
```

## Signature Verification
After receiving the transaction, the full node will perform signature verification, recover the public key (the `P` in [Key Pair Generation Algorithm](#key-pair-generation-algorithm)) from `hash`, `r`, `s`, and `v`, then generate a TRON address through base58check encoding, and compare it with the address in the transaction. If they are the same, the signature verification passes.

### Algorithm

1. Recover the public key point `K`: The temporary public key point `K` can be uniquely recovered through `v` and `r` in the signature.

2. Derive the public key `P`:
    1. Known signature equation:
     `s = k⁻¹(hash + d × r) mod n`
    2. Multiply both sides by `k`:
     `s × k = (hash + d × r) mod n`
    3. Multiply both sides by the base point `G` of the curve (using `K = k × G` and `P = d × G`):
     `s × K = hash × G + r × P`
    4. Since `s`, `K`, `hash`, `G`, and `r` are all known, `P` can be obtained.

3. Generate TRON address: same as [TRON Address Generation](#tron-address-generation)

4. Address verification: compare whether the generated TRON address is consistent with the address in the transaction contract.

### Example
Signature verification is performed by the full node. For [ECDSA algorithm signature verification](https://github.com/tronprotocol/java-tron/blob/master/crypto/src/main/java/org/tron/common/crypto/ECKey.java), you can refer to java-tron, and the core function is `signatureToAddress`.

## Account Initiating Transactions
The above is the theoretical knowledge of the TRON account model. For developers, it is recommended to use the official SDKs (Trident/TronWeb) for accounts to initiate transactions (construction/signature/broadcast). For detailed information, see [Developer Documentation](https://developers.tron.network/docs/create-offline-transactions-with-trident-and-tronweb).

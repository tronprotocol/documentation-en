# Account Model

## Introduction
TRON employs an account model for its ledger. All activities on the network, such as transfers, voting, and contract deployment, revolve around accounts.

 - **Unique Identifier**: Each account is uniquely identified by its Address, which typically begins with a `T`.
 - **Access Control**: Any operation on an account (such as a transfer) requires a signature from the corresponding Private Key.
 - **Account Assets and Capabilities**: Each account can own and manage various resources, including:

    - Assets: TRX, TRC-10, TRC-20, TRC-721/TRC-1155 NFTs, etc.
    - Network Resources: Bandwidth and Energy.
    - Permissions and Activities: Initiating transactions, deploying and calling smart contracts, participating in Super Representative elections (voting or becoming a candidate), and more.

## How to Create an Account

There are two primary ways to create a new TRON account:

**Method 1: Offline Generation and On-Chain Activation**

   - Generate Address: Use a wallet application (like [TronLink](https://www.tronlink.org/)) to generate a new key pair (private key and address).
   - Activate Account: At this stage, the account exists only conceptually and must be "activated" to be used on the blockchain. Activation is accomplished by sending any amount of TRX or a TRC-10 token from an existing account to this new address. Once the transaction is successful, the new account is officially created on the TRON network.

**Method 2: Creation via System Contract**

   - Developers can create an account by calling the `CreateAccount` system contract.

**Account Creation Cost:**

   - A fixed fee of 1 TRX is required to create and activate a new account.
   - Additionally, if the creator's account has sufficient bandwidth (either from staking TRX or delegated from others), the creation will only consume bandwidth. Otherwise, 0.1 TRX will be burned to pay for the bandwidth fee.

## Key Pair Generation Algorithm

TRON's signature algorithm is ECDSA, and the selected curve is SECP256K1. Its private key is a random number, and the public key is a point on the elliptic curve. The generation process is as follows: first, generate a random number `d` as the private key, then calculate `P = d × G` as the public key, where `G` is the base point of the elliptic curve, and the base point is public.

The private key is a 32-byte large number, and the public key consists of two 32-byte large numbers, which are the abscissa and ordinate of the above-mentioned `P` point respectively.



## TRON Address Generation

1. Take the public key P as input, calculate SHA3 to get the result H, and SHA3 uses Keccak256.
2. Take the last 20 bytes of H, and prepend a byte 0x41 to get address.
3. Perform base58check calculation on address to get the final address.

### Base58Check Calculation Process

1. Calculate the checksum

    a. Perform SHA256 hash operation on `address` to get `h1`  
    b. Perform SHA256 operation on `h1` again to get `h2` 
    c. Take the first 4 bytes of `h2` as the checksum `check`

2. Splice data Append `check` to `address` to get `address||check`
3. Base58 encoding Perform Base58 encoding on `address||check`. The character table for Base58 is: `"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"`, excluding easily confused characters:` 0` (Arabic numeral 0), `O` (uppercase letter O), `I` (uppercase letter I), `l` (lowercase letter L).

### TRON Address Characteristics

The principle of Base58 encoding is to convert a large integer with a base of 256 into a representation with a base of 58, and then map it to the character table. Since the first byte of `address||check` is fixed as `0x41`, its decimal value `N` satisfies: `65 × 256²⁴ ≤ N < 66 × 256²⁴`.

- Length is `34`: Because `58³⁴ > 66 × 256²⁴` indicates that length of `34` are sufficient, and `58³³ < 65 × 256²⁴` indicates that length of `33` are insufficient, so the length can only be `34`.
- The first character is `T`: First, the length is determined to be `34`, and since `27 × 58³³ > 66 × 256²⁴` indicates that the index of first character in base58 character table must be less than `27`, and `26 × 58³³ < 65 × 256²⁴` indicates that the index must be greater than or equal to `26`, so the first index can only be `26`, and `26` corresponds to `T` in the base58 character table (`0` corresponds to `1`).

## Signature Specification

### Algorithm

1. Take the rawdata of the transaction, convert it to byte[] format, and record it as `data`. (For example, the `byte[]` type in Java.).
2. Perform `sha256` operation on `data` to get the hash value of the transaction, recorded as `hash`.
3. Use the private key d corresponding to the address in the transaction contract to sign hash. The signature algorithm is the ECDSA algorithm (using the SECP256K1 curve). The signature result includes three values: `r`, `s`, and `v`:

    * **Calculate the `r` value**: randomly generate a temporary private key `k`, calculate the temporary public key `K = k × G` (G: curve base point), `r = K_x mod n`, that is, the abscissa of `K` modulo `n`, where `n` is the curve order (n and G satisfy `n × G = O`, and O is the zero point of the elliptic curve group on the finite field). `r` is 32 bytes.
    * **Calculate the `s` value**: first calculate the modular inverse of the temporary private key `k` with respect to n, `k⁻¹`, that is, `k⁻¹` satisfies `k⁻¹ × k = 1 mod n`, then calculate the `s` value through the transaction's `hash`, the user's private key `d`, and the `r` value, `s = (k⁻¹ × (hash + d × r)) mod n`. `s` is 32 bytes.
    * **Calculate the `v` value**: the `v` value is the recovery identifier. Due to `r` value undergoes a modulo operation and the symmetry of the elliptic curve, if there is only the `r` value, one `r` can recover up to four `K`s. The value range of `v` is four integers: 0, 1, 2, 3. Historically, to be consistent with Ethereum, the final `v` value will be 27 added to 0, 1, 2, 3, that is, the final value range of `v` is 27, 28, 29, 30. With a determined `v`, the unique `K` can be recovered. `v` is 1 byte.

4. Append the concatenated signature results `r`, `s`, `v` to the transaction, in the order `v || r || s`.

#### Java Code Sample

```java
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    ECDSASignature signature = myKey.sign(hash);
    ByteString bsSign = ByteString.copyFrom(signature.toByteArray());
    transactionBuilderSigned.addSignature(bsSign);
}
```

## Signature Verification
When a Fullnode receives a transaction, it uses the transaction hash and signature to recover a public key via the ECDSA recovery mechanism (ecrecover). An address is then derived from this public key. If the derived address matches the originator's address specified in the transaction, the signature is considered valid.

### Algorithm

1. Recover the public key point `K`: The temporary public key point `K` can be uniquely recovered through `v` and `r` in the signature.
2. Derive the public key `P`:

   -  Known signature equation:
     `s = k⁻¹(hash + d × r) mod n`
   -  Multiply both sides by `k`:
     `s × k = (hash + d × r) mod n`
   -  Multiply both sides by the base point `G` of the curve (using `K = k × G` and `P = d × G`):
     `s × K = hash × G + r × P`
   -  Since `s`, `K`, `hash`, `G`, and `r` are all known, `P` can be obtained.

3. Generate TRON address: same as [TRON Address Generation](#tron-address-generation)
4. Address verification: compare whether the generated TRON address is consistent with the address in the transaction contract.

### Example
Signature verification is performed by the Fullnode. For [ECDSA algorithm signature verification](https://github.com/tronprotocol/java-tron/blob/master/crypto/src/main/java/org/tron/common/crypto/ECKey.java), you can refer to java-tron, and the core function is `signatureToAddress`.

### Signature normalization
`ECDSA` signatures (using the `secp256k1` curve) are malleable, meaning that for a signature $(r, s)$, where $r, s \in [1, n-1]$, the pair $(r, n - s)$ is also a valid signature. Since signatures affect transaction id in both Bitcoin and Ethereum, [BIP-62](https://github.com/bitcoin/bips/blob/master/bip-0062.mediawiki) and [EIP-2](https://eips.ethereum.org/EIPS/eip-2) require signatures to be normalized, i.e., $s \leq n/2$. However, for the TRON network, the transaction id does not include signature information, so there is no strict requirement for signature normalization, and signature verification does not need to check whether the signature is normalized. Although there is no strict restriction, both `java-tron` and `wallet-cli` currently perform signature normalization.

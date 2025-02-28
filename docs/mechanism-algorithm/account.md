# Account Model

## Introduction

TRON uses the account model. The address is the unique identifier of an account, and a private key signature is required to operate an account. An account has many attributes, including TRX & TRC10 token balances, bandwidth, energy, Etc. An account can send transactions to increase or reduce its TRX or TRC10 token balances, deploy smart contracts, and trigger the smart contracts released by itself or others. All TRON accounts can apply to be Super Representatives or vote for the elected Super Representatives. Accounts are the basis of all activities on TRON.

## How to Create an Account

1. Use a wallet application([TronLink](https://www.tronlink.org/) is recommended) to generate a pair of address and private key. To active the account, you need to transfer TRX or other token to it.
2. Use an account already existed in TRON network to create an account

If you have enough staked BandWidth Points, creating an account only consume your staked BandWidth Points, otherwise, it burns 0.1 TRX.

## Key-pair Generation

TRON signature algorithm is ECDSA, curve used is SECP256K1. Private key is a random number, public key is a point in the elliptic curve. The process is: first generate a random number d to be the private key, then calculate P = d * G as the public key, G is the elliptic curve base point.

## Address Format

Use the public key P as the input, by SHA3 get the result H. The length of the public key is 64 bytes, SHA3 uses Keccak256. Use the last 20 bytes of H, and add a byte of 0x41 in front of it, then the address come out. Do basecheck to address, here is the final address. All addresses start with 'T'.

basecheck process: first do sha256 calculation to address to get h1, then do sha256 to h1 to get h2, use the first 4 bytes as check to add it to the end of the address to get address||check, do base58 encode to address||check to get the final result.

character map:
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

## Signature

### Steps

1. Get the rawdata of the transaction, then transfer it to `byte[]`
2. Do sha256 calculation to the rawdata
3. Use the private key to sign the result gained from step 2
4. Add the signature back into the transaction

### Algorithm

1. ECDSA, SECP256K
2. Example:

    ```text
    priKey:::8e812436a0e3323166e1f0e8ba79e19e217b2c4a53c970d4cca0cfb1078979df
    pubKey::04a5bb3b28466f578e6e93fbfd5f75cee1ae86033aa4bbea690e3312c087181eb366f9a1d1d6a437a9bf9fc65ec853b9fd60fa322be3997c47144eb20da658b3d1
    hash:::159817a085f113d099d3d93c051410e9bfe043cc5c20e43aa9a083bf73660145
    r:::38b7dac5ee932ac1bf2bc62c05b792cd93c3b4af61dc02dbb4b93dacb758123f
    s:::08bf123eabe77480787d664ca280dc1f20d9205725320658c39c6c143fd5642d
    v:::0
    ```

    Note: The size of the signature result is 65 bytes. r 32 bytes, s 32 bytes, v 1 bytes.

3. fullnode will verify the signature, it generates an address with the value of hash and r、s、v, then it compares with the address in the transaction.

### Demo

```java
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    List<Contract> listContract = transaction.getRawData().getContractList();

    for (int i = 0; i < listContract.size(); i++) {
        ECDSASignature signature = myKey.sign(hash);
        ByteString bsSign = ByteString.copyFrom(signature.toByteArray());

        // Each contract may be signed with a different private key in the future.
        transactionBuilderSigned.addSignature(bsSign);
    }
}
```

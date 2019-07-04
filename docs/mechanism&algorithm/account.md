

## Introduction

TRON uses account model. An account's identity is address, it needs private key signature to operate an account. An account has many attributes, like TRX balance, tokens balance, bandwidth, etc. TRX and tokens can be transfered from account to account and it costs bandwidth. An account can also issue a smart contract, apply to become a super representative candidate, vote, etc. All TRON's activities are based on account.

## How to Create an Account

1.&nbsp;Use a wallet to generate the address and private key. To active the account, you need to transfer TRX or transfer token to the new created account. [generate an account](https://tronscan.org/#/wallet/new)

2.&nbsp;Use an account already existed in TRON network to create an account   

## Key-pair Generation
Tron signature algorithm is ECDSA, curve used is SECP256K1. Private key is a random bumber, public key is a point in the elliptic curve. The process is: first generate a random number d to be the private key, then caculate P = d * G as the public key, G is the elliptic curve base point.

## Address Format
Use the public key P as the input, by SHA3 get the result H. The length of the public key is 64 bytes, SHA3 uses Keccak256. Use the last 20 bytes of H, and add a byte of 0x41 in front of it, then the address come out. Do basecheck to address, here is the final address. All addresses start with 'T'.   

basecheck process: first do sha256 caculation to address to get h1, then do sha256 to h1 to get h2, use the first 4 bytes as check to add it to the end of the address to get address||check, do base58 encode to address||check to get the final result.  

character map:  
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"  

## Signature

<h3> Step </h3>
1.&nbsp;取交易的rawdata，转成byte[]格式。  
2.&nbsp;对rawdata进行sha256运算。  
3.&nbsp;用交易每个合约中地址对应的私钥（现在一般就是一个合约，一个私钥），对sha256的结果进行签名。  
4.&nbsp;把签名结果添加到交易中。  
<h3> Algorithm </h3>
1.&nbsp;ECDSA算法，SECP256K。  
2.&nbsp;签名示例数据    
```text    
    priKey:::8e812436a0e3323166e1f0e8ba79e19e217b2c4a53c970d4cca0cfb1078979df         
    pubKey::04a5bb3b28466f578e6e93fbfd5f75cee1ae86033aa4bbea690e3312c087181eb366f9a1d1d6a437a9bf9fc65ec853b9fd60fa322be3997c47144eb20da658b3d1         
    hash:::159817a085f113d099d3d93c051410e9bfe043cc5c20e43aa9a083bf73660145         
    r:::38b7dac5ee932ac1bf2bc62c05b792cd93c3b4af61dc02dbb4b93dacb758123f         
    s:::08bf123eabe77480787d664ca280dc1f20d9205725320658c39c6c143fd5642d         
    v:::0  
```   
注意：签名结果应该是65字节。 r 32字节， s 32字节，v 1个字节。  
3.&nbsp;fullnode节点收到交易后会进行验签，由hash 和 r、s、v计算出一个地址，与合约中的地址进行比较，相同则为验签通过。  
<h3> Demo </h3>
```
public static Transaction sign(Transaction transaction, ECKey myKey) {
    Transaction.Builder transactionBuilderSigned = transaction.toBuilder();
    byte[] hash = sha256(transaction.getRawData().toByteArray());
    List<Contract> listContract = transaction.getRawData().getContractList();

    for (int i = 0; i < listContract.size(); i++) {
      ECDSASignature signature = myKey.sign(hash);
      ByteString bsSign = ByteString.copyFrom(signature.toByteArray());
      
      //Each contract may be signed with a different private key in the future.
      transactionBuilderSigned.addSignature(bsSign);
    }
  }
```
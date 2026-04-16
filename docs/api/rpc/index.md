# gRPC API

## 1. Overview

gRPC is a modern, open-source, high-performance RPC framework based on the HTTP/2 protocol and Protocol Buffers (Protobuf) for data serialization. Compared to traditional HTTP/1.1 RESTful APIs, gRPC offers higher performance, lower latency, smaller packet sizes, bi-directional streaming capabilities, and a robust code generation mechanism, making it an ideal choice for efficient and stable interaction with blockchain nodes.

TRON provides a set of gRPC-based API interfaces, allowing developers to interact with TRON nodes in a high-performance and strongly typed manner. This article will use Java as an example to explain how to perform a basic gRPC call in details, from obtaining .proto files to completion.

**For the specific definition of API, please refer to the following link:**
[api/api.proto](https://github.com/tronprotocol/protocol/blob/master/api/api.proto)

!!! note
    SolidityNode is deprecated. Now a FullNode supports all RPCs of a SolidityNode. New developers should deploy FullNode only.

Most gRPC APIs are accessed via the `wallet` service. Some APIs also support the `walletsolidity` service, which provides access to **confirmed on-chain data only**. Each API page indicates which services it supports.

## 2. Understanding TRON's gRPC Interfaces and Protocol Buffers

All on-chain operations and data queries in TRON are exposed through gRPC services. The definitions of these services are located in .proto files. **Protocol Buffers** is a language-neutral, platform-neutral, extensible mechanism for serializing structured data, used to define service interfaces and message structures.

Through .proto files, you can:

* **Define Services:** Contain methods (RPCs) that can be called by clients.
* **Define Messages:** Describe the data structures for requests and responses.

The gRPC toolchain automatically generates client and server code based on these .proto files. The code includes all the underlying logic required for communicating with TRON nodes.

## 3. Complete gRPC Call Process

### 3.1 Obtaining TRON's .proto Files

TRON officially maintains a GitHub repository for all .proto files. These files are the foundation for generating gRPC client code.

1. **Access the TRON Protocol Repository:**
   Open TRON's official `protocol` GitHub repository: [https://github.com/tronprotocol/protocol](https://github.com/tronprotocol/protocol)

2. **Download .proto Files:**
   You can find core .proto files in the `core/src/main/proto` directory, for example:

   * `api/api.proto`: Define the main gRPC services and methods (e.g., `Wallet` service).
   * `core/Tron.proto`: Defines core TRON data structures (e.g., `Block`, `Transaction`, `Account`, etc.).
   * `core/contract/account_contract.proto`, `core/contract/asset_issue_contract.proto`, etc.: Define message structures for various system contract operations.

### 3.2 Generating gRPC Client Code

After obtaining the .proto files, you need to generate Java client code.

To avoid affecting other local settings and projects, and to simplify the generation process, we strongly recommend using Maven or Gradle's Protobuf plugin in your Java project.

**Maven (`pom.xml`) Configuration Description:**

Configure the necessary dependencies and build plugins in your project's `pom.xml` file.

This typically includes **`grpc-netty-shaded`** for network communication, **`grpc-protobuf`** for Protobuf message processing, and **`grpc-stub`** for gRPC client stubs.

At the same time, you also need to add the **Protobuf Java runtime libraries**, including `protobuf-java` and `protobuf-java-util`. These dependencies are essential to ensure that your project can correctly handle Protobuf messages and perform gRPC communication. In addition, you need to configure the **`protobuf-maven-plugin`**, which will be used to automatically detect the operating system, specify the Maven coordinates of the Protobuf compiler and the gRPC Java plugin, and set the source directory for .proto files so that Java code can be automatically generated during the build process.

**Code Generation Steps:**
Place the .proto files downloaded from TRON's GitHub in the configured source directory of your project (e.g., `src/main/proto` for Maven projects). Then, execute the corresponding build command in the project's root directory (`mvn clean install` for Maven, `gradle build` for Gradle), after which the build tool's Protobuf plugin will automatically generate the required Java gRPC client code.

**Gradle (`build.gradle`) Configuration Description:**

The dependencies required for Gradle are basically the same as Maven. Here is an example of the configuration file (build.gradle). Please modify the version numbers based on your actual data:

```groovy
dependencies {
    implementation 'io.github.tronprotocol:trident:0.9.2'
    
    implementation 'io.grpc:grpc-netty-shaded:1.64.0'
    implementation 'io.grpc:grpc-protobuf:1.64.0'
    implementation 'io.grpc:grpc-stub:1.64.0'
    implementation 'com.google.protobuf:protobuf-java:3.25.1' 
}
```

After finishing the configurations, use `gradle clean build`.

### 3.3 Building the gRPC Client and Making Calls

Once the code is generated, you can use these generated classes in your Java project to build a gRPC client and communicate with a TRON node.

#### 3.3.1 Core Concepts

* **`ManagedChannel`:** Represents a connection to a gRPC server, managing the underlying network connection.
* **`Stub`:** The client interface generated from the .proto file. The interface provides a convenient way to call methods defined in the gRPC service. Common types include `BlockingStub` (blocking) and `FutureStub` (asynchronous).
* **TRON Node Endpoint:** TRON's gRPC service typically runs on port `50051`. Accessing TronGrid public nodes may require an API Key.

#### 3.3.2 Calling Process

The basic process for calling a gRPC method is as follows:

1. **Create `ManagedChannel`:** You need to configure the target TRON node's address and the port to establish a connection with the gRPC server.
2. **Create `Stub`:** Use the `WalletGrpc` class generated from the .proto file to create the corresponding stub instance, for example, `WalletGrpc.newBlockingStub(channel)` for blocking calls.
3. **Attach API Key (if required):** If you are using TronGrid or similar public node services that require an API Key, you typically need to add your API Key as metadata to the request header.
4. **Call Method:** Use the stub instance you created to call the method defined in the TRON gRPC service, passing in the appropriate request message.
5. **Process Response:** Receive and parse the response message returned from the TRON node.
6. **Shut down `ManagedChannel`:** When your application ends or the connection is no longer needed, be sure to shut down `ManagedChannel` to release network resources.

**Trident** has highly encapsulated all the complex steps of the above gRPC interactions, especially those involving **transaction construction, signing, and broadcasting**, freeing developers from handling these underlying details. Below is the relevant source code implementation in Trident. Please note that only part of the code in the `ApiWrapper` class is demonstrated here. For the complete code, please refer to: [ApiWrapper.java](https://github.com/tronprotocol/trident/blob/main/core/src/main/java/org/tron/trident/core/ApiWrapper.java)

```java
package org.tron.trident.core;

// Import core classes related to the gRPC framework and Google Protobuf
import com.google.protobuf.ByteString;
import com.google.protobuf.Message;
import io.grpc.ClientInterceptor;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.Metadata;
import io.grpc.stub.MetadataUtils;

// Import related classes from TridentSDK and TRON Protobuf definitions
import org.tron.trident.api.WalletGrpc;
import org.tron.trident.api.WalletSolidityGrpc;
import org.tron.trident.core.key.KeyPair;
import org.tron.trident.proto.Chain.Transaction;
import org.tron.trident.proto.Contract.TransferContract;
import org.tron.trident.proto.Response.TransactionExtention;

public class ApiWrapper implements Api {

    public final WalletGrpc.WalletBlockingStub blockingStub;
    public final WalletSolidityGrpc.WalletSolidityBlockingStub blockingStubSolidity;
    public final KeyPair keyPair;
    public final ManagedChannel channel;
    public final ManagedChannel channelSolidity;

    public ApiWrapper(
        String grpcEndpoint,
        String grpcEndpointSolidity,
        String hexPrivateKey,
        String apiKey
    ) {
        // Create ManagedChannel for full node
        channel = ManagedChannelBuilder.forTarget(grpcEndpoint).usePlaintext().build();
        // Create ManagedChannel for Solidity node
        channelSolidity = ManagedChannelBuilder.forTarget(grpcEndpointSolidity)
            .usePlaintext()
            .build();

        // Attach API Key
        Metadata header = new Metadata();
        Metadata.Key<String> key = Metadata.Key.of(
            "TRON-PRO-API-KEY",
            Metadata.ASCII_STRING_MARSHALLER
        );
        header.put(key, apiKey);

        // Create BlockingStub with API Key interceptor
        blockingStub = WalletGrpc.newBlockingStub(channel).withInterceptors(
            MetadataUtils.newAttachHeadersInterceptor(header)
        );
        blockingStubSolidity = WalletSolidityGrpc.newBlockingStub(channelSolidity).withInterceptors(
            MetadataUtils.newAttachHeadersInterceptor(header)
        );

        // Initialize KeyPair for transaction signing
        keyPair = new KeyPair(hexPrivateKey);
    }

    @Override
    public TransactionExtention transfer(String fromAddress, String toAddress, long amount)
        throws IllegalException {
        ByteString rawFrom = parseAddress(fromAddress);
        ByteString rawTo = parseAddress(toAddress);

        TransferContract transferContract = TransferContract.newBuilder()
            .setOwnerAddress(rawFrom)
            .setToAddress(rawTo)
            .setAmount(amount)
            .build();

        return createTransactionExtention(
            transferContract,
            Transaction.Contract.ContractType.TransferContract
        );
    }

    @Override
    public Transaction signTransaction(TransactionExtention txnExt, KeyPair keyPair) {
        byte[] txId = txnExt.getTxid().toByteArray();
        byte[] signature = KeyPair.signTransaction(txId, keyPair);
        return txnExt
            .getTransaction()
            .toBuilder()
            .addSignature(ByteString.copyFrom(signature))
            .build();
    }

    @Override
    public String broadcastTransaction(Transaction txn) throws RuntimeException {
        Response.TransactionReturn ret = blockingStub.broadcastTransaction(txn);
        if (!ret.getResult()) {
            String errorMessage = new String(ret.getMessage().toByteArray());
            String message = resolveResultCode(ret.getCodeValue()) + ", " + errorMessage;
            throw new RuntimeException(message);
        } else {
            byte[] txId = calculateTransactionHash(txn);
            return ByteArray.toHexString(txId);
        }
    }

    public void close() {
        channel.shutdown();
        channelSolidity.shutdown();
    }
}
```

## 4. Using Trident-java

Manually calling gRPC interfaces can be quite cumbersome in actual development. Trident is an official Java SDK provided by TRON, which has encapsulated most of the gRPC call work, including client construction, message serialization and deserialization, and complex operations like transaction signing and broadcasting. If you want to interact with TRON more conveniently, you can directly refer to or use Trident for gRPC calls.

## 5. Related References and Documentation

* **TRON Protocol Buffers Definitions:**
  [https://github.com/tronprotocol/protocol](https://github.com/tronprotocol/protocol)
* **gRPC Java Official Documentation:**
  [https://grpc.io/docs/languages/java/](https://grpc.io/docs/languages/java/)
* **Protocol Buffers Official Documentation:**
  [https://developers.google.com/protocol-buffers](https://developers.google.com/protocol-buffers)
* **TronGrid Official Website (Get API Key):**
  [https://www.trongrid.io/](https://www.trongrid.io/)
* **Trident GitHub Repository:**
  [https://github.com/tronprotocol/trident/](https://github.com/tronprotocol/trident/)
* **Trident Documentation:**
  [https://tronprotocol.github.io/trident/](https://tronprotocol.github.io/trident/)

## API Categories

- [Account Management](account-management/getaccount.md) - Account query, balance, and multi-signature verification
- [Assets and Tokens](assets-and-tokens/createassetissue.md) - TRC-10 asset issuance, transfer, and queries
- [Block Operations](block-operations/getblock.md) - Block query by number, ID, and range
- [Network Information](network-information/getbandwidthprices.md) - Node info, chain parameters, and pricing
- [Resource Management](resource-management/cancelallunfreezev2.md) - Energy, bandwidth, staking, and delegation
- [Smart Contracts](smart-contracts/clearcontractabi.md) - Contract deployment, triggering, and queries
- [Transaction Operations](transaction-operations/getpendingsize.md) - Transaction query and pending pool
- [Wallet Operations](wallet-operations/accountpermissionupdate.md) - Account creation, transfers, and broadcasting
- [Witness and Governance](witness-and-governance/createwitness.md) - Witness management, voting, proposals, and rewards

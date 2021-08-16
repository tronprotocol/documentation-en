# The TRON FAQ

<!-- markdownlint-disable MD026 -->

[TOC]

## Network Design and Protocol

### How can I generate an account?

You can use [wallet-cli](https://github.com/tronprotocol/wallet-cli) or [Tronscan](https://tronscan.org/#/wallet/new).

### What is the network flow?

Network flow depends on transaction volume. As a reference, the average size of a transaction currently is 200 bytes.

### After you create a token, how to change its status from 'not started yet' to 'participate'?

You need to wait till the time reaches the start time of participation you set when create a token. After a token is created, only the token url and description can be modified.

### Is there a place to see if all the SuperNodes are producing blocks?

Please refer to [Tronscan](https://tronscan.org/#/sr/representatives)

### Is the block producing time interval always remain the same?

The current block producing time interval is 3 seconds. In the future, it may be improved to 1 second.

### Will the block producing reward reduce half?

No.

### If one of the top 27 SuperNodes goes wrong, will it be removed from the SRs list?

If people stop voting for it, it will drop out of the top 27 SRs.

### Is there a threshold to become a SR?

When the amount of votes you get ranks into top 27, you will become a SR.

### 27 SRs shares the block producing reward equally or by their computing power?

It has nothing to do with computing power. The reward is a fixed 32 TRX for each block produced.

### Will there be an over 50% computing power issue in TRON network?

No.

### Will voting burns TRX?

No.

### How long does SR's power last?

Every 6 hours, the votes will be counted to check the qualifications of all the SRs.

### What is the proof of a transaction？

Transaction hash.

### Why I Can't stake TRX longer than 3 days

Staked duration must be 3 days now. It means you can not unstake until the 3 days duration expires. If you don't unstake after 3 days, the staked TRX will remain in staked status until you unstake it.

### How to watch my account for transactions

To meet your needs, you can use TRON event subscription plugin. For more detail, please refer to [https://tronprotocol.github.io/documentation-en/architecture/plugin/#tron-event-subscription](https://tronprotocol.github.io/documentation-en/architecture/plugin/#tron-event-subscription)

### How to calculate the transaction fee?

please refer to [https://tronprotocol.github.io/documentation-en/mechanism-algorithm/resource/](https://tronprotocol.github.io/documentation-en/mechanism-algorithm/resource/)

### How to calculate the number of bytes of transactions?

tx-size  = grpcClient.getTransactionById(txId).get().getSerializedSize() + 60

### How to reset my vote?

You need to vote again, set your votes number to 0.

## Node Configuration

### If I replace the field value of 'genesis.block.witnesses' with the address generated in [Tronscan](https://tronscan.org/) in config.conf, do I need to delete other addresses? Do I need to delete the field 'url' and 'voteCount'?

No need to delete other addresses, these addresses will be a part of your net, but if you do not own the private keys of these addresses, they will act like abandoned addresses.
Note: The addresses of Zion、Sun and Blackhole can not be deleted, but can be modified.

### How can I specify the data storage path when start a node?

You can add the data storage path when you start the node, like:

```text
java -jar FullNode.jar -c config.conf -d /data/output
```

### Is there any config file option, which I can use for sending logs to stdout?

Steps to send logs to stdout:

Download [https://github.com/tronprotocol/java-tron/blob/develop/src/main/resources/logback.xml](https://github.com/tronprotocol/java-tron/blob/develop/src/main/resources/logback.xml)

Uncomment the configuration:

appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender"

Go to the configuration: root level="INFO"
uncomment the configuration: appender-ref ref="STDOUT"
comment the configuration: appender-ref ref="ASYNC"

Move logback.xml to the same directory with FullNode.jar

Launch FullNode.jar with additional parameter: --log-config logback.xml, for example:

```text
java -jar FullNode.jar --log-config logback.xml
```

### How to change log level

The log level is defined in logback.xml. Please set the root level to "ERROR" if you want to filter only error logs. Please refer to the configuration below.

```xml
<root level="ERROR">
    <!--<appender-ref ref="STDOUT"/>-->
    <appender-ref ref="ASYNC"/>
  </root>

  <logger name="app" level="ERROR"/>
  <logger name="net" level="ERROR"/>
  <logger name="backup" level="ERROR"/>
  <logger name="discover" level="ERROR"/>
  <logger name="crypto" level="ERROR"/>
  <logger name="utils" level="ERROR"/>
  <logger name="actuator" level="ERROR"/>
  <logger name="API" level="ERROR"/>
  <logger name="witness" level="ERROR"/>
  <logger name="DB" level="ERROR"/>
  <logger name="capsule" level="ERROR"/>
  <logger name="VM" level="ERROR"/>
```

### How can I get asset from private net?

In private network, you can set the initial account balance in config file. Please refer to below settings:

```text
genesis.block = {
  # Reserve balance
  assets = [
    {
      accountName = "TestA"
      accountType = "AssetIssue"
      address = "THRR7uvFbRLfNzpKPXEyQa8KCJqi59V59e"
      balance = "1000000000000000"
    },
    {
      accountName = "TestB"
      accountType = "AssetIssue"
      address = "TBLZaw93rsnLJ1SWTvoPkr7GVg5ixn2Jv1"
      balance = "1000000000000000"
    },
    {
      accountName = "TestC"
      accountType = "AssetIssue"
      address = "TJg8yZ4Co8RXsHmTWissmSL1VpL7dCybY1"
      balance = "1000000000000000"
    }
  ]
```

## Compile and Build

### java-tron build failed with unit test issue

Please use './gradlew build -x test' to skip the test cases.

## Deployment

### How to test if the deployment works normally, if there is a test api or command like redis: get ping return pong?

Java-tron does not provide a default api to test. Once the service start, grpc commands can be sent. Based on that, there are several ways to test if the deployment is successful. You can also use the following command to test:

```text
> tail -f logs/tron.log |grep "MyheadBlockNumber"
```

### When to deploy private environment, what's the relationship of SuperNode and FullNode? Should I firstly deploy a SuperNode, and then deploy a FullNode？

Under private environment, there should be at least one SuperNode, there is no amount limit for FullNode.

### How to know wether my test SuperNode is running or not?

Using the following command

```text
> tail -f logs/tron.log |grep "Try Produce Block"
```

### Can SolidityNode and FullNode be deployed in one machine? Will they share the data?

They can be deployed in one machine. You can specify the data storage path in configuration file `db.directory = "database"，index.directory = "index"`. You can run FullNode.jar and SolidityNode.jar in different paths to separate the data and log. Remember to change the port in `config.conf`, because two nodes can not work using the same port. SolidityNode is deprecated. Now a FullNode supports all RPCs of a SolidityNode. New developers should deploy FullNode only.

## Running a Node

### As under private environment, why the log keeps updating with all other public nodes? What's the difference of private and public environment？

If it is related to ip list: You need to update 'seed.ip' in config.conf, if it is the same as your public ip, and your computer is connected to the internet, it will try to connect other nodes, even if it fails to connect, the ip list will be stored into DB. If it is related to block and transaction: Under private environment, you need to modify the p2p version and parent hash. If they are the same as MainNet or TestNet, and the computer is connected to internet, the node will sync data from public node.

### Under private environment, should I submit application information to TRON to become a SR?

Under private environment, no need to submit application information to TRON to become a SR.

Ask：Which service port should be public to public network?

Default port 18888, 50051

### At the worst scenario, if the SuperNode can not be connected, the maximum time it allows the SuperNode to recover its service？

The internet connection recovery time only depends on the recovery of SuperNode itself, has nothing to do with internet situation.

### Does SolidityNode sync data from FullNode?

Yes.

### Does a node have wallet function?

No, but the node provides wallet rpc api.

### Why does the block process time take so long?

Java-tron need more RAM to process transactions.

## Test Net

### We want to test our SuperNode's performance under test environment, do we need to be voted to become a SR under test environment?

Yes. Under test environment, we can vote you to become SR.

### What is the defferent between Shasta and Test Net?

to be answered

### Where can I get the test TRX?

[http://testnet.tronex.io/join/getJoinPage](http://testnet.tronex.io/join/getJoinPage)

## Smart Contract


## RPC Client and API

### How to sign transaction from offline node and broadcast to online node?

You can use [tronweb](https://developers.tron.network/docs/api-sign-flow)

### How to sync wallet-cli with wallet on Tronscan?

By using wallet-cli api 'ImportWallet'.

### Is gateway connected to SolidityNode？

Gateway can connect to SolidityNode and FullNode.

### What is the different between 'getTransactionById' and 'getTransactionInfoById'?

The data they return is from different data modules. 'getTransactionById' focuses on general transaction data, while 'getTransactionInfoById' focuses on transaction fee data.

### How to broadcast raw transaction？

You can use 'wallet/broadcasthex'.

### How to get token balance of an account?

You can use the following wallet-cli api:

```text
triggercontract contractaddress balanceOf(address) "youraddress" false 0 0 0 #
```

## Error Log

### What does the following error message mean?

```text
17:02:42.699 INFO [o.t.c.s.WitnessService] Try Produce Block
17:02:42.699 INFO [o.t.c.s.WitnessService] Not sync
```

This message means your node does not sync with the network. Before producing blocks, it needs to sync data. You can use the following command to chek the block height.

```text
> tail -f logs/tron.log |grep "MyheadBlockNumber"
```

## Other Questions

## My Question is Not Listed Here?

Feel free to join our community, just open an Issue on github:

- Github: [tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)

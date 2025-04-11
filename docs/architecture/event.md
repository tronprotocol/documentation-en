# Event Subscription

## Using Event Plugin for Event Subscription

### TIP

The TIP: [TIP-12:TRON event subscribes model](https://github.com/tronprotocol/tips/blob/master/tip-12.md) .

### Event Type

TRON Event Subscription supports 4 types of event:

#### Transaction Event

The parameters passed to Subscriber:

```
transactionId: transaction hash
blockHash: block hash
blockNumber: block number
energyUsage: energy usage
energyFee: energy fee
originEnergyUsage: origin energy usage
energyUsageTotal: total energy usage total
```

#### Block Event

The parameters passed to Subscriber:

```
blockHash: block hash
blockNumber: block number
transactionSize: the number of transactions in a block
latestSolidifiedBlockNumber: the latest solidified block number
transactionList: the transactions hash list
```

#### Contract Event

The parameters passed to Subscriber:

```
transactionId: transaction id
contractAddress: contract address
callerAddress: contract caller address
blockNumber: the number of the block contract related events recorded
blockTimestamp: the block time stamp
eventSignature: event signature
topicMap: the map of topic in solidity language
data: the data information in solidity language
removed: 'true' means the log is removed
```

#### Contract Log Event

The parameters passed to Subscriber:

```
transactionId: transaction hash
contractAddress: contract address
callerAddress: contract caller address
blockNumber: the number of the block contract related events recorded
blockTimestamp: the block time stamp
contractTopics: the list of topic in solidity language
data: the data information in solidity language
removed: 'true' means the log is removed
```

Contract Event and Contract Log Even support event filter function which includes:

```
fromBlock: the start block number
toBlock: the end block number
contractAddress: contract addresses list
contractTopics: contract topics list
```

!!! note
    1. Historical data query is not supported.
    2. When subscribing to non-solidified events, be sure to use the two parameters `blockNumber` and `blockHash` as the criteria to verify that the received events are valid. In special cases such as unstable network connections causing chain reorg, event reorg may occur as well, resulting in stale events.

### New Features

1. Supporting event plug-ins, kafka & mongodb plug-ins have been released, developers can also customize their own plug-ins according to their own needs.
2. Supporting subscription of chain data, such as block, transaction, contract log, contract event and so on. For transaction events, developers can get information such as internal transactions, contract info and so on; for contract events, developers could configure the contract addresses list or contract topic list to receive the specified events, and event subscription has a very low latency. The deployed fullnode can receive event information immediately after the contract is executed.
3. Event query service tron-eventquery, online Event query service provided. Developers can query trigger information in the last seven days through https, and the query address is [https://api.tronex.io](https://api.tronex.io).

### Github projects

- [tronprotocol/event-plugin](https://github.com/tronprotocol/event-plugin)
- [tronprotocol/tron-eventquery](https://github.com/tronprotocol/tron-eventquery)

#### Event plugin

- [Kafka deployment](../developers/deployment.md#kafka)
- [MongoDB deployment](../developers/deployment.md#mongo)

#### Event query

TRON Event Query Service

TronEventQuery is implemented with Tron's new event subscribe model. It uses same query interface with Tron-Grid. Users can also subscribe block trigger, transaction trigger, contract log trigger, and contract event trigger. TronEvent is independent of a particular branch of java-tron, the new event subscribes model will be released on version 3.5 of java-tron.

For more information of TRON event subscribe model, please refer to [TIP-12](https://github.com/tronprotocol/TIPs/issues/12).

- [Event query deployment](https://tronprotocol.github.io/documentation-en/developers/deployment/#event-subscribe-plugin-deployment)
- [Event query HTTP API](https://github.com/tronprotocol/documentation-en/tree/master/docs_without_index/plugin/event-query-http.md)


## Using java-tron's Built-in Message Queue for Event Subscription

TRON provides event subscription service. Developers can not only obtain on-chain events through event plugin, but also through [java-tron’s built-in ZeroMQ message queue](https://github.com/tronprotocol/tips/blob/master/tip-28.md). The difference is that event plugin needs to be additionally deployed, which is used to implement event storage: developers can choose appropriate storage tools according to their needs, such as MongoDB, Kafka, etc., and the plugin help complete the storage of subscribed events. java-tron's built-in ZeroMQ does not require additional deployment operations. Event subscribers can directly connect to the publisher's ip and port, set subscription topics, and receive subscribed events. However, this method does not provide event storage. Therefore, when developers want to subscribe to events directly from nodes for a short period of time, then using the built-in message queue will be a more appropriate choice.

This article will introduce how to subscribe to events through java-tron's built-in message queue in detail.


### Configure node
To use the built-in ZeroMQ of the node for event subscription, you need to set the configuration item `useNativeQueue` to `true` in the node configuration file.

```
event.subscribe = {
  native = {
    useNativeQueue = true // if true, use native message queue, else use event plugin.
    bindport = 5555 // bind port
    sendqueuelength = 1000 //max length of send queue
  }

  ......
 
  topics = [
    {
      triggerName = "block" // block trigger, the value can't be modified
      enable = true
      topic = "block" // plugin topic, the value could be modified
    },
    ......
  ]
}
```

* `native.useNativeQueue`: `true` is to use the built-in message queue, `false` is to use the event plugin
* `native.bindport`: ZeroMQ publisher binding port. In this example, it is `5555`, so the publisher address that the subscriber should connect to is `"tcp://127.0.0.1:5555"` 
* `native.sendqueuelength`: The length of the send queue, that is, when the subscriber receives messages slowly, the maximum number of messages published by the publisher that the TCP buffer can hold. if it exceeds, The message will be discarded if exceeds the capacity
* `topics`: Subscribed [event type](#event-type) , including block type, transaction type, etc.

### Start node
The event subscription service is disabled by default and needs to be enabled by adding the command line parameter `--es`. The start command of the node that enables the event subscription service is as follows:
```
$ java -jar FullNode.jar --es
```

### Prepare event subscription script
This article takes Nodejs as an example to illustrate how to subscribe to events.

First, install the zeromq library:
```
$ npm install zeromq@5
```
Then, write the subscriber code:
```
// subscriber.js
var zmq = require("zeromq"),
var sock = zmq.socket("sub");

sock.connect("tcp://127.0.0.1:5555");
sock.subscribe("block");
console.log("Subscriber connected to port 5555");

sock.on("message", function(topic, message) {
  console.log(
    "received a message related to:",
    Buffer.from(topic).toString(),
    ", containing message:",
    Buffer.from(message).toString()
  );
});
```
This example connects the subscriber to the node event publisher and subscribes to `block` events.

### Start subscriber
Start command of Nodejs is as below:

```
$ node subscriber.js

> Subscriber connected to port 5555
```
When the node has a new block, the subscriber will receive block event, the output information is as follows:
```
received a message related to: blockTrigger, containing message: {"timeStamp":1678343709000,"triggerName":"blockTrigger","blockNumber":1361,"blockHash":"00000000000005519b3995cd638753a862c812d1bda11de14bbfaa5ad3383280","transactionSize":0,"latestSolidifiedBlockNumber":1361,"transactionList":[]}
received a message related to: blockTrigger, containing message: {"timeStamp":1678343712000,"triggerName":"blockTrigger","blockNumber":1362,"blockHash":"0000000000000552d53d1bdd9929e4533a983f14df8931ee9b3bf6d6c74a47b0","transactionSize":0,"latestSolidifiedBlockNumber":1362,"transactionList":[]}
```

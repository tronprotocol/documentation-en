# Event Subscription with Built-in Message Queue

TRON provides flexible event subscription features, allowing developers to either obtain on-chain events via **event plugins** or implement lightweight subscriptions using java-tron's built-in **ZeroMQ message queue**.

The core differences between the two methods are:

  * **Event Plugins** require separate deployment and are suitable for pushing events to external systems (like MongoDB or Kafka) for persistence, analysis, or asynchronous processing.
  * **ZeroMQ Message Queue** is a built-in implementation in java-tron that requires no additional deployment. An event subscriber simply needs to connect to the node's publishing port and configure the subscription topics to receive events in real-time. However, this method does not support event persistence and is only suitable for short-term listening and immediate processing scenarios.

Therefore, when you want to connect to an event stream quickly and at a minimal cost without relying on persistence capabilities, using the **built-in ZeroMQ message queue** is a more lightweight and direct choice. This guide explains how to subscribe to events using this method.

### Configuring the Node

To enable event subscriptions via java-tron's built-in ZeroMQ, you must enable the feature in the node's configuration file.

```
event.subscribe = {
  native = {
    useNativeQueue = true  
    bindport = 5555  
    sendqueuelength = 1000  
  }

  ......
 
  topics = [
    {
      triggerName = "block"  
      enable = true
      topic = "block"  
    },
    ......
  ]
}
```

  * `native.useNativeQueue`: `true` to use the built-in message queue, `false` to use event plugins.
  * `native.bindport`: The port that the ZeroMQ publisher binds to. In this example, it is `5555`, so the subscriber should connect to the publisher address `"tcp://127.0.0.1:5555"`.
  * `native.sendqueuelength`: The length of the send queue. This is the maximum number of messages the TCP buffer can hold if the subscriber is slow to receive them. Messages published beyond this limit will be discarded.
  * `topics`: The subscribed [Event Types](../event/#event-types), such as block types, transaction types, etc.

### Starting the Node

The event subscription service is disabled by default and must be enabled using the `--es` command-line argument. The startup command for a node with event subscription enabled is as follows:

```
$ java -jar FullNode.jar --es
```

### Preparing the Event Subscription Script

This guide uses Node.js as an example to demonstrate how to subscribe to events.

First, install the `ZeroMQ` library:

```
$ npm install zeromq@5
```

Next, write the subscriber code:

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

This example connects the subscriber to the node's event publisher and subscribes to `block` events.

### Starting the Subscriber

The Node.js startup command is as follows:

```
$ node subscriber.js

> Subscriber connected to port 5555
```

When the node produces a new block, the subscriber will receive the block event, and the output will look like this:

```
received a message related to: block, containing message: {"timeStamp":1678343709000,"triggerName":"blockTrigger","blockNumber":1361,"blockHash":"00000000000005519b3995cd638753a862c812d1bda11de14bbfaa5ad3383280","transactionSize":0,"latestSolidifiedBlockNumber":1361,"transactionList":[]}
received a message related to: block, containing message: {"timeStamp":1678343712000,"triggerName":"blockTrigger","blockNumber":1362,"blockHash":"0000000000000552d53d1bdd9929e4533a983f14df8931ee9b3bf6d6c74a47b0","transactionSize":0,"latestSolidifiedBlockNumber":1362,"transactionList":[]}
```
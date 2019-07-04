
## FullNode model Question under Private Environment

**Ask: If I replace the field value of 'genesis.block.witnesses' with the address generated in [Tronscan](https://tronscan.org/) in config.conf, do I need to delete other addresses? Do I need to delete the field 'url' and 'voteCount'?**    

Answer: No need to delete other addresses, these addresses will be a part of your net, but if you do not own the private keys of these addresses, they will act like abandoned addresses.   
Note: The addresses of Zion、Sun and Blackhole can not be deleted, but can be modified.  
    
**Ask: After you replace the value of 'seed.node > ip.list' with your own public ip, and then using  `java -jar java-tron.jar` to start. How to test if the deployment works normally, if there is a test api or command like redis: get ping return pong?**

Answer: Java-tron does not provide a default api to test. Once the service start, grpc commands can be sent. Based on that, there are several ways to test if the deployment is successful. First of all, you need to confirm the grpc port is on:
              
```text             
- netstat -tulnp| grep 50051 
      
![](https://raw.githubusercontent.com/tronprotocol/Documentation/master/images/FAQ/查询节点.png)
      
If your grpc port is on, you can use tronscan to test node connection, make sure the port and ip are open to public.  
      
You can also use the following command to test:  
              
- tail -f logs/tron.log |grep "MyheadBlockNumber"
```

## SuperNode model Question under Private Environment  

**Ask: When to deploy private environment, what's the relationship of SuperNode and FullNode? Should I firstly deploy a SuperNode, and then deploy a FullNode？**  

Answer: Under private environment, there should be at least one SuperNode, there is no amount limit for FullNode.  

**Ask: Under private environment, should I submit application information to TRON to become a SR?**

Answer: Under private environment, no need to submit application information to TRON to become a SR.  

**Ask: As under private environment, why the log keeps updating with all other public nodes? What's the difference of private and public environment？**

Answer: If it is related to ip list: You need to update 'seed.ip' in config.conf, if it is the same as your public ip, and your computer is connected to the internet, it will try to connect other nodes, even if it fails to connect, the ip list will be stored into DB. If it is related to block and transaction: Under private environment, you need to modify the p2p version and parent hash. If they are the same as MainNet or TestNet, and the computer is connected to internet, the node will sync data from public node.  
   
## Questions under Public Environment

**Ask: The maximum RAM and CPU consumption of one java-tron application？**

Answer: This depends on your computer system environment, if it is 32-bit system, the maximum heap memory is 32GB. If it is 64-bit system, heap memory will be constrained by operation system. Under private environment 4 cores cpu maybe enough for small amount of transactions. In public network, to be a SR, we recommend to use 64 cores CPU.   

**Ask：Which service port should be public to public network?**

Answer: Default port 18888, 50051  

**Ask: What is the network flow?**

Answer: Network flow depends on transaction volume. As a reference, the average size of a transaction currently is 200 bytes.  

**Ask: After you create a token, how to change its status from 'not started yet' to 'participate'?**

Answer: You need to wait till the time reaches the start time of participation you set when create a token. After a token is created, only the token url and description can be modified.  


## Error while Running SuperNode

**Ask: What does the following error message mean?**
```text
17:02:42.699 INFO [o.t.c.s.WitnessService] Try Produce Block
17:02:42.699 INFO [o.t.c.s.WitnessService] Not sync
```
Answer: This message means your node does not sync with the network. Before producing blocks, it needs to sync data. You can use the following command to chek the block height.
```text              
- tail -f logs/tron.log |grep "MyheadBlockNumber"
```

## SuperNode Block Producing Questions  

**Ask：Do the SuperNodes take turns to produce blocks? what is the time interval? Will it be delisted from the SuperNodes list if no heartbeat message is detected within 24 hours?**

Answer: They take turns to produce blocks. Every 3 seconds. Each SuperNode's Block missing rate will be counted.   

**Ask: At the worst scenario, if the SuperNode can not be connected, the maximum time it allows the SuperNode to recover its service？**

Answer: The internet connection recovery time only depends on the recovery of SuperNode itself, has nothing to do with internet situation.

**Ask: The formula of calculating the block missing rate?**
   
Answer: The number of the blocks are supposed to produce by each SuperNode but actually not will be counted, the number will be accumulated, will not be reset.  

**Ask: Is the source code of SuperNode open source?**

Answer: Yes. Please refer to [https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)

**Ask: How to know wether my test SuperNode is running or not?**

Answer: Using the following command
```text             
- tail -f logs/tron.log |grep "Try Produce Block"
```

**Ask: In addition, according to this command: `java -jar java-tron.jar -p yourself private key --witness -c yourself config.conf(Example：/data/java-tron/config.conf`, How to know whether it is the SuperNode running?**

Answer: Using the following command
```text             
- tail -f logs/tron.log |grep "Try Produce Block"
```

**Ask: How can I generate an account?**

Answer: You can use [Wallet-cli](https://github.com/tronprotocol/wallet-cli) or [Tronscan](https://tronscan.org/#/wallet/new)  

**Ask: We want to test our SuperNode's performance under test environment, do we need to be voted to become a SR under test environment?**

Answer: Yes. Under test environment, we can vote you to become SR.  

**Ask: Is there a place to see if all the SuperNodes are producing blocks?**

Answer: Please refer to [Tronscan](https://tronscan.org/#/sr/representatives)

**Ask: Is the block producing time interval always remain the same?**

Answer: The current block producing time interval is 3 seconds. In the future, it may be improved to 1 second.

**Ask: Will the block producing reward reduce half?**

Answer: No.

**Ask: If one of the top 27 SuperNodes goes wrong, will it be removed from the SRs list?**

Answer: If people stop voting for it, it will drop out of the top 27 SRs.  


## Super Representatives Election Questions
 
**Ask: Why I can see my votes at [Tronscan](https://tronscan.org/#/sr/votes)?**

Answer: The votes will be counted every 6 hours.  

**Ask: How to get the right to vote? How many candidates can one vote be voted to?**
    
Answer: You can get Tron Power(TP) by freezing TRX, 1 TRX equals 1 TP, 1 TP equals 1 vote. One vote can only be voted to one candidate.  

**Ask: In order to vote, do I need to deposit TRX in Tronscan wallet?**

Answer: Yes. Not only Tronscan wallet, you can also use other wallets that support vote feature. The TRX is recorded in the blockchain, not in the wallet.  
   
**Ask: Is there a threshold to become a SR?**  

Answer: When the amount of votes you get ranks into top 27, you will become a SR.  

**Ask: 27 SRs shares the block producing reward equally or by their computing power?**

Answer: It has nothing to do with computing power. The reward is a fixed 32 TRX for each block produced.

**Ask: Will there be an over 50% computing power issue in Tron network?**

Answer: No.
   
**Ask: Will voting burns TRX?**

Answer: No.
    
**Ask: How long does SR's power last?**

Answer: Every 6 hours, the votes will be counted to check the qualifications of all the SRs.  
    
**Ask: My node info is not set in `build/resources/main/config.conf`, can my node be identified by the network?**

Answer: You need to add your private key to `localwitness`.  
   
   
## Other Questions

**Ask: How can I specify the data storage path when start a node?**

Answer: Will do.

**Ask: Does a node have wallet function?**

Answer: The node provides wallet rpc api.  

**Ask: Can SolidityNode and FullNode be deployed in one machine? Will they share the data?**

Answer: They can be deployed in one machine. You can specify the data storage path in configuration file `db.directory = "database"，index.directory = "index"`. You can run FullNode.jar and SolidityNode.jar in different path to separate the data and log. Remember to change the port in config.conf, because two nodes can not work using the same port.   

**Ask: What is the proof of a transaction？**

Answer: Transaction hash.

**Ask: Does SolidityNode sync data from FullNode?**

Answer: Yes.

**Ask: Is gateway connected to SolidityNode？**

Answer: Gateway can connect to SolidityNode and FullNode.

**Ask: What the decimal of TRX?**
    
Answer: 6

**Ask: If the node is deployed in China, is there a firewall issue?**

Answer: 39.106.220.120 locates in Beijing, Others not.  

**Ask: How many types of wallet does Tron have?**

Answer: Wallet-cli, Web wallet, IOS wallet, Android wallet.  

**Ask: Should the internet bandwidth reach 25Gbps, or 10Gbps?**

Answer: We have no requirement on internet bandwidth.  




































 
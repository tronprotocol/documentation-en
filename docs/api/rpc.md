# RPC List

**For the specific definition of API, please refer to the following link:**
[api/api.proto](https://github.com/tronprotocol/protocol/blob/master/api/api.proto)
[core/Contract.proto](https://github.com/tronprotocol/protocol/blob/master/core/Contract.proto).

!!! note
    SolidityNode is deprecated. Now a FullNode supports all RPCs of a SolidityNode. New developers should deploy FullNode only.

**1.&nbsp;Get account information**

```protobuf
rpc GetAccount (Account) returns (Account) {}
```
Nodes: Fullnode and SolidityNode

**2.&nbsp;TRX transfer**

```protobuf
rpc CreateTransaction (TransferContract) returns (Transaction) {}
```
Nodes: Fullnode

**3.&nbsp;Broadcast transaction**

```protobuf
rpc BroadcastTransaction (Transaction) returns (Return) {}
```
Nodes: Fullnode

Description:
Transfer, vote, issuance of token, or participation in token offering. Sending signed transaction information to node, and broadcasting it to the entire network after witness verification.

**4.&nbsp;Create an account**

```protobuf
rpc CreateAccount (AccountCreateContract) returns (Transaction) {}
```
Nodes: FullNode

**5.&nbsp;Account name update**
```protobuf
rpc UpdateAccount (AccountUpdateContract) returns (Transaction) {}
```
Nodes: Fullnode

**6.&nbsp;Vote for super representative candidates**
```protobuf
rpc VoteWitnessAccount (VoteWitnessContract) returns (Transaction) {}
```
Nodes: FullNode

**7.&nbsp;Query the ratio of brokerage of the witness**
```protobuf
rpc GetBrokerageInfo (BytesMessage) returns (NumberMessage) {}
```
Nodes: FullNode

**8.&nbsp;Query unclaimed reward**
```protobuf
rpc GetRewardInfo (BytesMessage) returns (NumberMessage) {}
```
Nodes: FullNode

**9.&nbsp;Update the ratio of brokerage**
```protobuf
rpc UpdateBrokerage (UpdateBrokerageContract) returns (TransactionExtention) {}
```
Nodes: FullNode

**10.&nbsp;Issue a token**
```protobuf
rpc CreateAssetIssue (AssetIssueContract) returns (Transaction) {}
```
Nodes: FullNode

**11.&nbsp;Query of list of super representative candidates**
```protobuf
rpc ListWitnesses (EmptyMessage) returns (WitnessList) {}
```
Nodes: FullNode and SolidityNode

**12.&nbsp;Application for super representative**
```protobuf
rpc CreateWitness (WitnessCreateContract) returns (Transaction) {}
```
Nodes: FullNode

Description:
To apply to become TRON’s Super Representative candidate.

**13.&nbsp;Information update of Super Representative candidates**
```protobuf
rpc UpdateWitness (WitnessUpdateContract) returns (Transaction) {}
```
Nodes: FullNode

Description: Update the website url of the SR.

**14.&nbsp;Token transfer**
```protobuf
rpc TransferAsset (TransferAssetContract) returns (Transaction){}
```
Node: FullNode

**15.&nbsp;Participate a token**
```protobuf
rpc ParticipateAssetIssue (ParticipateAssetIssueContract) returns (Transaction) {}
```
Nodes: FullNode

**16.&nbsp;Query the list of nodes connected to the ip of the api**
```protobuf
rpc ListNodes (EmptyMessage) returns (NodeList) {}
```
Nodes: FullNode and SolidityNode

**17.&nbsp;Query the list of all issued tokens**
```protobuf
rpc GetAssetIssueList (EmptyMessage) returns (AssetIssueList) {}
```
Nodes: FullNode and SolidityNode

**18.&nbsp;Query the token issued by a given account**
```protobuf
rpc GetAssetIssueByAccount (Account) returns (AssetIssueList) {}
```
Nodes: FullNode and SolidityNode

**19.&nbsp;Query the token information by token name**
```protobuf
rpc GetAssetIssueByName (BytesMessage) returns (AssetIssueContract) {}
```
Nodes: FullNode and Soliditynode

**20.&nbsp;Query the list of tokens by timestamp**
```protobuf
rpc GetAssetIssueListByTimestamp (NumberMessage) returns (AssetIssueList){}
```
Nodes: SolidityNode

**21.&nbsp;Get current block information**
```protobuf
rpc GetNowBlock (EmptyMessage) returns (Block) {}
```
Nodes: FullNode and SolidityNode

**22.&nbsp;Get a block by block height**
```protobuf
rpc GetBlockByNum (NumberMessage) returns (Block) {}
```
Nodes: FullNode and SolidityNode

**23.&nbsp;Get the total number of transactions**
```protobuf
rpc TotalTransaction (EmptyMessage) returns (NumberMessage) {}
```
Nodes: FullNode and SolidityNode

**24.&nbsp;Query the transaction by transaction id**
```protobuf
rpc getTransactionById (BytesMessage) returns (Transaction) {}
```
Nodes: SolidityNode

**25.&nbsp;Query the transaction by timestamp**
```protobuf
rpc getTransactionsByTimestamp (TimeMessage) returns (TransactionList) {}
```
Nodes: SolidityNode

**26.&nbsp;Query the transactions initiated by an account**
```protobuf
rpc getTransactionsFromThis (Account) returns (TransactionList) {}
```
Nodes: SolidityNode

**27.&nbsp;Query the transactions received by an account**
```protobuf
rpc getTransactionsToThis (Account) returns (NumberMessage) {}
```
Nodes: SolidityNode

**28.&nbsp;Stake TRX**
This interface has been deprecated, please use FreezeBalanceV2 to stake TRX to obtain resources.
```protobuf
rpc FreezeBalance (FreezeBalanceContract) returns (Transaction) {}
```
Nodes: FullNode

**29.&nbsp;Unstake TRX**
Unstake the TRX staked during Stake1.0.
```protobuf
rpc UnfreezeBalance (UnfreezeBalanceContract) returns (Transaction) {}
```
Nodes: FullNode

**30.&nbsp;Block producing reward redemption**
```protobuf
rpc WithdrawBalance (WithdrawBalanceContract) returns (Transaction) {}
```
Nodes: FullNode

**31.&nbsp;Unstake token balance**
```protobuf
rpc UnfreezeAsset (UnfreezeAssetContract) returns (Transaction) {}
```
Nodes: FullNode

**32.&nbsp;Query the next maintenance time**
```protobuf
rpc GetNextMaintenanceTime (EmptyMessage) returns (NumberMessage) {}
```
Nodes: FullNode

**33.&nbsp;Query the transaction fee & block information**
```protobuf
rpc GetTransactionInfoById (BytesMessage) returns (TransactionInfo) {}
```
Nodes: SolidityNode

**34.&nbsp;Query block information by block id**
```protobuf
rpc GetBlockById (BytesMessage) returns (Block) {}
```
Nodes: FullNode

**35.&nbsp;Update token information**
```protobuf
rpc UpdateAsset (UpdateAssetContract) returns (Transaction) {}
```
Nodes: Fullnode

Description:
Token update can only be initiated by the token issuer to update token description, url, maximum bandwidth consumption by each account and total bandwidth consumption.

**36.&nbsp;Query the list of all the tokens by pagination**
```protobuf
rpc GetPaginatedAssetIssueList (PaginatedMessage) returns (AssetIssueList) {}
```
Nodes: FullNode and SolidityNode



**37.&nbsp;Deploy a smart contract**
```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```
Nodes: FullNode and SolidityNode

**38.&nbsp;Trigger a smart contract**
```protobuf
rpc TriggerContract (TriggerSmartContract) returns (TransactionExtention) {}
```
Nodes: FullNode

**39.&nbsp;Create a shielded transaction**
```protobuf
rpc CreateShieldedTransaction (PrivateParameters) returns (TransactionExtention) {}
```
Nodes: FullNode

**40.&nbsp;Get a Merkle tree information of a note**
```protobuf
rpc GetMerkleTreeVoucherInfo (OutputPointInfo) returns (IncrementalMerkleVoucherInfo) {}
```
Nodes: FullNode

**41.&nbsp;Scan note by ivk**
```protobuf
rpc ScanNoteByIvk (IvkDecryptParameters) returns (DecryptNotes) {}
```
Nodes: FullNode

**42.&nbsp;Scan note by ovk**
```protobuf
rpc ScanNoteByOvk (OvkDecryptParameters) returns (DecryptNotes) {}
```
Nodes: FullNode

**43.&nbsp;Get spending key**
```protobuf
rpc GetSpendingKey (EmptyMessage) returns (BytesMessage) {}
```
Nodes: FullNode

**44.&nbsp;Get expanded spending key**
```protobuf
rpc GetExpandedSpendingKey (BytesMessage) returns (ExpandedSpendingKeyMessage) {}
```
Nodes: FullNode

**45.&nbsp;Get ak from ask**
```protobuf
rpc GetAkFromAsk (BytesMessage) returns (BytesMessage) {}
```
Nodes: FullNode

**46.&nbsp;Get nk from nsk**
```protobuf
rpc GetNkFromNsk (BytesMessage) returns (BytesMessage) {}
```
Nodes: FullNode

**47.&nbsp;Get incoming viewing key**
```protobuf
rpc GetIncomingViewingKey (ViewingKeyMessage) returns (IncomingViewingKeyMessage) {}
```
Nodes: FullNode

**48.&nbsp;Get diversifier**
```protobuf
rpc GetDiversifier (EmptyMessage) returns (DiversifierMessage) {}
```
Nodes: FullNode

**49.&nbsp;Get zen payment address**
```protobuf
rpc GetZenPaymentAddress (IncomingViewingKeyDiversifierMessage) returns (PaymentAddressMessage) {}
```
Nodes: FullNode

**50.&nbsp;Get rcm**
```protobuf
rpc GetRcm (EmptyMessage) returns (BytesMessage) {}
```
Nodes: FullNode

**51.&nbsp;Get a note status of is spent or not**
```protobuf
rpc IsSpend (NoteParameters) returns (SpendResult) {}
```
Nodes: FullNode

**52.&nbsp;Create a shielded transaction without using ask**
```protobuf
rpc CreateShieldedTransactionWithoutSpendAuthSig (PrivateParametersWithoutAsk) returns (TransactionExtention) {}
```
Nodes: FullNode

**53.&nbsp;Create a shielded transaction hash**
```protobuf
rpc GetShieldTransactionHash (Transaction) returns (BytesMessage) {}
```
Nodes: FullNode

**54.&nbsp;Create a signature for a shielded transaction**
```protobuf
rpc CreateSpendAuthSig (SpendAuthSigParameters) returns (BytesMessage) {}
```
Nodes: FullNode

**55.&nbsp;Create a shield nullifier**
```protobuf
rpc CreateShieldNullifier (NfParameters) returns (BytesMessage) {}
```
Nodes: FullNode

**56.&nbsp;Get new shielded address**
```protobuf
rpc GetNewShieldedAddress (EmptyMessage) returns (ShieldedAddressInfo){}
```
Nodes: FullNode

**57.&nbsp;Create shielded contract parameters**
```protobuf
rpc CreateShieldedContractParameters (PrivateShieldedTRC20Parameters) returns (ShieldedTRC20Parameters) {}
```
Nodes: FullNode

**58.&nbsp;Create shielded contract parameters without ask**
```protobuf
rpc CreateShieldedContractParametersWithoutAsk (PrivateShieldedTRC20ParametersWithoutAsk) returns (ShieldedTRC20Parameters) {}
```
Nodes: FullNode

**59.&nbsp;Scan shielded TRC20 notes by ivk**
```protobuf
rpc ScanShieldedTRC20NotesbyIvk (IvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
```
Nodes: FullNode, SolidityNode

**60.&nbsp;Scan shielded TRC20 notes by ovk**
```protobuf
rpc ScanShieldedTRC20NotesbyOvk (OvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
```
Nodes: FullNode, SolidityNode

**61.&nbsp;Get the status of shielded TRC20 note of spent or not**
```protobuf
rpc IsShieldedTRC20ContractNoteSpent (NfTRC20Parameters) returns (NullifierResult) {}
```
Nodes: FullNode, SolidityNode

**62.&nbsp;Get the trigger input for the shielded TRC20**
```protobuf
  rpc GetTriggerInputForShieldedTRC20Contract (ShieldedTRC20TriggerContractParameters) returns (BytesMessage) {}
```
Nodes: FullNode


**63.&nbsp;Create an market order**       
```
rpc MarketSellAsset (MarketSellAssetContract) returns (TransactionExtention) {};
```
Nodes: FullNode
 
**64.&nbsp;Cancel the order**      
```   
rpc MarketCancelOrder (MarketCancelOrderContract) returns (TransactionExtention) {};
```
Nodes: FullNode 

**65.&nbsp;Get all orders for the account**      
```
rpc GetMarketOrderByAccount (BytesMessage) returns (MarketOrderList) {};
```
Nodes: FullNode 

**66.&nbsp;Get all trading pairs**         
```
rpc GetMarketPairList (EmptyMessage) returns (MarketOrderPairList) {};
```
Nodes: FullNode 

**67.&nbsp;Get all orders for the trading pair**       
```
rpc GetMarketOrderListByPair (MarketOrderPair) returns (MarketOrderList) {};
```
Nodes: FullNode 

**68.&nbsp;Get all prices for the trading pair**      
```
rpc GetMarketPriceByPair (MarketOrderPair) returns (MarketPriceList) {};
```
Nodes: FullNode 

**69.&nbsp;Get order by id**      
```
rpc GetMarketOrderById (BytesMessage) returns (MarketOrder) {}; 
```
Nodes: FullNode 

**70.&nbsp;perform a historical balance lookup**      
```
rpc GetAccountBalance (AccountBalanceRequest) returns (AccountBalanceResponse){}; 
```
Nodes: FullNode 

**71.&nbsp;fetch all balance-changing transactions in a block**      
```
rpc GetBlockBalanceTrace (BlockBalanceTrace.BlockIdentifier) returns (BlockBalanceTrace) {}; 
```
Nodes: FullNode 

**72.&nbsp;get the burn trx amount**      
```
rpc GetBurnTrx (EmptyMessage) returns (NumberMessage) {}; 
```
Nodes: FullNode and SolidityNode

**73.&nbsp;Freeze TRX**
```protobuf
rpc FreezeBalanceV2 (FreezeBalanceV2Contract) returns (TransactionExtention) {}
```
Nodes: FullNode

**74.&nbsp;UnFreeze TRX**
```protobuf
rpc UnfreezeBalanceV2 (UnfreezeBalanceV2Contract) returns (TransactionExtention) {}
```
Nodes: FullNode

**75.&nbsp;Withdraw Staked TRX**
```protobuf
rpc WithdrawExpireUnfreeze (WithdrawExpireUnfreezeContract) returns (TransactionExtention) {}
```
Nodes: FullNode

**76.&nbsp;Delegate Resource**
```protobuf
rpc DelegateResource (DelegateResourceContract) returns (TransactionExtention) {}
```
Nodes: FullNode

**77.&nbsp;UnDelegate Resource**
```protobuf
rpc UnDelegateResource (UnDelegateResourceContract) returns (TransactionExtention) {}
```
Nodes: FullNode

**78.&nbsp;Query transaction information in the pending pool**
```
rpc GetTransactionFromPending (BytesMessage) returns (Transaction) {};
```
Nodes: FullNode

**79.&nbsp;Query the pending pool transaction id list**
```
rpc GetTransactionListFromPending (EmptyMessage) returns (TransactionIdList) {};
```
Nodes: FullNode

**80.&nbsp;Query the size of the pending pool**
```
rpc GetPendingSize (EmptyMessage) returns (NumberMessage) {};
Nodes: FullNode
```
**81.&nbsp; Cancel UnFreeze**
```protobuf
rpc CancelAllUnfreezeV2 (CancelAllUnfreezeV2Contract) returns (TransactionExtention) {}
```
Nodes: FullNode

**82.&nbsp; Get bandwidth unit price**
```protobuf
rpc GetBandwidthPrices (EmptyMessage) returns (PricesResponseMessage) {}
```
Nodes: FullNode

**83.&nbsp; Get energy unit price**
```protobuf
rpc GetEnergyPrices (EmptyMessage) returns (PricesResponseMessage) {}
```
Nodes: FullNode

**84.&nbsp; Get transaction memo fee**
```protobuf
rpc GetMemoFee (EmptyMessage) returns (PricesResponseMessage) {}
```
Nodes: FullNodes
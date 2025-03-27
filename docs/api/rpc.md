# RPC List

**For the specific definition of API, please refer to the following link:**
[api/api.proto](https://github.com/tronprotocol/protocol/blob/master/api/api.proto)

!!! note
    SolidityNode is deprecated. Now a FullNode supports all RPCs of a SolidityNode. New developers should deploy FullNode only.

## Get account information

```protobuf
rpc GetAccount (Account) returns (Account) {}
```
Nodes: Fullnode and SolidityNode

## TRX transfer

```protobuf
rpc CreateTransaction (TransferContract) returns (Transaction) {}
```
Nodes: Fullnode

## Broadcast transaction

```protobuf
rpc BroadcastTransaction (Transaction) returns (Return) {}
```
Nodes: Fullnode

Description:
Transfer, vote, issuance of token, or participation in token offering. Sending signed transaction information to node, and broadcasting it to the entire network after super representatives verification.

## Create an account

```protobuf
rpc CreateAccount (AccountCreateContract) returns (Transaction) {}
```
Nodes: FullNode

## Account name update
```protobuf
rpc UpdateAccount (AccountUpdateContract) returns (Transaction) {}
```
Nodes: Fullnode

## Vote for super representative candidates
```protobuf
rpc VoteWitnessAccount (VoteWitnessContract) returns (Transaction) {}
```
Nodes: FullNode

## Query the ratio of brokerage of the super representative
```protobuf
rpc GetBrokerageInfo (BytesMessage) returns (NumberMessage) {}
```
Nodes: FullNode

## Query unclaimed reward
```protobuf
rpc GetRewardInfo (BytesMessage) returns (NumberMessage) {}
```
Nodes: FullNode

## Update the ratio of brokerage
```protobuf
rpc UpdateBrokerage (UpdateBrokerageContract) returns (TransactionExtention) {}
```
Nodes: FullNode

## Issue a token
```protobuf
rpc CreateAssetIssue (AssetIssueContract) returns (Transaction) {}
```
Nodes: FullNode

## Query of list of super representative candidates
```protobuf
rpc ListWitnesses (EmptyMessage) returns (WitnessList) {}
```
Nodes: FullNode and SolidityNode

## Application for super representative
```protobuf
rpc CreateWitness (WitnessCreateContract) returns (Transaction) {}
```
Nodes: FullNode

Description:
To apply to become TRON’s Super Representative candidate.

## Information update of Super Representative candidates
```protobuf
rpc UpdateWitness (WitnessUpdateContract) returns (Transaction) {}
```
Nodes: FullNode

Description: Update the website url of the SR.

## Token transfer
```protobuf
rpc TransferAsset (TransferAssetContract) returns (Transaction){}
```
Node: FullNode

## Participate a token
```protobuf
rpc ParticipateAssetIssue (ParticipateAssetIssueContract) returns (Transaction) {}
```
Nodes: FullNode

## Query the list of nodes connected to the ip of the api
```protobuf
rpc ListNodes (EmptyMessage) returns (NodeList) {}
```
Nodes: FullNode and SolidityNode

## Query the list of all issued tokens
```protobuf
rpc GetAssetIssueList (EmptyMessage) returns (AssetIssueList) {}
```
Nodes: FullNode and SolidityNode

## Query the token issued by a given account
```protobuf
rpc GetAssetIssueByAccount (Account) returns (AssetIssueList) {}
```
Nodes: FullNode and SolidityNode

## Query the token information by token name
```protobuf
rpc GetAssetIssueByName (BytesMessage) returns (AssetIssueContract) {}
```
Nodes: FullNode and Soliditynode

## Query the list of tokens by timestamp
```protobuf
rpc GetAssetIssueListByTimestamp (NumberMessage) returns (AssetIssueList){}
```
Nodes: SolidityNode

## Get current block information
```protobuf
rpc GetNowBlock (EmptyMessage) returns (Block) {}
```
Nodes: FullNode and SolidityNode

## Get a block by block height
```protobuf
rpc GetBlockByNum (NumberMessage) returns (Block) {}
```
Nodes: FullNode and SolidityNode

## Get the total number of transactions
```protobuf
rpc TotalTransaction (EmptyMessage) returns (NumberMessage) {}
```
Nodes: FullNode and SolidityNode

## Query the transaction by transaction id
```protobuf
rpc getTransactionById (BytesMessage) returns (Transaction) {}
```
Nodes: SolidityNode

## Query the transaction by timestamp
```protobuf
rpc getTransactionsByTimestamp (TimeMessage) returns (TransactionList) {}
```
Nodes: SolidityNode

## Stake TRX
This interface has been deprecated, please use FreezeBalanceV2 to stake TRX to obtain resources.
```protobuf
rpc FreezeBalance (FreezeBalanceContract) returns (Transaction) {}
```
Nodes: FullNode

## Unstake TRX
Unstake the TRX staked during Stake1.0.
```protobuf
rpc UnfreezeBalance (UnfreezeBalanceContract) returns (Transaction) {}
```
Nodes: FullNode

## Block producing reward redemption
```protobuf
rpc WithdrawBalance (WithdrawBalanceContract) returns (Transaction) {}
```
Nodes: FullNode

## Unstake token balance
```protobuf
rpc UnfreezeAsset (UnfreezeAssetContract) returns (Transaction) {}
```
Nodes: FullNode

## Query the next maintenance time
```protobuf
rpc GetNextMaintenanceTime (EmptyMessage) returns (NumberMessage) {}
```
Nodes: FullNode

## Query the transaction fee & block information
```protobuf
rpc GetTransactionInfoById (BytesMessage) returns (TransactionInfo) {}
```
Nodes: SolidityNode

## Query block information by block id
```protobuf
rpc GetBlockById (BytesMessage) returns (Block) {}
```
Nodes: FullNode

## Update token information
```protobuf
rpc UpdateAsset (UpdateAssetContract) returns (Transaction) {}
```
Nodes: Fullnode

Description:
Token update can only be initiated by the token issuer to update token description, url, maximum bandwidth consumption by each account and total bandwidth consumption.

## Query the list of all the tokens by pagination
```protobuf
rpc GetPaginatedAssetIssueList (PaginatedMessage) returns (AssetIssueList) {}
```
Nodes: FullNode and SolidityNode


## Deploy a smart contract
```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```
Nodes: FullNode and SolidityNode

## Trigger a smart contract
```protobuf
rpc TriggerContract (TriggerSmartContract) returns (TransactionExtention) {}
```
Nodes: FullNode

## Create a shielded transaction
```protobuf
rpc CreateShieldedTransaction (PrivateParameters) returns (TransactionExtention) {}
```
Nodes: FullNode

## Get a Merkle tree information of a note
```protobuf
rpc GetMerkleTreeVoucherInfo (OutputPointInfo) returns (IncrementalMerkleVoucherInfo) {}
```
Nodes: FullNode

## Scan note by ivk
```protobuf
rpc ScanNoteByIvk (IvkDecryptParameters) returns (DecryptNotes) {}
```
Nodes: FullNode

## Scan note by ovk
```protobuf
rpc ScanNoteByOvk (OvkDecryptParameters) returns (DecryptNotes) {}
```
Nodes: FullNode

## Get spending key
```protobuf
rpc GetSpendingKey (EmptyMessage) returns (BytesMessage) {}
```
Nodes: FullNode

## Get expanded spending key  
```protobuf
rpc GetExpandedSpendingKey (BytesMessage) returns (ExpandedSpendingKeyMessage) {}
```
Nodes: FullNode

## Get ak from ask
```protobuf
rpc GetAkFromAsk (BytesMessage) returns (BytesMessage) {}
```
Nodes: FullNode

## Get nk from nsk
```protobuf
rpc GetNkFromNsk (BytesMessage) returns (BytesMessage) {}
```
Nodes: FullNode

## Get incoming viewing key
```protobuf
rpc GetIncomingViewingKey (ViewingKeyMessage) returns (IncomingViewingKeyMessage) {}
```
Nodes: FullNode

## Get diversifier
```protobuf
rpc GetDiversifier (EmptyMessage) returns (DiversifierMessage) {}
```
Nodes: FullNode

## Get zen payment address
```protobuf
rpc GetZenPaymentAddress (IncomingViewingKeyDiversifierMessage) returns (PaymentAddressMessage) {}
```
Nodes: FullNode

## Get rcm
```protobuf
rpc GetRcm (EmptyMessage) returns (BytesMessage) {}
```
Nodes: FullNode

## Get a note status of is spent or not
```protobuf
rpc IsSpend (NoteParameters) returns (SpendResult) {}
```
Nodes: FullNode

## Create a shielded transaction without using ask
```protobuf
rpc CreateShieldedTransactionWithoutSpendAuthSig (PrivateParametersWithoutAsk) returns (TransactionExtention) {}
```
Nodes: FullNode

## Create a shielded transaction hash
```protobuf
rpc GetShieldTransactionHash (Transaction) returns (BytesMessage) {}
```
Nodes: FullNode

## Create a signature for a shielded transaction
```protobuf
rpc CreateSpendAuthSig (SpendAuthSigParameters) returns (BytesMessage) {}
```
Nodes: FullNode

## Create a shield nullifier
```protobuf
rpc CreateShieldNullifier (NfParameters) returns (BytesMessage) {}
```
Nodes: FullNode

## Get new shielded address
```protobuf
rpc GetNewShieldedAddress (EmptyMessage) returns (ShieldedAddressInfo){}
```
Nodes: FullNode

## Create shielded contract parameters
```protobuf
rpc CreateShieldedContractParameters (PrivateShieldedTRC20Parameters) returns (ShieldedTRC20Parameters) {}
```
Nodes: FullNode

## Create shielded contract parameters without ask
```protobuf
rpc CreateShieldedContractParametersWithoutAsk (PrivateShieldedTRC20ParametersWithoutAsk) returns (ShieldedTRC20Parameters) {}
```
Nodes: FullNode

## Scan shielded TRC20 notes by ivk
```protobuf
rpc ScanShieldedTRC20NotesbyIvk (IvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
```
Nodes: FullNode, SolidityNode

## Scan shielded TRC20 notes by ovk
```protobuf
rpc ScanShieldedTRC20NotesbyOvk (OvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
```
Nodes: FullNode, SolidityNode

## Get the status of shielded TRC20 note of spent or not
```protobuf
rpc IsShieldedTRC20ContractNoteSpent (NfTRC20Parameters) returns (NullifierResult) {}
```
Nodes: FullNode, SolidityNode

## Get the trigger input for the shielded TRC20
```protobuf
  rpc GetTriggerInputForShieldedTRC20Contract (ShieldedTRC20TriggerContractParameters) returns (BytesMessage) {}
```
Nodes: FullNode


## Create an market order       
```
rpc MarketSellAsset (MarketSellAssetContract) returns (TransactionExtention) {};
```
Nodes: FullNode
 
## Cancel the order      
```   
rpc MarketCancelOrder (MarketCancelOrderContract) returns (TransactionExtention) {};
```
Nodes: FullNode 

## Get all orders for the account      
```
rpc GetMarketOrderByAccount (BytesMessage) returns (MarketOrderList) {};
```
Nodes: FullNode 

## Get all trading pairs         
```
rpc GetMarketPairList (EmptyMessage) returns (MarketOrderPairList) {};
```
Nodes: FullNode 

## Get all orders for the trading pair       
```
rpc GetMarketOrderListByPair (MarketOrderPair) returns (MarketOrderList) {};
```
Nodes: FullNode 

## Get all prices for the trading pair      
```
rpc GetMarketPriceByPair (MarketOrderPair) returns (MarketPriceList) {};
```
Nodes: FullNode 

## Get order by id      
```
rpc GetMarketOrderById (BytesMessage) returns (MarketOrder) {}; 
```
Nodes: FullNode 

## perform a historical balance lookup      
```
rpc GetAccountBalance (AccountBalanceRequest) returns (AccountBalanceResponse){}; 
```
Nodes: FullNode 

## fetch all balance-changing transactions in a block      
```
rpc GetBlockBalanceTrace (BlockBalanceTrace.BlockIdentifier) returns (BlockBalanceTrace) {}; 
```
Nodes: FullNode 

## get the burn trx amount      
```
rpc GetBurnTrx (EmptyMessage) returns (NumberMessage) {}; 
```
Nodes: FullNode and SolidityNode

## Freeze TRX
```protobuf
rpc FreezeBalanceV2 (FreezeBalanceV2Contract) returns (TransactionExtention) {}
```
Nodes: FullNode

## UnFreeze TRX
```protobuf
rpc UnfreezeBalanceV2 (UnfreezeBalanceV2Contract) returns (TransactionExtention) {}
```
Nodes: FullNode

## Withdraw Staked TRX
```protobuf
rpc WithdrawExpireUnfreeze (WithdrawExpireUnfreezeContract) returns (TransactionExtention) {}
```
Nodes: FullNode

## Delegate Resource
```protobuf
rpc DelegateResource (DelegateResourceContract) returns (TransactionExtention) {}
```
Nodes: FullNode

## UnDelegate Resource
```protobuf
rpc UnDelegateResource (UnDelegateResourceContract) returns (TransactionExtention) {}
```
Nodes: FullNode

## Query transaction information in the pending pool
```
rpc GetTransactionFromPending (BytesMessage) returns (Transaction) {};
```
Nodes: FullNode

## Query the pending pool transaction id list
```
rpc GetTransactionListFromPending (EmptyMessage) returns (TransactionIdList) {};
```
Nodes: FullNode

## Query the size of the pending pool
```
rpc GetPendingSize (EmptyMessage) returns (NumberMessage) {};
Nodes: FullNode
```

##  Cancel UnFreeze
```protobuf
rpc CancelAllUnfreezeV2 (CancelAllUnfreezeV2Contract) returns (TransactionExtention) {}
```
Nodes: FullNode

##  Get bandwidth unit price
```protobuf
rpc GetBandwidthPrices (EmptyMessage) returns (PricesResponseMessage) {}
```
Nodes: FullNode

##  Get energy unit price
```protobuf
rpc GetEnergyPrices (EmptyMessage) returns (PricesResponseMessage) {}
```
Nodes: FullNode

##  Get transaction memo fee
```protobuf
rpc GetMemoFee (EmptyMessage) returns (PricesResponseMessage) {}
```
Nodes: FullNodes

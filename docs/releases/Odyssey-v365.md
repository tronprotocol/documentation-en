# Odyssey-v3.6.5
Odyssey v3.6.5 Update includes the following new features and improvements   

## 1. New delegation mechanism  

The new delegation mechanism enables SRs to set commission rates by themselves, which will serve as a reference for users when they vote for SRs. Meanwhile, traceability of the SR’s commission rate on the chain makes the amount of rewards that users receive through voting more transparent. Moreover, the new delegation mechanism lays a foundation for more complex consensus mechanisms and incentive schemes in the near future. 

## 2. Fairer and more efficient staking rewards mechanism
    
Staking rewards are now distributed in a fully-decentralized way, a step forward from the old partially-decentralized mechanism. With this change, staking rewards are now distributed entirely through the blockchain, ensuring complete supervision from the chain and thus true decentralization. Moreover, the new mechanism cuts unnecessary reward distribution transactions, signaling lower bandwidth consumption and higher efficiency on the TRON network.

## 3. Fairer incentive mechanism

Block rewards decreased from 32 TRX to 16 TRX, while voting rewards increased from 16 TRX to 160 TRX. The adjustment will boost voter turnout in the community, with more TRX locked up by users in the TRON ecosystem. This move is accompanied by the new staking rewards mechanism to guarantee real staking revenues to users.

## 4. Improvement and optimization of TVM

(1) Added a new VM instruction ISCONTRACT(0xd4), which has made smart contract development more flexible by allowing developers to identify the type of the target address in VMs when writing contracts. 
batchvalidatesign(bytes32 hash, bytes[] memory signatures, address[] memory addresses) 

(2) Adopted a multi-thread method for VMs to verify signatures, which is faster than ecrecover of Ethereum while cutting Energy consumption by half.
Contract address: 0x09. To use it in solidity: batchvalidatesign(bytes32 hash, bytes[] memory signatures, address[] memory addresses) 
validatemultisign(address accountAddress, uint256 permissionId, bytes32 content, bytes[] signatures)

(3) Added a new pre-compiled contract to boost multi-signature verification in TVM, speeding up the verification process and reducing Energy consumption.

(4) Banned transfer TRX to smart contract address by two system contract TransferContract and TransferAssetContract. The transfer would fail if the target address is a smart 	 address when using TransferContract and TransferAssetContract. This can prevent general users from transferring assets to smart contract address by mistake, avoiding users’ asset loss.

(5) Allowed automatic activation of inactive accounts when transferring TRX/ TRC10 tokens to accounts in smart contracts. 

(6) Added triggerConstantContract feature for SolidityNode and FullNode so as to improve the functionality of node APIs.

## 5. Improvement of the dynamic adjustment scheme of Energy upper limit

The method of calculating Energy consumed per unit of time shifted from only calculating the staked Energy consumed to all Energy consumed. With this change, statistics of Energy consumption will be more accurate and effective, providing reference for adjusting Energy upper limit, saving users’ costs of using TRON blockchain network and improving network efficiency.
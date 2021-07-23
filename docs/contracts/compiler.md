# Compiler

## Tools

<h3> 1. TronStudio </h3>

Support the build, debug, run, etc. for solidity language written smart contract.
[https://developers.tron.network/docs/tron-studio-intro](https://developers.tron.network/docs/tron-studio-intro)

<h3> 2. TronIDE </h3>

Support the build, debug, run, etc. for solidity language written smart contract.
[http://www.tronide.io](http://www.tronide.io)

<h3> 3. TronBox </h3>

Support the build, deploy, transplant, etc. for solidity language written smart contract.
[https://developers.tron.network/docs/tron-box-user-guide](https://developers.tron.network/docs/tron-box-user-guide)

<h3> 4. TronWeb </h3>
Provide http api service for the usage of smart contract.
[https://developers.tron.network/docs/tron-web-intro](https://developers.tron.network/docs/tron-web-intro)

<h3> 5. TronGrid </h3>
Provide smart contract event query service.
[https://developers.tron.network/docs/tron-grid-intro](https://developers.tron.network/docs/tron-grid-intro)

## Development

First you can use TronStudio to write, build and debug the smart contract. After you finish the development of the contract, you can copy it to [SimpleWebCompiler](https://github.com/tronprotocol/tron-demo/tree/master/SmartContractTools/SimpleWebCompiler) to compile to get ABI and ByteCode. We provide a simple data read/write smart contract code example to demonstrate:

```text
pragma solidity ^0.4.0;
contract DataStore {

    mapping(uint256 => uint256) data;

    function set(uint256 key, uint256 value) public {
        data[key] = value;
    }

    function get(uint256 key) view public returns (uint256 value) {
        value = data[key];
    }
}
```

** Start a Private Net **

Make sure the fullnode code has been deployed locally, you can check if 'Produce block successfully' log appears in FullNode/logs/tron.log

** Develop a Smart Contract **

Copy the code example above to remix to debug.

** Compile in SimpleWebCompiler for ABI and ByteCode **

Copy the code example above to SimpleWebCompiler to get ABI and ByteCode.
Because TRON's compiler is a little different from Ethereum, so you can not get ABI and ByteCode by using Remix. But it will soon be supported.

** Using Wallet-cli to Deploy **

Download Wallet-Cli and build

```text
shell
# download cource code
git clone https://github.com/tronprotocol/wallet-cli
cd  wallet-cli
# build
./gradlew build
cd  build/libs
```

Note: You need to change the node ip and port in config.conf

start wallet-cli

```text
java -jar wallet-cli.jar
```

after started, you can use command lines to operate:

```text
importwallet
<input your password twice for your account>
<input your private key>
login
<input your password you set>
getbalance
```

deploy contract

```text
Shell
# contract deployment command
DeployContract contractName ABI byteCode constructor params isHex fee_limit consume_user_resource_percent <value> <library:address,library:address,...>

# parameters
contract_name: Contract name
ABI: ABI from SimpleWebCompiler
bytecode: ByteCode from SimpleWebCompiler
constructor: When deploy contract, this will be called. If is needed, write as constructor(uint256,string). If not, just write #
params: The parameters of the constructor, use ',' to split, like  1, "test", if no constructor, just write #
fee_limit: The TRX consumption limit for the deployment, unit is SUN(1 SUN = 10^-6 TRX)
consume_user_resource_percent: Consume user's resource percentage. It should be an integer between [0, 100]. if 0, means it does not consume user's resource until the developer's resource has been used up
value: The amount of TRX transfer to the contract when deploy
library: If the contract contains library, you need to specify the library address

# example
deploycontract DataStore [{"constant":false,"inputs":[{"name":"key","type":"uint256"},{"name":"value","type":"uint256"}],"name":"set","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"key","type":"uint256"}],"name":"get","outputs":[{"name":"value","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}] 608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b25040029 # # false 1000000 30 0
If it is deployed successfully, it will return 'Deploy the contract successfully'
```

get the contract address

```text
Your smart contract address will be: <contract address>

# in this example
Your smart contract address will be: TTWq4vMEYB2yibAbPV7gQ4mrqTyX92fha6
```

call the contract to store data, query data

```text
Shell
# call contract command
triggercontract <contract_address> <method> <args> <is_hex> <fee_limit> <value>

# parameters
contract_address: Contract address, like TTWq4vMEYB2yibAbPV7gQ4mrqTyX92fha6
method: The method called, like set(uint256,uint256) or fool(), use ',' to split the parameters. Do not leave space between parameters
args: The parameters passed to the method called, use ',' to split the parameters. Do not leave space between parameters
is_hex: whether the input parameters is Hex, false or true
fee_limit: The TRX consumption limit for the trigger, unit is SUN(1 SUN = 10^-6 TRX)
value: The amount of TRX transfer to the contract when trigger

# trigger example
## set mapping 1->1
triggercontract TTWq4vMEYB2yibAbPV7gQ4mrqTyX92fha6 set(uint256,uint256) 1,1 false 1000000  0000000000000000000000000000000000000000000000000000000000000000

## get mapping key = 1
triggercontract TTWq4vMEYB2yibAbPV7gQ4mrqTyX92fha6 get(uint256) 1 false 1000000  0000000000000000000000000000000000000000000000000000000000000000
```

If the function called is constant or view, wallet-cli will return the result directly.
If it contains library, before deploy the contract you need to deploy the library first. After you deploy library, you can get the library address, then fill the address in library:address,library:address,...

```text
# for instance, using remix to get the bytecode of the contract, like:
608060405234801561001057600080fd5b5061013f806100206000396000f300608060405260043610610041576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063f75dac5a14610046575b600080fd5b34801561005257600080fd5b5061005b610071565b6040518082815260200191505060405180910390f35b600073<b>__browser/oneLibrary.sol.Math3__________<\b>634f2be91f6040518163ffffffff167c010000000000000000000000000000000000000000000000000000000002815260040160206040518083038186803b1580156100d357600080fd5b505af41580156100e7573d6000803e3d6000fd5b505050506040513d60208110156100fd57600080fd5b81019080805190602001909291905050509050905600a165627a7a7230582052333e136f236d95e9d0b59c4490a39e25dd3a3dcdc16285820ee0a7508eb8690029
```

The address of the library deployed before is: TSEJ29gnBkxQZR3oDdLdeQtQQykpVLSk54
When you deploy, you need to use browser/oneLibrary.sol.Math3:TSEJ29gnBkxQZR3oDdLdeQtQQykpVLSk54 as the parameter of deploycontract.


## What is Wallet-CLI?
wallet-cli is an interactive command-line wallet that supports the TRON network for signing and broadcasting transactions in a secure local environment, as well as access to on-chain data. wallet-cli supports key management, you can import the private key into the wallet, wallet-cli will encrypt your private key with a symmetric encryption algorithm and store it in a keystore file. wallet-cli does not store on-chain data locally. It uses gRPC to communicate with a java-tron node. You need to configure the java-tron node to be linked in the configuration file. The following figure shows the process of the use of wallet-cli to sign and broadcast when transferring TRX:
![](https://i.imgur.com/NRKmZmE.png)

The user first runs the `Login` command to unlock the wallet, and then runs the `SendCoin` command to send TRX, wallet-cli will build and sign the transaction locally, and then call the BroadcastTransaction gRPC API of the java-tron node to broadcast the transaction to the network. After the broadcast is successful, the java-tron node will return the transaction hash to wallet-cli, and wallet-cli will display the transaction hash to the user.

Install and run: [wallet-cli](https://github.com/tronprotocol/wallet-cli)


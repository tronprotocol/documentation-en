
## What is Wallet-CLI?
Wallet-Cli is an interactive command-line wallet that supports the TRON network for signing and broadcasting transactions in a secure local environment, as well as access to on-chain data. Wallet-Cli supports key management, you can import the private key into the wallet, Wallet-Cli will encrypt your private key with a symmetric encryption algorithm and store it in a keystore file. Wallet-Cli does not store on-chain data locally. It uses gRPC to communicate with a Java-tron node. You need to configure the Java-tron node to be linked in the configuration file. The following figure shows the process of the use of Wallet-Cli to sign and broadcast when transferring TRX:
![](https://i.imgur.com/NRKmZmE.png)

The user first runs the `Login` command to unlock the wallet, and then runs the `SendCoin` command to send TRX, Wallet-Cli will build and sign the transaction locally, and then call the BroadcastTransaction gRPC API of the Java-tron node to broadcast the transaction to the network. After the broadcast is successful, the Java-tron node will return the transaction hash to Wallet-Cli, and Wallet-Cli will display the transaction hash to the user.

Install and run: [Wallet-Cli](https://github.com/tronprotocol/wallet-cli)


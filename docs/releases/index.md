# Releases

## Binary Integrity Check

All released files after 3.7 will provide signatures signed by the Tron Account: `TKeAcHxgErbVXrG3N3TZiSV6AT566BHTj2`.

### Signature Verification

You can verify the signature by tronweb.

```js
const Trx = require('tronweb').Trx;

console.log(Trx.verifySignature(SHA256, ADDRESS, SIGNATURE));
```

Suppose we got a `FullNode.jar` with a SHA256 hash `2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e`, and a Tron signature `21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b`.

To verify the integrity of the released file:

```shell
# First calculate the sha256 hash

sha256sum FullNode.jar  # or shasum -a 256 FullNode.jar (macOS)
# 2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e  FullNode.jar

# Then check the signature

npm install -g tronweb
node -e 'console.log(require("tronweb").Trx.verifySignature(
    "2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e",
    "TKeAcHxgErbVXrG3N3TZiSV6AT566BHTj2",
    "21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b"
  ))'
# true

# Now you've verified the integrity of the binary release file.
```

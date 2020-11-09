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

### Version Signature
- Odyssey-3.7
FullNode sha256sum: 2fca93b09da4ac62641e03838e77fce99b4711ddb0c09aa91656c80fc9556d2e  
FullNode signature: 21435e32131feb6d00ba8048df04e112e02569ec851064d8ecad2d4dd5da44b7628ddce16823dadfff6fd683fc58cee74964970621a845ee459e2c96a750de551b   
SolidityNode sha256sum: fcdea8b3e511306218ba442fb0828f0413574012d646c39c212a59f6ba5844bc  
SolidityNode signature: 6dcad6e02f17467e5cfebeefa0f9963da08e7da10feebefdec47d689fecc30f104c9b7f5e784b883e7ceb786fe55188356c42c306d727fb7819eed2a71f788361c  

- GreatVoyage-4.0.0
FullNode sha256sum: d3f8f9fde64bdefaadae784d09de97172e5e8a3fe539217e12b89963983a530d  
FullNode signature: e788dbaf2fe35f099f65b2403cfb0d7cbe7f4611f8c5ff8151e4bd84ae468d2e541043c9cde9e74500003027ae9f25cdda81a9bcd60abb45ca7a69f965f4dcc71c  
SolidityNode sha256sum: adddf88423c6c31f1f25ed39b10779c24dd7cdcf37f2325c02b2f2ecfc97e1f6  
SolidityNode signature: e3b9859f178f7851dedb7a0a8deb715e5f1e3af10b1064c36f2727ec2b8825510df4fd7b09d7d049204e5df3e8d5b87778e83a15ca96ce786f7977a6cb48bca91b  

- GreatVoyage-4.1.1:
FullNode sha256sum: 30e716b86b879af1e006c2b463903ae3835e239e32e2b01c2a1b903a153897fe  
FullNode signature: 5faee65a448bb9aa77835992ca3d24e50d8a76b7934f80664ad38e83179c8114278fdef4494de7231f8e40de86461676a7aa4a54c795f4c692e91d90e156ec471b  
SolidityNode sha256sum: 10a160181053b421109ecace74df5fc0f8860bc8a70181add65fd9a292c35a44  
SolidityNode signature: 1d1413b13adf7778f9a720294eca066ac728ad636d166505276f5ff1f63973c100c04778f937f240f10107edb7de477604857867fc4dbdb68238169c978fc3da1b  


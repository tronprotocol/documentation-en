
# Documentation Guide

+ For TRON brief information, please check out [TRON Overview](Tron-overview.md)
+ For TRON virtual machine information, please check out [TRON Virtual Machine](Tron-VM.md)
+ For TRON http api, please check out [TRON Http Api](Tron-http.md)
+ For TRON RPC api, please check out [TRON RPC Api](Tron-rpc.md)  
+ For TRON official public nodes ip, please check out [TRON Official Public Nodes](Tron-official-public-nodes.md)  
+ For TRON node deployment, please check out [TRON Deployment](Tron-deployment.md)   
+ For TRON shielded transaction, please check out [TRON Shieled Transaction](Tron-shielded-transaction.md)  
+ For TRON multi-signatures, please check out [TRON Multi-signatures](Tron-multi-signatures.md)  
+ For TRON resources, please check out [TRON Resources](Tron-resources.md)  
+ For TRON Q&A, please check out [TRON Q&A](Tron-QA.md)   

# Tips Guide 
+ [TRON Wallet Proposal](https://github.com/tronprotocol/TIPs/blob/master/tip-01.md)  
+ [TRON Token Standard](https://github.com/tronprotocol/TIPs/blob/master/tip-10.md)  
+ [TRON Event Subscription Model](https://github.com/tronprotocol/TIPs/blob/master/tip-12.md)  
+ [Design of TRON account](https://github.com/tronprotocol/TIPs/blob/master/tip-13.md)    
+ [TRON Account Multi-Signature](https://github.com/tronprotocol/TIPs/blob/master/tip-16.md)  
+ [TRON Adaptive Energy Limit Model](https://github.com/tronprotocol/TIPs/blob/master/tip-17.md)  
+ [TRC-20 Token Standard](https://github.com/tronprotocol/TIPs/blob/master/tip-20.md)  
+ [Implement of DB storage with RocksDB](https://github.com/tronprotocol/TIPs/blob/master/tip-24.md)  
+ [Built-in Message Queue in Event Subscription Model](https://github.com/tronprotocol/TIPs/blob/master/tip-28.md)  
+ [To Support Contract without ABI in Event Subscription Model](https://github.com/tronprotocol/TIPs/blob/master/tip-34.md)

# Getting Started as TRON Community Developers

TRON is a global, open-source platform for decentralized applications. 

Thank you for considering to help out with the source code! We welcome contributions from anyone on the internet, and are grateful for even the smallest of fixes!

GitHub is used to track issues and contribute code, suggestions, feature requests or documentation.

If you'd like to contribute to TRON, please fork, fix, commit and send a pull request (PR) for the maintainers to review and merge into the main base. If you wish to submit more complex changes though, please check up with the core developers first on our channel to ensure those changes are in line with the general philosophy of the project and/or get some early feedback which can make both your efforts much lighter as well as our review and merge procedures quick and simple.

Your PR will be reviewed according to the Code Review Guidelines.

We encourage a PR early approach, meaning you create the PR the earliest even without the fix/feature. This will let core developers and other volunteers know you picked up an issue. These early PRs should indicate 'in progress' status.

** Developer Community **

* [Discord](https://discord.gg/GsRgsTD)   
* [Gitter](https://gitter.im/tronprotocol/allcoredev)   

## How to Contribute to TRON Documentation

There are two documentation repositories:  
[documentation-EN](https://github.com/tronprotocol/documentation-EN) is the English version.   
[documentation-ZH](https://github.com/tronprotocol/documentation-ZH) is the Chinese version.  

We use MkDocs to build documentation project. Documentation source files are written in Markdown, and configured with a single YAML configuration file.

You can edit or add a documentation file in /docs/ folder.

## How to Submit a TIP

TRON Improvement Proposals (TIPs) describe standards for the TRON platform, including core protocol specifications, client APIs, and contract standards.

The TIPS repository is [https://github.com/tronprotocol/TIPs](https://github.com/tronprotocol/TIPs)

Your first PR should be a first draft of the final TIP. It must meet the formatting criteria enforced by the build (largely, correct metadata in the header). An editor will manually review the first PR for a new TIP and assign it a number before merging it. Make sure you include a discussions-to header with the URL to a discussion forum or open GitHub issue where people can discuss the TIP as a whole.  Please refer to the [TIP template](https://github.com/tronprotocol/TIPs/blob/master/template.md)


## How to Contribute to java-tron

**Branch Introduction**

``master`` branch:  
This branch contains the latest code released to the production environment. It can only be merged, and can not be modified directly in this branch.

``develop`` branch:  
This branch is the main development branch. It contains the complete code that is going to release. It can only be merged, and can not be modified directly in this branch.

``feature`` branch:  
This branch is used to develop new features. It is created based on ``develop`` branch. Once the development is finished, it should be merged into ``develop`` branch, and then delete the branch.

``release`` branch:  
This is the branch that is going to be released. It is created based on ``develop`` branch. In this branch, small fix and modification of final version of metadata is allowed. When the code is released, this branch should be merged into ``master`` branch(tag needed) and ``develop`` branch. The final test before release uses this branch.

``hotfix`` branch:  
This branch is used to fix a bug when an online bug is found. It is created based on ``master`` branch. When bug fix is done, it should be merged into ``master`` branch(as a new release) and ``develop`` and then delete the branch. branch.

**Writing a new feature:**    

When you start to develop a new feature, please create a feature branch from ``develop`` branch under ``origin/feature``.
```text
$ git checkout -b feature/my-feature develop
# switch to 'feature/my-feature'
```

When you finish the development, the new feature should be merged into ``develop`` branch.
```text
$ git commit -m "description"
# submit the code
$ git checkout develop
# switch to 'develop'
$ git pull
# update branch
$ git checkout feature/my-feature
# switch to 'feature/my-feature'
$ git merge develop
# merge 'develop', need to fix the conflict
$ git push
# submit to GitHub
# make a Pull Request to wait the core developers to check
$ git branch -d feature/my-feature
# once it is merged, delete 'feature/my-feature'
```

**Fixing online bugs:**   

When you start to fix an online bug, please create a hotfix branch from ``master`` branch under ``origin/hotfix``.
```text
$ git checkout -b hotfix/my-hotfix master
# switch to 'hotfix/my-hotfix'
$ git commit -a -m "Bumped version number to 3.1.4"
# submit and modify the version number
```
When you finish the fix, it should be merged into ``master`` branch and ``develop`` branch.
```text
$ git commit -m "description"
# submit the code
$ git checkout master
# switch to 'master'
$ git pull
# update branch
$ git checkout hotfix/my-hotfix
# switch to 'hotfix/my-hotfix'
$ git merge master
# merge 'master', need to fix the conflict
$ git push
# make a Pull Request to wait the core developers to check
# tag 'master'

$ git checkout develop
# switch to 'develop'
$ git pull
# update branch
$ git checkout hotfix/my-hotfix
# switch to 'hotfix/my-hotfix'
$ git merge develop
# merge 'develop', need to fix the conflict
$ git push
# make a Pull Request to wait the core developers to check

$ git branch -d hotfix/my-hotfix
# once it is merged, delete 'my-hotfix'
```

Your commit messages should detail why you made your change in addition to what you did (unless it is a tiny change).

Finally, please make a PR.

Additionally, if you are writing a new feature, please ensure you add appropriate test cases under ``/src/test``.




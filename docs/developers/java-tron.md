The java-tron repository is: [https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron)    

<h2>Branch Introduction</h2>

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

<h2>Writing a new feature</h2>   

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

<h2>Fixing online bugs:</h2>   

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
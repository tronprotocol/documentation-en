# Developer Guide

Thank you for considering to help out with the source code! We welcome contributions from anyone, and are grateful for even the smallest of fixes!

GitHub is used to track issues and contribute code, suggestions, feature requests or documentation. If you want to participate in java-tron development, please follow the Github code submission process as follows:

* Fork java-tron repository
* Fix the code
* Commit the code
* Send a pull request
* The maintainers review and merge into the main code base

For small fixes, you can send a pull request (PR) directly, but make sure the PR includes a detailed description. For more complex changes, you need to submit an issue to the [TIP repository](https://github.com/tronprotocol/tips) detailing your motivations, implementation plans, etc. For how to submit a TIP issue, please refer to [TIP Specification](tips.md).

We encourage java-tron developers to submit PRs as soon as possible. Even if they are not fully developed, you can submit a PR first, so that other developers can know that the TIP Issue corresponding to this PR is in the state of `In Progress`.

Developers should develop and submit a PR based on the `develop` branch, reviewers will review the PR according to [Code Review Guidelines](#code-review-guidelines).



## Key Branches
java-tron only has `master`, `develop`, `release-*`, `feature-*`, and `hotfix-*` branches, which are described below:

* ``develop`` branch

    The `develop` branch only accepts merge requests from other forked branches or`release_*` branches. It is not allowed to directly push changes to the `develop` branch. A `release_*` branch has to be pulled from the develop branch when a new build is to be released.
    
* ``master`` branch

    `release_*` branches and `hotfix/*` branches should only be merged into the `master` branch when a new build is released.
    
* ``release`` branch

    `release_*` is a branch pulled from the `develop` branch for release. It should be merged into `master` after a regression test and will be permanently kept in the repository. If a bug is identified in a `release_*` branch, its fixes should be directly merged into the `release_*` branch. After the fixes passing the regression test, the `release_*` branch should be merged back into the `develop` branch. Essentially, a `release_*` branch serves as a snapshot for each release.

- ``feature`` branch

    `feature/*` is an important feature branch pulled from the `develop` branch. After the `feature/*` branch is code-complete, it should be merged back to the `develop` branch. The `feature/*` branch is maintainable.


- ``hotfix`` branch

    It is pulled from the `master` branch and should be merged back into the `master` branch and the `develop` branch. Only pull requests of the fork repository (pull requests for bug fixes) should be merged into the `hotfix/` branch. `hotfix/` branches are used only for fixing bugs found after release.
    
## Submitting Code

If you want to contribute codes to java-tron, please follow the following steps:

* Fork java-tron repository

    Fork a new repository from [tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) to your personal code repository
    
    ```
    $ git clone https://github.com/yourname/java-tron.git

    $ git remote add upstream https://github.com/tronprotocol/java-tron.git   ("upstream" refers to upstream projects repositories, namely tronprotocol's repositories, and can be named as you like it. We usually call it "upstream" for convenience) 
    ```
    
* Edit the code in the fork repository 
    
    Before developing new features, please synchronize your fork repository with the upstream repository.
    
    ```
    git fetch upstream 
    git checkout develop 
    git merge upstream/develop --no-ff   (Add --no-ff to turn off the default fast merge mode)
    ```
    
     Pull a new branch from the develop branch of your repository for local development. Please refer to [Branch Naming Conventions](#branch-naming-conventions)。

    ```
    git checkout -b feature/branch_name develop
    ```

    Write and commit the new code when it is completed. Please refer to [Commit Messages](#commit-messages)
    ```
    git add .
    git commit -m 'commit message'
    ```
     
    Commit the new branch to your personal remote repository
     
    ```
    git push origin new_feature
    ```

* Push code

    Submit a pull request (PR) from your repository to `tronprotocol/java-tron`.
    Please be sure to click on the link in the red box shown below. Select the base branch for tronprotocol and the compare branch for your personal fork repository.
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/javatron_pr.png)



## Code Review Guidelines
The only way to get code into java-tron is to send a pull request. Those pull requests need to be reviewed by someone. The following guide explains our expectations around PRs for both authors and reviewers.


### The Process
The first decision to make for any PR is whether it’s worth including at all. To make the decision we must understand what the PR is about. If there isn’t enough description content or the diff is too large, request an explanation. Anyone can do this part.

We expect that reviewers check the style and functionality of the PR, providing comments to the author using the GitHub review system. Reviewers should follow up with the PR until it is in good shape, then approve the PR. Approved PRs can be merged by the code maintainer.

When communicating with authors, be polite and respectful.

### Functional Checks
For PRs that fix an issue, reviewers should try reproduce the issue and verify that the pull request actually fixes it. Authors can help with this by including a unit test that fails without (and passes with) the change.

For PRs adding new features, reviewers should attempt to use the feature and comment on how it feels to use it. For example: if a PR adds a new command line flag, use the program with the flag and comment on whether the flag feels useful.

We expect appropriate unit test coverage. Reviewers should verify that new code is covered by unit tests.

### Code Style
We would like all developers to follow a standard development flow and coding style. Therefore, we suggest the following:

1. Review the code with coding style checkers.
2. Review the code before submission.
3. Run standardized tests.

`Sonar`-scanner and `Travis CI` continuous integration scanner will be automatically triggered when a pull request has been submitted. When a PR passes all the checks, the **java-tron** maintainers will then review the PR and offer feedback and modifications when necessary.  Once adopted, the PR will be closed and merged into the `develop` branch.

We are glad to receive your pull requests and will try our best to review them as soon as we can. Any pull request is welcome, even if it is for a typo.

Please kindly address the issue you find. We would appreciate your contribution.

Please do not be discouraged if your pull request is not accepted, as it may be an oversight. Please explain your code as detailed as possible to make it easier to understand.

Please make sure your submission meets the following code style:

- The code must conform to [Google Code Style](https://google.github.io/styleguide/javaguide.html).
- The code must have passed the Sonar scanner test.
- The code has to be pulled from the `develop` branch.

### Branch Naming Conventions
Branch naming should follow the following guidelines:

1. Always name the `master` branch and `develop` branch as "master" and "develop".
2. Name the `release_*` branch using version numbers, which are assigned by the project lead (e.g., Odyssey-v3.1.3, 3.1.3, etc.).
3. Use `hotfix/` as the prefix of the `hotfix` branch, briefly describe the bug in the name, and connect words with underline (e.g., hotfix/typo, hotfix/null_point_exception, etc.).
4. Use `feature/` as the prefix of the `feature` branch, briefly describe the feature in the name, and connect words with underline (e.g., feature/new_resource_model, etc.).

### Pull Request Guidelines
Pull Requests should follow the following specifications:

1. Create one PR for one issue.
2. Avoid massive PRs.
3. Write an overview of the purpose of the PR in its title.
4. Write a description of the PR for future reviewers.
5. Elaborate on the feedback you need (if any).

#### Commit Messages

Commit messages should follow the rule below, we provide a template with corresponding instructions.

Template:
```
<commit type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The message header is a single line that contains a succinct description of the change containing a `commit type`, an optional `scope` and a subject.

`commit type` describes the kind of change that this commit is providing:
* feat     (new feature)
* fix      (bug fix)
* docs     (changes to documentation)
* style    (formatting, missing semi colons, etc. no code change)
* refactor (refactoring production code)
* test     (adding or refactoring tests. no production code change)
* chore    (updating grunt tasks etc. no production code change)

The `scope` can be anything specifying place of the commit change. For example:`protobuf`,`api`,`test`,`docs`,`build`,`db`,`net`.You can use * if there isn't a more fitting scope.

The `subject` contains a succinct description of the change:
1. Limit the subject line, which briefly describes the purpose of the commit, to 50 characters.
2. Start with a verb and use first-person present-tense (e.g., use "change" instead of "changed" or "changes").
3. Do not capitalize the first letter.
4. Do not end the subject line with a period.
5. Avoid meaningless commits. It is recommended to use the git rebase command.

Message body use the imperative, present tense: "change" not "changed" nor "changes". The body should include the motivation for the change and contrast this with previous behavior.

Here is an example:
```
feat(block): optimize the block-producing logic

1. increase the priority that block producing thread acquires synchronization lock
2. add the interruption exception handling in block-producing thread

Closes #1234
```
If the purpose of this submission is to modify one issue, you need to refer to the issue in the footer, starting with the keyword Closes, such as `Closes #1234`, if multiple bugs have been modified, separate them with commas, such as `Closes #123, #245, #992`.

### Special Situations And How To Deal With Them
As a reviewer, you may find yourself in one of the situations below. Here’s how to deal with those:

* The author doesn’t follow up: ping them after a while (i.e. after a few days). If there is no further response, close the PR or complete the work yourself.
* Author insists on including refactoring changes alongside bug fixes: We can tolerate small refactorings alongside any change. If you feel lost in the diff, ask the author to submit the refactoring as an independent PR, or at least as an independent commit in the same PR.
* Author keeps rejecting your feedback: You may close the PR.

## Conduct
While contributing, please be respectful and constructive, so that participation in our project is a positive experience for everyone.

Examples of behavior that contributes to creating a positive environment include:

* Using welcoming and inclusive language
  Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior include:

* The use of sexualized language or imagery and unwelcome sexual attention or advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others’ private information, such as a physical or electronic address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a professional setting


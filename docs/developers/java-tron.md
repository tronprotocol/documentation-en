# Developer Guide
Thank you for contributing to the development of java-tron source code!

Whether it is a minor bug fix or a major feature enhancement, we value your contributions.

On GitHub, you can:

- Track issues
- Contribute code
- Suggest improvements
- Request new features
- Collaborate on maintaining documentation

If you plan to contribute to java-tron development, please follow the process below.



## Contribution Process Overview

1. **Fork the Repository**
    Fork the [java-tron repository](https://github.com/tronprotocol/java-tron) to your personal account.
2. **Modify Code**
    Create a new branch from the develop branch and begin implementation.
3. **Submit Changes**
    Commit your changes with clear commit messages.
4. **Create a Pull Request (PR)**
    Push your changes to your forked repository and submit a PR to the official repository.
5. **Code Review and Merge**
    Maintainers will review your PR based on the [Code Review Guidelines](#code-review-guidelines) and merge it into the `develop` branch if it meets the requirements.

## Submission Rules

- **Minor Fixes**
    You can directly submit a PR, but ensure it includes a complete description.
- **Major Changes**
    For complex architectural or logic changes, please first submit a TRON Improvement Proposal (TIP) in the [TIP repository](https://github.com/tronprotocol/tips), detailing the motivation and implementation plan.
    Refer to the [TIP Specification](tips.md).
- **Early PR Submission**
    We encourage developers to submit PRs early, even if the feature is not yet complete. This notifies the community that development of the associated TIP has started.
- **Development Branch**
    All development should be based on the `develop` branch, followed by a PR submission.

## Branch Management
The `java-tron` repository includes the following main branch types:

- **`develop` Branch**
    - Used for daily development
    - Accepts merges exclusively from contributor forks and `release_*` branches
    - When preparing a new release, a `release_*` branch is created from this branch
- **`master` Branch**
    - Used only for releases
    - Only merges from `release_*` and `hotfix/*` branches
- **`release_*` Branch**
    - Created from `develop` for version finalization and regression testing
    - Merged into `master` branch after regression testing
    - Retained permanently as a point-in-time release snapshot
    - Bug fixes are merged directly into this branch and synchronized back to `develop`
- **`feature/*` Branch**
    - Created from `develop` for new feature development
    - Merged back into `develop` after feature completion
    - Can be maintained long-term
- **`hotfix/*` Branch**
    - Created from `master` for urgent bug fixes
    - Only accepts bug-fix pull requests from forked repositories
    - Must be merged back into both `master` and `develop` to ensure consistency

## Code Submission Process
### 1. Fork and Clone the Repository
```
git clone https://github.com/yourname/java-tron.git
cd java-tron
git remote add upstream https://github.com/tronprotocol/java-tron.git
```
> `upstream` refers to the official repository. The name can be customized, but `upstream` is the conventional choice
### 2. Sync Upstream Code
```
git fetch upstream
git checkout develop
git merge upstream/develop --no-ff
```
> The `--no-ff` flag prevents fast-forward merges, preserving a clear record of the merge event in the commit history.
### 3. Create a Development Branch
```
git checkout -b feature/branch_name develop
```
### 4. Commit Changes
```
git add .
git commit -m "commit message"
```
### 5. Push the Branch
```
git push origin feature/branch_name
```
### 6. Create a Pull Request
From your own repository, submit a Pull Request (PR) to `tronprotocol/java-tron`.
   ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/javatron_pr.png)
It’s recommended to select the options in the red box, setting `develop` branch of the `tronprotocol/java-tron` as the base branch and your forked repository’s branch as the compare branch.

## Code Review Guidelines
The only way to merge code into **java-tron** is through **a Pull Request (PR)**.
All PRs must be reviewed before merging.

### Review Process
- Reviewers are responsible for verifying the PR's objectives and technical impact.
- For PRs lacking descriptions or with excessive changes, reviewers may request additional clarification.
- Reviewers check code style, feature completeness, and test coverage.
- Reviewers should remain polite, respectful, and follow up promptly.

### Feature Validation
- **For Bug Fixes**
    - Reviewers must attempt to reproduce the reported issue to validate the effectiveness of the fix.
    - It’s recommended that submitters provide unit tests that fail before the fix and pass after.
- **New Feature PRs**
    - Reviewers should test the new feature and provide feedback.
    - All new code must include unit tests.

### Code Specification Requirements

- Adhere to automated code formatting standards before submission.
- Self-test before submission.
- Pass standardized tests.

CI Tools:

- Sonar: Static code analysis
- Travis CI: Continuous integration checks

Once all checks pass, maintainers will review and merge into `develop`.

> **Coding Standards**
>- Follow the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
>- All PRs must be based on the `develop` branch

## Branch Naming Conventions

1. `master` and `develop` are fixed names.
2. `release_*`: Named with the `release_` prefix plus the version number, assigned by the project lead (e.g., `release_v4.8.0` for the `GreatVoyage-v4.8.0(Kant)` release).
3. `hotfix/*`: For urgent fixes, connecting words with underscores (e.g., `hotfix/typo`, `hotfix/null_point_exception`).
4. `feature/*`: For new feature development, connecting words with underscores (e.g., `feature/new_resource_model`).

## Pull Request Specifications

1. One PR should address a single issue.
2. Avoid excessively large changes.
3. Title: Briefly describe the PR’s purpose.
4. Description: Provide detailed information for reviewers.
5. Specify areas where feedback is needed.
6. Do not capitalize the first letter of the title.
7. Do not end the title with a period.

## Commit Message Specifications
Recommended format:

```
<type>(<scope>): <subject>

<body>

<footer>
```
### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes (no functional changes)
- `refactor`: Code refactoring
- `test`: Test code changes
- `chore`: Build process or auxiliary tooling changes (no production code change)

The `scope` specifies the place of the change, for example: `protobuf`, `api`, `test`, `docs`, `build`, `db`, `net`. Use `*` if there isn't a more fitting scope.

### Subject Specifications

1. Limit to 50 characters; do not end with a period.
2. Start with a verb and use the first-person present tense (e.g., use `change` instead of `changed` or `changes`).
3. Start with a lowercase letter.
4. Avoid meaningless commits. It is recommended to use the `git rebase` command.

Example:
```
feat(block): optimize the block-producing logic

1. increase the priority for acquiring synchronization lock
2. add interruption exception handling in block-producing thread

Closes #1234
```

## Handling Special Cases

- **Submitter Not Following Up**
    - Contact after a few days; if no response, the PR may be closed or continued by others.
- **Submitter Refactoring While Fixing Bugs**
    - Small-scale refactoring is acceptable.
    - Large-scale changes should be split into separate PRs or at least separate commits.
- **Submitter Rejects Feedback**
    - Reviewers may close the PR.

## Conduct
Please maintain respect and constructiveness to foster a positive community atmosphere.

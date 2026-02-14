# Contributing Guide

Thank you for taking time to contribute to english documentation of java-tron.

Whether you're fixing a typo, updating outdated information, or adding new tutorials, contributions of any size are welcome and appreciated. This guide is designed to help you submit contributions smoothly and easily.

**Note**: Due to the simple nature of this project, we currently maintain only the `master` branch with no complex development branch workflow.


## How to Contribute

### Reporting Issues

If you find errors, broken links, or unclear explanations while reading the documentation, please let us know via Issues.

1.  Before submitting an Issue, please search to see if a similar issue already exists.
2.  For simple typos or formatting issues, we recommend submitting a fix directly via a Pull Request.
3.  For content questions, please clearly describe the problem you encountered and how you expect the documentation to read.

### Submitting Changes

You can modify the documentation directly via Pull Requests.

1.  **Fork this Repository**: Click the Fork button in the top-right corner to copy this project to your account.
2.  **Clone to Your Local Machine**: Clone the forked repository to your computer.
    ```bash
    git clone https://github.com/your-username/documentation-en.git
    ```
3.  **Add Upstream Repository**: Add the official repository as "upstream" to sync updates later.
    ```bash
    git remote add upstream https://github.com/tronprotocol/documentation-en.git
    ```
4.  **Sync Latest Code**: Before starting your changes, ensure your local `master` branch is up to date with the official repository.
    ```bash
    git checkout master
    git fetch upstream master
    git merge upstream/master
    git push origin master  # Optional, syncs to your personal remote repository(origin)
    ```
5.  **Create a Branch**：
    Create a descriptive branch helps keep your local modifications organized.
    ```bash
    git checkout -b fixes/fix-typo
    ```
6.  **Make Changes**: Edit the documentation using Markdown syntax under branch `fixes/fix-typo`
7.  **Commit Changes**：
    ```bash
    git add .
    git commit -m "fix typo in getting started with java-tron"
    git push origin fixes/fix-typo # Push the Branch to your personal remote repository(origin)
    ```
8.  **Open a Pull Request**：
    Open a Pull Request on your GitHub targeting the official repository's `master` branch.
    **Notice**
    - Since we don't maintain a `develop` branch, your PR will directly target the `master` branch.
    - Please describe in detail what you changed and why.


## FAQ

**Q: I don't see a `develop` branch. Which branch should I submit my PR to?**
A: Submit your PR directly to the `master` branch. It will be merged after review.

**Q: I want to rewrite a large section. Can I submit a PR directly?**
A: We recommend opening an Issue first to describe your idea and confirm the direction before starting work. This helps avoid wasted effort.

**Q: How long until my changes are merged?**
A: Maintainers will try to review PRs within 3 business days. Simple typo fixes are usually merged quickly.

---

Thank you again for your contribution!

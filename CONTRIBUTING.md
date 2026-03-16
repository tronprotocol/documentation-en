# Contributing Guide

Thank you for taking time to contribute to english documentation of java-tron.

Whether you're fixing a typo, updating outdated information, or adding new tutorials, contributions of any size are welcome and appreciated. This guide is designed to help you submit contributions smoothly and easily.

**Note**: Due to the simple nature of this project, we currently maintain only the `master` branch and forgo complex Git workflows such as `develop` or `release` branch strategies.


## How to Contribute

### Reporting Issues

If you find errors, broken links, unclear explanations, or suggested content while reading the documentation, please let us know via Issues.

1.  Before submitting an Issue, please search [existing issues](https://github.com/tronprotocol/documentation-en/issues?q=is%3Aissue%20state%3Aclosed%20OR%20state%3Aopen) first to avoid duplicates.
2.  For simple typos or formatting issues, we recommend submitting a fix directly via a Pull Request.
3.  For other content questions, please clearly describe the problem you encountered and how you expect the documentation to read.
    *  Ask a question
      Feel free to ask any `documentation-en` related question to solve your doubt. Please click **Ask a question** in GitHub Issues, using [Ask a question](.github/ISSUE_TEMPLATE/ask-a-question.md) template.
    *  Report an error
      If you think you've found an error with `documentation-en`, please click **Report an error** in GitHub Issues, using [Report an error](.github/ISSUE_TEMPLATE/report-an-error.md) template.
    *  Request a feature
      If you have any good content suggestions for `documentation-en`, please click **Request a feature** in GitHub Issues, using [Request a feature](.github/ISSUE_TEMPLATE/request-a-feature.md) template.

### Submitting Changes

If you want to modify the documentation, please follow the following steps.

* Fork the Repository

  Visit [tronprotocol/documentation-en](https://github.com/tronprotocol/documentation-en/) and click **Fork** to create a fork repository under your GitHub account.

* Setup Local Environment

  Clone your fork repository to local and add the official repository as **upstream**.
    ```
    git clone https://github.com/yourname/documentation-en.git

    cd documentation-en

    git remote add upstream https://github.com/tronprotocol/documentation-en.git
    ```

* Synchronize and Fix

  Before making new fixes, please synchronize your local `master` branch with the upstream repository and update to your fork repository.
    ```
    git fetch upstream
    # `--no-ff` means to turn off the default fast merge mode
    git merge upstream/master --no-ff
    git push origin master
    ```

  Create a new branch for fixing.
    ```
    git checkout -b branch_name master
    ```

* Commit and Push

  Write and commit the new code when it is completed.
     ```
     git add .
     git commit -m 'commit message'
     ```

  Push the new branch to your fork repository
     ```
     git push origin branch_name
     ```

* Submit a pull request

  Submit a pull request (PR) from your fork repository to `tronprotocol/documentation-en`. Please select `master` as the base branch for `tronprotocol/documentation-en` and the compare branch for your fork repository.

## FAQ

**Q: I don't see a `develop` branch. Which branch should I submit my PR to?** 

A: Submit your PR directly to the `master` branch. It will be merged after review.

**Q: I want to rewrite a large section. Can I submit a PR directly?**

A: We recommend opening an Issue first to describe your idea and confirm the direction before starting work. This helps avoid wasted effort.

**Q: How long until my changes are merged?**

A: Maintainers will try to review PRs within 3 business days. Simple typo fixes are usually merged quickly.

---

Thank you again for your contribution!

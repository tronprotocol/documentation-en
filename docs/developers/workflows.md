# java-tron CI Workflows

This page summarizes the GitHub Actions checks that contributors need to understand when preparing a java-tron pull request. The workflow files in java-tron remain the source of truth if the implementation changes.

## When Workflows Run

| Workflow | Pull request target | Documentation-only PR | Other triggers |
| --- | --- | --- | --- |
| PR Check (`pr-check.yml`) | `develop`, `release_**` | Runs | Push to `master` or `release_**` |
| PR Build (`pr-build.yml`) | `master`, `develop`, `release_**` | Skipped | Manual dispatch |
| Single-node integration (smoke) (`integration-test-single-node.yml`) | `develop`, `release_**` | Skipped | Push to `master` or `release_**`; manual dispatch |
| CodeQL (`codeql.yml`) | `develop` | Skipped | Push to `develop`, `master`, or `release_**`; weekly schedule |
| Math usage (`math-check.yml`) | `develop`, `release_**` | Runs | Push to `master` or `release_**`; manual dispatch |
| Reviewer assignment (`pr-reviewer.yml`) | `develop`, `release_**` | Runs | None |
| Cancel PR workflows (`pr-cancel.yml`) | Any branch | Runs when an unmerged PR is closed | None |

PR Build, the single-node integration (smoke) workflow, and CodeQL are skipped when a pull request changes only documentation or certain repository-metadata files. If the same pull request includes any other file, the applicable workflows run normally. PR Check, Math usage, reviewer assignment, and cancellation do not have this path exclusion.

## PR Validation and Code Checks

For pull requests targeting `develop` or `release_**`, PR Check enforces these title and description rules:

- Use `type: description` or `type(scope): description`.
- Keep the title between 10 and 72 characters.
- Use one of these types: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`, `ci`, `perf`, `build`, or `revert`.
- Do not start the description portion with an uppercase ASCII letter, and do not end the title with a period.
- Provide a PR description of at least 20 characters after leading and trailing whitespace is removed.
- An unknown scope produces a warning rather than a failure.

The workflow also runs Checkstyle and validates `common/src/main/resources/reference.conf`, including its key format, nesting depth, service-port conflicts, and configuration comments. These checks also run for documentation-only pull requests targeting `develop` or `release_**`.

## Multi-platform Build and Coverage

When triggered by a pull request, PR Build executes the full Gradle build across four environments:

| Environment | Architecture | JDK | Platform-specific checks |
| --- | --- | --- | --- |
| macOS 26 | ARM64 | 17 | Regular framework tests use RocksDB |
| Ubuntu 24.04 | ARM64 | 17 | Regular framework tests use RocksDB |
| Rocky Linux 8 container | x86-64 | 8 | Focused RocksDB engine tests |
| Debian 11 container | x86-64 | 8 | Focused RocksDB tests and coverage reports |

The coverage gates require:

- More than 60% coverage for changed Java source lines. The gate is skipped when there are no changed Java source lines.
- No more than a 0.1 percentage-point decrease in overall coverage relative to the base revision.

## Integration, Security, and Math Checks

The documented source version includes a single-node integration workflow that runs the smoke-test subset against one node. The full single-node suite and the multi-node integration workflow are not run by GitHub Actions.

The smoke workflow runs for applicable pull requests targeting `develop` or `release_**`, on pushes to `master` or `release_**`, and when started manually.

CodeQL runs on pull requests targeting `develop` only. It also runs on pushes to `develop`, `master`, and `release_**`, and on a weekly schedule.

The Math usage workflow rejects direct `java.lang.Math` usage and directs contributors to `org.tron.common.math.StrictMathWrapper`. It also runs for documentation-only pull requests targeting `develop` or `release_**`.

## Scope Validation and Reviewer Assignment

PR validation and reviewer assignment use separate scope lists. PR validation recognizes 32 scopes, while reviewer assignment maps 26 scopes:

| Category | Count | Scopes |
| --- | ---: | --- |
| Recognized and mapped by both | 24 | `framework`, `chainbase`, `actuator`, `consensus`, `common`, `crypto`, `plugins`, `protocol`, `net`, `db`, `vm`, `tvm`, `api`, `jsonrpc`, `rpc`, `http`, `event`, `config`, `trie`, `metrics`, `test`, `docker`, `lite`, `toolkit` |
| Recognized only by PR validation | 8 | `block`, `proposal`, `log`, `version`, `freezeV2`, `DynamicEnergy`, `stable-coin`, `reward` |
| Mapped only by reviewer assignment | 2 | `backup`, `ci` |

An unknown PR scope only produces a validation warning. Reviewer assignment uses a separate scope mapping.

## Cancellation on Close

When a pull request is closed without being merged, java-tron attempts to cancel queued or running instances of:

- PR Build
- CodeQL
- Single-node integration (smoke)

## Sonar Configuration

The java-tron repository retains `sonar-project.properties` and the SonarQube Gradle plugin configuration for static analysis. Sonar is not invoked by java-tron's GitHub Actions workflows. An external Sonar or SonarCloud integration, if configured, is outside the workflow files described here.

## Running Checks Locally

The [development example](demo.md#4-checkstyle-code-style-check) provides the recommended Checkstyle, full-build, and RocksDB commands, including the JDK and storage-engine differences between ARM64 and x86-64.

# TIP Specification and Guidelines

**TRON Improvement Proposals (TIPs)** document the entire improvement process for the TRON network, from community suggestions and discussions to final adoption. Each TIP is a detailed design document that covers its underlying principles and technical specifications, to help community members fully understand its content. TIPs are a core unit of TRON's community governance, and anyone can freely submit a TIP. Through community discussion, the community decides whether to develop it into a common standard or incorporate it into a network upgrade. The proposer of a TIP is responsible for encouraging developer participation in the community, building consensus for the TIP, and recording all dissenting opinions.


## TIP Types

TIPs are primarily categorized into two types: `Standard Track` and `Informational`.

* **`Standard Track`**: These TIPs describe changes that affect how TRON is implemented, such as modifications to block or transaction validity rules, proposed application standards, or any changes that affect the interoperability of TRON applications. `Standard Track` TIPs can be further subdivided into the following categories:

    * **`Core`**: TIPs that require a consensus fork[^1] for implementation. This category also includes TIPs that don't require a consensus fork but still need discussion by core developers.
    * **`Networking`**: Improvements to the network protocol.
    * **`Interface`**: Improvements to API/RPC specifications and standards.
    * **`TRC`**: Application-level standards, including smart contract standards like TRC-20.
    * **`TVM`**: Improvements to the TRON Virtual Machine.
    
* **`Informational`**: These TIPs describe issues related to TRON's design or provide general guidance or information to the TRON community, but do not propose new features.


## TIP Workflow

Before submitting a TIP, we recommend first creating a TIP **Issue** for community discussion and add a link to this issue in the TIP's title. The format of the TIP issue should be consistent with the content of the TIP. The specific process for submitting a TIP is as follows:

1.  **Fork** the GitHub [TIPs repository](https://github.com/tronprotocol/TIPs).
2.  Create a new TIP in your forked repository, following the [TIP template](https://github.com/tronprotocol/TIPs/blob/master/template.md).
3.  Submit a **Pull Request (PR)** to the TRON TIPs repository.

Strictly follow the `markdown` requirements of the [template](https://github.com/tronprotocol/TIPs/blob/master/template.md) when writing a TIP, and ensure that the TIP title includes a link to the TIP Issue or a discussion forum address so that community members can fully discuss the TIP. If a TIP involves the development of new features in java-tron and has a corresponding development PR, you need to cross-reference each other's GitHub links in both the TIP and the java-tron PR to ensure the traceability of the new feature's requirements analysis and development code.

After a new TIP's initial PR submission, the TIP will be in the **`Draft`** state. The editor will review the TIP to ensure it meets certain formatting standards and assign a TIP number before merging it.

Once the TIP is considered mature and ready to move to the next phase, you should:

* For **Core TIPs**, you must follow the process in the [TRON Project Management Repository](https://github.com/tronprotocol/pm?tab=readme-ov-file#tron-core-devs-meetings-and-sr-meetings-overview) to submit your TIP to the agenda for discussion at an upcoming core developers meeting. If the core developers decide to accept your TIP, the TIP editor will update its status to **`Accepted`**.
* For **other types of TIPs**, you can submit a PR to change the TIP's status to **`Final (non-Core)`**. The TIP editor will then review your draft and ask for any dissenting opinions. If the TIP editor determines that the TIP has not yet reached preliminary consensus, they may close your PR and ask you to continue modifying the draft.

### TIP Status

A TIP may go through the following statuses:

* **`Draft`**: The TIP is in a rapid iteration and modification phase.
* **`Last Call`**: The TIP has completed its initial iteration and is ready for review by others.
* **`Accepted`**: After a Core TIP's proposer has resolved the required technical changes and the TIP has been in the `Last Call` state for at least 2 weeks, core developers will decide whether to include the TIP as part of a hard fork and add it to the client development (this process is not part of the TIP workflow). Once a decision is made, the TIP will enter the `Final` state.
* **`Final (non-Core)`**: A non-Core TIP has been in the `Last Call` state for at least 2 weeks, and all changes have been completed.
* **`Final (Core)`**: The core developers have decided to implement the TIP, and it will be included in an upcoming release or has already been implemented in a released version.
* **`Active`**: If a TIP may never be completed, its status can be `Active`.
* **`Abandoned`**: A TIP is no longer tracked or maintained by its submitter, or it may no longer be the technically preferred solution.
* **`Rejected`**: A TIP that breaks functionality or a `Core` TIP that has been rejected by core developers and will not be implemented.
* **`Superseded`**: A TIP that was previously `Final` but is no longer considered the optimal solution.
* **`Deferred`**: A TIP that is not currently accepted but may be accepted in the future.


## TIP Composition

A TIP consists of two parts: the header and the main content.

### TIP Header

The TIP header contains the TIP number, a short descriptive title (limited to 44 characters), author details, a link to the discussion, TIP status, TIP type, creation date, etc. For the specific format, refer to:

```
tip: <to be assigned>
title: <TIP title>
author: <a list of the author's or authors' name(s) and/or username(s), or name(s) and email(s), e.g. (use with the parentheses or triangular brackets): FirstName LastName (@GitHubUsername), FirstName LastName <foo@bar.com>, FirstName (@GitHubUsername) and GitHubUsername (@GitHubUsername)>
discussions-to: <URL>
status: <Draft | Last Call | Accepted | Final | Deferred>
type: <Standards Track (Core, Networking, Interface, TRC, VM) | Informational>
category (*only required for Standard Track): <Core | Networking | Interface | TRC | VM>
created: <date created on, in ISO 8601 (yyyy-mm-dd) format>
requires (*optional): <TIP number(s)>
replaces (*optional): <TIP number(s)>
```

### TIP Body

The TIP body should include the following sections:

* **`Simple Summary`**: A brief description of the TIP.
* **`Abstract`**: A concise, easy-to-understand technical summary of the `Specification` section. Readers should be able to understand the main function of the TIP by reading only the `Abstract`.
* **`Motivation`**: (Optional) Motivation is an important part of a TIP. It should clearly explain why the current protocol is insufficient to address the problem this TIP targets. This section can be omitted if the motivation is obvious.
* **`Specification`**: The technical specification, which details the new feature's syntax and semantics and should be sufficiently comprehensive.
* **`Rationale`**: Describes the design's motivation and the reasons for the design decisions made. It serves to supplement the `Specification`. The `Rationale` should also describe alternative designs and related work, and include an explanation of significant objections or concerns raised during the TIP's discussion.
* **`Backwards Compatibility`**: (Optional) If the TIP's changes introduce backwards compatibility issues, the TIP should include a `Backwards Compatibility` section describing these incompatibilities and their impact. The TIP must state how these incompatibilities are intended to be handled.
* **`Test Cases`**: (Optional) For TIPs that affect consensus, implementation-related test cases must be included. This section can be omitted for non-Core TIPs.
* **`Implementation`**: This section does not need to be completed before the TIP is assigned the `Accepted` status but must be completed before the TIP is assigned the `Final` status. When discussing many API details, "general consensus and working code" are necessary.


## Linking to External Resources

Since external resources may change at any time (e.g., broken links, content moved or modified), TIPs should not directly include links to them.


## Linking to Other TIPs

A TIP can reference other TIPs. References to other TIPs should follow the `TIP-N` format, where `N` is the number of the referenced TIP, and must be accompanied by a link. The link must be a relative path to ensure it is valid in the TIPs GitHub repository as well as in all forks. For example, you can use `[TIP-1](/tips/TIP-1)` to reference `TIP-1`.


## Auxiliary Files

Images, diagrams, and other auxiliary files should be stored in a subdirectory of the TIPs repository's `assets` folder, for example: `assets/TIP-N/` (where N is the TIP number). When linking to images within a TIP, a relative path should be used, such as: `../assets/TIP-1/image.png`.


[^1]: **Consensus fork**: A phenomenon in a blockchain network where nodes have different opinions on changes to protocol rules, leading to a divergence in the blockchain's history.
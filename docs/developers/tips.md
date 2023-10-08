# TRON Improvement Proposals (TIPs)

TIP stands for TRON Improvement Proposal. TIPs record the entire process of TRON improvement, including the process of community making suggestions, discussions, and adoption. A TIP is a design document about a proposal, including the rationale and technical specifications of the proposal. Community users can read the TIP document to learn more about the proposal.

TIPs are the unit around which governance happens in TRON，anyone is free to propose one, and then community participants will debate to determine if it should be adopted as a standard or included in a network upgrade. The TIP author is responsible for building consensus within the community and documenting dissenting opinions. 

## TIP Types
TIPs are mainly divided into `Standard Track` and `Informational`:

* `Standard Track` :  Describes any change that affects most or all TRON implementations, such as a change in block or transaction validity rules, proposed application standards/conventions, or any change or addition that affects the interoperability of applications using TRON. Furthermore, Standard TIPs can be broken down into the following categories.

    * `Core`:  Improvements requiring a consensus fork, as well as changes that are not necessarily consensus critical but may be relevant to "core dev" discussions.
    * `Networking`: Improvements around network protocol.
    * `Interface`:  Improvements around client API/RPC specifications and standards.
    * `TRC`：Application-level standards and conventions, including contract standards such as token standards (TRC-20).
    * `TVM`：mprovements around TRON Virtual Machine.

* `Informational`: Describes a TRON design issue, or provides general guidelines or information to the TRON community, but does not propose a new feature.


## TIP Work Flow

Before you submit a TIP, you need to create an issue for comment and add the issue URL to your TIP header. The format of a TIP issue is consistent with the content of TIP. The process of submitting TIP is as follows:

1. Fork the [TIP repository](https://github.com/tronprotocol/TIPs) by clicking "Fork" in the top right.
2. Add your TIP to your fork of the repository. There is a [TIP template](https://github.com/tronprotocol/TIPs/blob/master/template.md) here.
3. Submit a Pull Request to TRON's TIPs repository.

Please use `markdown` to write TIP in strict accordance with the requirements of [template](https://github.com/tronprotocol/TIPs/blob/master/template.md). Make sure you include a discussions-to header with the URL to a discussion forum or open GitHub issue where people can discuss the TIP as a whole. If a TIP is about the feature development of java-tron, and a PR of the development exists, in your TIP and your java-tron's PR you need to refer each other's github link to make the requirements analysis of new features and development code traceable.

Your first PR for a new TIP will be in the state of `draft`. It must meet the formatting criteria enforced by the build. An editor will manually review it and assign it a number before merging it.

When you believe your TIP is mature and ready to progress past the `draft` phase, you should do one of two things:

* For a Standards Track TIP of type Core, ask to have your issue added to the agenda of an upcoming All Core Devs meeting, where it can be discussed for inclusion in a future hard fork. If core devs agree to include it, the TIP editors will update the state of your TIP to `Accepted`.
* For all other TIPs, open a PR changing the state of your TIP to `Final(non-Core)`. An editor will review your draft and ask if anyone objects to its being finalized. If the editor decides there is no rough consensus, they may close the PR and request you fix the issues in the draft before trying again.

### TIP Status
A TIP may go through the following states:

- `Draft`: A TIP that is undergoing rapid iteration and changes.
- `Last Call`:  A TIP that is done with its initial iteration and ready for review by a wide audience.
- `Accepted`: A core TIP that has been in the `Last Call` for at least 2 weeks and any technical changes that were requested have been addressed by the author. The process for Core Devs to decide whether to encode a TIP into their clients as part of a hard fork is not part of the TIP process. If such a decision is made, the TIP will move to the `final`.
- `Final (non-Core)`: A TIP that has been in the `Last Call` for at least 2 weeks and any technical changes that were requested have been addressed by the author. 
- `Final (Core)`: A TIP that the Core Devs have decided to implement and release in a future version or has already been released.
- `Active`: If the TIPs are never meant to be completed, the TIPs may have a status of `Active`.
- `Abandoned`: If a TIP is no longer pursued by the original authors or it may not be a (technically) preferred option anymore.
- `Rejected`: A TIP that is fundamentally broken or a Core TIP that was rejected by the Core Devs and will not be implemented.
- `Superseded`: A TIP which was previously Final but is no longer considered state-of-the-art. Another TIP will be in the Final status and cite the Superseded TIP.
- `Deferred`: A TIP which isn't accepted now, may be accepted in the future.



## TIP Structure
A TIP consists of a title preamble and body content.
### TIP Header Preamble

The TIP header preamble contains the TIP number, a short descriptive title (limited to a maximum of 44 characters), author details, discussion link, TIP status, TIP type, creation time, etc. Please refer to the specific format:
```

---
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
---  

```

### TIP Body
TIP body should have the following parts:

* `Simple Summary`：Provide a simplified explanation of the TIP.
* `Abstract`： A short (~200 word) description of the technical issue being addressed. It should be a very terse and human-readable version of the `specification` section. Someone should be able to read only the abstract to get the gist of what this specification does.
* `Motivation`: (optional) A motivation section is critical for TIPs. It should clearly explain why the existing protocol specification is inadequate to address the problem that the TIP solves. This section may be omitted if the motivation is evident.
* `Specification`：The technical specification should detail the syntax and semantics of any new feature.
* `Rationale`：The rationale fleshes out the specification by describing what motivated the design and why particular design decisions were made. It should describe alternate designs that were considered and related work. The rationale should discuss important objections or concerns raised during the discussion around the TIP.
* `Backwards Compatibility` ：(optional) All TIPs that introduce backward incompatibilities must include a section describing these incompatibilities and their consequences. The TIP must explain how the author proposes to deal with these incompatibilities. 
* `Test Cases` ：(optional) Test cases for an implementation are mandatory for TIPs that are affecting consensus changes. This section may be omitted for non-Core proposals.
* `Implementation`：The implementations must be completed before any TIP is given the status `Final`, but it need not be completed before the TIP is `accepted`. The principle of "rough consensus and running code" is still useful when it comes to resolving many discussions of API details.


## Linking to External Resources
Links to external resources SHOULD NOT be included. External resources may disappear, move, or change unexpectedly.

## Linking to other TIPs
References to other TIPs should follow the format `TIP-N` where N is the TIP number you are referring to. Each TIP that is referenced in a TIP MUST be accompanied by a relative markdown link. The link MUST always be done via relative paths so that the links work in TIP GitHub repository and forks of TIP repository. For example, you would link to TIP-1 with `[TIP-1](/TIPS/tip-1)`.

## Auxiliary Files
Images, diagrams and auxiliary files should be included in a subdirectory of the `assets` folder for that TIP as follows: `assets/tip-N` (where N is to be replaced with the TIP number). When linking to an image in the TIP, use relative links such as `../assets/tip-1/image.png`.


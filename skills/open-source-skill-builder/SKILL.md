---
name: open-source-skill-builder
description: Build, validate, test, and optionally publish a complete Agent Skill project from a user's brief. Use when a user asks to create, package, improve, open-source, install, or submit a Skill for Codex, Claude Code, skills.sh, or another Agent Skills-compatible client. Produce a standards-compliant repository, run isolated installation and fresh-agent behavior tests without making the user test it, protect personal identity by default, and publish to GitHub or skills.sh only after the exact public identity and external actions are explicitly approved.
---

# Open-Source Skill Builder

## Mission

Turn a skill brief into a focused, portable, tested Agent Skill project. Keep local creation and testing autonomous. Treat public GitHub creation, pushes, and skills.sh ingestion as separate privacy-gated actions.

## Required resources

Read only the resources needed for the current phase:

- Read `references/standards.md` before choosing the Skill structure or metadata.
- Read `references/project-workflow.md` before creating or changing project files.
- Read `references/verification.md` before claiming the Skill works.
- Read `references/publication.md` before any GitHub, remote installation, or skills.sh action.
- Copy and adapt files from `assets/` instead of recreating their structure.

## Non-negotiable gates

- Default to local-only development. Do not infer permission to publish from a request to create or test a Skill.
- Before public publication, show the exact GitHub owner, repository URL, commit author name and email, license attribution, and any README identity references. Require explicit approval of that disclosure set.
- Never use the currently authenticated GitHub account merely because it is available.
- Respect `DISABLE_TELEMETRY` and `DO_NOT_TRACK`. Do not override either setting to trigger skills.sh ingestion.
- Create or update a Markdown implementation plan under the target project's `plan/` directory before implementation.
- Do not make the user perform acceptance testing. Use validators, isolated installation, and a fresh agent session yourself.
- Do not claim completion from structural validation or unit tests alone. At least one fresh-agent behavior test must pass.
- Preserve unrelated files and changes. Never stage, commit, or publish material outside the confirmed project scope.
- Never place credentials, personal paths, user documents, test transcripts with personal data, or authentication files in the Skill or repository.

## Workflow

### 1. Convert the brief into a contract

Extract or derive:

- user goal and representative requests;
- positive and negative activation cases;
- required inputs, typed states, outputs, and failure behavior;
- irreversible or external actions and their approval points;
- deterministic operations that need scripts;
- references and reusable output templates;
- target clients and environment requirements;
- repository name, license preference, and intended visibility.

Ask only questions whose answers would materially change the design or authorize an external action. State safe assumptions and continue when the brief is sufficient.

### 2. Refresh the standards

Follow `references/standards.md`. Prefer the shared Agent Skills specification for the portable core and add client-specific metadata outside `SKILL.md`. Recheck current primary sources when platform behavior, installation commands, or publication rules may have changed.

### 3. Plan and scaffold

Follow `references/project-workflow.md`.

1. Create the project directory and `plan/` implementation file.
2. Use an available first-party Skill creator or its initializer. If unavailable, create the specification's minimal structure directly.
3. Keep repository documentation outside the installable Skill directory.
4. Implement the smallest useful set of `references/`, `scripts/`, and `assets/`.
5. Add `agents/openai.yaml` when targeting Codex or ChatGPT surfaces.
6. Add evaluation cases for direct, implicit, incomplete, negative, edge, and safety behavior.

### 4. Implement for progressive disclosure

Keep `SKILL.md` focused on the core workflow. Move detailed standards, variants, examples, and publication instructions into one-level-deep references. Use scripts only for deterministic or repeatedly error-prone operations and test every added script.

Write instructions in imperative form. Put all activation guidance in the frontmatter description. Never add a redundant README inside the Skill folder.

### 5. Verify locally

Follow every applicable layer in `references/verification.md`:

1. structural and metadata validation;
2. deterministic script or unit tests;
3. local repository discovery;
4. isolated installation into a temporary directory;
5. fresh-agent activation and behavior tests;
6. negative-trigger and approval-gate tests;
7. repository-aware implementation review.

If no fresh supported agent runtime is available, report the exact gap and do not label the release fully verified.

### 6. Install for private use

When the user wants to use the Skill personally, install the verified Skill into the user's approved local or global Skill directory. Confirm the installed path, then run a new ephemeral agent session and verify that the trace reads that installed copy.

Do not install permanently when an isolated temporary installation is enough for testing.

### 7. Publish only after the privacy gate

Read `references/publication.md`. If any publication identity field or approval is missing, stop only the public phase and leave the tested local project usable.

When all public disclosures are approved:

1. run the privacy and secret review;
2. verify GitHub authentication matches the approved owner;
3. create or update the repository with the approved visibility;
4. push only reviewed commits;
5. repeat discovery and installation from the remote source;
6. trigger skills.sh ingestion only when telemetry consent permits it;
7. verify the rendered catalog page, not only its HTTP status.

### 8. Report evidence

Use `assets/release-report-template.md`. Lead with what is usable now. Include local and remote paths as applicable, verification commands and results, fresh-agent cases, Git commit or repository links, skills.sh status, privacy decisions, unresolved risks, and any phase intentionally withheld.

## Completion contract

Declare the project complete only when:

- the plan matches the delivered files;
- the Skill passes structural validation and discovery;
- all deterministic scripts pass their tests;
- isolated installation succeeds;
- at least one fresh agent activates and follows the Skill from raw user input;
- a negative or safety case is exercised;
- material review findings are resolved;
- local installation is verified when requested;
- public identity approval exists for every published surface;
- remote installation passes after publication;
- the skills.sh page renders the correct Skill when catalog inclusion was requested.

If publication is withheld for privacy, say that the local Skill is complete and the public release is intentionally not performed.

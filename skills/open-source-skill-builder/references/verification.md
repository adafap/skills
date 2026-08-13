# Verification and Forward Testing

## Principle

The developer owns acceptance testing. Do not ask the user to prove that the Skill activates or works. Preserve raw commands, outputs, generated artifacts, and fresh-agent traces as evidence.

## Layer 1: structural validation

Run every applicable validator:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/SKILL_NAME
uvx --from skills-ref agentskills validate skills/SKILL_NAME
```

If `uvx` or the `skills-ref` package is unavailable, record that fact rather than silently treating another validator as identical. The specification may still show `skills-ref validate`, but the package verified on 2026-07-31 exposes the `agentskills` executable.

Also verify:

- YAML and JSON files parse;
- all linked files exist;
- `SKILL.md` and source files respect line limits;
- no TODO placeholder remains;
- the root README installation source is correct;
- the plan matches the delivered project.

## Layer 2: deterministic behavior

Run every bundled script with:

- one normal case;
- one boundary case;
- one invalid-input case.

Add automated unit tests for calculations, parsers, state transitions, and output schemas. Do not substitute a successful import or syntax check for behavior coverage.

## Layer 3: local discovery

From the repository root, confirm that the official CLI discovers exactly the intended Skills:

```bash
npx skills add . --list
```

Unexpected Skills, missing Skills, stale descriptions, or duplicate names fail this layer.

## Layer 4: isolated installation

Create an explicit temporary directory and install from the local source without changing the user's permanent setup:

```bash
TEST_ROOT="$(mktemp -d)"
cd "$TEST_ROOT"
npx skills add /absolute/path/to/project \
  --skill SKILL_NAME \
  --agent codex \
  --agent claude-code \
  --copy \
  --yes
```

Verify the installed `SKILL.md` paths and compare the copied project tree with the source. Clean up only the exact temporary directory after evidence is captured.

Installation proves packaging, not behavior.

## Layer 5: fresh-agent behavior

Use a new session that has not seen the implementation discussion or evaluation answers. For Codex, prefer an isolated project installation and:

```bash
codex exec \
  --ephemeral \
  --skip-git-repo-check \
  --sandbox workspace-write \
  --cd "$TEST_ROOT" \
  "RAW USER REQUEST"
```

Use `--sandbox read-only` when the Skill should not create files. Save the final message with `--output-last-message` or the full event stream with `--json` when trace evidence matters.

Confirm from the trace that the agent read the isolated installed Skill path. A globally installed Skill with the same name can contaminate the test; the trace must establish which copy was used.

Run these cases:

1. direct invocation using the client's explicit Skill syntax;
2. implicit activation without naming the Skill;
3. incomplete input that requires the correct follow-up;
4. a related negative request that should not activate;
5. an edge or fallback path;
6. an external-action or safety boundary;
7. the primary successful workflow and output artifact.

Do not tell the test agent that it is being evaluated. Do not include expected answers or suspected defects in its prompt.

At least one authenticated fresh agent must execute the workflow. A Claude Code file-copy check does not prove Claude behavior. If a requested client CLI is unavailable or unauthenticated, report that client-specific behavior gap separately.

## Layer 6: implementation review

After material changes, perform a repository-aware review:

- trace `description -> SKILL.md -> references/scripts/assets -> generated output`;
- verify that every required resource is reachable from `SKILL.md`;
- compare evaluation expectations with actual behavior;
- inspect external-action and privacy gates;
- map tests to risky steps;
- fix material findings and rerun affected layers.

## Layer 7: remote verification

After an authorized GitHub publication, repeat from the remote source:

```bash
npx skills add OWNER/REPOSITORY --list
```

Then install into a new temporary directory and repeat at least the main fresh-agent case. A local pass does not prove that the pushed repository contains the same release.

## Completion evidence

Record:

- validator commands and results;
- script and unit-test totals;
- discovered Skill names;
- isolated installation destinations;
- raw forward-test prompts and final outputs;
- whether activation was direct or implicit;
- Git commit and remote source when applicable;
- unverified client runtimes or platform-index delays.

Never claim end-to-end coverage from unit tests alone.

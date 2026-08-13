# Agent Skill Standards

## Source snapshot

Verified on 2026-07-31. Recheck these primary sources before relying on platform-specific behavior:

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills overview: https://agentskills.io/home
- Codex and ChatGPT Skill guidance: https://learn.chatgpt.com/docs/build-skills.md
- Codex non-interactive mode: https://learn.chatgpt.com/docs/non-interactive-mode.md
- Open `skills` CLI: https://github.com/vercel-labs/skills
- skills.sh CLI documentation: https://www.skills.sh/docs/cli
- skills.sh API and cache documentation: https://www.skills.sh/docs/api
- GitHub repository creation: https://cli.github.com/manual/gh_repo_create

The Agent Skills specification currently shows `skills-ref validate`. The Python package verified on 2026-07-31 exposes the executable as `agentskills`; the working isolated command is:

```bash
uvx --from skills-ref agentskills validate path/to/skill
```

## Portable core

Use the intersection supported by Agent Skills-compatible clients:

```text
skill-name/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
├── references/
└── assets/
```

Only `SKILL.md` is required. Create optional directories only when they support the workflow.

For maximum portability, keep the YAML frontmatter to:

```yaml
---
name: skill-name
description: Explain what the Skill does and when it should activate.
---
```

The shared specification permits optional fields, but clients differ. Put OpenAI-specific interface metadata in `agents/openai.yaml` instead of depending on optional frontmatter.

## Naming and metadata

- Use 1 to 64 lowercase ASCII letters, digits, and hyphens.
- Do not begin or end with a hyphen or use consecutive hyphens.
- Match the directory name to the `name` value exactly.
- Keep `description` non-empty and under 1,024 characters.
- Front-load the user goal and recognizable trigger terms.
- State both what the Skill does and when it should activate.
- Put detailed workflow instructions in the body, not the description.

For `agents/openai.yaml`:

- quote all string values;
- use a human-facing `display_name`;
- keep `short_description` between 25 and 64 characters;
- make `default_prompt` a short sentence that explicitly contains `$skill-name`;
- omit icons, colors, tool dependencies, and invocation policy unless they are actually required.

## Progressive disclosure

Treat context as a limited resource:

1. Clients initially load `name` and `description`.
2. They load the full `SKILL.md` after activation.
3. They load referenced files and execute scripts only as needed.

Keep `SKILL.md` below 500 lines and preferably below 5,000 tokens. Keep references one level deep and focused. Link every resource directly from `SKILL.md` with a clear condition for reading or running it.

## Instruction design

- Keep one recognizable user goal per Skill.
- Use imperative instructions with explicit inputs, steps, outputs, and stop conditions.
- Define what the agent must not infer.
- Separate reversible local work from external or irreversible actions.
- Use typed fields or explicit states for fragile decisions.
- Add scripts only when deterministic reliability or repeated computation justifies them.
- Make scripts self-contained, document dependencies, validate inputs, and return useful errors.
- Keep templates in `assets/` and reference material in `references/`.
- Do not add process notes, installation guides, changelogs, or a README inside the installable Skill folder.

## Compatibility strategy

Use the shared core for Codex, Claude Code, and other compatible clients. Verify each requested client through the official `skills` CLI or that client's documented installation path. Do not claim behavioral compatibility merely because file copying succeeded.

For Codex, test both direct `$skill-name` invocation and implicit activation. Use `codex exec --ephemeral` for independent non-interactive tests when available.

## Minimum evaluation inventory

Every Skill needs representative cases for:

- direct activation;
- implicit activation;
- incomplete input;
- a related request that should not activate;
- an edge or failure path;
- a safety or external-action boundary;
- the primary successful output.

Store evaluation inputs and observable expectations outside the installable Skill directory so fresh-agent tests cannot read the answer key.

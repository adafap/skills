# {{DISPLAY_NAME}}

`{{SKILL_NAME}}` {{ONE_SENTENCE_PURPOSE}}

## Important boundaries

{{SAFETY_AND_AUTHORIZATION_BOUNDARIES}}

## Install

```bash
npx skills add {{OWNER}}/{{REPOSITORY}}
```

Optional agent-specific or global installation:

```bash
npx skills add {{OWNER}}/{{REPOSITORY}} \
  --skill {{SKILL_NAME}} \
  --agent codex \
  --agent claude-code \
  --global
```

## Use

```text
${{SKILL_NAME}} {{EXAMPLE_REQUEST}}
```

## Verify

```bash
{{VALIDATION_COMMAND}}
{{TEST_COMMAND}}
npx skills add . --list
```

## Sources

{{PRIMARY_SOURCE_LIST_AND_RETRIEVAL_DATE}}

## Repository structure

```text
skills/{{SKILL_NAME}}/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/
└── assets/
```

Only directories used by this Skill should be present.

## License

{{LICENSE}}

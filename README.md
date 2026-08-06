# Agent Skills by AipengHuang

Focused, source-grounded Agent Skills that follow the open Agent Skills format.

## Install

List the available Skills:

```bash
npx skills add AipengHuang/skills --list
```

Install the California wrongful-termination pre-check:

```bash
npx skills add AipengHuang/skills --skill ca-wrongful-termination-precheck
```

Then ask your agent to use `$ca-wrongful-termination-precheck` with your facts.

## California Wrongful Termination Pre-check

This Skill organizes California termination facts into:

- a careful issue pre-check;
- a deadline-urgency map;
- an evidence-preservation checklist; and
- a neutral, lawyer-ready chronology.

It does not decide whether a termination was unlawful, predict damages or a settlement, replace a lawyer, file a complaint, or contact an employer or agency. Its legal references point to current California legislative and agency pages and the EEOC; users and agents must recheck primary sources before relying on a deadline or current legal rule.

## Repository layout

```text
skills/
  ca-wrongful-termination-precheck/
    SKILL.md
    agents/openai.yaml
    references/sources.md
tests/evals.json
```

## License

[MIT](LICENSE)

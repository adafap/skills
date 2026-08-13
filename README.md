# Adafap Agent Skills

Public, source-grounded Agent Skills maintained by the Adafap team. This repository is the single public source for skills.sh and Agent Skills-compatible clients.

## Install

List Skills:

```bash
npx skills add adafap/skills --list
```

Install one Skill globally:

```bash
npx skills add adafap/skills --skill de-dismissal-severance-check --global
```

## Published Skills

- `ca-wrongful-termination-precheck`: California employment termination issue pre-check.
- `de-dismissal-severance-check`: German dismissal deadlines and severance comparison workflow.
- `open-source-skill-builder`: standards, testing, privacy gates, and release workflow for public Agent Skills.

Legal-information Skills do not provide individualized legal advice. Recheck current primary sources and seek qualified counsel for urgent or high-impact decisions.

## Repository layout

```text
skills/<skill-name>/        # installable Agent Skills only
tooling/                    # repository validation
tests/evals/                # fresh-agent evaluation cases
tests/python/               # deterministic script tests
registry.json               # publication registry
```

Do not put repository READMEs, plans, CI, or cross-Skill tests inside installable Skill directories.

## Verify

```bash
corepack enable
pnpm install
pnpm verify
```

## License and security

The repository uses the [MIT License](LICENSE). Report vulnerabilities and unsafe legal-rule errors through [SECURITY.md](SECURITY.md), not a public issue containing personal facts.

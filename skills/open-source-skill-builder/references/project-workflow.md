# Skill Project Workflow

## Brief contract

Translate the user's description into this explicit project contract:

| Field | Required outcome |
| --- | --- |
| Goal | One sentence describing the user result |
| Triggers | Direct and indirect requests that should activate |
| Exclusions | Related requests that should not activate |
| Inputs | Required, optional, typed, and sensitive fields |
| Outputs | Files, responses, schemas, and quality requirements |
| Workflow | Ordered steps, decisions, fallbacks, and stop conditions |
| Tools | Required CLIs, MCP servers, APIs, or local runtimes |
| Resources | References, scripts, and templates worth bundling |
| Safety | External actions, secrets, personal data, and approval gates |
| Targets | Codex, Claude Code, other clients, or a portable baseline |
| Release | Local-only, private, public, GitHub owner, and license |

Keep unknown fields explicit. Ask only when an unknown would change the design or authorize publication.

## Repository contract

Use this default standalone layout:

```text
project-name/
├── .gitignore
├── LICENSE
├── README.md
├── plan/
│   └── YYYY-MM-DD-description.md
├── skills/
│   └── skill-name/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── scripts/
│       ├── references/
│       └── assets/
└── tests/
    └── evals.json
```

Omit unused optional directories. Keep repository-level documentation, plans, tests, and contribution guidance outside the installable Skill folder.

## Implementation plan

Create the plan before implementation. Include:

- objective;
- implementation steps;
- affected areas;
- verification approach;
- progress checklist;
- final outcome.

Keep it synchronized after findings, scope changes, publication decisions, and final verification.

## Scaffold

Prefer an available first-party creator. For Codex's built-in creator, initialize the Skill and generate `agents/openai.yaml` deterministically by passing the three interface values to the initializer.

When no creator exists, create the minimal portable core directly and validate it with the Agent Skills reference validator.

## Resources

Choose resources by repeated need:

- Put current standards, domain rules, schemas, and detailed variants in `references/`.
- Put deterministic transformations or calculations in `scripts/`.
- Put reusable output files and templates in `assets/`.
- Do not copy documentation into multiple files.
- Keep each file focused and below the project's file-size limit.

## Root README

Adapt `assets/repository-readme-template.md`. Include:

- what the Skill does;
- important safety or authorization limits;
- the simplest installation command first;
- optional project-local, global, and agent-specific flags afterward;
- an invocation example;
- verification commands;
- primary source provenance;
- repository structure;
- license and contribution expectations.

Do not make optional CLI flags look mandatory. For a single-Skill repository, lead with:

```bash
npx skills add OWNER/REPOSITORY
```

## Evaluation file

Copy `assets/evals-template.json` to `tests/evals.json`. Keep expectations observable. Do not write hidden reasoning or include the intended answer in forward-test prompts.

## Privacy-safe content

Before testing or publication:

- replace local absolute paths with portable commands or placeholders;
- remove personal names, emails, account identifiers, tokens, screenshots, documents, and raw private transcripts;
- keep test data fictional and clearly non-personal;
- inspect generated metadata, README text, license attribution, Git remotes, and commit identity;
- avoid copying authentication files, lock files from personal installations, or agent session logs.

Use the requested license. If the user explicitly requests open-source publication but gives no license, state the proposed default before publication. Never infer that a personal legal name should appear in the license.

# Privacy-Gated Publication

## Publication identity contract

Before creating a public repository or pushing to one, construct and show this disclosure set:

| Field | Required value |
| --- | --- |
| GitHub owner | Exact public username or organization |
| Repository | Exact public repository name and URL |
| Visibility | `public`, `private`, or `internal` |
| Commit author | Exact public author name |
| Commit email | Exact public email or approved no-reply address |
| License | Exact license and copyright attribution |
| README identities | Every person, company, domain, or contact reference |
| skills.sh source | Expected public owner/repository/skill URL |

Require explicit approval after displaying the values. Approval to make a Skill does not approve this disclosure set. Never substitute the currently authenticated account for a missing owner decision.

## Pre-publication privacy review

Inspect:

- every tracked file and filename;
- Git status and staged diff;
- Git commit author and committer configuration;
- repository remotes;
- license attribution;
- README links and badges;
- test fixtures, screenshots, logs, and transcripts;
- environment, credential, and agent-state files;
- full commit history when the repository is not new.

Use dedicated secret-scanning tools when available. A clean diff does not prove a clean history.

Stop publication if any personal or secret field lacks approval. Keep the local project usable.

## GitHub publication

Verify tools and identity:

```bash
gh --version
gh auth status
git status --short
git diff --check
```

Confirm that the authenticated account matches the approved owner. For a new repository with no shared base history, a reviewed initial commit may be pushed directly to the default branch. For an existing repository, use a scoped branch and draft pull request unless the user explicitly requests another workflow.

Create a new authorized repository with the approved settings, for example:

```bash
gh repo create OWNER/REPOSITORY \
  --public \
  --source . \
  --remote origin \
  --push \
  --description "DESCRIPTION"
```

Do not copy this example's visibility when the approved contract differs.

After publication, verify the owner, visibility, default branch, license, topics, remote commit, and clean working tree through read-only GitHub and Git checks.

## Remote installation

Lead user documentation with the shortest command:

```bash
npx skills add OWNER/REPOSITORY
```

Optional flags may select a Skill, install globally, target agents, copy rather than symlink, or skip prompts. Do not present optional flags as required.

Before release completion:

1. run remote `--list` discovery;
2. install the exact remote Skill into a new temporary directory;
3. verify Codex and Claude Code destinations when requested;
4. run at least one fresh-agent case from the remote install.

## skills.sh ingestion

skills.sh uses the open `skills` CLI and anonymous installation telemetry for catalog and ranking data. There is no repository file that guarantees listing.

Respect privacy controls. If `DISABLE_TELEMETRY` or `DO_NOT_TRACK` is set, do not override it. Explain that automated catalog ingestion cannot be triggered without separate consent.

When telemetry consent and publication approval exist:

1. perform a real remote installation with the official CLI;
2. allow for documented search and detail-page caches;
3. construct the expected page as `https://www.skills.sh/OWNER/REPOSITORY/SKILL_NAME`, using the public lowercase owner route used by the site;
4. inspect the rendered page's heading, repository, installation command, and Skill content;
5. do not rely on HTTP status alone because a rendered not-found page may still return HTTP 200;
6. distinguish a live detail page from keyword-search indexing, which may update later;
7. verify exact search separately with `npx skills find SKILL_NAME` when the user requires keyword discoverability.

Do not claim security-audit results, install counts, first-seen dates, or search visibility until the platform displays them.

If indexing is delayed, continue bounded checks at cache-respecting intervals and report the exact pending state. Do not alter repository identity or create duplicate repositories to force indexing.

# Infisical environment sync

This repository uses the shared Adax Infisical Cloud project. Secret values are never stored in Git. The tracked `.infisical.json` file contains only the non-secret project link, and `.infisical-env` maps remote folders to gitignored local files.

## New computer

1. Install the CLI: `brew install infisical/get-cli/infisical`.
2. Authenticate with your authorized Adax account: `infisical login`.
3. From any Adax repository root, run `pnpm env:sync`.

`pnpm env:sync` is the standard command. It synchronizes the Infisical `dev` environment for all Adax repositories cloned as sibling directories.

For single-repository or non-development maintenance, use `./scripts/infisical-env.sh pull <environment>`. Preview and Production require explicit access and use `staging` and `prod`. Pulling atomically replaces every local file mapped for that environment.

Administrators can upload an existing mapped file with `./scripts/infisical-env.sh push <environment> --yes`. Normal development should only pull from Infisical.

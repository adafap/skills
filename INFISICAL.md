# Infisical environment sync

This repository uses the shared Adax Infisical Cloud project. Secret values are never stored in Git. The tracked `.infisical.json` file contains only the non-secret project link, and `.infisical-env` maps remote folders to gitignored local files.

## New computer

1. Install the CLI: `brew install infisical/get-cli/infisical`.
2. Authenticate with your authorized Adax account: `infisical login`.
3. From this repository root, run `./scripts/infisical-env.sh pull dev`.

If all Adax repositories are cloned as sibling directories, run `./scripts/infisical-env.sh pull-all dev` from any one of them to synchronize the whole workspace.

`pull` defaults to `dev`. Preview and Production require explicit access and use `staging` and `prod`. Pulling atomically replaces every local file mapped for that environment.

Administrators can upload an existing mapped file with `./scripts/infisical-env.sh push <environment> --yes`. Normal development should only pull from Infisical.

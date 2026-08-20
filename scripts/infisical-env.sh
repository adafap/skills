#!/usr/bin/env bash

set -euo pipefail
umask 077

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST_FILE="$REPO_ROOT/.infisical-env"
TEMP_FILE=""
TEMP_DIR=""

cleanup_temp() {
  if test -n "$TEMP_FILE"; then
    rm -f "$TEMP_FILE"
  fi
  if test -n "$TEMP_DIR"; then
    rmdir "$TEMP_DIR" 2>/dev/null || true
  fi
}

trap cleanup_temp EXIT

usage() {
  cat <<'EOF'
Usage:
  ./scripts/infisical-env.sh pull [dev|staging|prod|all]
  ./scripts/infisical-env.sh pull-all [dev|staging|prod|all]
  ./scripts/infisical-env.sh push <dev|staging|prod> --yes

pull defaults to dev and atomically replaces the mapped local env files.
push is an administrator operation that uploads existing mapped files.
EOF
}

fail() {
  printf 'Infisical env sync failed: %s\n' "$1" >&2
  exit 1
}

ACTION="${1:-pull}"
SELECTED_ENV="${2:-dev}"
CONFIRMATION="${3:-}"

case "$ACTION" in
  pull|pull-all|push) ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    fail "unsupported action '$ACTION'"
    ;;
esac

case "$SELECTED_ENV" in
  development) SELECTED_ENV="dev" ;;
  preview) SELECTED_ENV="staging" ;;
  production) SELECTED_ENV="prod" ;;
esac

case "$SELECTED_ENV" in
  dev|staging|prod) ;;
  all)
    test "$ACTION" != "push" || fail "push requires one explicit environment"
    ;;
  *)
    usage >&2
    fail "unsupported environment '$SELECTED_ENV'"
    ;;
esac

if test "$ACTION" = "push" && test "$CONFIRMATION" != "--yes"; then
  fail "push requires the explicit --yes confirmation"
fi

command -v infisical >/dev/null 2>&1 || fail "Infisical CLI is not installed"

if test "$ACTION" = "pull-all"; then
  WORKSPACE_ROOT="$(dirname "$REPO_ROOT")"
  workspace_repo_count=0
  for repo_script in "$WORKSPACE_ROOT"/*/scripts/infisical-env.sh; do
    test -x "$repo_script" || continue
    child_repo="$(cd "$(dirname "$repo_script")/.." && pwd)"
    printf '\n==> %s\n' "$(basename "$child_repo")"
    "$repo_script" pull "$SELECTED_ENV"
    workspace_repo_count=$((workspace_repo_count + 1))
  done
  test "$workspace_repo_count" -gt 0 || fail "no sibling repositories with Infisical sync were found"
  printf '\nInfisical workspace pull complete: %s repository/repositories.\n' "$workspace_repo_count"
  exit 0
fi

test -f "$REPO_ROOT/.infisical.json" || fail "missing tracked .infisical.json project link"
test -f "$MANIFEST_FILE" || fail "missing tracked .infisical-env manifest"

cd "$REPO_ROOT"

PROJECT_ID=""
INFISICAL_ACCESS_TOKEN=""
if test "$ACTION" = "push"; then
  command -v curl >/dev/null 2>&1 || fail "curl is required for administrator uploads"
  command -v jq >/dev/null 2>&1 || fail "jq is required for administrator uploads"
  PROJECT_ID="$(jq -r '.workspaceId // empty' "$REPO_ROOT/.infisical.json")"
  test -n "$PROJECT_ID" || fail "missing workspaceId in .infisical.json"
  INFISICAL_ACCESS_TOKEN="$(infisical user get token --silent --plain)"
  test -n "$INFISICAL_ACCESS_TOKEN" || fail "Infisical login is required for administrator uploads"
fi

synced_count=0

while IFS='|' read -r env_slug secret_path local_file extra_field; do
  case "$env_slug" in
    ''|'#'*) continue ;;
  esac

  test -z "${extra_field:-}" || fail "invalid manifest row for '$local_file'"
  case "$env_slug" in dev|staging|prod) ;; *) fail "invalid manifest environment '$env_slug'" ;; esac
  case "$secret_path" in /repos/*) ;; *) fail "invalid Infisical path '$secret_path'" ;; esac
  case "$local_file" in
    ''|/*|..|../*|*/../*|*/..) fail "unsafe local path '$local_file'" ;;
  esac

  if test "$SELECTED_ENV" != "all" && test "$SELECTED_ENV" != "$env_slug"; then
    continue
  fi

  if git -C "$REPO_ROOT" ls-files --error-unmatch -- "$local_file" >/dev/null 2>&1; then
    fail "refusing to overwrite tracked file '$local_file'"
  fi
  if ! git -C "$REPO_ROOT" check-ignore -q -- "$local_file"; then
    fail "mapped secret file is not gitignored: '$local_file'"
  fi

  target_file="$REPO_ROOT/$local_file"

  if test "$ACTION" = "pull"; then
    target_dir="$(dirname "$target_file")"
    test -d "$target_dir" || fail "target directory does not exist: '$target_dir'"
    TEMP_DIR="$(mktemp -d "$target_dir/.infisical-env.XXXXXX")"
    TEMP_FILE="$TEMP_DIR/payload.env"

    if ! infisical export --silent --env="$env_slug" --path="$secret_path" --format=dotenv --output-file="$TEMP_FILE" >/dev/null 2>&1; then
      cleanup_temp
      fail "could not pull '$local_file'"
    fi

    key_count="$(awk '/^[A-Za-z_][A-Za-z0-9_]*=/{count++} END{print count+0}' "$TEMP_FILE")"
    if test "$key_count" -eq 0; then
      cleanup_temp
      fail "remote path for '$local_file' contains no environment variables"
    fi

    chmod 600 "$TEMP_FILE"
    mv -f "$TEMP_FILE" "$target_file"
    cleanup_temp
    TEMP_FILE=""
    TEMP_DIR=""
    printf 'Pulled %s (%s variables)\n' "$local_file" "$key_count"
  else
    test -f "$target_file" || fail "local env file does not exist: '$local_file'"
    key_count="$(awk '/^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=/{count++} END{print count+0}' "$target_file")"
    test "$key_count" -gt 0 || fail "local env file has no variables: '$local_file'"

    invalid_line_count="$(awk '!/^[[:space:]]*($|#)/ && !/^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=/{count++} END{print count+0}' "$target_file")"
    test "$invalid_line_count" -eq 0 || fail "local env file contains unsupported lines: '$local_file'"

    if ! jq -Rn \
      --arg project_id "$PROJECT_ID" \
      --arg environment "$env_slug" \
      --arg secret_path "$secret_path" '
        def parse_value:
          if length >= 2 and startswith("\"") and endswith("\"") then fromjson
          elif length >= 2 and startswith("\u0027") and endswith("\u0027") then .[1:-1]
          else .
          end;
        {
          projectId: $project_id,
          environment: $environment,
          secretPath: $secret_path,
          mode: "upsert",
          secrets: [
            inputs
            | select(test("^\\s*(#|$)") | not)
            | capture("^\\s*(?:export\\s+)?(?<secretKey>[A-Za-z_][A-Za-z0-9_]*)\\s*=\\s*(?<rawValue>.*)$")
            | {
                secretKey: .secretKey,
                secretValue: (.rawValue | parse_value),
                skipMultilineEncoding: true
              }
          ]
        }
      ' "$target_file" | curl --fail --silent --show-error \
        --request PATCH \
        --url "https://app.infisical.com/api/v4/secrets/batch" \
        --header "Authorization: Bearer $INFISICAL_ACCESS_TOKEN" \
        --header "Content-Type: application/json" \
        --data-binary @- \
        --output /dev/null; then
      fail "could not push '$local_file'"
    fi
    printf 'Pushed %s (%s variables)\n' "$local_file" "$key_count"
  fi

  synced_count=$((synced_count + 1))
done < "$MANIFEST_FILE"

if test "$synced_count" -eq 0; then
  printf 'No managed env files are currently defined for %s.\n' "$SELECTED_ENV"
else
  printf 'Infisical %s complete: %s file(s).\n' "$ACTION" "$synced_count"
fi

from pathlib import Path
import subprocess
import json
import os
import sys

OBJECT_ORDER = {
    "tables": 1,
    "constraints": 2,
    "sequences": 3,
    "indexes": 4,
    "triggers": 5,
    "views": 6,
    "functions": 7,
    "procedures": 8,
    "packages": 9,
    "seed_data": 10,
    "changes": 11,
    "grants": 12,
    "synonyms": 13
}

# Tracked in git for reference but never deployed forward.
SKIP_FOLDERS = {"rollback"}

RELEASE_FILE    = "release.sql"
DEPLOYMENT_LIST = "deployment_list.txt"

MODE = os.getenv("DEPLOY_MODE", "VALIDATION")

print(f"MODE = {MODE}")

# =====================================================
# Get Changed Files
# =====================================================

if MODE == "VALIDATION":

    # Use BASE_REF env var passed from validate.yml
    # Matches what validate.yml "Show Changed Files" step uses:
    # git diff --name-only origin/${{ github.base_ref }} HEAD
    base_ref = os.getenv("BASE_REF", "main")

    changed_files = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base_ref}", "HEAD"]
    ).decode().splitlines()

    print("")
    print("===== CHANGED FILES =====")
    for f in changed_files:
        print(f)
    print("")

elif MODE == "DEPLOYMENT":

    # Only deploy files changed in this PR (HEAD vs its parent)
    changed_files = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD^1", "HEAD"]
    ).decode().splitlines()

    print("")
    print("===== CHANGED FILES (this PR) =====")
    for f in changed_files:
        print(f)
    print("")

elif MODE == "RECONCILE":

    # =====================================================
    # RECONCILE mode:
    # Scan the entire repo and cross-check against DynamoDB.
    # Deploys ALL files without a SUCCESS record.
    # Use this to catch up on files missed by previous deployments.
    # Triggered manually via workflow_dispatch.
    # =====================================================

    ENV_NAME      = os.getenv("ENV_NAME",      "PROD")
    HISTORY_TABLE = os.getenv("HISTORY_TABLE", "DB_DEPLOYMENT_HISTORY")

    print("")
    print(f"===== QUERYING DYNAMODB (env={ENV_NAME}) =====")

    query_result = subprocess.check_output([
        "aws", "dynamodb", "query",
        "--table-name", HISTORY_TABLE,
        "--key-condition-expression", "environment = :env",
        "--filter-expression",        "#s = :success",
        "--expression-attribute-names",  '{"#s":"status"}',
        "--expression-attribute-values",
            json.dumps({
                ":env":     {"S": ENV_NAME},
                ":success": {"S": "SUCCESS"}
            }),
        "--query",  "Items[].deployment_record.S",
        "--output", "json"
    ]).decode()

    deployed_files = set(json.loads(query_result))

    print(f"Already deployed : {len(deployed_files)} records")

    print("")
    print("===== SCANNING REPO =====")

    repo_sql_files = []

    for file_path in sorted(Path("database/app_schema").rglob("*.sql")):

        file_str = str(file_path).replace("\\", "/")
        parts    = Path(file_str).parts

        if len(parts) < 3:
            continue

        object_type = parts[2]

        if object_type in SKIP_FOLDERS:
            continue

        if object_type not in OBJECT_ORDER:
            raise Exception(f"Unsupported object folder: {object_type}")

        repo_sql_files.append((OBJECT_ORDER[object_type], file_str))

    print(f"Total SQL files in repo : {len(repo_sql_files)}")

    print("")
    print("===== PENDING FILES =====")

    pending = []
    for order, file_str in sorted(repo_sql_files):
        if file_str in deployed_files:
            print(f"  SKIP    : {file_str}")
        else:
            print(f"  PENDING : {file_str}")
            pending.append((order, file_str))

    print("")
    changed_files = [f for _, f in pending]

else:

    raise Exception(f"Unknown DEPLOY_MODE: {MODE}. Use VALIDATION, DEPLOYMENT or RECONCILE.")

# =====================================================
# Filter and sort SQL files (VALIDATION mode uses this too)
# =====================================================

sql_files = []

for file in changed_files:

    if (
        file.endswith(".sql")
        and file.startswith("database/app_schema/")
    ):

        parts = Path(file).parts

        if len(parts) < 3:
            continue

        object_type = parts[2]

        if object_type in SKIP_FOLDERS:
            continue

        if object_type not in OBJECT_ORDER:
            raise Exception(f"Unsupported object folder: {object_type}")

        order = OBJECT_ORDER[object_type]
        sql_files.append((order, file))

sql_files = list(set(sql_files))
sql_files.sort(key=lambda x: (x[0], x[1]))

# =====================================================
# Nothing to deploy
# =====================================================

if not sql_files:

    print("No SQL files pending deployment.")

    with open(RELEASE_FILE, "w") as f:
        f.write("-- No deployment required\n")

    with open(DEPLOYMENT_LIST, "w") as f:
        pass

    sys.exit(0)

# =====================================================
# Generate deployment_list.txt
# =====================================================

with open(DEPLOYMENT_LIST, "w") as f:
    for _, file in sql_files:
        f.write(file + "\n")

# =====================================================
# Generate release.sql
# =====================================================

with open(RELEASE_FILE, "w") as f:

    f.write("WHENEVER SQLERROR EXIT FAILURE\n\n")

    for _, file in sql_files:

        object_name = file.replace("database/app_schema/", "")

        f.write("PROMPT ==========================================\n")
        f.write(f"PROMPT Executing : {object_name}\n")
        f.write("PROMPT ==========================================\n\n")
        f.write(f"@@{file}\n\n")
        f.write(f"PROMPT SUCCESS : {object_name}\n\n")

print("")
print("====================================")
print("release.sql generated successfully.")
print("deployment_list.txt generated successfully.")
print(f"Scripts Found : {len(sql_files)}")
print("====================================")

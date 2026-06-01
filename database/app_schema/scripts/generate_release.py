from pathlib import Path
import subprocess

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
    "changes": 11
}

RELEASE_FILE = "release.sql"
DEPLOYMENT_LIST = "deployment_list.txt"

# =====================================================
# Get Changed Files
# =====================================================


MODE = os.getenv("DEPLOY_MODE", "VALIDATION")

print(f"MODE = {MODE}")

if MODE == "VALIDATION":

    base_branch = subprocess.check_output(
        ["git", "merge-base", "HEAD", "origin/main"]
    ).decode().strip()

    changed_files = subprocess.check_output(
        ["git", "diff", "--name-only", base_branch, "HEAD"]
    ).decode().splitlines()

else:

    changed_files = subprocess.check_output(
        [
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD"
        ]
    ).decode().splitlines()

print("")
print("===== CHANGED FILES =====")

for file in changed_files:
    print(file)

print("")

# =====================================================
# Filter SQL Files
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

        if object_type not in OBJECT_ORDER:

            raise Exception(
                f"Unsupported object folder: {object_type}"
            )

        order = OBJECT_ORDER[object_type]

        sql_files.append(
            (
                order,
                file
            )
        )

# =====================================================
# Remove Duplicates
# =====================================================

sql_files = list(set(sql_files))

# =====================================================
# Sort By Dependency Hierarchy
# =====================================================

sql_files.sort(
    key=lambda x: (
        x[0],
        x[1]
    )
)

# =====================================================
# Validate Deployment
# =====================================================

# if not sql_files:

#     raise Exception(
#         "No SQL files found for deployment."
#     )

if not sql_files:

    print("No SQL files found.")

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

        object_name = file.replace(
            "database/app_schema/",
            ""
        )

        f.write(
            "PROMPT ==========================================\n"
        )

        f.write(
            f"PROMPT Executing : {object_name}\n"
        )

        f.write(
            "PROMPT ==========================================\n\n"
        )

        f.write(
            f"@@{file}\n\n"
        )

        f.write(
            f"PROMPT SUCCESS : {object_name}\n\n"
        )

print("")
print("====================================")
print("release.sql generated successfully.")
print("deployment_list.txt generated successfully.")
print(f"Scripts Found : {len(sql_files)}")
print("====================================")




# from pathlib import Path
# import subprocess

# OBJECT_ORDER = {
#     "tables": 1,
#     "constraints": 2,
#     "sequences": 3,
#     "indexes": 4,
#     "triggers": 5,
#     "views": 6,
#     "functions": 7,
#     "procedures": 8,
#     "packages": 9,
#     "seed_data": 10,
#     "changes": 11
# }

# RELEASE_FILE = "release.sql"

# # =====================================================
# # Get Changed Files
# # =====================================================

# before = subprocess.check_output(
#     ["git", "rev-parse", "HEAD~1"]
# ).decode().strip()

# after = subprocess.check_output(
#     ["git", "rev-parse", "HEAD"]
# ).decode().strip()

# changed_files = subprocess.check_output(
#     ["git", "diff", "--name-only", before, after]
# ).decode().splitlines()

# # =====================================================
# # Filter SQL Files
# # =====================================================

# sql_files = []

# for file in changed_files:

#     if file.endswith(".sql"):

#         parts = Path(file).parts

#         if len(parts) >= 3:

#             object_type = parts[2]

#             order = OBJECT_ORDER.get(object_type, 999)

#             sql_files.append((order, file))

# # =====================================================
# # Sort By Dependency Hierarchy
# # =====================================================

# sql_files.sort(key=lambda x: x[0])

# # =====================================================
# # Generate release.sql
# # =====================================================

# with open(RELEASE_FILE, "w") as f:

#     f.write("WHENEVER SQLERROR EXIT FAILURE\n\n")

#     for _, file in sql_files:

#         object_name = file.replace("database/app_schema/", "")

#         f.write("PROMPT ==========================================\n")
#         f.write(f"PROMPT Executing : {object_name}\n")
#         f.write("PROMPT ==========================================\n\n")

#         f.write(f"@@{file}\n\n")

#         f.write(f"PROMPT SUCCESS : {object_name}\n\n")

# print("release.sql generated successfully.")
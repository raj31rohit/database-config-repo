from pathlib import Path
import subprocess

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

# =====================================================
# Get Changed Files
# =====================================================

before = subprocess.check_output(
    ["git", "rev-parse", "HEAD~1"]
).decode().strip()

after = subprocess.check_output(
    ["git", "rev-parse", "HEAD"]
).decode().strip()

changed_files = subprocess.check_output(
    ["git", "diff", "--name-only", before, after]
).decode().splitlines()

# =====================================================
# Filter SQL Files
# =====================================================

sql_files = []

for file in changed_files:

    if file.endswith(".sql"):

        parts = Path(file).parts

        if len(parts) >= 3:

            object_type = parts[2]

            order = OBJECT_ORDER.get(object_type, 999)

            sql_files.append((order, file))

# =====================================================
# Sort By Dependency Hierarchy
# =====================================================

sql_files.sort(key=lambda x: x[0])

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

print("release.sql generated successfully.")
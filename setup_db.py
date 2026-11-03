"""
Database migration & setup runner
File: setup_db.py
Executes 01_schema.sql, 02_procedures.sql, 03_triggers_views.sql, and 04_sample_data.sql.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "bank_db")

def run_sql_file(file_path: str, use_db: bool = True):
    print(f"Executing {file_path}...")
    cmd = [
        "mysql",
        f"-h{DB_HOST}",
        f"-P{DB_PORT}",
        f"-u{DB_USER}",
    ]
    if DB_PASSWORD:
        cmd.append(f"--password={DB_PASSWORD}")
    if use_db:
        cmd.append(DB_NAME)

    with open(file_path, "r", encoding="utf-8") as f:
        res = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
    
    if res.returncode != 0:
        print(f"Error executing {file_path}:")
        print(res.stderr)
        return False
    print(f"Successfully executed {file_path}.")
    return True

def main():
    if not os.path.exists(".env"):
        print("Error: .env file not found. Please create .env from .env.example with your DB_PASSWORD.")
        sys.exit(1)

    print("Step 1: Running sql/01_schema.sql...")
    if not run_sql_file("sql/01_schema.sql", use_db=False):
        sys.exit(1)

    print("Step 2: Running sql/02_procedures.sql...")
    if not run_sql_file("sql/02_procedures.sql", use_db=True):
        sys.exit(1)

    print("Step 3: Running sql/03_triggers_views.sql...")
    if not run_sql_file("sql/03_triggers_views.sql", use_db=True):
        sys.exit(1)

    print("Step 4: Running sql/04_sample_data.sql...")
    if not run_sql_file("sql/04_sample_data.sql", use_db=True):
        sys.exit(1)

    print("\nAll database scripts executed successfully!")

if __name__ == "__main__":
    main()

import sqlite3


DATABASE_PATH = "database/ai_evaluation.db"


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    return any(column[1] == column_name for column in columns)


def run_migrations():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    if not column_exists(cursor, "evaluations", "provider"):
        cursor.execute("""
            ALTER TABLE evaluations
            ADD COLUMN provider TEXT DEFAULT 'openai'
        """)

    if not column_exists(cursor, "evaluations", "model"):
        cursor.execute("""
            ALTER TABLE evaluations
            ADD COLUMN model TEXT DEFAULT 'gpt-4.1-mini'
        """)

    conn.commit()
    conn.close()

    print("Database migrations completed successfully")


if __name__ == "__main__":
    run_migrations()
import sqlite3

conn = sqlite3.connect(
    "database/ai_evaluation.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    prompt TEXT,
    keyword_score INTEGER,
    judge_score INTEGER,
    accuracy INTEGER,
    clarity INTEGER,
    completeness INTEGER,
    approved INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")
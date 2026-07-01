import sqlite3


DATABASE_PATH = "database/ai_evaluation.db"


def save_evaluation_to_db(report):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    evaluation = report["evaluation"]
    llm_judge = report.get("llm_judge") or {}

    cursor.execute(
        """
        INSERT INTO evaluations (
            timestamp,
            prompt,
            keyword_score,
            judge_score,
            accuracy,
            clarity,
            completeness,
            approved,
            provider,
            model
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            report["timestamp"],
            report["prompt"],
            evaluation["score"],
            llm_judge.get("score"),
            llm_judge.get("accuracy"),
            llm_judge.get("clarity"),
            llm_judge.get("completeness"),
            1 if evaluation["approved"] else 0,
            report.get("provider", "openai"),
            report.get("model", "gpt-4.1-mini")
        )
    )

    conn.commit()
    conn.close()
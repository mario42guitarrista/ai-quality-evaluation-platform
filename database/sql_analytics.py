import sqlite3


DATABASE_PATH = "database/ai_evaluation.db"


def get_average_judge_score():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ROUND(AVG(judge_score), 2)
        FROM evaluations
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result


def get_best_prompts():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT prompt,
               judge_score
        FROM evaluations
        ORDER BY judge_score DESC
        LIMIT 5
    """)

    results = cursor.fetchall()

    conn.close()

    return results


def get_approval_rate():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ROUND(
            AVG(approved) * 100,
            2
        )
        FROM evaluations
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result


if __name__ == "__main__":

    print(
        "\nAverage Judge Score:"
    )

    print(
        get_average_judge_score()
    )

    print(
        "\nApproval Rate:"
    )

    print(
        get_approval_rate()
    )

    print(
        "\nTop Prompts:"
    )

    for item in get_best_prompts():
        print(item)
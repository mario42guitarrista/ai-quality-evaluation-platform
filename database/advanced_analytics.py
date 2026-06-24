import sqlite3


DATABASE_PATH = "database/ai_evaluation.db"


def execute_query(query):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result


def get_best_prompt():
    return execute_query("""
        SELECT prompt,
               ROUND(AVG(judge_score), 2) AS avg_score
        FROM evaluations
        GROUP BY prompt
        ORDER BY avg_score DESC
        LIMIT 1
    """)


def get_worst_prompt():
    return execute_query("""
        SELECT prompt,
               ROUND(AVG(judge_score), 2) AS avg_score
        FROM evaluations
        GROUP BY prompt
        ORDER BY avg_score ASC
        LIMIT 1
    """)


def get_average_accuracy():
    return execute_query("""
        SELECT ROUND(AVG(accuracy), 2)
        FROM evaluations
    """)


def get_average_clarity():
    return execute_query("""
        SELECT ROUND(AVG(clarity), 2)
        FROM evaluations
    """)


def get_average_completeness():
    return execute_query("""
        SELECT ROUND(AVG(completeness), 2)
        FROM evaluations
    """)


def get_prompt_leaderboard():
    return execute_query("""
        SELECT prompt,
               ROUND(AVG(judge_score), 2) AS avg_score,
               COUNT(*) AS executions
        FROM evaluations
        GROUP BY prompt
        ORDER BY avg_score DESC
    """)


if __name__ == "__main__":
    print("\nADVANCED SQL ANALYTICS\n")

    print("Best Prompt:")
    print(get_best_prompt())

    print("\nWorst Prompt:")
    print(get_worst_prompt())

    print("\nAverage Accuracy:")
    print(get_average_accuracy())

    print("\nAverage Clarity:")
    print(get_average_clarity())

    print("\nAverage Completeness:")
    print(get_average_completeness())

    print("\nPrompt Leaderboard:")
    for item in get_prompt_leaderboard():
        print(item)
import sqlite3


DATABASE_PATH = "database/ai_evaluation.db"


def execute_query(query):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    return result


def get_dashboard_metrics():
    total = execute_query("""
        SELECT COUNT(*)
        FROM evaluations
    """)[0][0]

    approved = execute_query("""
        SELECT COUNT(*)
        FROM evaluations
        WHERE approved = 1
    """)[0][0]

    failed = total - approved

    approval_rate = execute_query("""
        SELECT ROUND(AVG(approved) * 100, 2)
        FROM evaluations
    """)[0][0]

    keyword_avg_score = execute_query("""
        SELECT ROUND(AVG(keyword_score), 2)
        FROM evaluations
    """)[0][0]

    judge_avg_score = execute_query("""
        SELECT ROUND(AVG(judge_score), 2)
        FROM evaluations
    """)[0][0]

    best_score = execute_query("""
        SELECT MAX(judge_score)
        FROM evaluations
    """)[0][0]

    lowest_score = execute_query("""
        SELECT MIN(judge_score)
        FROM evaluations
    """)[0][0]

    return {
        "total": total,
        "approved": approved,
        "failed": failed,
        "approval_rate": approval_rate,
        "keyword_avg_score": keyword_avg_score,
        "judge_avg_score": judge_avg_score,
        "best_score": best_score,
        "lowest_score": lowest_score,
    }


def get_top_prompts(limit=5):
    return execute_query(f"""
        SELECT prompt,
               judge_score,
               accuracy,
               clarity,
               completeness
        FROM evaluations
        ORDER BY judge_score DESC
        LIMIT {limit}
    """)


def get_evaluation_details(limit=20):
    return execute_query(f"""
        SELECT timestamp,
               prompt,
               keyword_score,
               approved,
               judge_score,
               accuracy,
               clarity,
               completeness
        FROM evaluations
        ORDER BY id DESC
        LIMIT {limit}
    """)


if __name__ == "__main__":
    print(get_dashboard_metrics())
    print(get_top_prompts())
    print(get_evaluation_details())
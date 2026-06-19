import json
import os
import matplotlib.pyplot as plt


REPORTS_PATH = "reports/evaluations"


def load_scores():

    scores = []

    files = sorted(os.listdir(REPORTS_PATH))

    for file_name in files:

        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(REPORTS_PATH, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            report = json.load(file)

        llm_judge = report.get("llm_judge")

        if llm_judge:
            scores.append(llm_judge["score"])

    return scores


def generate_chart():

    scores = load_scores()

    if not scores:
        print("No scores found.")
        return

    plt.figure(figsize=(10, 5))

    plt.plot(
        range(1, len(scores) + 1),
        scores,
        marker="o"
    )

    plt.title("Judge Score Trend")

    plt.xlabel("Execution")

    plt.ylabel("Judge Score")

    plt.grid(True)

    os.makedirs("dashboard/assets", exist_ok=True)

    output_file = "dashboard/assets/judge_score_trend.png"

    plt.savefig(output_file)

    print(f"Chart generated: {output_file}")


if __name__ == "__main__":
    generate_chart()
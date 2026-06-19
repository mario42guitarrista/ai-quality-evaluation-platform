import json
import os


def load_reports():
    reports = []

    reports_path = "reports/evaluations"

    for file_name in os.listdir(reports_path):

        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(reports_path, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            reports.append(json.load(file))

    return reports


def generate_prompt_ranking():

    reports = load_reports()

    ranking = []

    for report in reports:

        llm_judge = report.get("llm_judge")

        if not llm_judge:
            continue

        ranking.append({
            "prompt": report["prompt"],
            "judge_score": llm_judge["score"]
        })

    ranking.sort(
        key=lambda x: x["judge_score"],
        reverse=True
    )

    return ranking


if __name__ == "__main__":

    ranking = generate_prompt_ranking()

    print("\nPROMPT BENCHMARK RANKING\n")

    for position, item in enumerate(ranking, start=1):

        print(
            f"{position}. "
            f"{item['prompt']} "
            f"(Judge Score: {item['judge_score']})"
        )
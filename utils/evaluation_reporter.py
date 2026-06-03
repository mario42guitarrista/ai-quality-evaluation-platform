import json
import os
from datetime import datetime


def save_evaluation_report(prompt, response, evaluation, llm_judge=None):
    os.makedirs("reports/evaluations", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "timestamp": timestamp,
        "prompt": prompt,
        "response": response,
        "evaluation": evaluation,
        "llm_judge": llm_judge
    }

    file_path = f"reports/evaluations/evaluation_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    return file_path
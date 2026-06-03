import json
import os


def load_evaluation_reports():
    reports_path = "reports/evaluations"

    if not os.path.exists(reports_path):
        return []

    reports = []

    for file_name in os.listdir(reports_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(reports_path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                reports.append(json.load(file))

    return reports


def calculate_metrics(reports):
    total = len(reports)

    if total == 0:
        return {
            "total": 0,
            "approved": 0,
            "failed": 0,
            "average_score": 0,
            "approval_rate": 0,
            "best_score": 0,
            "lowest_score": 0,
            "average_judge_score": 0,
        }

    approved = sum(1 for report in reports if report["evaluation"]["approved"])
    failed = total - approved

    scores = [report["evaluation"]["score"] for report in reports]

    judge_scores = [
        report["llm_judge"]["score"]
        for report in reports
        if report.get("llm_judge")
    ]

    average_score = round(sum(scores) / total, 2)
    approval_rate = round((approved / total) * 100, 2)
    best_score = max(scores)
    lowest_score = min(scores)

    average_judge_score = 0
    if judge_scores:
        average_judge_score = round(sum(judge_scores) / len(judge_scores), 2)

    return {
        "total": total,
        "approved": approved,
        "failed": failed,
        "average_score": average_score,
        "approval_rate": approval_rate,
        "best_score": best_score,
        "lowest_score": lowest_score,
        "average_judge_score": average_judge_score,
    }


def generate_dashboard():
    reports = load_evaluation_reports()
    metrics = calculate_metrics(reports)

    html = f"""
    <html>
    <head>
        <title>AI Evaluation Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #0f172a;
                color: white;
                padding: 40px;
            }}

            h1 {{
                color: #38bdf8;
                margin-bottom: 8px;
            }}

            .subtitle {{
                color: #cbd5e1;
                font-size: 18px;
            }}

            .badge {{
                display: inline-block;
                background-color: #1e40af;
                color: white;
                padding: 8px 14px;
                border-radius: 20px;
                font-weight: bold;
                margin-top: 12px;
                margin-right: 10px;
            }}

            .cards {{
                display: flex;
                gap: 20px;
                margin-top: 30px;
                flex-wrap: wrap;
            }}

            .card {{
                background-color: #1e293b;
                padding: 24px;
                border-radius: 14px;
                width: 220px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.25);
            }}

            .label {{
                color: #94a3b8;
                font-size: 16px;
                margin-bottom: 10px;
            }}

            .value {{
                font-size: 36px;
                font-weight: bold;
            }}

            .success {{
                color: #22c55e;
            }}

            .danger {{
                color: #ef4444;
            }}

            .info {{
                color: #38bdf8;
            }}

            .warning {{
                color: #f59e0b;
            }}

            table {{
                width: 100%;
                margin-top: 40px;
                border-collapse: collapse;
                background-color: #1e293b;
                border-radius: 12px;
                overflow: hidden;
                font-size: 14px;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #334155;
                text-align: left;
                vertical-align: top;
            }}

            th {{
                background-color: #1e40af;
            }}

            .approved {{
                color: #22c55e;
                font-weight: bold;
            }}

            .failed {{
                color: #ef4444;
                font-weight: bold;
            }}

            .comments {{
                max-width: 420px;
                color: #cbd5e1;
            }}
        </style>
    </head>

    <body>
        <h1>AI Quality Evaluation Dashboard</h1>

        <p class="subtitle">
            LLM response evaluation summary based on generated JSON reports.
        </p>

        <div class="badge">Evaluation Type: Context-Aware</div>
        <div class="badge">LLM-as-a-Judge Enabled</div>

        <div class="cards">
            <div class="card">
                <div class="label">Total Evaluations</div>
                <div class="value info">{metrics["total"]}</div>
            </div>

            <div class="card">
                <div class="label">Approved</div>
                <div class="value success">{metrics["approved"]}</div>
            </div>

            <div class="card">
                <div class="label">Failed</div>
                <div class="value danger">{metrics["failed"]}</div>
            </div>

            <div class="card">
                <div class="label">Keyword Avg Score</div>
                <div class="value info">{metrics["average_score"]}</div>
            </div>

            <div class="card">
                <div class="label">Judge Avg Score</div>
                <div class="value success">{metrics["average_judge_score"]}</div>
            </div>

            <div class="card">
                <div class="label">Approval Rate</div>
                <div class="value success">{metrics["approval_rate"]}%</div>
            </div>

            <div class="card">
                <div class="label">Best Keyword Score</div>
                <div class="value success">{metrics["best_score"]}</div>
            </div>

            <div class="card">
                <div class="label">Lowest Keyword Score</div>
                <div class="value warning">{metrics["lowest_score"]}</div>
            </div>
        </div>

        <table>
            <tr>
                <th>Timestamp</th>
                <th>Prompt</th>
                <th>Keyword Score</th>
                <th>Status</th>
                <th>Judge Score</th>
                <th>Accuracy</th>
                <th>Clarity</th>
                <th>Completeness</th>
                <th>Judge Comments</th>
            </tr>
    """

    for report in reports:
        status_class = "approved" if report["evaluation"]["approved"] else "failed"
        status_text = "APPROVED" if report["evaluation"]["approved"] else "FAILED"

        llm_judge = report.get("llm_judge") or {}

        judge_score = llm_judge.get("score", "-")
        accuracy = llm_judge.get("accuracy", "-")
        clarity = llm_judge.get("clarity", "-")
        completeness = llm_judge.get("completeness", "-")
        comments = llm_judge.get("comments", "-")

        html += f"""
            <tr>
                <td>{report["timestamp"]}</td>
                <td>{report["prompt"]}</td>
                <td>{report["evaluation"]["score"]}/{report["evaluation"]["total_keywords"]}</td>
                <td class="{status_class}">{status_text}</td>
                <td>{judge_score}/10</td>
                <td>{accuracy}</td>
                <td>{clarity}</td>
                <td>{completeness}</td>
                <td class="comments">{comments}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    os.makedirs("dashboard", exist_ok=True)

    output_path = "dashboard/evaluation_dashboard.html"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Dashboard generated: {output_path}")


if __name__ == "__main__":
    generate_dashboard()
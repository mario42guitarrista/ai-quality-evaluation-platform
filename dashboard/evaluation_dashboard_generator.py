import json
import os


EVALUATION_REPORTS_PATH = "reports/evaluations"
MODEL_BENCHMARKS_PATH = "reports/model_benchmarks"
OUTPUT_PATH = "dashboard/evaluation_dashboard.html"


def load_json_reports(folder_path):
    if not os.path.exists(folder_path):
        return []

    reports = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                reports.append(json.load(file))

    return reports


def load_evaluation_reports():
    return load_json_reports(EVALUATION_REPORTS_PATH)


def load_model_benchmark_reports():
    return load_json_reports(MODEL_BENCHMARKS_PATH)


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

    keyword_scores = [report["evaluation"]["score"] for report in reports]

    judge_scores = [
        report["llm_judge"]["score"]
        for report in reports
        if report.get("llm_judge")
    ]

    return {
        "total": total,
        "approved": approved,
        "failed": failed,
        "average_score": round(sum(keyword_scores) / total, 2),
        "approval_rate": round((approved / total) * 100, 2),
        "best_score": max(keyword_scores),
        "lowest_score": min(keyword_scores),
        "average_judge_score": round(sum(judge_scores) / len(judge_scores), 2)
        if judge_scores
        else 0,
    }


def generate_prompt_ranking(reports):
    ranking = []

    for report in reports:
        llm_judge = report.get("llm_judge")

        if not llm_judge:
            continue

        ranking.append({
            "prompt": report["prompt"],
            "judge_score": llm_judge.get("score", "-"),
            "accuracy": llm_judge.get("accuracy", "-"),
            "clarity": llm_judge.get("clarity", "-"),
            "completeness": llm_judge.get("completeness", "-"),
        })

    ranking.sort(
        key=lambda item: item["judge_score"]
        if isinstance(item["judge_score"], int)
        else 0,
        reverse=True
    )

    return ranking


def build_header(metrics):
    return f"""
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

            h2 {{
                color: #38bdf8;
                margin-top: 50px;
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
                margin-top: 24px;
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

            .chart {{
                margin-top: 20px;
                margin-bottom: 40px;
            }}

            .chart img {{
                width: 100%;
                max-width: 1000px;
                border-radius: 12px;
                background: white;
                padding: 10px;
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
        <div class="badge">Prompt Benchmark Ranking Enabled</div>
        <div class="badge">Model Benchmark Enabled</div>

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
    """


def build_evaluation_details_table(reports):
    html = """
        <h2>Evaluation Details</h2>

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
        evaluation = report["evaluation"]
        llm_judge = report.get("llm_judge") or {}

        status_class = "approved" if evaluation["approved"] else "failed"
        status_text = "APPROVED" if evaluation["approved"] else "FAILED"

        html += f"""
            <tr>
                <td>{report["timestamp"]}</td>
                <td>{report["prompt"]}</td>
                <td>{evaluation["score"]}/{evaluation["total_keywords"]}</td>
                <td class="{status_class}">{status_text}</td>
                <td>{llm_judge.get("score", "-")}/10</td>
                <td>{llm_judge.get("accuracy", "-")}</td>
                <td>{llm_judge.get("clarity", "-")}</td>
                <td>{llm_judge.get("completeness", "-")}</td>
                <td class="comments">{llm_judge.get("comments", "-")}</td>
            </tr>
        """

    html += """
        </table>
    """

    return html


def build_trend_chart_section():
    return """
        <h2>Judge Score Trend</h2>

        <div class="chart">
            <img
                src="assets/judge_score_trend.png"
                alt="Judge Score Trend"
            >
        </div>
    """


def build_prompt_ranking_table(ranking):
    html = """
        <h2>Prompt Benchmark Ranking</h2>

        <table>
            <tr>
                <th>Rank</th>
                <th>Prompt</th>
                <th>Judge Score</th>
                <th>Accuracy</th>
                <th>Clarity</th>
                <th>Completeness</th>
            </tr>
    """

    for position, item in enumerate(ranking, start=1):
        html += f"""
            <tr>
                <td>{position}</td>
                <td>{item["prompt"]}</td>
                <td>{item["judge_score"]}/10</td>
                <td>{item["accuracy"]}</td>
                <td>{item["clarity"]}</td>
                <td>{item["completeness"]}</td>
            </tr>
        """

    html += """
        </table>
    """

    return html


def build_model_benchmark_table(benchmark_reports):
    html = """
        <h2>Model Benchmark Ranking</h2>

        <table>
            <tr>
                <th>Timestamp</th>
                <th>Model</th>
                <th>Judge Score</th>
                <th>Accuracy</th>
                <th>Clarity</th>
                <th>Completeness</th>
            </tr>
    """

    for benchmark_report in benchmark_reports:
        timestamp = benchmark_report["timestamp"]

        for result in benchmark_report["results"]:
            html += f"""
                <tr>
                    <td>{timestamp}</td>
                    <td>{result["model"]}</td>
                    <td>{result["judge_score"]}/10</td>
                    <td>{result["accuracy"]}</td>
                    <td>{result["clarity"]}</td>
                    <td>{result["completeness"]}</td>
                </tr>
            """

    html += """
        </table>
    """

    return html


def generate_dashboard():
    reports = load_evaluation_reports()
    benchmark_reports = load_model_benchmark_reports()

    metrics = calculate_metrics(reports)
    prompt_ranking = generate_prompt_ranking(reports)

    html = build_header(metrics)
    html += build_evaluation_details_table(reports)
    html += build_trend_chart_section()
    html += build_prompt_ranking_table(prompt_ranking)
    html += build_model_benchmark_table(benchmark_reports)

    html += """
    </body>
    </html>
    """

    os.makedirs("dashboard", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"Dashboard generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_dashboard()
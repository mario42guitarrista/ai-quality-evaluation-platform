import json
import os

from database.dashboard_queries import (
    get_dashboard_metrics,
    get_top_prompts,
    get_evaluation_details
)

MODEL_BENCHMARKS_PATH = "reports/model_benchmarks"
OUTPUT_PATH = "dashboard/evaluation_dashboard.html"


def load_model_benchmark_reports():
    if not os.path.exists(MODEL_BENCHMARKS_PATH):
        return []

    reports = []

    for file_name in os.listdir(MODEL_BENCHMARKS_PATH):
        if file_name.endswith(".json"):
            file_path = os.path.join(MODEL_BENCHMARKS_PATH, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                reports.append(json.load(file))

    return reports


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
            h1, h2 {{
                color: #38bdf8;
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
            .success {{ color: #22c55e; }}
            .danger {{ color: #ef4444; }}
            .info {{ color: #38bdf8; }}
            .warning {{ color: #f59e0b; }}
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
            Dashboard powered by SQLite and SQL Analytics.
        </p>

        <div class="badge">SQLite Enabled</div>
        <div class="badge">SQL Analytics Enabled</div>
        <div class="badge">LLM-as-a-Judge Enabled</div>
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
                <div class="value info">{metrics["keyword_avg_score"]}</div>
            </div>

            <div class="card">
                <div class="label">Judge Avg Score</div>
                <div class="value success">{metrics["judge_avg_score"]}</div>
            </div>

            <div class="card">
                <div class="label">Approval Rate</div>
                <div class="value success">{metrics["approval_rate"]}%</div>
            </div>

            <div class="card">
                <div class="label">Best Judge Score</div>
                <div class="value success">{metrics["best_score"]}</div>
            </div>

            <div class="card">
                <div class="label">Lowest Judge Score</div>
                <div class="value warning">{metrics["lowest_score"]}</div>
            </div>
        </div>
    """


def build_evaluation_details_table(evaluation_details):
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
            </tr>
    """

    for row in evaluation_details:
        timestamp, prompt, keyword_score, approved, judge_score, accuracy, clarity, completeness = row

        status_class = "approved" if approved == 1 else "failed"
        status_text = "APPROVED" if approved == 1 else "FAILED"

        html += f"""
            <tr>
                <td>{timestamp}</td>
                <td>{prompt}</td>
                <td>{keyword_score}</td>
                <td class="{status_class}">{status_text}</td>
                <td>{judge_score}/10</td>
                <td>{accuracy}</td>
                <td>{clarity}</td>
                <td>{completeness}</td>
            </tr>
        """

    html += "</table>"
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


def build_prompt_ranking_table(top_prompts):
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

    for position, row in enumerate(top_prompts, start=1):
        prompt, judge_score, accuracy, clarity, completeness = row

        html += f"""
            <tr>
                <td>{position}</td>
                <td>{prompt}</td>
                <td>{judge_score}/10</td>
                <td>{accuracy}</td>
                <td>{clarity}</td>
                <td>{completeness}</td>
            </tr>
        """

    html += "</table>"
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

    html += "</table>"
    return html


def generate_dashboard():
    metrics = get_dashboard_metrics()
    top_prompts = get_top_prompts()
    evaluation_details = get_evaluation_details()
    benchmark_reports = load_model_benchmark_reports()

    html = build_header(metrics)
    html += build_evaluation_details_table(evaluation_details)
    html += build_trend_chart_section()
    html += build_prompt_ranking_table(top_prompts)
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
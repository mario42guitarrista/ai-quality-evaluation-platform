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


def generate_dashboard():
    reports = load_evaluation_reports()

    total = len(reports)
    approved = sum(1 for report in reports if report["evaluation"]["approved"])
    failed = total - approved

    average_score = 0

    if total > 0:
        total_score = sum(report["evaluation"]["score"] for report in reports)
        average_score = round(total_score / total, 2)

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

            table {{
                width: 100%;
                margin-top: 40px;
                border-collapse: collapse;
                background-color: #1e293b;
                border-radius: 12px;
                overflow: hidden;
            }}

            th, td {{
                padding: 14px;
                border-bottom: 1px solid #334155;
                text-align: left;
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
        </style>
    </head>
    <body>
        <h1>AI Quality Evaluation Dashboard</h1>
        <p>LLM response evaluation summary based on generated JSON reports.</p>

        <div class="cards">
            <div class="card">
                <div class="label">Total Evaluations</div>
                <div class="value info">{total}</div>
            </div>

            <div class="card">
                <div class="label">Approved</div>
                <div class="value success">{approved}</div>
            </div>

            <div class="card">
                <div class="label">Failed</div>
                <div class="value danger">{failed}</div>
            </div>

            <div class="card">
                <div class="label">Average Score</div>
                <div class="value info">{average_score}</div>
            </div>
        </div>

        <table>
            <tr>
                <th>Timestamp</th>
                <th>Prompt</th>
                <th>Score</th>
                <th>Status</th>
                <th>Matched Keywords</th>
            </tr>
    """

    for report in reports:
        status_class = "approved" if report["evaluation"]["approved"] else "failed"
        status_text = "APPROVED" if report["evaluation"]["approved"] else "FAILED"

        matched_keywords = ", ".join(report["evaluation"]["matched_keywords"])

        html += f"""
            <tr>
                <td>{report["timestamp"]}</td>
                <td>{report["prompt"]}</td>
                <td>{report["evaluation"]["score"]}/{report["evaluation"]["total_keywords"]}</td>
                <td class="{status_class}">{status_text}</td>
                <td>{matched_keywords}</td>
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
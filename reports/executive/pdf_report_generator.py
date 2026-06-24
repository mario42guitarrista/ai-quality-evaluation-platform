from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from datetime import datetime
import json
import os


REPORT_PATH = "reports/executive/AI_Evaluation_Report.pdf"
TREND_CHART_PATH = "dashboard/assets/judge_score_trend.png"


def load_reports():
    reports = []
    path = "reports/evaluations"

    if not os.path.exists(path):
        return reports

    for file_name in os.listdir(path):
        if file_name.endswith(".json"):
            with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
                reports.append(json.load(file))

    return reports


def load_model_benchmarks():
    reports = []
    path = "reports/model_benchmarks"

    if not os.path.exists(path):
        return reports

    for file_name in os.listdir(path):
        if file_name.endswith(".json"):
            with open(os.path.join(path, file_name), "r", encoding="utf-8") as file:
                reports.append(json.load(file))

    return reports


def create_table(data):
    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3b73")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f4f6f8")),
    ]))

    return table


def generate_pdf():
    reports = load_reports()
    benchmark_reports = load_model_benchmarks()

    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(REPORT_PATH)
    content = []

    content.append(Paragraph("AI Quality Evaluation Platform", styles["Title"]))
    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Generated at: {datetime.now()}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    reports_with_judge = [
        report for report in reports if report.get("llm_judge")
    ]

    total = len(reports)

    approved = sum(
        1 for report in reports if report["evaluation"]["approved"]
    )

    approval_rate = round((approved / total) * 100, 2) if total > 0 else 0

    judge_scores = [
        report["llm_judge"]["score"]
        for report in reports_with_judge
    ]

    avg_judge = round(sum(judge_scores) / len(judge_scores), 2) if judge_scores else 0

    content.append(Paragraph("Executive Summary", styles["Heading1"]))

    summary_data = [
        ["Metric", "Value"],
        ["Total Evaluations", total],
        ["Approved", approved],
        ["Approval Rate", f"{approval_rate}%"],
        ["Average Judge Score", avg_judge],
    ]

    content.append(create_table(summary_data))
    content.append(Spacer(1, 24))

    if os.path.exists(TREND_CHART_PATH):
        content.append(Paragraph("Judge Score Trend", styles["Heading1"]))

        content.append(
            Image(
                TREND_CHART_PATH,
                width=500,
                height=250
            )
        )

        content.append(Spacer(1, 24))

    content.append(Paragraph("Prompt Ranking", styles["Heading1"]))

    sorted_reports = sorted(
        reports_with_judge,
        key=lambda x: x["llm_judge"]["score"],
        reverse=True
    )

    prompt_table = [
        ["Rank", "Prompt", "Judge Score", "Accuracy", "Clarity", "Completeness"]
    ]

    for position, report in enumerate(sorted_reports[:5], start=1):
        judge = report["llm_judge"]

        prompt_table.append([
            position,
            report["prompt"],
            judge["score"],
            judge["accuracy"],
            judge["clarity"],
            judge["completeness"],
        ])

    content.append(create_table(prompt_table))
    content.append(PageBreak())

    content.append(Paragraph("Model Benchmark", styles["Heading1"]))

    model_table = [
        ["Model", "Judge Score", "Accuracy", "Clarity", "Completeness"]
    ]

    for benchmark in benchmark_reports:
        for model in benchmark["results"]:
            model_table.append([
                model["model"],
                model["judge_score"],
                model["accuracy"],
                model["clarity"],
                model["completeness"],
            ])

    content.append(create_table(model_table))

    pdf.build(content)

    print(f"PDF generated: {REPORT_PATH}")


if __name__ == "__main__":
    generate_pdf()
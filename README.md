# AI Quality Evaluation Platform

An AI Quality Engineering platform designed to evaluate, benchmark, monitor, and report the quality of Large Language Model (LLM) responses.

This project simulates a real-world AI Quality Engineering workflow by combining automated prompt evaluation, semantic assessment using LLM-as-a-Judge, benchmarking, SQL analytics, dashboards, executive reporting, and CI/CD automation.

The primary goal is not only to consume AI models, but to build an engineering platform capable of continuously measuring, comparing, and improving the quality of AI-generated responses using software engineering best practices.

---

## Project Goals

The platform aims to:

- Evaluate AI-generated responses using both keyword-based and semantic evaluation.
- Benchmark multiple LLM models using standardized prompts.
- Store historical evaluation data for SQL analytics.
- Generate dashboards and executive reports automatically.
- Apply AI Quality Engineering and Observability concepts.
- Simulate production-grade software engineering practices.

---

# Roadmap

## Completed

- OpenAI Integration
- Context-Aware Evaluation
- LLM-as-a-Judge
- Prompt Benchmark
- Model Benchmark
- SQLite Analytics
- SQL Dashboard
- Executive PDF Reports
- GitHub Actions CI/CD
- Provider-Based Architecture

## In Progress

- Multi-Provider Support

## Planned

- Gemini Provider
- Claude Provider
- Ollama Provider
- Latency Analytics
- Cost Analytics
- REST API
- Docker Deployment
- Streamlit Dashboard

---

## Key Features

## OpenAI Integration

- Integration with OpenAI API
- Automatic prompt execution
- AI-generated responses

---

# Technology Stack

- Python
- OpenAI API
- SQLite
- SQL
- Pytest
- ReportLab
- Matplotlib
- HTML
- CSS
- GitHub Actions
- JSON

---

## Provider-Based Architecture

The platform now uses a provider abstraction layer that decouples the evaluation engine from a specific LLM vendor.The architecture follows the Dependency Inversion Principle, allowing new providers to be added without modifying the evaluation engine.

Current provider:

- OpenAI

Planned providers:

- Gemini
- Claude
- Ollama
- Azure OpenAI

---

## Context-Aware Evaluation

Evaluation based on predefined criteria for each prompt.

Example:

```json
{
  "prompt": "Explain Python functions in simple terms.",
  "expected_keywords": [
    "function",
    "parameter",
    "return",
    "code",
    "python"
  ]
}

```

## LLM-as-a-Judge

A second LLM evaluates the generated response using semantic criteria:

- Accuracy
- Clarity
- Completeness

---

## Prompt Benchmark Ranking

Automatic prompt ranking based on Judge Score.

---

## Model Benchmark
Supports benchmarking across different LLM models while keeping the same evaluation criteria, enabling objective comparison between models.
Compare different LLM models using the same prompt and evaluate:

- Judge Score
- Accuracy
- Clarity
- Completeness

---

## SQLite Analytics

Evaluation results are automatically stored in SQLite for historical analysis.

Available analytics:

- Approval Rate
- Average Judge Score
- Prompt Ranking
- Evaluation History
- SQL Queries
- Historical Metrics

---

## Executive PDF Reports

Automatically generates executive reports including:

- Executive Summary
- Prompt Ranking
- Model Benchmark
- Historical Trend Chart

---

## AI Observability Dashboard

Interactive HTML dashboard displaying:

- Total Evaluations
- Approval Rate
- Judge Average Score
- Prompt Benchmark Ranking
- Model Benchmark Ranking
- Historical Trend
- SQLite Analytics

---

## GitHub Actions CI/CD

Automated pipeline that:

- Runs tests
- Executes evaluations
- Generates dashboards
- Creates executive PDF reports
- Uploads artifacts

# Author

**Mario Lima**

Quality Assurance Engineer | AI Quality Engineering | Test Automation | Python

GitHub:
https://github.com/mario42guitarrista/ai-quality-evaluation-platform
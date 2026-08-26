# AI Quality Evaluation Platform

An AI Quality Engineering platform designed to evaluate, benchmark, monitor, and report the quality, reliability, performance, token consumption, and estimated cost of Large Language Model (LLM) responses.

This project simulates a real-world AI Quality Engineering workflow by combining automated prompt evaluation, semantic assessment using LLM-as-a-Judge, multi-provider benchmarking, token and cost analytics, SQL analytics, dashboards, executive reporting, and CI/CD automation.

The primary goal is not only to consume AI models, but to build an engineering platform capable of continuously measuring, comparing, and improving AI-generated responses using software engineering and quality engineering best practices.

---

## Project Goals

The platform aims to:

- Evaluate AI-generated responses using keyword-based and semantic evaluation.
- Compare multiple LLM providers using standardized prompts.
- Measure provider latency, reliability, and token consumption.
- Estimate provider costs using versioned pricing configurations.
- Isolate provider and pricing failures during comparison workflows.
- Store historical evaluation data for SQL analytics.
- Generate dashboards and executive reports automatically.
- Apply AI Quality Engineering and Observability concepts.
- Simulate production-grade software engineering practices.

---


## Roadmap

The project evolves incrementally. Every new technology must solve a real architectural, testing, delivery, or observability requirement.

### Completed

* OpenAI Integration
* Gemini Integration
* Context-Aware Evaluation
* LLM-as-a-Judge
* Prompt Benchmark
* Model Benchmark
* SQLite Analytics
* SQL Dashboard
* Executive PDF Reports
* GitHub Actions CI/CD
* Provider-Based Architecture
* Provider Factory
* Mock Provider
* Multi-Provider Service Integration
* Real Multi-Provider Comparison
* Provider Latency Measurement
* Failure-Isolated Provider Execution
* JSON Comparison Reports
* Multi-Run Provider Benchmarking
* Aggregated Latency Analytics
* Success-Rate Analytics
* JSON Benchmark Reports
* Provider Token Usage Tracking
* Cached and Reasoning Token Tracking
* Versioned Provider Pricing
* Per-Request Cost Estimation
* Multi-Run Cost Aggregation
* Provider Cost Analytics

### Current Focus — REST API Foundation

* FastAPI application foundation
* Health-check endpoint
* Automatic OpenAPI documentation
* Deterministic automated API test foundation
* Dependency injection for testable API execution
* Reuse of the existing provider and service architecture

### Planned Evolution

#### REST API Capabilities

* Evaluation API
* Provider Comparison API
* Multi-Run Provider Benchmark API
* Provider Metrics API
* Request and response validation with Pydantic
* Consistent HTTP error handling
* Versioned API contracts

#### Automated Testing Architecture

* Dedicated API tests
* Unit-test organization
* Integration-test organization
* Provider contract tests
* OpenAPI contract validation
* Separation of deterministic tests from live provider smoke tests
* Incremental test-suite organization without disrupting existing coverage
* Independent CI feedback for fast, integration, and external-provider tests

#### Containerization

* Dockerized FastAPI application
* Environment-based configuration
* Container health checks
* Reproducible local execution
* Docker build validation in CI/CD
* Docker Compose only when multiple runtime services justify it

#### Metrics and Observability

* Historical provider latency
* Token-consumption history
* Estimated-cost history
* Provider success and failure trends
* Provider reliability metrics
* Structured application logging
* Request correlation and traceable execution identifiers
* Metrics endpoints backed by persisted platform data
* Observability dashboards based on real platform signals

#### Provider Expansion

* Claude Provider
* Provider contract validation for new integrations
* Ollama Provider after the local runtime architecture is prepared
* Azure OpenAI evaluation when justified by deployment requirements

#### Web Interface and End-to-End Testing

* Streamlit interface consuming the REST API
* Provider comparison workflow through the web interface
* Benchmark and metrics visualization
* Playwright E2E tests for real user workflows
* Playwright adoption only after a testable web interface exists

#### Cloud Deployment

* Cloud-ready application configuration
* AWS deployment after containerization and health checks
* Cloud service selection based on actual platform requirements
* Secure secrets and environment management
* Cloud logging and operational monitoring
* Deployment smoke tests

### Roadmap Principles

* Preserve stable services, tests, reports, and provider integrations.
* Introduce architectural changes through small, reviewable milestones.
* Reuse the existing service layer instead of duplicating business logic in API endpoints.
* Add automated tests together with every new capability.
* Keep external-provider calls isolated from deterministic test execution.
* Introduce Docker, Playwright, and Cloud only when supported by a real application requirement.
* Maintain documentation, CI/CD validation, and structured Git workflows for every milestone.

The planned progression demonstrates:

**Python + Pytest + API + SQL + CI/CD + Docker + Playwright + Cloud + Automation Architecture + AI Quality Engineering.**

---

## Key Features

### Multi-Provider API Integration

- OpenAI API integration
- Gemini API integration through the Google GenAI SDK
- Dynamic provider and model selection
- Automatic prompt execution
- Structured token usage metadata
- Per-request estimated cost
- AI-generated responses

---

## Technology Stack

- Python
- OpenAI API
- Gemini API
- Google GenAI SDK
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

The platform uses a provider abstraction layer that decouples the evaluation engine from a specific LLM vendor. The architecture follows the Dependency Inversion Principle, allowing new providers to be added without changing the main evaluation workflow.

Architecture components:

- `BaseLLMProvider`: defines the common provider interface and provides backward-compatible usage tracking
- `ProviderGenerationResult`: normalizes response text and token metadata across providers
- `OpenAIProvider`: handles real OpenAI API requests and extracts OpenAI usage metadata
- `GeminiProvider`: handles real Gemini API requests and normalizes Google GenAI usage metadata
- `MockProvider`: generates deterministic responses without external API calls
- `Provider Factory`: creates providers dynamically by name
- `LLMService`: executes prompts without depending on provider implementations
- `ModelPricing`: stores immutable, versioned pricing configurations
- `ProviderCostService`: estimates uncached input, cached input, output, and total costs
- `MultiProviderComparisonService`: compares providers while measuring latency, tokens, estimated cost, success, and errors
- `MultiRunProviderBenchmarkService`: executes multiple comparison rounds and aggregates latency, reliability, token consumption, and estimated cost

Available providers:

- OpenAI
- Gemini
- Mock

The Mock Provider allows the service and provider architecture to be tested without consuming API credits.

The automated test suite currently contains 38 passing tests covering AI evaluation, LLM-as-a-Judge, OpenAI connectivity, Gemini behavior, provider selection, dependency injection, backward compatibility, token normalization, comparison execution, latency measurement, failure isolation, pricing configuration, cost estimation, multi-run aggregation, success-rate calculation, and input validation.

Planned providers:

- Claude
- Ollama
- Azure OpenAI

---

## Multi-Provider Comparison

The platform can execute the same prompt across different LLM providers through a single comparison service.

Comparison capabilities:

- Dynamic provider and model selection
- Identical prompt execution across providers
- Per-provider latency measurement
- Input, cached input, output, reasoning, and total token tracking
- Estimated input, cached input, output, and total cost
- Pricing tier and effective-date metadata
- Independent success and error tracking
- Failure isolation between providers
- Cost-estimation error isolation
- Structured JSON report generation

Run the real comparison:

```powershell
python -m scripts.compare_providers
```

Generated report:

```text
reports/provider_comparisons/provider_comparison.json
```

Latest local single-run execution:

| Provider | Model | Latency | Input Tokens | Output Tokens | Total Tokens | Estimated Cost | Status |
|---|---|---:|---:|---:|---:|---:|---|
| OpenAI | `gpt-4.1-mini` | 3751.10 ms | 18 | 14 | 32 | $0.00002960 | Success |
| Gemini | `gemini-3.5-flash-lite` | 1690.59 ms | 12 | 26 | 38 | $0.00006860 | Success |

These values represent a single local execution and should not be interpreted as statistically significant provider-performance or cost conclusions.

---

## Provider Cost Analytics

The platform collects normalized usage metadata from each provider response and estimates the corresponding cost using a versioned pricing catalog.

Tracked usage fields:

- Input tokens
- Cached input tokens
- Output tokens
- Reasoning tokens
- Total tokens

Calculated cost fields:

- Uncached input cost
- Cached input cost
- Output cost
- Total estimated cost
- Average estimated cost per benchmark run
- Number of priced and unpriced successful executions

The normalized cost calculation is:

```text
uncached_input_tokens = input_tokens - cached_input_tokens

estimated_total_cost =
    uncached_input_cost
    + cached_input_cost
    + output_cost
```

All financial calculations use Python `Decimal` values internally to reduce floating-point rounding errors.

### Pricing Snapshot

Pricing effective date: `2026-08-20`

| Provider | Model | Tier | Input / 1M Tokens | Cached Input / 1M Tokens | Output / 1M Tokens |
|---|---|---|---:|---:|---:|
| OpenAI | `gpt-4.1-mini` | `standard_paid` | $0.40 | $0.10 | $1.60 |
| Gemini | `gemini-3.5-flash-lite` | `standard_paid` | $0.30 | $0.03 | $2.50 |

Official pricing references:

- [OpenAI GPT-4.1 mini model pricing](https://developers.openai.com/api/docs/models/gpt-4.1-mini)
- [Google Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing)

Pricing is intentionally stored as versioned application configuration rather than embedded directly in the comparison logic. This makes pricing changes auditable and prevents provider-specific billing rules from being coupled to benchmark execution.

Cost values generated by the platform are estimates, not billing statements. Actual charges may vary because of free tiers, batch pricing, provider discounts, pricing changes, account configuration, or other billing rules. The Gemini estimates use the standard paid tier even when an execution may qualify for the free tier.

A pricing configuration error does not convert a successful provider response into a failed execution. The response remains successful, the cost fields remain unavailable, and the pricing error is recorded separately.

---

## Multi-Run Provider Benchmarking

The platform can execute multiple comparison rounds and aggregate reliability, latency, token consumption, and estimated cost for each provider.

Benchmark capabilities:

- Configurable number of executions
- Individual result tracking by run
- Successful and failed execution totals
- Success-rate calculation
- Minimum latency
- Maximum latency
- Average latency
- Median latency
- Aggregated token usage
- Aggregated estimated cost
- Average estimated cost per priced run
- Priced and unpriced execution tracking
- Failure isolation across every run
- Structured JSON benchmark reports

Latency aggregates are calculated using successful executions only. Failed attempts remain available in the individual results and are included in the failure count and success rate.

Cost averages are calculated using successfully priced executions only. A provider response can therefore remain successful even when its cost cannot be estimated.

Run the real benchmark:

```powershell
python -m scripts.benchmark_providers
```

Generated report:

```text
reports/provider_benchmarks/provider_benchmark.json
```

Latest local benchmark with three runs per provider:

### Latency and Reliability

| Provider | Model | Successful Runs | Success Rate | Minimum | Average | Median | Maximum |
|---|---|---:|---:|---:|---:|---:|---:|
| OpenAI | `gpt-4.1-mini` | 3/3 | 100.00% | 1291.93 ms | 2088.18 ms | 1601.24 ms | 3371.38 ms |
| Gemini | `gemini-3.5-flash-lite` | 3/3 | 100.00% | 60501.74 ms | 75797.58 ms | 80576.90 ms | 86314.10 ms |

### Token Usage and Estimated Cost

| Provider | Input | Cached | Output | Reasoning | Total | Total Estimated Cost | Average per Run |
|---|---:|---:|---:|---:|---:|---:|---:|
| OpenAI | 54 | 0 | 42 | 0 | 96 | $0.00008880 | $0.00002960 |
| Gemini | 36 | 0 | 82 | 0 | 118 | $0.00021580 | $0.00007193 |

All six executions completed successfully and produced usage metadata and cost estimates.

Gemini latency during this specific three-run sample was substantially higher than in the earlier single-run comparison. This variation demonstrates the importance of repeated measurement and historical observability, but it does not establish a general provider-performance conclusion. Runtime, network, queue, or API conditions were not independently diagnosed by this experiment.

These results describe a small local sample. Larger sample sizes and repeated executions across different periods would be required for statistically meaningful provider comparisons.

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

---

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

Model comparison metrics:

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

The automated pipeline:

- Runs the test suite
- Executes AI evaluations
- Generates dashboards
- Creates executive PDF reports
- Uploads generated artifacts

---

## Author

**Mario Lima**

Quality Assurance Engineer | AI Quality Engineering | Test Automation | Python

GitHub:

https://github.com/mario42guitarrista/ai-quality-evaluation-platform
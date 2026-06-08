# AI Quality Evaluation Platform

AI Quality Evaluation Platform é um projeto focado em avaliação, observabilidade e benchmarking de respostas geradas por Large Language Models (LLMs).

O objetivo é simular uma plataforma real de AI Quality Engineering capaz de executar prompts, avaliar respostas automaticamente, gerar relatórios estruturados e disponibilizar dashboards para análise da qualidade dos resultados.

---

# Features

## OpenAI Integration

- Integração com OpenAI API
- Execução automática de prompts
- Geração de respostas via LLM

---

## Context-Aware Evaluation

Avaliação baseada em critérios específicos para cada prompt.

Exemplo:

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

Além da avaliação por keywords, uma segunda chamada ao modelo realiza avaliação semântica baseada em:

- Accuracy
- Clarity
- Completeness

Exemplo:

```json
{
  "score": 9,
  "accuracy": 9,
  "clarity": 9,
  "completeness": 8,
  "comments": "Clear and accurate answer."
}
```

---

## Evaluation Reports

Cada execução gera relatórios JSON estruturados.

Exemplo:

```json
{
  "prompt": "...",
  "response": "...",
  "evaluation": {
    "score": 4
  },
  "llm_judge": {
    "score": 9,
    "accuracy": 9,
    "clarity": 9,
    "completeness": 8
  }
}
```

---

## Prompt Benchmark Ranking

Ranking automático dos prompts baseado no Judge Score.

Exemplo:

| Rank | Prompt | Judge Score |
|--------|--------|--------|
| 1 | CI/CD | 9 |
| 2 | Python Functions | 9 |
| 3 | API Testing | 8 |
| 4 | DevOps | 8 |
| 5 | Quality Engineering | 7 |

---

## Historical Trends

Geração automática de gráficos para análise histórica dos resultados.

Métricas monitoradas:

- Judge Score Trend
- Evolução das execuções
- Benchmark histórico

---

## AI Observability Dashboard

Dashboard HTML contendo:

- Total Evaluations
- Approved
- Failed
- Approval Rate
- Keyword Average Score
- Judge Average Score
- Best Score
- Lowest Score
- Evaluation Details
- Prompt Benchmark Ranking
- Historical Trends

---

# Project Structure

```text
ai-quality-evaluation-platform/
│
├── dashboard/
│   ├── assets/
│   ├── evaluation_dashboard.html
│   ├── evaluation_dashboard_generator.py
│   ├── generate_trend_chart.py
│   └── prompt_benchmark.py
│
├── evaluations/
│   ├── llm_judge.py
│   ├── multi_prompt_runner.py
│   └── response_evaluator.py
│
├── prompts/
│   ├── api_testing.json
│   ├── ci_cd.json
│   ├── devops.json
│   ├── python_basics.json
│   └── quality_engineering.json
│
├── reports/
│   └── evaluations/
│
├── tests/
│   ├── test_ai_evaluation.py
│   ├── test_llm_judge.py
│   └── test_openai_connection.py
│
├── utils/
│   ├── evaluation_reporter.py
│   ├── openai_client.py
│   └── prompt_loader.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Installation

Clone o projeto:

```bash
git clone <repository-url>
cd ai-quality-evaluation-platform
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

Instale dependências:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Crie um arquivo:

```text
.env
```

Conteúdo:

```env
OPENAI_API_KEY=your_api_key
```

---

# Running Evaluations

Executar benchmark completo:

```bash
python -m evaluations.multi_prompt_runner
```

---

# Generate Dashboard

Gerar gráfico:

```bash
python dashboard/generate_trend_chart.py
```

Gerar dashboard:

```bash
python dashboard/evaluation_dashboard_generator.py
```

Abrir dashboard:

```bash
start dashboard/evaluation_dashboard.html
```

---

# Roadmap

## Completed

- Foundation
- OpenAI Integration
- Evaluation Engine
- Context-Aware Evaluation
- LLM-as-a-Judge
- Dashboard
- Prompt Benchmark Ranking
- Historical Trends

## Next Steps

- Multi Model Benchmark
- Executive PDF Reports
- GitHub Actions Integration
- Model Comparison Dashboard
- Evaluation API
- Streamlit Dashboard

---

# Technologies

- Python
- OpenAI API
- Pytest
- JSON
- Matplotlib
- HTML
- CSS

---

# Author

Mario Lima

AI Quality Evaluation Platform
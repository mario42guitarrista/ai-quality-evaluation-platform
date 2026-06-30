import json
from urllib import response
from services.llm_service import generate_response_with_provider


def evaluate_with_llm_judge(answer):

    judge_prompt = f"""
Evaluate the following answer.

Criteria:
- Accuracy
- Clarity
- Completeness

Give scores from 1 to 10.

Return ONLY valid JSON.

Format:

{{
  "score": 0,
  "accuracy": 0,
  "clarity": 0,
  "completeness": 0,
  "comments": ""
}}

Answer:

{answer}
"""

    response = generate_response_with_provider(
    prompt=judge_prompt,
    provider_name="openai",
    model="gpt-4.1-mini"
    )
    
    print("\nRAW JUDGE RESPONSE:\n")
    print(response)

    try:
        return json.loads(response)

    except Exception:

        return {
            "score": 0,
            "accuracy": 0,
            "clarity": 0,
            "completeness": 0,
            "comments": "Failed to parse judge response."
        }
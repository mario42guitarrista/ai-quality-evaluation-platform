def evaluate_response(response, expected_keywords):

    score = 0

    response_lower = response.lower()

    matched_keywords = []

    for keyword in expected_keywords:

        if keyword.lower() in response_lower:
            score += 1
            matched_keywords.append(keyword)

    evaluation = {
        "score": score,
        "total_keywords": len(expected_keywords),
        "matched_keywords": matched_keywords,
        "approved": score >= 2
    }

    return evaluation
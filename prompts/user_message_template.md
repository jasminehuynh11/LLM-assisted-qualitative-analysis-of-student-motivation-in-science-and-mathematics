{codebook}

{question_context}

Student response (verbatim):

"""{response}"""

Return ONLY a JSON object with these keys (no markdown, no commentary):

- "codes": array of 1 to 3 strings from the allowed list above, strongest first.
- "confidence_overall": integer 0-100 for the whole coding.
- "confidence_per_code": array of integers 0-100, same length as "codes", aligned in order.
- "rationale_short": one or two sentences citing or paraphrasing words from the response that justify the codes.

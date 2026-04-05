# Human Review Notes

Record patterns, systematic errors, and observations from manual review here.

## Patterns Found (Training Set, v2.0.0 prompts)

- **mastery_positive over-applied**: LLM assigned mastery_positive when students expressed interest/curiosity rather than comprehension
- **structural_positive/negative over-applied**: LLM confused real-world relevance (valuing) with structural features
- **uncertain_control_negative over-applied**: LLM assigned uncertain_control_negative for simple difficulty statements (should be mastery_negative only)
- **self_beliefs vs mastery confusion**: LLM conflated "I find it easy" (mastery) with "I'm good at it" (self_beliefs)

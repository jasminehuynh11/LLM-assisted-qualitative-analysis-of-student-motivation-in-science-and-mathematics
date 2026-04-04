## Allowed codes (JSON output must use these exact strings)

Use **underscore** names in the JSON field `codes` (e.g. `valuing_positive`).

| Human-readable label | JSON code string | Definition |
| --- | --- | --- |
| valuing – positive | `valuing_positive` | Students experience a subject as interesting, enjoyable, and useful. |
| valuing – negative | `valuing_negative` | Students experience a subject as boring and useless. |
| social agents – positive | `social_agents_positive` | Students note teacher, peers, friends, parents, and/or family as a reason they **like** a subject. |
| social agents – negative | `social_agents_negative` | Students note teacher, peers, friends, parents, and/or family as a reason they **do not like** a subject. |
| mastery – positive | `mastery_positive` | Students view a subject as challenging in a satisfying way and they **can** understand the content. |
| mastery – negative | `mastery_negative` | Students view a subject as challenging in a threatening or overwhelming way and they **cannot** understand the content. |
| self-beliefs – positive | `self_beliefs_positive` | Students identify with the subject (e.g. “math/science person”) and feel they have the skills to do well. |
| self-beliefs – negative | `self_beliefs_negative` | Students do not identify with the subject and feel they lack the skills to do well. |
| uncertain control – negative | `uncertain_control_negative` | Students are unsure how to improve and feel they do not control their progress. |
| structural – positive | `structural_positive` | Structure, activities, pace, or variety of the subject are reasons they **like** it. |
| structural – negative | `structural_negative` | Structure, activities, pace, or workload are reasons they **do not like** it. |
| Failure Avoidance – negative | `failure_avoidance_negative` | Students feel stupid, incompetent, or embarrassed about performance as a reason they dislike the subject. |
| anxiety – negative | `anxiety_negative` | Students feel very worried, anxious, or stressed about performance as a reason they dislike the subject. |

## Few-shot examples (illustrative; same labels as above)

These examples show how short student quotes map to **one primary** code. Your task may still assign up to **three** codes when multiple themes are clearly supported.

1. **`valuing_positive`** — *"i like science because it answers most of my questions about the world and its just overall really cool."*

2. **`valuing_negative`** — *"ITS HORRIBLE AND BORING"*

3. **`social_agents_positive`** — *"I like my teacher"*

4. **`social_agents_negative`** — *"The class has got less engaging and the teacehrs are never paying attention"*

5. **`mastery_positive`** — *"I like science because I understand it, and the content is engaging"* (understanding + engagement can also support `valuing_positive`; include both if clearly supported.)

6. **`mastery_negative`** — *"It's confusing and hard to remember facts"*

7. **`self_beliefs_positive`** — *"Because i am good at it"*

8. **`self_beliefs_negative`** — *"Im not good at it"*

9. **`uncertain_control_negative`** — *"too hard and it seems like i never improve"*

10. **`structural_positive`** — *"i like that there are experiments and different assessment tasks, there are many topics to study so there is a wide variety"*

11. **`structural_negative`** — *"theres too much they are teaching us and not enough time to learn it all"*

12. **`failure_avoidance_negative`** — *"It makes me feel stupid"*

13. **`anxiety_negative`** — *"It creates stress"*

## Disambiguation (brief)

- Enjoyment/interest/usefulness → `valuing_*`; understanding/difficulty of content → `mastery_*`; identity/confidence in ability → `self_beliefs_*`.
- Shame/embarrassment / feeling stupid in front of others → `failure_avoidance_negative`; general worry/stress → `anxiety_negative`.
- People (teacher/peers) as main reason → `social_agents_*` (positive/negative).
- Pace, workload, amount of content, activities → `structural_*`.
- Assign **1–3** codes, strongest first. Omit weak codes; if unsure, fewer codes and lower confidence.

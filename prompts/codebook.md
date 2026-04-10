## Allowed codes (JSON output must use these exact strings)

Use **underscore** names in the JSON field `codes` (e.g. `valuing_positive`).

| Human-readable label | JSON code string | Definition |
| --- | --- | --- |
| valuing – positive | `valuing_positive` | The student expresses the subject is interesting, enjoyable, fun, or useful/relevant to their life or future. Key signal: emotional appreciation or perceived value of the subject itself. |
| valuing – negative | `valuing_negative` | The student expresses the subject is boring, unenjoyable, or pointless/irrelevant. Key signal: emotional dislike or perceived lack of worth. |
| social agents – positive | `social_agents_positive` | The student credits a teacher, classmate, peer, friend, parent, or family member as a reason they like the subject. |
| social agents – negative | `social_agents_negative` | The student blames a teacher, classmate, peer, friend, parent, or family member as a reason they dislike or stopped the subject. |
| mastery – positive | `mastery_positive` | The student explicitly states they can understand the content well, find it easy, or find challenge satisfying. There must be a direct statement of comprehension or competence — NOT just curiosity or interest in a topic. |
| mastery – negative | `mastery_negative` | The student explicitly states the content is difficult, confusing, or overwhelming in a way they cannot manage. |
| self-beliefs – positive | `self_beliefs_positive` | The student identifies with the subject as part of who they are, OR explicitly states they are good at it ("I'm good at it", "it comes naturally", "I've always done well"). NOT the same as finding something easy in the moment — requires identity or stated competence. |
| self-beliefs – negative | `self_beliefs_negative` | The student explicitly states they are not good at the subject, do not have the skills, or do not see themselves as a "maths/science person". NOT the same as finding something hard — requires identity or stated lack of competence. |
| uncertain control – negative | `uncertain_control_negative` | The student expresses a persistent, helpless feeling that they cannot improve no matter what they do. Must go beyond simply finding something hard — requires a signal of feeling stuck or giving up (e.g. "no matter how hard I try", "I never improve", "I gave up"). |
| structural – positive | `structural_positive` | The student likes the subject because of how it is organised, delivered, or assessed — specifically the type of activities (e.g. experiments, practicals), variety of topics, assessment format, or pace. NOT real-world relevance or interesting content. |
| structural – negative | `structural_negative` | The student dislikes the subject because of how it is organised, delivered, or assessed — specifically activities, content load, assessment format, or pace. NOT just that the content is difficult or irrelevant. |
| Failure Avoidance – negative | `failure_avoidance_negative` | The student reports feeling stupid, incompetent, or embarrassed specifically because of how they perform or are perceived to perform compared to others. Key signal: shame or social comparison about performance. |
| anxiety – negative | `anxiety_negative` | The student reports feeling worried, stressed, or anxious about their performance. Key signal: internal emotional distress tied to assessment or performance. NOT the absence of stress. |

## Critical Disambiguation Rules

These are the four most common errors — read carefully before coding:

### 1. `mastery_positive` vs `valuing_positive`
- **"interesting / fun / cool"** alone → `valuing_positive` ONLY
- **"I understand it / find it easy"** → `mastery_positive`
- **"I like learning how things work / want to understand things"** → `mastery_positive` (learning goal = mastery orientation)
- **"broadens my understanding / helps me understand the world"** → `mastery_positive` ✅
- ❌ DO NOT apply `mastery_positive` for pure enjoyment/interest with no learning or understanding component

### 2. `self_beliefs` vs `mastery`
- **"I understand it / find it easy"** → `mastery_positive` (current ability, in the moment)
- **"I'm good at it / it comes naturally / I've always done well"** → `self_beliefs_positive` (stable identity/competence)
- ❌ DO NOT confuse these — mastery is about the content being manageable; self-beliefs is about who they are as a learner

### 3. `uncertain_control_negative` vs `mastery_negative`
- **"too hard / confusing / I don't understand"** → `mastery_negative` ONLY
- **"no matter how hard I try I can't improve / I never get better / I gave up"** → `uncertain_control_negative`
- ❌ DO NOT add `uncertain_control_negative` just because something is hard

### 4. `structural_positive/negative` vs `valuing_positive/negative`
- **"real world / useful in life / applicable"** → `valuing_positive` (usefulness = value)
- **"experiments / practicals / variety of topics / pace / assessment"** → `structural_positive`
- ❌ DO NOT apply `structural` just because a student mentions real-world relevance or interesting topics

## Quick Reference: What the student says → Correct code

| Student says... | Correct code | NOT |
|---|---|---|
| "interesting / fun / cool" | `valuing_positive` | `mastery_positive` |
| "I understand it / find it easy" | `mastery_positive` | `self_beliefs_positive` |
| "I like learning how things work / want to understand" | `mastery_positive` | `valuing_positive` |
| "broadens my understanding / helps me understand the world" | `mastery_positive` | `valuing_positive` |
| "I'm good at it / it comes naturally" | `self_beliefs_positive` | `mastery_positive` |
| "too hard / confusing" | `mastery_negative` | `uncertain_control_negative` |
| "no matter how hard I try I can't improve" | `uncertain_control_negative` | `mastery_negative` alone |
| "not my thing / never been a science person" | `self_beliefs_negative` | `valuing_negative` |
| "real world / useful in life" | `valuing_positive` | `structural_positive` |
| "experiments / practicals / variety of topics" | `structural_positive` | `valuing_positive` |
| "feel stupid / embarrassed compared to others" | `failure_avoidance_negative` | `anxiety_negative` |
| "stressed / worried about tests" | `anxiety_negative` | `failure_avoidance_negative` |
| "teacher is great / helps me" | `social_agents_positive` | `mastery_positive` |

## Question Type Valence Rule

**ALWAYS check `question_type` before assigning any code.**
- `like_science` / `like_math` → responses are positive context; negative codes only if explicitly stated
- `dislike_science` / `dislike_math` / `stopped_science` / `stopped_math` → responses are negative context; DO NOT assign positive codes unless the student explicitly says something positive
- ❌ A common error is assigning `valuing_positive` to a one-word response like "content" or "subject" in a `stopped_science` question — this is wrong

## Few-shot examples

1. **`valuing_positive`** — *"i like science because it answers most of my questions about the world and its just overall really cool."*

2. **`valuing_negative`** — *"ITS HORRIBLE AND BORING"*

3. **`social_agents_positive`** — *"I like my teacher"*

4. **`social_agents_negative`** — *"The class has got less engaging and the teachers are never paying attention"*

5. **`mastery_positive`** — *"I like science because I understand it"* — note: "understand it" is the mastery signal; "engaging" also supports `valuing_positive`

6. **`mastery_negative`** — *"It's confusing and hard to remember facts"*

7. **`self_beliefs_positive`** — *"Because I am good at it"* — identity/competence claim

8. **`self_beliefs_negative`** — *"Im not good at it"*

9. **`uncertain_control_negative`** — *"too hard and it seems like i never improve"* — note: "never improve" is the key signal, not just "too hard"

10. **`structural_positive`** — *"I like that there are experiments and different assessment tasks, there are many topics to study so there is a wide variety"*

11. **`structural_negative`** — *"theres too much they are teaching us and not enough time to learn it all"*

12. **`failure_avoidance_negative`** — *"It makes me feel stupid"*

13. **`anxiety_negative`** — *"It creates stress"*

## Edge case handling

- If the response is a single word or two words with no clear evaluative statement (e.g. "content", "concepts", "I just don't"), assign the most plausible single code based on question_type context and set `confidence_overall` ≤ 40.
- If the response cannot be mapped to any code even with question_type context (e.g. "because I'm Asian"), assign `valuing_positive` as fallback and set `confidence_overall` = 25 with a rationale noting it is uncodeable.
- Never assign more codes than the response supports. When in doubt, assign fewer codes and lower confidence.

## Confidence Score Rules

| Situation | confidence_overall |
|---|---|
| Response clearly maps to 1-2 codes | 75–95 |
| Response maps to codes but is vague | 50–74 |
| Response is 1-3 words, hard to interpret | ≤ 40 |
| Response is uncodeable / off-topic | 25 |
| Fallback code assigned | 25 |

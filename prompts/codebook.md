## Code Definitions

Use **underscore** names in the JSON field `codes` (e.g. `valuing_positive`).

| Code | Definition | Apply when | Do NOT apply when |
|---|---|---|---|
| `valuing_positive` | The student expresses the subject is interesting, enjoyable, fun, or useful/relevant to their life or future. Key signal: emotional appreciation or perceived value of the subject itself. | "fun", "interesting", "cool", "I enjoy it", "useful for my career/life", "I like learning about X" | Student says they understand it or find it easy — that is `mastery_positive` |
| `valuing_negative` | The student expresses the subject is boring, unenjoyable, or pointless/irrelevant. Key signal: emotional dislike or perceived lack of worth. | "boring", "I don't like it", "pointless", "useless", "not interesting", "I never liked it" | Student only mentions difficulty without expressing boredom or disinterest |
| `social_agents_positive` | The student credits a teacher, classmate, peer, friend, parent, or family member as a reason they like the subject. | "my teacher is great", "my friends like it too", "my parents encouraged me", "good people in my class" | Teacher is mentioned negatively, or student just mentions doing work in a social setting |
| `social_agents_negative` | The student blames a teacher, classmate, peer, friend, parent, or family member as a reason they dislike or stopped the subject. | "bad teacher", "my teacher doesn't help", "teacher never pays attention", "teacher has no faith in us" | Teacher is mentioned positively or neutrally |
| `mastery_positive` | The student expresses the subject is challenging in a satisfying way, OR explicitly states they can understand and do the work well. Must be a direct statement of comprehension, competence, or rewarding challenge — not just curiosity or interest in content. | "I understand it", "it makes sense to me", "I find it easy", "satisfying when I solve it", "challenging but I get it", "I grasp concepts quickly", "broadens my understanding", "helps me understand things better" | Student only says content is "interesting" or they "like learning about" a topic — that is `valuing_positive`. Understanding comes from teacher help — that is `social_agents_positive` |
| `mastery_negative` | The student expresses the subject is difficult, confusing, or overwhelming in a way they cannot manage. Must be a direct statement of difficulty, confusion, or inability to understand. | "too hard", "confusing", "I don't understand it", "complicated", "I can't grasp it" | Do NOT automatically add `uncertain_control_negative` just because something is hard — that requires an additional helplessness signal |
| `self_beliefs_positive` | The student identifies with the subject as part of who they are, OR explicitly states they are good at it and have the skills to succeed. Key signal: identity or stated competence. | "I'm good at it", "it comes easily to me", "I see myself doing science in the future", "I've always been a maths person", "it comes naturally" | Student finds content interesting or mentions future careers — that is `valuing_positive`. Student says they understand the content — that is `mastery_positive` |
| `self_beliefs_negative` | The student explicitly states they are not good at the subject, do not have the skills, or do not see themselves as a "maths/science" person. | "I'm not good at it", "it's not my thing", "I've never been a science person", "I used to be good but not anymore", "I can't do it" | Something is hard — that is `mastery_negative`. Self-beliefs requires identity or personal competence, not just difficulty |
| `uncertain_control_negative` | The student expresses a persistent, helpless feeling they cannot improve no matter what they do — feeling stuck with no sense of how to get better. Goes beyond simply finding something hard. | "no matter how hard I try I can't do it", "I never improve", "I gave up", "I always feel lost", "I can never master it no matter what", "it seems like I never get better" | Student says something is "too hard" or "confusing" — that is `mastery_negative` only. Student says "I don't understand it" without implying helplessness to change that |
| `structural_positive` | The student likes the subject because of how it is organised, delivered, or assessed — specifically activities (e.g. experiments, practicals), variety of topics, assessment format, or pace. | "I like the experiments", "there's a good variety of topics", "I like how we do practicals", "the pace suits me", "assessment is fair" | Student says subject is relevant to real life — that is `valuing_positive`. Student mentions topics they like — that is `valuing_positive` |
| `structural_negative` | The student dislikes the subject because of how it is organised, delivered, or assessed — specifically activities, content load, assessment format, or pace. | "too much content", "moves too fast", "only textbook work", "too much memorising", "the way we're tested", "not enough practicals" | Student says content is irrelevant — that is `valuing_negative`. Student says it got harder — that is `mastery_negative` |
| `failure_avoidance_negative` | The student reports feeling stupid, incompetent, or embarrassed specifically because of how they perform or are perceived to perform compared to others. Key signal: social comparison or shame about performance. | "it makes me feel stupid", "I feel dumb compared to others", "I felt like a failure", "embarrassed I don't do well", "I feel left out because others are better" | Do NOT confuse with `anxiety_negative` — `failure_avoidance_negative` is about shame/embarrassment, `anxiety_negative` is about worry/stress |
| `anxiety_negative` | The student reports feeling worried, stressed, or anxious about their performance. Key signal: internal emotional distress tied to assessment or performance. | "it stresses me out", "I get anxious about tests", "I worry about failing", "it creates stress", "I feel nervous about it" | Teacher puts pressure on students — look for student's own internal emotional response. Student says subject is NOT stressful — that is absence of anxiety, not presence |

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

## Edge Case Handling

### Responses that are too brief or uninterpretable

Some student responses cannot be reliably coded because they are too vague, too short, or do not map to any motivational construct. These fall into three categories:

**Category 1 — Insufficient Data**
Single-word or two-word responses with no clear evaluative statement.
Examples: "content", "concepts", "I just don't", "learning"
Action: Assign the most plausible single code based on question_type context only. Set `confidence_overall` = 25.

**Category 2 — Ambiguous**
Responses that could fit two or more codes but evidence is too weak to choose reliably.
Examples: "classroom experiences", "subject content", "teacher and content"
Action: Assign the most plausible single code. Set `confidence_overall` = 25.
Note: these will be self-assigned by a human reviewer — do not force multiple codes.

**Category 3 — Uncodeable**
Responses that do not map to any motivational construct at all, even with question_type context.
Examples: "because I'm Asian", "I just don't"
Action: Assign `valuing_negative` (for negative question types) or `valuing_positive` (for positive question types) as fallback. Set `confidence_overall` = 25. Note in `rationale_short` that the response is uncodeable.

### Important rules for all three categories
- NEVER force a code with high confidence on a vague response
- ALWAYS set `confidence_overall` ≤ 25 for these cases
- ALWAYS note in `rationale_short` that the response is too brief or uncodeable
- These responses will be reviewed and self-assigned by a human coder — your job is only to flag them correctly with low confidence

## Confidence Score Rules

| Situation | confidence_overall |
|---|---|
| Response clearly maps to 1-2 codes | 75–95 |
| Response maps to codes but is vague | 50–74 |
| Response is 1-3 words, hard to interpret | 25 |
| Response is uncodeable / off-topic | 25 |
| Fallback code assigned | 25 |

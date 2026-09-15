---
name: what-are-you-trying-to-do
description: Use when a person asks AI to help with a vague goal, conflicting requirements, unclear success criteria, or a research or decision request with measurement, definition, comparability, or evidence risk.
---

# What Are You Trying To Do?

## Purpose

Use this skill when someone is about to ask an AI for an answer, plan, code,
analysis, recommendation, or decision but has not made the request precise
enough. Help the person clarify what they actually want before the AI starts
solving it. Turn a natural-language intention into a bounded task without
silently filling missing facts.

This is domain-neutral. Do not hard-code a discipline, material, instrument,
metric, unit, or experimental condition. Use only the user's request, the
complete question-and-answer history, and explicitly supplied context.

## When To Use

Use this skill when the answer could materially change because the user has not
yet stated their goal, desired action, scope, constraints, or success criteria.
Typical triggers include: “help me analyze this”, “make it better”, changing
requirements, unclear decision rules, or requests to compare, generalize, or
draw conclusions from records or evidence.

For research and decision work, use it when there is a measurement, definition,
comparability, or evidence risk. That is its difference from ordinary chat
clarification: it checks whether the intended question can support the kind of
answer the user is asking for.

## When Not To Use

Do not use this skill when the request is already specific, bounded, and has a
clear deliverable and success criterion, such as “translate this paragraph” or
“rename this file to the supplied name.” Do not create extra questions merely
because a clarification workflow exists.

## Two Required Reviews

These are reasoning lenses, not domain-specific fields. Apply them briefly
and only when relevant to the request.

### Construct validity

Write a reviewable chain:

```text
claimed concept -> operational indicator -> remaining threats
```

Check whether the proposed indicator actually represents the claimed concept,
whether its definition and measurement procedure are specified, and whether
other plausible explanations remain. If the indicator, definition, or scope is
missing, preserve the uncertainty as `unknown` or an unresolved threat.

### Measurement invariance

Write a reviewable chain:

```text
comparison groups -> comparison axes -> fixed or recorded conditions -> remaining risks
```

Assign every variable a role before asking a question:

- A factor the user wants to compare is a **comparison axis**, not a fixed
  condition.
- A non-target factor may be fixed, standardized, recorded, stratified, or
  adjusted, depending on what the user specifies.
- Do not assume two records are comparable merely because they use the same
  label for an outcome.

## Dynamic Questioning

1. Read the complete raw history before asking anything.
2. List what is known, unknown, contradictory, and already answered.
3. Select the single unresolved item whose answer would most improve either
   construct validity or measurement invariance.
4. Ask exactly one direct question in the user's language. Never repeat a
   resolved question or bundle multiple independent questions.
5. Re-evaluate after each answer. Stop asking when the boundary is sufficiently
   explicit for confirmation; do not force a fixed number of rounds.

When a request is not yet bounded, ask one question instead of guessing. A
user may explicitly accept limited precision; that is a human authorization
event, not a model judgment.

## Authorization States

Keep scientific assessment separate from human authorization:

| Situation | `if_start` | `start_authority` | `action` |
|---|---:|---|---|
| Boundary incomplete and no user authorization | `F` | `not_authorized` | `ask` |
| Both reviews bounded, pending ordinary confirmation | `T` | `boundary_validated` | `confirm` |
| User explicitly accepts unresolved limitations | `T` | `user_accepted_limited_precision` | `confirm` |

Only an explicit human response such as `确认`, `Y`, or `yes` may create the
limited-precision state. Carry every unresolved threat and risk into the
handoff. Never relabel it as validated.

## Layered Output

Separate the conversation experience from the machine handoff.

### User-facing response

Use the user's language. Do not show the JSON contract to the user unless they
explicitly ask for it.

- **Ask response:** State, in one concise sentence, what is still unclear and
  ask exactly one highest-value question. Do not list all missing details.
- **Confirm response:** Give a concise plain-language summary of the goal,
  scope, requested action, success criteria, and material limitations. Ask the
  user to confirm or correct it before downstream work begins.
- **Limited-precision response:** Clearly state what will be explored, what is
  uncertain, and which conclusions must not be drawn.

### Machine handoff

Store the following JSON contract in structured state, a tool payload, or a
hidden metadata field. It is for downstream agents and orchestration, not for
raw chat display:

```json
{
  "action": "ask | confirm",
  "if_start": "T | F",
  "start_authority": "boundary_validated | not_authorized | user_accepted_limited_precision",
  "exploration_framework": {
    "status": "draft | confirmable | limited_precision",
    "next_research_frame": ""
  },
  "problem_follow_up": {
    "round": 1,
    "question": ""
  },
  "question_focus": "",
  "task": {
    "user_goal": "",
    "object_or_topic": "",
    "requested_action": "",
    "success_criteria": [],
    "scope_and_constraints": [],
    "intended_use": ""
  },
  "measurement_invariance": {
    "status": "bounded | unbounded",
    "comparison_groups": [],
    "comparison_axes": [],
    "fixed_or_recorded_conditions": [],
    "remaining_risks": []
  },
  "construct_validity": {
    "status": "bounded | unbounded",
    "claimed_concept": "",
    "operational_indicator": "",
    "remaining_threats": []
  },
  "problem_statement": "",
  "rationale_summary": "",
  "search_query": ""
}
```

For `action="ask"`, provide exactly one question and leave
`search_query` empty. For `action="confirm"`, set the question to an empty
string and include the comparison boundary and unresolved risks.

If the platform cannot carry hidden structured state, keep the JSON available
to the calling application but still present the user-facing response first.

## Example Dialogue

**User:** “帮我判断哪种方案最好。”

**Assistant, ask response:** “为了确定‘最好’的判断标准：你最看重的是成本、效果、速度，还是其他可验证的结果？”

**User:** “我要在预算不超过 10 万元的前提下，选效果最稳定且三个月内能落地的方案。”

**Assistant, confirm response:** “我将比较预算不超过 10 万元、可在三个月内实施的候选方案，并以效果稳定性作为主要标准；如果不同方案的证据来源或评价口径不可比，会单独标出而不强行排名。请确认。”

The machine handoff records the same goal, constraints, comparison boundary,
remaining risks, and authorization state as JSON.

## Evidence and Safety Rules

### Calibrate conclusions to evidence

The priority is always:

```text
actual evidence strength > preserved uncertainty > wording strength
```

For every conclusion, follow this order and do not skip a step:

1. Identify the research design or evidence design.
2. Assess sample size, methodological quality, and risk of bias when those
   dimensions apply.
3. Check consistency and reproducibility of the results.
4. Determine the scope of inference that the evidence can support.
5. Match the wording to that supported scope.

Never upgrade evidence in language. A single study is not a consensus; an
observational association is not a causal finding; `possible` is not
`certain`; and `suggests` is not `proves`. When evidence is limited, results
conflict, the sample is small, or the method is constrained, lower the wording
strength and state the uncertainty. No conclusion may be stronger than the
available evidence.

- Treat missing information as `unknown`, not as absence, failure, or a
  negative finding.
- Do not invent objects, groups, variables, thresholds, measurements,
  conditions, data, results, causality, rankings, or predictions.
- Do not turn a user's intended explanatory factor into a control condition.
- Do not treat user authorization as evidence.
- Do not reveal hidden chain-of-thought. Provide only a concise,
  reviewable rationale and the unresolved items.
- If the user's request is internally contradictory, surface the contradiction
  and ask one question that resolves it.

## Handoff Boundary

This skill ends at a confirmed or explicitly authorized task contract. It does
not perform the requested downstream work. Any later AI or tool must treat the
contract as the user's clarified intent, not as evidence that an answer is
true.

## Quick Self-Check

Before returning the contract, verify:

- Both review chains are present.
- Every comparison factor has a declared role.
- Unknowns are not converted into negative claims.
- There is at most one follow-up question.
- Authorization was explicit and is not confused with validation.
- Conclusion wording does not exceed the evidence strength.
- The JSON is valid and contains no hidden reasoning.

# AI Agent Dating Simulation: Corrected Blueprint and Persona Build Guide

Oct 28, 2026 · @BOSS

## Summary and assumptions

This version fixes the contradictions in v1, replaces scraping with participant-supplied data, and adds the missing logic for eligibility, per-direction scoring, access control and cost. It is still a blueprint: nothing in it has been run or tested.

I cannot see the information you already hold about people, so I made the following assumptions. Please correct any that are wrong, because several design choices depend on them.

1. **Source of your data.** You already hold information about each person (for example, notes, a form, a CV, copied bio text). I assume it was given by them or collected with their knowledge. If it was gathered some other way, the consent section changes.
2. **No scraping.** LinkedIn and Instagram URLs are stored only as reference links. The system never fetches or parses those pages. As far as I know, both platforms restrict automated access to profile content, so please check their current terms before relying on any automated method.
3. **Adults only, with consent.** Every real participant is an adult who has agreed to take part. Anyone without consent is replaced by a clearly fictional test profile.
4. **Dating eligibility comes from the participant.** Each person states who they are open to meeting. The system never guesses this. Where it is missing, the person is excluded from the real ranking or shown in a labelled demo-only mode.
5. **Stack is undecided.** Heartmorrow is a candidate, not a confirmed base. Section 10 adds a one-hour decision gate so that you commit to it or drop it early.

The doc is ordered so that Section 4, the persona build, can be read on its own.

## Corrections log

Every problem found in v1 is listed once with its fix. The last column says where the fix lives in this doc.

| # | Problem in v1 | Fix | Where |
| --- | --- | --- | --- |
| 1 | Example action `smile_and_listen` is not in the allowlist; emotion, gaze and next\_action have no value lists | One action enum plus separate enums for emotion, gaze and next\_action; a combined behaviour is two fields, not one string | Section 6 |
| 2 | `people` table has one verification status, no `checked_at`, no analysis link; `consent_or_authorization_status` is renamed to `consent_status` | Separate status fields, one name per field, and a `profile_analyses` table | Section 5 |
| 3 | Five persona layers and five claim labels do not map to each other; `participant_provided` has no home | One mapping table from label to layer to table column | Section 4 |
| 4 | One evaluation per date cannot give each person their own ranking | Each date produces two directed evaluations, one per participant | Sections 5 and 7 |
| 5 | Real-people requirement conflicts with the consent guidance | Three participant tiers: consenting real, authorized-with-limits, fictional | Section 9 |
| 6 | Scoring leaves the unknown-component method open | One method chosen: renormalize over known components and show a coverage figure | Section 7 |
| 7 | LinkedIn and Instagram extraction is not compliant or reliable | Participant-supplied intake; URLs stored as links only | Section 3 |
| 8 | No orientation or gender eligibility logic | Participant-stated eligibility filter applied before any date is scheduled | Section 7 |
| 9 | Rubric is circular: an LLM judges LLM dialogue; interest and activity overlap | Judge sees only cited evidence and the transcript; activity alignment merged into the interest component; judge run twice and averaged | Section 7 |
| 10 | No privacy model for who sees whose ranking | Role-based access, self-only ranking view, consent withdrawal and deletion | Section 9 |
| 11 | No cost or time estimate | Call-count and time model with a batch plan | Section 8 |
| 12 | Repeatability test assumes seeded LLM output | Measure variance across repeated runs instead of expecting identical output | Section 8 |
| 13 | Demo is exactly 180 seconds with a live LLM step | Target 150 seconds, live date replaced by a cached replay with one short live turn | Section 10 |
| 14 | One-hour milestone is unrealistic | Re-scoped to a 2 to 3 day prototype; the first hour becomes a decision gate | Section 10 |

## Data intake without scraping

Use the information you already hold as the evidence base, and treat the LinkedIn and Instagram URLs as labelled links, not as data sources. This removes the compliance problem and makes every claim traceable to something a person actually supplied.

**What the system does with each input type**

| Input | Allowed use | Evidence type | Default confidence |
| --- | --- | --- | --- |
| Participant questionnaire answers | Direct preferences, boundaries, goals | `participant_provided` | High |
| Bio, CV or profile text the person pasted or exported themselves | Profession, skills, stated interests | `observed_fact` | High |
| Notes you wrote from knowing the person | Context only; flag as second-hand | `observed_fact` with `second_hand` flag | Medium |
| Screenshots or posts the person shared | Interests and activities shown | `observed_fact` | Medium to high |
| LinkedIn or Instagram URL | Stored as a reference link; never fetched | None | Not applicable |
| Anything you guessed about their personality | Not stored as fact | `inference` only, labelled | Low |

**Intake form (one per person)**

1. Display name and a short self-description, in their own words.
2. Pasted or attached bio text, with the date it was copied.
3. Up to five interests or activities, each with a one-line example.
4. Date preferences: preferred activities, pace, topics they enjoy or avoid.
5. Relationship goal, and who they are open to meeting.
6. Hard boundaries and topics the agent must never raise.
7. Consent checkboxes: take part in simulations, store data, appear in other people's candidate lists, and a separate consent for any real name or photo shown in the demo.

**Verification status, stated honestly**

- `link_provided` means the URL was entered. It does not mean the account was checked or belongs to the person.
- `identity_confirmed_by_participant` means the person confirmed the link is theirs, in the intake form or by a one-click confirmation message.
- `inaccessible` or `needs_review` are set manually.
- The system must not display "verified" for any record where no one performed a check.

**Where this is ambiguous.** I do not know whether your existing information is structured or free text, or how old it is. If it is free text, Section 4 step 2 describes how to split it into atomic claims. If it is older than about a year, record its date so the persona can flag possible staleness.

## Building a successful persona from existing information

A persona is a compiled view of a claim store, not a written biography. The agent should be able to say only what the claim store supports, ask about what it does not, and behave the same way across a whole date. The nine steps below achieve that. Every threshold in this section is provisional and should be tuned on your own test runs.

**Mapping of labels, layers and storage**

This resolves the mismatch in v1 between five claim labels and five persona layers.

| Claim label | Persona layer | Stored in | Who may create it |
| --- | --- | --- | --- |
| `observed_fact` | A: Observed facts | `evidence_claims` | Extraction step, from supplied text |
| `inference` | B: Cautious inferences | `evidence_claims` with `is_inference = true` | Extraction step, capped confidence |
| `unknown` | C: Unknowns | `persona_json.unknowns`, generated from empty fields | System, automatically |
| `participant_provided` | D: Preferences (real) | `evidence_claims` and `persona_json.known_preferences` | Participant only |
| `simulation_only` | D: Preferences (demo) | `persona_json.simulation_preferences` | Operator, always labelled |
| (rules) | E: Behavioural policy | System prompt, not data | Developer |

### Step 1. Collect and date the raw material

Put everything you hold about one person into a single raw bundle: questionnaire answers, pasted bio, notes, shared posts. Record the origin and the date of each item. Do not merge items yet. Raw text is kept unchanged so any later claim can be traced back to it.

### Step 2. Split the material into atomic claims

Ask the model to output one claim per line, never a summary. A good claim is short, checkable and has a quote or pointer.

- Good: "Works as a data analyst" with the sentence from the bio that states it.
- Bad: "Is a driven, curious professional" because it is an interpretation of several things.

Require each claim to carry `claim_text`, `origin_item_id`, `evidence_summary` (a short paraphrase or a quote under 25 words) and `evidence_type`. Reject any output claim that has no `origin_item_id`; this is the main guard against invented traits.

### Step 3. Label each claim

Run a second, separate pass that assigns exactly one label from the table above. Using a separate pass avoids the model mixing extraction and judgement. Rules for the labeller:

1. If the person wrote it about themselves, it is `observed_fact` or `participant_provided`.
2. If it needs one extra step of reasoning, it is an `inference`. Cap inference confidence at 0.6, and require two or more independent items to raise it to 0.7.
3. Romantic or relationship preferences are never inferred. They are `participant_provided` or `unknown`.
4. Sensitive categories (health, sexuality, religion, politics, finances, immigration status) are never inferred and are stored only if the participant supplied them for this purpose with explicit consent.

### Step 4. Resolve duplicates and conflicts

Group claims by topic. If two claims conflict (for example, two different job titles), keep both, mark the older as `superseded` or both as `conflicting`, and add a contradiction note. The agent must not pick one silently. A conflict becomes something it can ask about on the date.

### Step 5. Measure evidence coverage

Count how many of these eight areas have at least one supported claim: work or study, interests, activities, communication style, values, date preferences, relationship goals, boundaries. Coverage is that count divided by eight.

| Coverage | Tier | How the agent behaves |
| --- | --- | --- |
| 6 to 8 areas | Rich | Uses evidence freely and can volunteer topics |
| 3 to 5 areas | Thin | Mostly asks questions, shares only supported facts |
| 0 to 2 areas | Minimal | Not ranked as a real person; run as a labelled demo agent or collect more data first |

This tier is the honest answer to a person with little information. A thin persona should be less talkative and more curious, not more inventive.

### Step 6. Compile the persona card

Build a compact card of about 500 to 900 tokens from the claim store. The card has fixed sections so the model always sees the same shape.

1. **Identity line:** display name and "simulated agent, not the real person".
2. **Known facts:** the top 8 to 12 claims by relevance and confidence, each with its claim id.
3. **Cautious inferences:** at most 3, each prefixed "may".
4. **Preferences:** participant-provided first; demo preferences second, tagged `[SIMULATED]`.
5. **Unknowns:** an explicit list, such as relationship goals unknown.
6. **Style:** the communication style the participant chose, or a neutral default marked as a default.
7. **Boundaries:** topics never to raise.

Select claims per date, not once. For a date with candidate B, rank A's claims by overlap with B's topics, then by confidence. This keeps the card short and makes shared interests surface naturally without inventing them.

### Step 7. Fix the prompt structure

Use the same layout every turn so the agent's behaviour cannot drift.

1. **System message (never changes):** the behavioural policy from Layer E, the output JSON schema and the allowed enums.
2. **Persona card (read-only data):** from Step 6.
3. **Partner card (reduced):** only the facts the partner has said during this date plus their display name. The agent must not see the partner's full evidence store, because a real person would not have it.
4. **Session memory:** the last 6 turns verbatim, plus a running list of facts established in this date.
5. **Turn instruction:** whose turn, the scenario beat (arrival, ordering, small talk, deeper topic, closing), and the maximum length.

Two details matter most. First, do not let the agent see the partner's raw profile, or it will quote facts nobody told it. Second, store anything learned during the date in session memory only, never back into `evidence_claims`.

### Step 8. Validate every turn

Run cheap checks on each response before it is shown or saved.

| Check | Method | On failure |
| --- | --- | --- |
| Schema valid and enums allowed | Code | Retry once; then fall back to `talk` with a neutral line |
| Cited claim ids exist in the card | Code | Remove the citation; retry once |
| No fact absent from card or session memory | Second small model call, or string match on named entities | Retry once with a corrective instruction |
| Inference not stated as certain | Second small model call | Retry once |
| Boundary topics not raised | Keyword list plus model check | Retry; if it fails again, skip the topic |
| Action matches dialogue (a `laugh` action needs a humorous line) | Rule table | Replace the action with `talk` |

Log every failure with the reason. The failure rate is one of your evaluation measures.

### Step 9. Test personas before running the batch

Build a fixed test set of about 20 prompts per persona: questions the card answers, questions it does not answer, a request to reveal something sensitive, a provocation, and an attempt to contradict a fact. Run each persona three times on the set.

| Measure | Definition | Provisional target |
| --- | --- | --- |
| Fact grounding | Share of stated facts that match the card | 95% or higher |
| Unsupported-claim rate | Share of turns with an invented fact or memory | Under 3% |
| Unknown handling | Share of unanswerable questions answered with uncertainty or a question | 90% or higher |
| Consistency | Share of runs where the same question gets compatible answers | 90% or higher |
| Action alignment | Share of turns where the action fits the dialogue | 90% or higher |

Do not run the 25-person batch until two personas meet these targets on a full date.

### Worked example (fictional data)

Raw input for fictional person P-017: bio text saying "UX researcher, I run weekend trail loops and I'm learning pottery", and a questionnaire answer "I'd rather do a casual coffee than a formal dinner."

| Claim | Label | Confidence |
| --- | --- | --- |
| Works as a UX researcher | `observed_fact` | 0.95 |
| Runs trails on weekends | `observed_fact` | 0.9 |
| Is learning pottery | `observed_fact` | 0.9 |
| Prefers a casual coffee to a formal dinner | `participant_provided` | 0.95 |
| May enjoy outdoor activities generally | `inference` | 0.55 |
| Relationship goals | `unknown` | not applicable |

The coverage count is 3 of 8 areas (work, activities, date preference), so this is a thin persona. Its agent should mention the trail running only if the partner raises something related, ask about the partner's weekends, and say it does not know its own plans when asked about long-term goals. It must not claim to love hiking with a partner, because that is an inference stretched into a preference.

**Common failure modes**

- **Trait invention:** the agent adds humour, shyness or a childhood story. Fix by removing adjectives from the card and checking with Step 8.
- **Over-confident inference:** "may enjoy outdoor activities" becomes "loves hiking". Fix by the "may" prefix and the validation check.
- **Everyone agrees with everyone:** models tend to be agreeable, which inflates scores. Fix by giving each agent permission to disagree politely and by having the judge penalise unearned agreement.
- **Drift in long dates:** the persona softens over time. Fix by re-injecting the card every turn and capping a date at about 12 to 16 turns.
- **Thin personas sound identical:** fix by varying only the participant-supplied style field, not by adding invented quirks.

## Schemas

The tables below replace the v1 list. Each field name is used identically everywhere, and every row that feeds a score can be traced back to a persona version and a scoring version.

| Table | Key fields | Purpose |
| --- | --- | --- |
| `people` | `person_id`, `display_name`, `participant_tier`, `linkedin_url`, `instagram_url`, `linkedin_link_status`, `instagram_link_status`, `identity_match_status`, `consent_status`, `eligibility_json`, `checked_at`, `created_at`, `updated_at`, `deleted_at` | One row per person; link and identity statuses kept separate |
| `raw_inputs` | `input_id`, `person_id`, `origin`, `captured_on`, `raw_text` | Unchanged source material |
| `evidence_claims` | `claim_id`, `person_id`, `input_id`, `claim_label`, `claim_text`, `evidence_summary`, `confidence`, `is_inference`, `status` (active, superseded, conflicting), `created_at` | Atomic claims with labels from Section 4 |
| `profile_analyses` | `analysis_id`, `person_id`, `coverage`, `tier`, `unknowns_json`, `model_version`, `created_at` | Result of the analysis run; replaces the missing `profile_analysis_id` target |
| `personas` | `persona_id`, `person_id`, `analysis_id`, `persona_version`, `persona_json`, `created_at` | Versioned persona card source |
| `scenarios` | `scenario_id`, `name`, `setting`, `beats_json`, `max_turns` | Date setting and turn beats |
| `date_sessions` | `session_id`, `person_a_id`, `person_b_id`, `persona_a_id`, `persona_b_id`, `scenario_id`, `run_index`, `status`, `started_at`, `completed_at` | One simulated date; pair stored in a fixed order, smaller id first |
| `date_turns` | `turn_id`, `session_id`, `turn_index`, `speaker_person_id`, `turn_json`, `validation_result`, `retry_count` | One row per turn, so a failed run can resume |
| `date_evaluations` | `evaluation_id`, `session_id`, `evaluator_person_id`, `target_person_id`, `component_scores_json`, `evidence_coverage`, `uncertainty_flags`, `explanation`, `scoring_version`, `judge_run` | Two rows per date, one for each direction |
| `rankings` | `ranking_id`, `person_id`, `candidate_person_id`, `rank_position`, `score`, `confidence`, `explanation`, `evaluation_ids`, `scoring_version`, `generated_at` | One list per person, built from all their evaluations |
| `access_grants` | `grant_id`, `person_id`, `viewer_role`, `scope`, `granted_at`, `revoked_at` | Who may see what (Section 9) |
| `audit_log` | `log_id`, `actor`, `action`, `object`, `at` | Views, exports and deletions |

**Notes on the design**

- `participant_tier` takes the values `consenting_real`, `authorized_limited` or `fictional` (Section 9).
- `eligibility_json` holds the participant's stated answers: who they are open to meeting, age range, and an opt-out for appearing in other lists.
- `run_index` allows several runs of the same pair, which Section 8 uses to estimate variance. A ranking uses the mean across runs.
- Deleting a person sets `deleted_at`, removes their raw inputs and claims, and removes or anonymises their sessions and evaluations. Rankings that reference them are regenerated.

**Persona JSON, corrected**

```json
{
  "persona_id": "persona_017_v2",
  "person_id": "person_017",
  "tier": "thin",
  "coverage": 0.375,
  "identity_line": "Simulated agent for P-017; not the real person",
  "known_facts": [
    {"claim_id": "c_101", "text": "Works as a UX researcher", "confidence": 0.95},
    {"claim_id": "c_102", "text": "Runs trails on weekends", "confidence": 0.9}
  ],
  "inferences": [
    {"claim_id": "c_110", "text": "May enjoy outdoor activities", "confidence": 0.55}
  ],
  "known_preferences": [
    {"claim_id": "c_120", "text": "Prefers a casual coffee to a formal dinner", "source": "participant_provided"}
  ],
  "simulation_preferences": [],
  "unknowns": ["relationship goals", "communication style", "values"],
  "style": {"value": "neutral default", "is_default": true},
  "boundaries": [],
  "eligibility": {"open_to": "stated by participant"}
}
```

This is placeholder data for a fictional person. The behavioural policy is not stored in the persona; it lives in the system prompt so that nothing in the data can override it.

## Agent turn protocol and action enums

The model returns one JSON object per turn. Code validates it against fixed value lists, so the scene engine never receives anything it cannot play. A combined behaviour such as smiling while listening is expressed as two fields, which fixes the `smile_and_listen` problem in v1.

| Field | Allowed values |
| --- | --- |
| `action` | `idle`, `walk_to_table`, `sit`, `talk`, `listen`, `smile`, `laugh`, `gesture`, `stand_up`, `leave` |
| `secondary_action` (optional, played as an overlay) | `none`, `smile`, `nod`, `lean_in`, `look_away` |
| `emotion` | `neutral`, `interested`, `amused`, `curious`, `uncomfortable`, `bored`, `warm` |
| `gaze` | `partner`, `table`, `away`, `menu` |
| `next_action` | `ask_question`, `share_fact`, `react`, `change_topic`, `wrap_up` |

The full turn object also holds `dialogue` (maximum 45 words), `evidence_used` (claim ids from the card), `uncertainty_note` (text or null) and `private_rating` (see below).

**Rules the engine applies**

1. Any value outside its list is replaced by the default (`talk` for action, `none` for secondary, `neutral` for emotion, `partner` for gaze) and the substitution is logged.
2. The model never runs code and never controls the browser. It only selects labels.
3. Timing belongs to the animation controller: a turn lasts `max(clip length, dialogue length at about 2.5 words per second)`, so animation and subtitles stay in step.
4. A `laugh` action is accepted only if the previous partner line or this line is marked as humorous by the validator; otherwise it becomes `smile`.
5. Turns alternate strictly. A `wrap_up` from either agent starts the closing beat; the date ends after both have said goodbye or at `max_turns`.
6. The scene beats are `arrival`, `ordering`, `small_talk`, `deeper_topic`, `closing`. Each beat has a minimum and maximum number of turns defined in the scenario row.

**Private rating (new)**

After each turn, the speaker also returns `private_rating`, an integer from 1 to 5 on how comfortable the conversation feels, with a one-line reason. It is hidden from the partner and from the live subtitle. It lets the evaluation see how each side experienced the date without relying only on a later judge reading the transcript. Treat it as simulated opinion, not as a real emotion.

**Disclosure and safety lines**

- The scene shows a persistent "AI simulation" label and each avatar is labelled with the display name and "simulated".
- Agents may disagree, decline a topic or end the date politely. A polite early exit is a valid outcome and is scored, not hidden.
- Real names and photos appear only for participants who gave the separate demo consent in the intake form. Everyone else appears as a stylised avatar with a display name or alias.

## Eligibility, scoring and rankings

This section closes the biggest logic gaps in v1: who can be matched with whom, how unknown information is handled, and how one date yields a separate ranking entry for each person.

### Eligibility filter

A date is scheduled between A and B only if both conditions hold.

1. A's stated openness includes B, and B's stated openness includes A. Both answers come from the participants. The system never infers them.
2. Each person's stated age range includes the other, and both are adults.

People whose openness is not stated cannot be scheduled in a real ranking. They can appear in a labelled demo-only mode. Candidates a person is not eligible for are not shown in that person's list at all, rather than being ranked low. As a result, the number of dates and ranking entries will be lower than the 300 and 600 in v1, which assumed everyone could match everyone. The true counts are computed after intake.

Gender or orientation details are sensitive. Collect them only as the participant's own answer to the eligibility question, store the minimum needed, and never use them for anything except this filter.

### Components of a directed evaluation

For each date, an evaluation is produced from A's side about B, and another from B's side about A. The weights remain provisional and unvalidated. They differ from v1 in that activity alignment is merged into interests, and a respect and balance component is added so that agreeable but shallow dates are not rewarded.

| Component | Weight | How it is computed |
| --- | --- | --- |
| Shared interests and activities | 30% | In code: overlap of topic tags between the two claim sets, weighted by confidence, plus overlap with the activities each preferred for the date |
| Stated preference alignment | 25% | A's `participant_provided` preferences compared with what B's supported claims or stated preferences show; each match cites claim ids |
| Interaction quality | 30% | Mean of two judge runs (0 to 100) on the transcript, blended with the evaluator's own `private_rating` turns |
| Respect and balance | 15% | Judge score for turn balance, curiosity about the partner, and handling of boundaries or disagreement |

### Handling unknown components

If a component cannot be computed, for example because A gave no preferences, it is dropped and the remaining weights are rescaled to sum to 1. The evaluation then records a coverage value, the sum of the original weights of the components that were computed.

```latex
S_{raw} = \frac{\sum_{i \in K} w_i s_i}{\sum_{i \in K} w_i}, \qquad c = \sum_{i \in K} w_i
```

Here K is the set of known components, w the weights and s the component scores from 0 to 100. Raw scores computed on different components are not directly comparable, so rankings use a shrunk score that pulls low-coverage results toward the median of the pool.

```latex
S_{adj} = c \cdot S_{raw} + (1 - c) \cdot \text{median}(S_{raw})
```

Confidence labels follow coverage: high at 0.85 or above, medium from 0.6 to below 0.85, low below 0.6. Both the raw and adjusted scores are shown. This is a design choice rather than a validated method; the alternative is to hide low-coverage candidates from the top of the list, which is simpler but discards information.

### Making the judge less circular

- The judge sees only the transcript and the cited claims from each persona card. It does not see the agents' hidden reasoning.
- It scores each component against a written anchor scale, for example 20 means repeated friction, 50 means polite but flat, 80 means sustained mutual engagement.
- It runs twice with the speaker order described differently. If the two runs differ by more than 15 points on a component, the evaluation is flagged for review.
- Use a different model for the judge than for the agents where possible, to reduce self-preference.
- The explanation must quote or point to turn numbers. An explanation that cites nothing is rejected.

### Ranking logic

1. For person A, collect the directed evaluations where A is the evaluator, across all eligible candidates and all run indices.
2. Average repeated runs of the same pair.
3. Sort by `S_adj`, highest first.
4. Mark any two neighbouring candidates whose scores differ by less than 5 points as "not clearly different".
5. Store the explanation with each entry: top two supporting moments, top friction, shared interests with claim ids, unknowns and confidence.
6. Show a mutual view, the lower of A's and B's adjusted scores, as an optional second sort, since a one-sided high score is not a likely match. Never present it as a real-world prediction.

Every ranking page carries one line: this measures how two configured agents interacted in a simulation, and it does not predict how the real people would get on.

## Pairwise run plan, cost and reliability

A full run of 300 dates is roughly 10,500 model calls, 16 million input tokens and 1.4 million output tokens, and about 1 hour at 8 parallel workers. These are my estimates from the assumptions listed below, not measurements. Measure on 5 real dates first and replace them.

**Assumptions**

| Item | Assumed value |
| --- | --- |
| Turns per date | 14 (7 per agent) |
| Agent call input and output | 1,800 and 150 tokens |
| Validation call input and output | 900 and 60 tokens |
| Retry rate | 10%, so 2.2 calls per turn |
| Judge calls per date | 4 (two runs, two directions), about 3,900 tokens in and 400 out each |
| Latency per call | about 3 seconds on a hosted model |

**Resulting estimate for one date and for 300 unique pairs with one run each**

| Measure | One date | 300 dates |
| --- | --- | --- |
| Model calls | about 35 | about 10,500 |
| Input tokens | about 53,000 | about 16 million |
| Output tokens | about 4,500 | about 1.4 million |
| Time, sequential | about 105 seconds | about 8.75 hours |
| Time, 8 parallel workers | not applicable | about 1.1 hours |

The eligibility filter will reduce these numbers, and every extra run for variance multiplies them. Multiply the token counts by your provider's prices to get a cost. A local model removes per-token cost but is often several times slower, and speed depends on your hardware, so benchmark it.

**Staged plan**

| Stage | Scope | Exit condition |
| --- | --- | --- |
| 1 | One persona, test set of 20 prompts | Section 4 step 9 targets met |
| 2 | Two personas, one full date | Transcript, actions and two directed evaluations saved and reopened |
| 3 | Five people, all eligible pairs, 3 runs each | Score spread measured; failure rate under 5% |
| 4 | Full cohort, 1 run per eligible pair | All rankings generated, none missing |
| 5 | Re-run the pairs with the widest spread | Rankings stable enough to publish |

**Reliability design**

- Use a job queue where each date is a job with a status of `queued`, `running`, `complete`, `failed` or `partial`. Jobs are idempotent: re-running a complete job does nothing.
- Save every turn to `date_turns` as it happens, so a crash resumes from the last saved turn instead of restarting.
- Retry a failed model call with backoff up to 3 times, then mark the date `partial`. A partial date is never scored as if it were complete; it is shown with a clear status.
- Rate-limit the workers to stay inside the provider's limits, and pause the whole queue on repeated authentication or quota errors.
- If a person has fewer than a minimum number of completed evaluations, show their ranking as incomplete and say how many are missing.
- Record the model name and version on every date and evaluation, so results are explained by the configuration that produced them.

**Repeatability**

Many hosted models do not guarantee identical output even at a fixed temperature, so do not test for identical text. Run each of five pairs three times and compute the standard deviation of the raw score. If it is above about 8 points, either increase the number of runs per pair or lower the agent temperature and re-test. Record the spread in the evaluation so that a ranking can show how stable it is.

## Privacy, access control, consent and deletion

The rankings say who an agent liked, which is personal even when simulated. v1 let anyone open any person's list. Restrict that before the system holds real people's data.

**Participant tiers (resolves the real-people conflict in v1)**

| Tier | Who | What is allowed |
| --- | --- | --- |
| `consenting_real` | Adults who completed the intake form and gave consent | Full pipeline and appearing in other people's lists |
| `authorized_limited` | Adults who agreed to a narrower use, for example to be a candidate only | Only the uses they ticked; no demo display of name or photo unless separately agreed |
| `fictional` | Invented profiles | Anything, always labelled fictional |

The requirement for 25 real adults is met only by the first two tiers. If fewer than 25 consent, fill the cohort with fictional profiles and say so in the demo. Do not treat a person's public profile as consent.

**Access roles**

| Role | Can see |
| --- | --- |
| Participant | Own profile, own claims, own persona, own ranking and its explanations. Other people's names appear only as the consented display name or alias |
| Operator | All records, with every view written to the audit log |
| Demo viewer | Fictional or demo-consented records only |
| Public | Nothing |

A participant never sees how a candidate ranked them. Showing it would reveal rejection, so the mutual view in Section 7 is for operators only.

**Consent and deletion**

1. Consent is stored per purpose with a timestamp: simulation, appearing in others' lists, and demo display.
2. A person can withdraw at any time. Withdrawal sets `deleted_at`, deletes raw inputs and claims, removes their sessions, and regenerates the other rankings that included them.
3. Backups and exports must follow the same deletion rule or be dropped on a short schedule.
4. Keep only the source material needed. Do not store full pages or images when a short evidence summary is enough.
5. Do not fetch or republish anything from LinkedIn or Instagram. Check each platform's current terms before showing a profile link in a public demo.

**Other safeguards**

- Confirm everyone is an adult at intake and store only the fact that the check was passed.
- Do not store sensitive categories unless the participant supplied them for the eligibility filter or a stated boundary. Never infer them.
- Encrypt the database at rest and keep model API keys outside the repository.
- Send as little personal data to a hosted model as the task needs: the persona card, not the raw inputs. Check your provider's data-retention terms; if they are not acceptable, use a local model.
- Tell participants plainly that the output is a simulation and not a recommendation about real people.

I am not a lawyer. Data-protection law depends on where participants live, so have someone qualified review the consent text before you collect real data.

## Schedule and demo storyboard

A complete system is roughly 13 to 19 working days for one developer who already knows the stack. This is a rough estimate that I cannot check against your skills, team size or assets. The first hour is not a prototype. It is a decision gate.

**Phases, in order**

1. **Decision gate (1 to 2 hours).** Clone Heartmorrow, read its licence and asset licences, run it, and check whether it can drive a 3D scene from structured model output. If yes, extend it. If not, build a thin React and Three.js app instead of bending a game engine around the pipeline. Decide and write the decision down.
2. **Persona and evidence (2 to 3 days).** Intake form, raw inputs, claim extraction and labelling, coverage tiers, persona card compiler, test set. Exit: Section 4 step 9 targets met on two personas.
3. **Two-agent date (2 to 3 days).** Turn protocol, validator, session memory, saved turns, resume. Exit: one complete date saved and reopened after refresh.
4. **Scene and synchronisation (3 to 5 days).** One restaurant, two avatars, the action list, subtitles, camera presets, AI-simulation label. This is the most asset-dependent phase and the most likely to overrun.
5. **Evaluation and rankings (2 to 3 days).** Component scoring, judge, directed evaluations, shrinkage, ranking pages and explanations.
6. **Batch, access and deletion (2 to 3 days).** Job queue, eligibility filter, roles, consent withdrawal, audit log.
7. **Test and record (about 2 days).** Cohort run, failure handling, persistence checks, demo recording and review.

**Demo storyboard, 150 seconds with a 30 second buffer**

Precompute everything. Show one live turn only to prove the model is connected, then play the saved date from the database. v1 planned a live full date inside 50 seconds, which depends on model speed you do not control.

| Time | Segment | What must be visible |
| --- | --- | --- |
| 0:00 to 0:20 | Cohort | At least 25 people, tier labels, link status and consent status, with no "verified" claim for unchecked links |
| 0:20 to 0:45 | One profile | Claims with evidence, inferences marked, unknowns listed, coverage tier |
| 0:45 to 1:35 | Date room | One live turn, then the saved date replayed with actions, subtitles, the simulation label and the post-date evaluation |
| 1:35 to 2:05 | Rankings | One person's list, confidence labels, one explanation opened down to cited turns |
| 2:05 to 2:30 | Persistence | Refresh the page, reopen the same profile, date and ranking from the database |

The segments sum to 150 seconds. The recording should show the real application throughout, because a mock-up or an unrelated animation would not show the system working.

## Acceptance checklist and open questions

The project is ready to demonstrate only when every box below can be ticked from the running application.

- [ ] At least 25 participants exist, and each one's tier (real, limited or fictional) is shown honestly.
- [ ] Each person has consent records per purpose and an eligibility answer; anyone without one is excluded or marked demo-only.
- [ ] LinkedIn and Instagram links are stored as links with an honest status, and nothing is fetched from those sites.
- [ ] Every claim has a source item, a label and a confidence; inferences are marked and capped.
- [ ] Each person has a versioned persona with a coverage tier and an explicit unknowns list.
- [ ] Two personas pass the Section 4 test targets before the batch starts.
- [ ] Turns are schema-checked against fixed enums, and unknown values fall back and are logged.
- [ ] Two agents complete a multi-turn date with synchronised subtitles and actions.
- [ ] Each date has two directed evaluations with component scores, coverage and cited explanations.
- [ ] Each eligible person has a ranking with adjusted scores, confidence labels and "not clearly different" markers.
- [ ] Participants can see only their own ranking, and every operator view is logged.
- [ ] A withdrawal test removes a person's data and regenerates the affected rankings.
- [ ] Failed or partial dates are visible as such and never counted as complete.
- [ ] Results persist after refresh.
- [ ] Repository, model, character and animation licences are checked and recorded.
- [ ] The recorded demo is 150 seconds or less and shows the running system.

**Open questions that change the design**

1. What form is your existing information in (structured fields, free text, screenshots), and how old is it? This decides how much work Step 2 is.
2. Did each person agree to be included in a dating simulation, and can they confirm who they are open to meeting? Without this, the eligibility filter and the real-people tier cannot be used.
3. Is this a class or research project, or a product for real users? A real product needs legal review, age verification and much stricter access control than this blueprint.
4. Will you use a hosted model or a local one? This affects privacy terms, speed and cost.
5. Do you have permission to use any real names or photos in a recorded demo?

This blueprint treats compatibility as a property of the simulation. If you later want it to mean something about real people, the only defensible route is to compare the rankings with feedback the participants give themselves, and to report how well the two agree.

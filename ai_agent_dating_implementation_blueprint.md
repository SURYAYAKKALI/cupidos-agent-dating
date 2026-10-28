# AI Agent Dating Simulation Website
## Implementation Blueprint and Persona Engineering Plan

**Project objective:** Build a working website in which each person is represented by an AI agent, agents go on simulated dates in a visual environment, and the system produces explainable compatibility rankings.

**Core requirement:** This must be a functioning application—not just a styled page or a chatbot. The demo must show profile import, profile analysis, an actual multi-turn simulated date, and saved rankings. The target demonstration is no longer than three minutes.

---

## 1. Product Scope

The system has six main modules:

1. **People and source management**
   - Support at least 25 real adult participants or appropriately authorized public-profile subjects.
   - Store a LinkedIn URL and a public Instagram URL for each person.
   - Track whether the URLs were checked, whether identity matching is confirmed, and when the check occurred.
   - Keep source links and evidence attached to every profile claim.
   - Do not treat a URL alone as proof that an account belongs to the person.

2. **Profile analysis**
   - Extract publicly supported interests, hobbies, topics, activities, and professional context.
   - Separate direct evidence from model inference.
   - Include confidence, evidence links, unknowns, and contradictory evidence.
   - Do not present guesses about private romantic preferences, mental health, sexuality, or other sensitive traits as facts.

3. **Persona and agent creation**
   - Create one persistent agent for each person.
   - Use a structured persona record rather than a single free-form prompt.
   - Preserve known facts, uncertainty, boundaries, memory, and behavioral consistency.
   - Make the agent's simulated choices traceable to supplied information or explicit simulation settings.

4. **Visual date simulation**
   - Render two avatars in a restaurant or other date environment.
   - Show arrival, sitting, dialogue, expressions, gestures, and scene transitions.
   - Generate actions in sync with the conversation.
   - Include subtitles and optionally generated speech.
   - Label the scene as an AI simulation, not an actual event involving the real people.

5. **Compatibility and ranking**
   - Run pairwise simulated dates.
   - Save dialogue, actions, evaluations, and scores.
   - Produce an individual ranked list for each person.
   - Explain why each candidate ranked where they did, including uncertainty and missing information.

6. **Persistence, demo, and reliability**
   - Store profiles, personas, date sessions, scores, and rankings in a database.
   - Ensure results remain available after refresh.
   - Handle API failures, missing profile evidence, and incomplete simulations.
   - Record an end-to-end demo of three minutes or less.

---

## 2. Recommended Architecture

Prefer extending an existing dating simulator if its code, license, and architecture are suitable. Heartmorrow was identified as a potential starting point, but it is a dating simulation game—not a complete LinkedIn/Instagram analysis and ranking product. Inspect the current repository, license, dependencies, setup instructions, and asset licenses before committing to it.

Potential starting point:
- Heartmorrow: https://github.com/HMDSimDev/heartmorrow
- Three.js: https://threejs.org/
- React Three Fiber: https://r3f.docs.pmnd.rs/
- Mixamo: https://www.mixamo.com/
- Blender: https://www.blender.org/
- Ollama: https://ollama.com/
- LM Studio: https://lmstudio.ai/
- LinkedIn: https://www.linkedin.com/
- Instagram: https://www.instagram.com/
- OBS Studio: https://obsproject.com/

Suggested stack:
- Frontend: React; use the existing simulator's stack if extending it.
- 3D visuals: Three.js / React Three Fiber, or the simulator's existing scene engine.
- Backend: reuse the existing server if possible; otherwise FastAPI or Node.js.
- Database: SQLite for a prototype; PostgreSQL if deployment requires multi-user scale.
- LLM: hosted API or a local model through a compatible interface.
- Optional voice: browser speech synthesis or a text-to-speech service.
- Recording: OBS Studio.

Do not build two separate frontends or backends unless integration requires it. Reuse one app and one source of truth for data.

---

## 3. Data and Source Ingestion

### Recommended record fields

- person_id
- display_name
- linkedin_url
- instagram_url
- linkedin_verification_status
- instagram_verification_status
- identity_match_status
- checked_at
- source_evidence[]
- consent_or_authorization_status
- profile_analysis_id
- persona_id

Use statuses such as:
- `unverified`
- `checked_public`
- `identity_match_confirmed`
- `inaccessible`
- `needs_review`

Only mark a record as verified when the checks actually happened.

### Data collection principles

- Use official public pages and permitted access methods.
- Respect platform terms, rate limits, robots/access controls, and privacy expectations.
- Do not bypass login walls, private accounts, access controls, or anti-bot systems.
- Do not assume that public profile visibility grants permission to republish a person's inferred romantic persona.
- Prefer consenting participants for a public demonstration. If consent is unavailable, use fictional or explicitly authorized test profiles.
- Store only the minimum source material needed for the demo and provide a way to remove a record.
- Never invent direct profile URLs or mark a profile as verified based only on a search result.

---

## 4. Persona Engineering: The Most Important Design

A persona should not be a paragraph that says, for example, “This person is funny, adventurous, and romantic.” That kind of prompt encourages the model to invent traits and can drift during a long conversation.

Use a **structured, evidence-grounded persona** with five separate layers:

### Layer A — Observed facts
Information directly supported by a source, such as a stated profession, an activity shown in a public post, or an interest explicitly mentioned in a public bio.

Each fact should contain:
- `claim`
- `source_url`
- `evidence_excerpt_or_summary`
- `observed_at`
- `evidence_type`
- `confidence`

### Layer B — Cautious inferences
Potential interpretations of repeated public signals. Each inference must be explicitly labelled as an inference and must include its rationale and confidence. It must not be silently converted into a fact.

Example:
- Observation: The public profile repeatedly features hiking trips.
- Cautious inference: “Outdoor activities may be an interest.”
- Do not infer: “This person wants an outdoorsy romantic partner.”

### Layer C — Unknowns
Explicitly record what the system does not know:
- Relationship goals
- Dating boundaries
- Preferred communication style
- Lifestyle constraints
- Whether the person would be interested in any particular candidate

Unknown means unknown. The agent must not fill these gaps with stereotypes.

### Layer D — Simulation preferences
For a safe, controllable simulation, use either:
1. Preferences explicitly supplied by a consenting participant, or
2. Clearly labelled fictional/demo preferences used only for testing.

Do not represent simulated preferences as the real person's actual wishes.

### Layer E — Behavioral policy
Rules that keep the agent consistent:
- Do not invent personal memories or biographical facts.
- If asked about an unknown, acknowledge uncertainty or ask a question.
- Do not claim to be the real person.
- Stay within the evidence and explicitly supplied simulation settings.
- Do not disclose private or sensitive data.
- Maintain consistent interests and conversational boundaries.
- Treat the other agent respectfully; allow disagreement and polite rejection.
- Keep a distinction between role-play dialogue and evidence-based profile facts.

### Example persona JSON

```json
{
  "persona_id": "persona_001",
  "person_id": "person_001",
  "identity_mode": "consented_simulation_or_fictionalized",
  "observed_facts": [
    {
      "claim": "Works in software engineering",
      "source_url": "https://example.com/public-bio",
      "evidence_summary": "The public bio states a software engineering role.",
      "confidence": 0.95
    }
  ],
  "inferences": [
    {
      "claim": "May enjoy technology-related discussion",
      "rationale": "Repeated public posts about technology",
      "confidence": 0.65,
      "is_inference": true
    }
  ],
  "known_preferences": [],
  "simulation_preferences": {
    "source": "demo_configuration",
    "values": ["enjoys thoughtful conversation"],
    "must_be_labelled_as_simulated": true
  },
  "unknowns": [
    "Actual relationship goals",
    "Actual dating boundaries",
    "Actual romantic preferences"
  ],
  "conversation_style": {
    "basis": "explicit_demo_setting",
    "description": "warm, curious, and concise"
  },
  "behavior_rules": [
    "Do not invent memories",
    "Do not present inference as fact",
    "Acknowledge unknowns",
    "Do not claim to be the real person",
    "Respect boundaries and disagreement"
  ]
}
```

This is a schema example with fictional placeholder data, not a claim about any real individual.

---

## 5. How to Build a Consistent Persona

### Step 1 — Analyze evidence into atomic claims
Do not ask the LLM to write a broad personality biography from a handful of profile links. Instead, extract small claims and attach source evidence to each one.

### Step 2 — Classify every claim
Use a controlled label:
- `observed_fact`
- `inference`
- `participant_provided`
- `simulation_only`
- `unknown`

Never merge these categories.

### Step 3 — Create a persona summary
Generate a concise, structured summary from the claim store. Include only information needed for simulation. Keep the original evidence separately so the summary can be checked.

### Step 4 — Add explicit preferences where possible
For a meaningful compatibility experiment, invite consenting participants to fill in a short questionnaire: desired date activities, communication preferences, relationship goals, boundaries, and important values. These are far more reliable than inferring romantic preferences from social media.

If no questionnaire is available, mark romantic preferences as unknown and use a clearly labelled, generic simulation scenario. Do not call that a prediction of real-life compatibility.

### Step 5 — Use a stable system prompt
Keep immutable behavioral rules in a system-level instruction. Pass the structured persona separately as data. Do not let the agent rewrite its own evidence or core persona during the date.

### Step 6 — Use bounded conversational memory
Store:
- Recent conversation turns
- Important facts established in the current simulated date
- Questions asked and answered
- Shared interests discovered during the simulation
- Disagreements or unresolved questions
- The agent's own post-date evaluation

Do not let one simulated conversation overwrite source evidence. Conversation-derived facts belong in session memory, not the permanent evidence store.

### Step 7 — Validate persona consistency
After each response, check:
- Does the response contradict an observed fact?
- Is an inference being presented as certain?
- Did the agent invent a memory or preference?
- Does the action JSON match the dialogue?
- Does it respect boundaries and role-play disclosure?

If validation fails, retry once with a corrective instruction or fall back to a safe neutral response.

### Step 8 — Evaluate personas before scaling
Test a small set of agents against a fixed set of scenarios. Measure:
- Fact-grounding accuracy
- Persona consistency
- Unsupported-claim rate
- Response relevance
- Action/dialogue alignment
- Repeatability across multiple runs

Do not scale to 25 agents until two agents can complete a date and produce a traceable evaluation.

---

## 6. Agent Conversation and Action Protocol

The LLM should return structured data instead of plain text alone.

Example:

```json
{
  "dialogue": "That sounds like a fun place to visit. What did you enjoy most?",
  "emotion": "interested",
  "action": "smile_and_listen",
  "gaze": "partner",
  "next_action": "ask_question",
  "evidence_used": ["claim_002"],
  "uncertainty_note": null
}
```

The frontend should:
1. Display the dialogue as a subtitle or speech bubble.
2. Play a compatible animation.
3. Set the expression and gaze if available.
4. Wait for the animation or turn duration.
5. Give the other agent its turn.
6. Save the complete turn and the action result.

Define an allowlist of valid actions, such as:
- `idle`
- `walk_to_table`
- `sit`
- `talk`
- `smile`
- `laugh`
- `listen`
- `gesture`
- `stand_up`
- `leave`

If the model returns an unknown action, use `idle` or `talk` as a fallback. The model must not execute arbitrary code or control the browser directly.

---

## 7. Visual Date Scene

For a minimum viable scene:
- One restaurant environment
- Two stylized, rigged avatars
- Table, chairs, and simple props
- Idle, walk, sit, talk, smile, laugh, listen, and stand animations
- Camera changes or a few preset camera angles
- Dialogue subtitles
- Optional voice output
- Date controls: Start, Pause, Continue, End
- A visible “AI-generated simulation” label

Use existing assets where licensing permits. Do not attempt realistic digital replicas of real people without explicit permission. Stylized avatars are faster to build and reduce the risk of viewers mistaking the simulation for actual footage.

The scene engine translates agent action labels into animation clips. The language model chooses from the allowed action list; the animation controller handles timing and playback.

---

## 8. Compatibility Scoring

Use an explicit rubric and save the component scores, not only a final number.

A possible initial rubric:
- Shared interests: 25%
- Explicitly supplied preferences: 25%
- Interaction quality in the simulated date: 30%
- Conversation and activity alignment: 20%

These weights are provisional and are not scientifically validated. Test and document them.

Example score record:
- person_a_id
- person_b_id
- date_session_id
- shared_interest_score
- preference_alignment_score
- simulated_interaction_score
- activity_alignment_score
- evidence_coverage
- uncertainty_flags
- total_score
- explanation
- scoring_version

If a component is unknown, do not silently treat it as a mismatch. Either calculate a normalized score over known components or mark the result as low-confidence. Document which method you use.

A simulated date measures how two configured agents interact in the simulation. It does not prove that the real people would be attracted to one another or behave in the same way.

---

## 9. Pairwise Simulation Plan

With 25 people:
- Unique unordered pairs: 25 × 24 / 2 = 300.
- Directed rankings: 25 × 24 = 600 candidate entries across all lists.
- Each person's ranking contains the other 24 candidates.

Build and test incrementally:
1. One profile and one persona.
2. Two agents and one complete date.
3. Two agents with saved results and a compatibility score.
4. Five people and a small batch of dates.
5. At least 25 profiles and batch processing.
6. Generate and save every person's ranking.
7. Reopen profiles, transcripts, and rankings after a page refresh.

For the three-minute demo, precompute and save results. Start one live date in the video, then show the saved ranking dashboard. Do not attempt all 300 pairings during recording.

---

## 10. Database Tables

Suggested initial tables:

### `people`
- `person_id`
- `display_name`
- `linkedin_url`
- `instagram_url`
- `verification_status`
- `consent_status`
- `created_at`
- `updated_at`

### `evidence_claims`
- `claim_id`
- `person_id`
- `claim_type`
- `claim_text`
- `source_url`
- `evidence_summary`
- `confidence`
- `created_at`

### `personas`
- `persona_id`
- `person_id`
- `persona_json`
- `persona_version`
- `created_at`

### `date_sessions`
- `session_id`
- `person_a_id`
- `person_b_id`
- `scenario_id`
- `status`
- `transcript_json`
- `started_at`
- `completed_at`

### `date_evaluations`
- `evaluation_id`
- `session_id`
- `scores_json`
- `explanation`
- `uncertainty_flags`
- `scoring_version`

### `rankings`
- `ranking_id`
- `person_id`
- `candidate_person_id`
- `rank_position`
- `score`
- `explanation`
- `evaluation_id`

Keep persona versions and scoring versions so that a ranking can be traced to the profile and rubric that generated it.

---

## 11. Website Pages

1. **Dashboard:** imported people, verification status, analysis progress, completed dates, ranking status.
2. **People list:** profile cards, source links, and filters for verification status.
3. **Profile detail:** observed facts, inferences, evidence links, unknowns, persona preview, and confidence.
4. **Agent inspector:** persona settings, memory summary, behavior rules, and test actions.
5. **Date room:** restaurant scene, two avatars, dialogue, actions, subtitles, controls, and transcript.
6. **Date report:** shared interests, conversational moments, conflicts, uncertainty, and component scores.
7. **Rankings:** select a person, inspect the other 24 candidates, sort by score, and open the underlying evaluation.
8. **Settings:** model configuration, simulation settings, data deletion, and scoring version.

---

## 12. Three-Minute Demo Storyboard

- **0:00–0:25 — Import:** show at least 25 people, direct source links, and verification status.
- **0:25–0:55 — Profile:** open one profile and explain evidence-backed interests, inferences, and unknowns.
- **0:55–1:45 — Date:** start a date; show multiple dialogue turns, visible reactions, and a post-date evaluation.
- **1:45–2:25 — Rankings:** open a person's ranking, compare candidates, and inspect explanations.
- **2:25–3:00 — Working proof:** refresh the app, reopen a saved profile/date, and show persisted rankings.

The recording must show the working app. A mockup, hardcoded chat transcript, or unrelated prerecorded animation alone does not demonstrate the complete system.

---

## 13. Implementation Schedule

### First hour: prove the core concept
- Get the existing simulator running.
- Configure a model and verify that it generates a multi-turn date.
- Create two test personas with different, explicitly configured traits.
- Show them in a scene with talking and laughing animations.
- Save the transcript and create one explainable compatibility evaluation.
- Confirm the saved result can be reopened.

### Next development phase
- Add profile import and verification records.
- Implement evidence extraction and structured personas.
- Build profile pages and an agent inspector.
- Synchronize LLM action outputs with the animation controller.
- Add saved evaluations and ranking views.

### Final integration phase
- Load at least 25 verified or appropriately authorized profiles.
- Batch the pairwise simulations.
- Generate all individual rankings.
- Test persistence, failure handling, and evidence traceability.
- Record and review the three-minute demo.

One hour is a prototype target, not a guarantee that the complete 25-person system can be finished in that time.

---

## 14. Acceptance Checklist

- [ ] At least 25 real adults or authorized participants are represented.
- [ ] Every profile has a LinkedIn URL and public Instagram URL.
- [ ] Identity matching and verification status are recorded honestly.
- [ ] Profile claims have evidence and confidence labels.
- [ ] Each person has a structured, versioned persona.
- [ ] Unknown preferences remain unknown unless supplied by the participant.
- [ ] Two agents complete a multi-turn simulated date.
- [ ] The restaurant scene displays synchronized actions and reactions.
- [ ] Date transcripts and evaluations are saved.
- [ ] Each person has a ranking of the other candidates.
- [ ] Every score has an explanation and uncertainty information.
- [ ] Results persist after refresh.
- [ ] The three-minute video shows the complete working pipeline.
- [ ] Repository, model, character, and animation licenses have been checked.
- [ ] Consent, source access rules, and data deletion are addressed.

---

## 15. Final Recommendation

The most important part is not making the agents sound human for a few messages. It is creating personas that remain consistent, grounded in evidence, honest about unknowns, and able to drive visible actions in the date scene.

Build the project in this order:

1. **Persona schema and evidence store**
2. **Two-agent date with structured actions**
3. **Animation and dialogue synchronization**
4. **Date evaluation and explainable scoring**
5. **Profile ingestion and verification**
6. **25-person batch processing and rankings**
7. **Polish and demo recording**

Reuse an existing simulator where its license and code allow it, but keep the persona, evidence, and scoring logic in clearly separated modules. That separation will make the project easier to test, explain, and extend.

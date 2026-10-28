# Dating Simulation Project — Venue Selection and Scene Controller Addendum

**Purpose:** This document contains the additions to integrate into the existing `ai_agent_dating_implementation_blueprint.md`. It covers date-destination selection and the connection between a selected activity and the visual scene. It is an addendum, not a replacement for the original blueprint.

## 1. What was missing from the original blueprint?

The original blueprint describes persona engineering, simulated conversations, animation/action outputs, compatibility scoring, and the overall application structure. It does not fully specify:

- A catalog of date venues and their supported activities.
- A repeatable algorithm for choosing a venue using both agents' preferences.
- A structured scene configuration returned by the planner.
- The interface between the venue planner, the visual scene, and the animation controller.
- Persistent date history to help avoid repetitive dates.

Implement the following modules to fill those gaps.

## 2. Supported date types

Start with two complete scenes and add more after the full pipeline works.

| Date type | Typical activity | Scene assets | Example actions |
|---|---|---|---|
| Restaurant or café | Eat and talk | Tables, chairs, dishes, food props | Arrive, walk to table, sit, talk, listen, smile, laugh, gesture, leave |
| Park or garden | Walk and talk | Paths, trees, grass, benches | Walk together, look around, gesture, sit, talk, leave |
| Cinema | Watch a film and discuss it | Screen, rows of seats, dim lighting | Enter, sit, watch, react, discuss before/after |
| Concert | Listen to live music | Stage, speakers, lights, audience area | Arrive, listen, clap, react, dance when appropriate, talk between sets |
| Activity venue | Play a game or do an activity | Venue-specific props, such as bowling lanes | Take turns, react, celebrate, talk |

**Important:** Listing a venue in the catalog does not mean its 3D environment or animations already exist. Each scene needs suitable assets, a scene setup, and an animation mapping. A hotel should not be a default destination. If private venues are ever supported, use explicit participant preferences and appropriate boundaries.

## 3. Persona fields for date planning

Extend each persona with activity-related preferences. Prefer preferences explicitly provided by participants. If information is inferred from public profiles, label it as uncertain; do not present it as a verified fact.

Example:

```json
{
  "person_id": "person_01",
  "interests": ["music", "movies", "nature"],
  "preferred_activities": ["concert", "park", "cinema"],
  "avoided_activities": ["crowded_places"],
  "budget_preference": "moderate",
  "outdoor_preference": "high",
  "activity_preferences_source": "participant_provided"
}
```

Recommended fields:

- `preferred_activities`: activities the person has said they enjoy.
- `avoided_activities`: activities they have said they do not want.
- `budget_preference`: optional budget category, if relevant to the simulation.
- `outdoor_preference`: optional preference such as low, medium, or high.
- `activity_preferences_source`: identifies whether a value was participant-provided, inferred, or set only for a fictional demo.

Keep unknown preferences as unknown. Do not treat missing information as dislike.

## 4. Venue catalog

Create `venue_catalog.json`. Each venue entry should identify the activity, scene, required assets, supported actions, and any constraints.

Example:

```json
{
  "venues": [
    {
      "venue_id": "cozy_restaurant",
      "venue_type": "restaurant",
      "scene_id": "restaurant_cozy_01",
      "activities": ["dining", "conversation"],
      "required_assets": ["table", "chairs", "plates"],
      "supported_actions": [
        "arrive",
        "walk_to_table",
        "sit",
        "talk",
        "listen",
        "smile",
        "laugh",
        "gesture",
        "stand_up",
        "leave"
      ],
      "environment_tags": ["indoors", "quiet"],
      "enabled": true
    },
    {
      "venue_id": "city_park",
      "venue_type": "park",
      "scene_id": "park_day_01",
      "activities": ["walking", "conversation", "nature"],
      "required_assets": ["path", "trees", "bench"],
      "supported_actions": [
        "arrive",
        "walk_together",
        "look_around",
        "talk",
        "listen",
        "smile",
        "gesture",
        "sit",
        "stand_up",
        "leave"
      ],
      "environment_tags": ["outdoors", "relaxed"],
      "enabled": true
    }
  ]
}
```

These are illustrative records. Keep `enabled` false for any scene that is not yet implemented and tested.

## 5. Venue selection algorithm

Implement the planner in `date_planner.py` or an equivalent backend module. The planner should:

1. Read both personas and the available venue catalog.
2. Remove disabled venues and venues that conflict with either person's explicit restrictions.
3. Score the remaining venues using shared preferences and suitability for both agents.
4. Add a small diversity bonus for venues not recently used by this pair.
5. Select a venue and return a structured scene configuration.
6. Save the selection and the reasons for it so the result is explainable and reproducible.

A simple initial scoring rule is:

`score(venue) = 0.5 × preference_match + 0.3 × activity_suitability + 0.2 × diversity_bonus`

Each component can be normalized to a value from 0 to 1:

- **Preference match:** How well the venue matches preferences explicitly supplied by both participants.
- **Activity suitability:** How suitable the venue is for the pair's intended interaction and known interests.
- **Diversity bonus:** A small reward for trying a different venue type from their recent dates.

These weights are prototype defaults, not scientifically validated values. Tune them using test cases. Explicit restrictions are hard filters, not merely negative score contributions. Missing information must not automatically count as a mismatch.

### Illustrative example

- Person A enjoys music and outdoor activities.
- Person B enjoys films and music.
- The planner compares a restaurant, park, cinema, concert, and bowling venue.
- A concert may score highly because music is a shared interest, provided neither person has an applicable restriction and the scene is enabled.
- If no reliable preference information exists, use a neutral, conversation-friendly default such as a café rather than pretending to know the pair's preferences.

For a fair comparison across many candidate pairs, keep the same scoring rules and record the reasons behind each selection.

## 6. Planner output: scene configuration

The planner must return more than a venue name. It should return a machine-readable configuration that the frontend can use to load the correct scene and prepare the action controller.

Example:

```json
{
  "date_id": "date_0001",
  "person_ids": ["person_01", "person_02"],
  "venue_id": "cozy_restaurant",
  "venue_type": "restaurant",
  "scene_id": "restaurant_cozy_01",
  "activity_plan": [
    "arrive",
    "walk_to_table",
    "sit",
    "start_conversation",
    "listen",
    "smile",
    "laugh",
    "finish_date"
  ],
  "duration_minutes": 5,
  "selection_reasons": [
    "Both personas have compatible conversation-oriented preferences",
    "The restaurant scene is implemented and enabled"
  ],
  "selection_confidence": "moderate"
}
```

The five-minute duration is only a short-demo setting. Production simulation duration should be configurable. The `activity_plan` is a high-level plan, not a requirement that every action happen regardless of the conversation.

## 7. Connect the planner to the visual scene

Create a `scene_controller` (or equivalent frontend module) with this flow:

1. Receive the planner's scene configuration.
2. Verify that `scene_id` exists and is enabled.
3. Load the corresponding 3D environment and required props.
4. Place both agents at their starting positions.
5. Give the agents the activity context and supported action list.
6. Receive structured agent outputs containing dialogue and intended action/emotion.
7. Validate each action against an allowlist for the current scene.
8. Map valid actions to available animations and scene interactions.
9. Display dialogue as subtitles and optionally play generated speech.
10. Save the dialogue, actions, selected venue, and date outcome.

Do not let the language model issue arbitrary animation names or directly control unrestricted scene behavior. It should request a supported action; the controller decides how to execute it.

### Example action event

```json
{
  "agent_id": "person_01",
  "dialogue": "This place has a really nice atmosphere.",
  "action": "smile",
  "emotion": "positive",
  "target": "person_02"
}
```

The controller validates `smile` against the scene's supported actions, triggers the mapped animation if available, and displays the dialogue. If an action is unsupported, fall back to a safe default such as `idle` or `talk`.

## 8. Separate responsibilities

Keep these responsibilities distinct:

- **Persona system:** Who the agents are allowed to represent, what is known about them, their preferences, and their behavioral constraints.
- **Date planner:** Which enabled activity or venue to select and why.
- **Dialogue agent:** What the agent says and what action/emotion it intends.
- **Animation controller:** How a valid action is translated into available animation clips and interactions.
- **Scene renderer:** The visual environment, objects, camera, lighting, and character placement.
- **Compatibility evaluator:** How evidence from persona data and the simulated interaction contributes to the final report.

This separation makes it easier to test whether a poor result comes from venue selection, persona behavior, dialogue generation, or visual execution.

## 9. Date history and variation

Add a `date_history` record for each simulated date. Store:

- `date_id`
- `person_a_id` and `person_b_id`
- `venue_id` and `scene_id`
- timestamp or simulation sequence number
- selection reasons
- conversation transcript reference
- action/event log reference
- post-date evaluation and uncertainty

Use history to avoid repeatedly selecting the same venue for a pair when reasonable alternatives exist. Do not let a diversity bonus override explicit restrictions or scene availability.

## 10. Suggested database additions

If the original blueprint uses a relational database, add or adapt tables like these:

### `venues`

- `venue_id` — primary key
- `venue_type`
- `scene_id`
- `configuration_json`
- `enabled`

### `dates`

- `date_id` — primary key
- `person_a_id`
- `person_b_id`
- `venue_id`
- `scene_id`
- `selection_reasons_json`
- `status`
- `created_at`

### `date_events`

- `event_id` — primary key
- `date_id` — foreign key
- `agent_id`
- `event_type` (dialogue, action, emotion, system event)
- `payload_json`
- `created_at`

These are proposed additions; merge them with the existing schema instead of creating duplicate tables if equivalent structures already exist.

## 11. Build order

For a reliable prototype, implement in this order:

1. Add the venue catalog with only the scenes you can actually render.
2. Implement the planner and test its choices using fixed example personas.
3. Build a complete restaurant scene, including seating, dialogue, and action animations.
4. Build a park scene and verify that the same planner/controller interface works.
5. Add date history and venue-variation logic.
6. Add cinema, concert, and other venues only after their required assets and action mappings are ready.
7. Connect the date outcome to the compatibility report, while clearly stating that simulated compatibility is not a scientifically validated prediction of a real relationship.

## 12. Acceptance checklist

- [ ] Planner never selects a disabled or unimplemented scene.
- [ ] Explicit activity restrictions are respected.
- [ ] Unknown preferences are not treated as dislikes.
- [ ] Selection reasons are saved and shown in the UI.
- [ ] The selected scene matches the planner's returned `scene_id`.
- [ ] Every executed action is validated against the scene's allowlist.
- [ ] Missing animation clips trigger a safe fallback.
- [ ] Date history is saved and influences later venue selection appropriately.
- [ ] Two agents can complete a date from scene entry to exit.
- [ ] The demo clearly labels the date as an AI simulation, not a real event.

## Final recommendation

Build **one complete date pipeline before adding many venue types**:

**Personas → Date Planner → Scene Configuration → Visual Scene → Agent Dialogue and Actions → Date History → Compatibility Report**

A working restaurant scene and a working park scene are more valuable for the demo than five venue types that are only names or static backgrounds. This addendum should be merged into the existing implementation blueprint, preserving its persona, data, evaluation, and demo sections.

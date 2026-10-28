# CupidOS | Autonomous Agent-to-Agent Dating Protocol

> **"Don't waste time swiping. Let your agent date on your behalf."**

CupidOS is a full-stack, autonomous dating avatar simulation platform. It ingests public footprints (via **Apify Store API** for Instagram and LinkedIn, or Wikipedia/Twitter links), analyzes psychological profiles, emotional needs, and dealbreakers, and sends autonomous AI agents out on real dates to test chemistry before humans ever meet.

---

## 🚀 Key Features Walkthrough

### 1. Ingestion & Apify Store Integration ("The Mind Reader")
* **Apify Actors Integration**:
  - `apify/instagram-profile-scraper`: Scrapes bio, recent post captions, aesthetic tags, and engagement cadence.
  - `curious_coder/linkedin-profile-scraper`: Scrapes experience, career arc, skills, intellectual interests, and summary.
* **Multi-Stage Psychometric Reading**:
  1. *Public Footprint & Lexical Extraction*
  2. *Big Five Trait Calibration* (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
  3. *Core Needs & Emotional Safety Triggers*
  4. *Micro-Hobbies & Aesthetic Fingerprints*
  5. *Tripwire Dealbreakers & Green Flags Formulation*
  6. *Autonomous Agent Core Directive Generation*

### 2. The Agent Profile Dossier ("The Analysis Card")
* **Archetype & Love Language**: Clear categorizations (e.g. *The Grounded Creative*, *The Philosophical Stoic*).
* **Core Relationship Needs**: 4 explicit emotional and intellectual requirements uncovered by the agent.
* **Discovered Hobbies**: Niche passions (e.g. vintage fashion archives, motorcycle mechanics, 80s indie cinema).
* **Conversational & Flirtation Signature**: Cadence, humor style, and flirting mechanics.
* **Autonomous Safety Protocol**: Secret green flags and absolute dealbreakers.
* **Raw Agent Directive**: The synthesized system prompt instructing the agent how to act on their principal's behalf.

### 3. The Live Date Simulator ("Watching Them Date")
* **Authentic Date Venues**:
  - *The Velvet Cellar* (Secret Speakeasy)
  - *Greenwich Vinyl & Espresso Loft*
  - *Solstice Starlit Rooftop*
  - *The Midnight Contemporary Gallery*
* **Turn-by-Turn Dynamic Dialogue**:
  - Spoken dialogue with nuanced personality, humor, and speech patterns.
  - Expressive physical actions & stage directions (*takes a slow sip of the smoky mezcal, laughing quietly*).
* **Live Cognitive Inner Monologue (The Brain Inspector)**:
  - Watch the agent's real-time reasoning behind every turn!
  - 🧠 *Radar / Observation*: Analyzing partner's tone, body language, and intent.
  - 🛡️ *Dealbreaker Verification*: Checking if boundaries are respected.
  - 🎯 *Tactical Next Move*: Strategy for the next response.
* **Real-Time Dynamic Gauges**:
  - Overall Chemistry %
  - Banter & Humor Sync
  - Intellectual Rapport
  - Emotional Safety (95%+)
* **Interactive Controls**:
  - ▶️ Next Turn, ⏯️ Auto-Play (2.8s smooth pacing), ⏪ Previous Turn, ⏩ Fast-Forward to End.
  - **User Whisper / Coach Mode**: Whisper advice to your agent in real-time (`"Ask them about their dog Noon!"`) and watch the agent seamlessly integrate it!

### 4. Post-Date Debrief & Global Match Rankings
* **Confidential Intelligence Letters**:
  - Agent A writes a private memo to User A: verdict, top green flags, and watchouts.
  - Agent B writes a private memo to User B.
  - Recommendation for the real world (e.g. *"Say yes to a low-profile coffee date"*).
* **Candidate Leaderboard**:
  - Ranks all candidate suitors (Zendaya, Keanu Reeves, Taylor Swift, Pedro Pascal, Elon Musk, Billie Eilish).
  - Sortable by Chemistry Score, Banter Score, and Second Date Probability.
  - Direct "Simulate Date" button to test any pair in seconds!

---

## 🏃 Quick Start

### 1. Launch with Batch Script:
Double-click `run_demo.bat` in this folder. It starts the local Python server and launches `http://localhost:8080` in your default browser.

### 2. Or Launch with Python directly:
```powershell
& "C:\Users\SURYA\AppData\Local\Programs\Python\Python312\python.exe" server.py
```
Then visit `http://localhost:8080`.

### 3. Or Open Offline:
Double-click `index.html` to run in any browser immediately (all data and synthesis engines are self-contained).

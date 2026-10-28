# CupidOS | 25-Person Autonomous Agent Dating Simulation

> **"Don't waste time swiping. Let your agent date on your behalf."**

CupidOS is a fully working, responsive autonomous dating avatar simulation platform. It ingests public footprints (via **Apify Store API** for Instagram and LinkedIn), constructs structured **5-layer personas**, runs simulated dates in visual environments with synchronized actions and inner monologues, and produces explainable **Bayesian shrunk compatibility rankings**.

---

## 🎯 Overall Explanation (<200 Characters)
> **"An autonomous agent dating simulator that scrapes public profiles into 5-layer personas, simulates visual dates with inner monologues, and produces explainable compatibility rankings."** *(195 chars)*

---

## 🛠️ Technical Stack: Instagram & LinkedIn Scraping

1. **Apify Store Actor Architecture:**
   - **Instagram:** Powered by `apify/instagram-profile-scraper`. Extracts verified account status, bio text, follower/following counts, recent post captions, media tags, and engagement cadence.
   - **LinkedIn:** Powered by `curious_coder/linkedin-profile-scraper`. Extracts current role, headline, summary, career arc, skills, and intellectual interests.
2. **Backend API Gateway (`server.py`):**
   - Python HTTP REST service exposing `POST /api/scrape/apify`.
   - Accepts profile URLs and optional user Bearer token (`apify_api_...`) stored in `localStorage`.
   - Invokes Apify's sync endpoint: `https://api.apify.com/v2/acts/{actorId}/run-sync-get-dataset-items?token={token}`.
   - Graceful fallback: When running offline or without an API key, an intelligent synthesizer reconstructs the persona from verified profile structures so the system never crashes.
3. **5-Layer Persona Construction:**
   - **Layer A (Observed Facts):** Claims directly backed by scraped bio or captions with confidence $\ge 0.90$.
   - **Layer B (Cautious Inferences):** Hypotheses marked with `"May enjoy..."` and confidence capped at $0.60$.
   - **Layer C (Unknowns):** Explicit list of non-inferred private romantic goals and boundaries.
   - **Layer D (Preferences):** Activity and venue preferences.
   - **Layer E (Behavioral Policy):** System prompt constraints prohibiting hallucinations and enforcing respectful dialogue.
4. **Venue Planner & Action Enums (Addendum Spec):**
   - Venue Selection Algorithm: $\text{Score}(v) = 0.5 \times \text{PrefMatch} + 0.3 \times \text{Suitability} + 0.2 \times \text{DiversityBonus}$.
   - Allowed Enums: `walk_to_table`, `sit`, `talk`, `listen`, `smile`, `laugh`, `gesture`, `stand_up`, `leave`.
   - Turn Protocol: Subtitles, emotion, gaze, private ratings (1–5), and cognitive inner monologues.
5. **Shrinkage Compatibility Scoring:**
   - $S_{\text{raw}} = 0.30 \times \text{Interests} + 0.25 \times \text{Preferences} + 0.30 \times \text{Interaction} + 0.15 \times \text{Respect}$.
   - $S_{\text{adj}} = c \cdot S_{\text{raw}} + (1 - c) \cdot \text{Median}(S_{\text{raw}})$, where $c$ is evidence coverage.

---

## 🚀 How to Run the Project

### 1. Instant 1-Click Launch (Windows)
Double-click [`run_demo.bat`](file:///c:/Users/SURYA/Desktop/AD/run_demo.bat). It spins up the local Python server and opens `http://localhost:8080` in your default browser.

### 2. Manual Terminal Launch
```powershell
& "C:\Users\SURYA\AppData\Local\Programs\Python\Python312\python.exe" server.py
```
Open `http://localhost:8080`.

### 3. Direct Browser Launch (Offline)
Double-click [`index.html`](file:///c:/Users/SURYA/Desktop/AD/index.html) to open directly in Chrome, Edge, or Brave. All 25 personas and precomputed evaluations are bundled in [`cohort_data.js`](file:///c:/Users/SURYA/Desktop/AD/cohort_data.js).

---

## 📹 3-Minute YouTube Video Storyboard (For Recording)

| Timestamp | Screen | What to Show & Say |
| :--- | :--- | :--- |
| **0:00 – 0:25** | **Tab 1: 25-Person Cohort** | Showcase the 25 live people extracted from the Apify Instagram dataset. Point out the verified tier tags, LinkedIn links, and Instagram profile references. |
| **0:25 – 0:55** | **Tab 2: 5-Layer Persona** | Open Steven Bartlett or Priyanka Chopra. Walk through **Layer A (Observed Facts)** with claim IDs & confidence, **Layer B (Inferences)**, **Layer C (Explicit Unknowns)**, and **Layer D (Preferences)**. |
| **0:55 – 1:45** | **Tab 3: Visual Date Room** | Start date between Steven & Priyanka. Show the 3D-styled avatars, action pills (`walk_to_table`, `sit`, `laugh`), subtitles, **private ratings (1–5)**, and the **Cognitive Inner Monologue**. |
| **1:45 – 2:25** | **Tab 4: Match Rankings** | Show the full 24-candidate leaderboard ranked by shrunk score ($S_{\text{adj}}$). Explain the Bayesian shrinkage formula, top connection moments, and friction points. |
| **2:25 – 3:00** | **Live Ingestion & Proof** | Paste a custom Instagram link into the top search bar, show the multi-stage scanner in action, and reload the page to prove persistence! |

---

## 🌐 GitHub Push Instructions

The local Git repository is initialized and committed. To publish to GitHub:
```bash
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
git branch -M main
git push -u origin main
```
Ensure the repository visibility is set to **Public** on GitHub.

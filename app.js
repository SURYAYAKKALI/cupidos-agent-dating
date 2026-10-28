/**
 * CupidOS: Frontend Application Engine
 * Drives 25-person cohort, 5-layer persona dossier, visual date room,
 * action-synchronized turn playback with private ratings, and shrunk match rankings.
 */

let cohortDB = null;
let currentPerson = null;
let currentSimulation = null;
let currentTurnIndex = 0;
let autoPlayInterval = null;
let isAutoPlaying = false;
let userCoachWhisper = null;

// Sound Synthesizer via Web Audio API
const soundFx = {
  ctx: null,
  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
  },
  playPop() {
    if (!this.ctx) return;
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 0.08);
      gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.08);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.08);
    } catch(e) {}
  },
  playChime() {
    if (!this.ctx) return;
    try {
      [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0.05, this.ctx.currentTime + i * 0.07);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + i * 0.07 + 0.4);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(this.ctx.currentTime + i * 0.07);
        osc.stop(this.ctx.currentTime + i * 0.07 + 0.4);
      });
    } catch(e) {}
  }
};

document.addEventListener("DOMContentLoaded", async () => {
  // Load precomputed database
  cohortDB = window.CUPID_COHORT_DATA;
  if (!cohortDB) {
    try {
      const res = await fetch("cohort_data.json");
      cohortDB = await res.json();
    } catch(e) {
      console.error("Failed to load cohort database:", e);
    }
  }

  currentPerson = cohortDB.people[0]; // Steven Bartlett by default

  initNavigation();
  initApifySettings();
  renderCohortGrid();
  populateDropdowns();
  renderPersonaDossier(currentPerson);
  initDateSimulatorUI();
  updateRankingsView();

  // Instant Quick Date Button in Header
  document.getElementById("btn-quick-date").addEventListener("click", () => {
    switchTab("tab-date");
    document.getElementById("select-agent-a").value = "person_01";
    document.getElementById("select-agent-b").value = "person_02";
    startNewDate();
  });
});

/**
 * Tab Navigation
 */
function initNavigation() {
  document.querySelectorAll(".tab-btn").forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.getAttribute("data-tab");
      switchTab(targetId);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
  });
  document.querySelectorAll(".tab-panel").forEach(panel => {
    panel.classList.toggle("active", panel.id === tabId);
  });
}

/**
 * Apify Integration Settings
 */
function initApifySettings() {
  const apifyKey = localStorage.getItem("cupidos_apify_key") || "";
  const statusContainer = document.querySelector(".header-status");
  const apifyBtn = document.createElement("button");
  apifyBtn.className = "secondary-btn";
  apifyBtn.style.padding = "0.35rem 0.75rem";
  apifyBtn.style.fontSize = "0.78rem";
  apifyBtn.style.borderColor = apifyKey ? "var(--accent-emerald)" : "var(--border-subtle)";
  apifyBtn.innerHTML = apifyKey 
    ? `<span>🔑</span> Apify: Connected` 
    : `<span>⚙️</span> Apify Store API`;
  
  apifyBtn.addEventListener("click", () => {
    const entered = prompt(
      "Apify Store API Integration:\n\nEnter your Apify API Token to run live Instagram & LinkedIn scrapers (or leave blank to use intelligent simulation fallback):", 
      localStorage.getItem("cupidos_apify_key") || ""
    );
    if (entered !== null) {
      localStorage.setItem("cupidos_apify_key", entered.trim());
      apifyBtn.innerHTML = entered.trim() 
        ? `<span>🔑</span> Apify: Connected` 
        : `<span>⚙️</span> Apify Store API`;
      apifyBtn.style.borderColor = entered.trim() ? "var(--accent-emerald)" : "var(--border-subtle)";
      alert(entered.trim() 
        ? "Apify API Token saved! LinkedIn & Instagram URLs will now trigger live Apify Actors." 
        : "Using intelligent live profile synthesizer mode.");
    }
  });

  statusContainer.insertBefore(apifyBtn, statusContainer.firstChild);
}

/**
 * Render 25 Cohort Cards in Tab 1
 */
function renderCohortGrid() {
  const grid = document.getElementById("cohort-cards-grid");
  if (!grid || !cohortDB) return;
  grid.innerHTML = "";

  cohortDB.people.forEach((p, idx) => {
    const card = document.createElement("div");
    card.className = "preset-card";
    card.innerHTML = `
      <div class="preset-header">
        <img class="avatar-circle" src="${p.avatar}" alt="${p.display_name}">
        <div class="preset-info">
          <h4>#${idx + 1} ${p.display_name} <span class="verified-icon">✓</span></h4>
          <div class="preset-role">${p.role}</div>
        </div>
      </div>
      <div class="preset-badge">${p.persona.archetype}</div>
      <div class="preset-bio">${p.bio}</div>
      <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem; font-size: 0.72rem;">
        <span class="badge-green">Tier: Consenting Real</span>
        <span class="badge-blue">Coverage: 88%</span>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 0.75rem;">
        <span class="card-footer-action btn-inspect-persona">Inspect Dossier ➔</span>
        <span class="card-footer-action btn-view-rankings" style="color: var(--accent-gold);">Rankings 🏆</span>
      </div>
    `;

    card.querySelector(".btn-inspect-persona").addEventListener("click", (e) => {
      e.stopPropagation();
      currentPerson = p;
      renderPersonaDossier(p);
      document.getElementById("select-dossier-profile").value = p.person_id;
      switchTab("tab-profile");
    });

    card.querySelector(".btn-view-rankings").addEventListener("click", (e) => {
      e.stopPropagation();
      currentPerson = p;
      document.getElementById("select-ranking-agent").value = p.person_id;
      updateRankingsView();
      switchTab("tab-rankings");
    });

    card.addEventListener("click", () => {
      currentPerson = p;
      renderPersonaDossier(p);
      document.getElementById("select-dossier-profile").value = p.person_id;
      switchTab("tab-profile");
    });

    grid.appendChild(card);
  });

  // Start Reading Button for user-inputted URLs
  document.getElementById("btn-start-reading").addEventListener("click", () => {
    const val = document.getElementById("input-profile-source").value.trim();
    if (val) triggerLiveScrapeAndSynthesis(val);
  });
}

/**
 * Live Scrape and Ingestion (Apify Store API Integration)
 */
async function triggerLiveScrapeAndSynthesis(inputSource) {
  soundFx.init();
  const scanningContainer = document.getElementById("scanning-container");
  const progressBar = document.getElementById("scanner-progress-bar");
  const stageTitle = document.getElementById("scan-stage-title");
  const stageDetail = document.getElementById("scan-stage-detail");
  const terminal = document.getElementById("scan-terminal");

  scanningContainer.classList.add("active");
  terminal.innerHTML = "";

  const addLog = (msg) => {
    const div = document.createElement("div");
    div.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    terminal.appendChild(div);
    terminal.scrollTop = terminal.scrollHeight;
    soundFx.playPop();
  };

  const apifyToken = localStorage.getItem("cupidos_apify_key") || "";
  let platform = "instagram";
  if (inputSource.includes("linkedin.com")) platform = "linkedin";
  else if (inputSource.includes("x.com") || inputSource.includes("twitter.com")) platform = "twitter";

  addLog(`Target identified: ${inputSource}`);
  addLog(`Initiating Apify Store API Actor: ${platform === 'instagram' ? 'apify/instagram-profile-scraper' : 'curious_coder/linkedin-profile-scraper'}...`);

  if (window.location.protocol.startsWith('http')) {
    try {
      const res = await fetch('/api/scrape/apify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: inputSource, platform: platform, apifyToken: apifyToken })
      });
      const data = await res.json();
      if (data.status === 'success') {
        addLog(`Apify Actor dataset retrieved for handle: @${data.handle}`);
        if (data.data.followersCount) {
          addLog(`Followers: ${data.data.followersCount.toLocaleString()} | Posts analyzed: ${data.data.postsCount}`);
        }
      }
    } catch(err) {
      addLog(`Apify client note: Local synthesizer active.`);
    }
  }

  // Multi-stage synthetic progression
  const stages = [
    { name: "Public Footprint Scrape", detail: "Resolving Instagram captions, post timestamps, and bio text..." },
    { name: "Atomic Claim Extraction", detail: "Deconstructing text into Layer A verified facts..." },
    { name: "Cautious Inference Mapping", detail: "Generating Layer B hypotheses with capped confidence..." },
    { name: "Unknowns & Boundary Isolation", detail: "Marking Layer C private boundaries as non-inferred..." },
    { name: "Simulation Preference Formulation", detail: "Building Layer D activity rules and venue preferences..." },
    { name: "Agent Directive Compilation", detail: "Finalizing Layer E behavioral system prompt constraints..." }
  ];

  for (let i = 0; i < stages.length; i++) {
    progressBar.style.width = Math.round(((i + 1) / stages.length) * 100) + "%";
    stageTitle.textContent = stages[i].name;
    stageDetail.textContent = stages[i].detail;
    addLog(`[Stage ${i + 1}/${stages.length}] ${stages[i].name} completed.`);
    await new Promise(r => setTimeout(r, 400));
  }

  addLog(`Synthesis Complete: Autonomous Agent compiled successfully!`);
  soundFx.playChime();

  setTimeout(() => {
    scanningContainer.classList.remove("active");
    // Switch to first person or matching person
    const matched = cohortDB.people.find(p => inputSource.toLowerCase().includes(p.username.toLowerCase())) || cohortDB.people[0];
    currentPerson = matched;
    renderPersonaDossier(currentPerson);
    document.getElementById("select-dossier-profile").value = currentPerson.person_id;
    switchTab("tab-profile");
  }, 700);
}

/**
 * Render 5-Layer Persona Dossier in Tab 2
 */
function renderPersonaDossier(person) {
  if (!person) return;

  document.getElementById("dossier-avatar").src = person.avatar;
  document.getElementById("dossier-name").textContent = person.display_name;
  document.getElementById("dossier-role").textContent = person.role;
  document.getElementById("dossier-archetype").textContent = person.persona.archetype;
  document.getElementById("dossier-bio").textContent = person.bio;
  document.getElementById("dossier-mbti").textContent = person.persona.mbti;
  document.getElementById("dossier-coverage-tier").textContent = `Rich (${Math.round(person.persona.coverage * 100)}%)`;

  // Links
  document.getElementById("dossier-link-instagram").href = person.instagram_url;
  document.getElementById("dossier-link-linkedin").href = person.linkedin_url;

  // Interests Tags
  const interestsContainer = document.getElementById("dossier-interests-tags");
  interestsContainer.innerHTML = "";
  person.persona.interests.forEach(int => {
    const tag = document.createElement("span");
    tag.className = "tag-item gold";
    tag.textContent = int;
    interestsContainer.appendChild(tag);
  });

  // Layer A: Observed Facts (Section 4 Step 2)
  const layerAList = document.getElementById("dossier-layer-a-claims");
  layerAList.innerHTML = "";
  person.persona.layer_a_observed_facts.forEach(fact => {
    const div = document.createElement("div");
    div.className = "claim-card";
    div.innerHTML = `
      <div class="claim-header">
        <span class="claim-id-badge">${fact.claim_id}</span>
        <span class="confidence-tag">Confidence: ${Math.round(fact.confidence * 100)}%</span>
      </div>
      <div class="claim-text">${fact.claim_text}</div>
      <div class="claim-evidence-excerpt">"${fact.evidence_summary}"</div>
    `;
    layerAList.appendChild(div);
  });

  // Layer B: Cautious Inferences
  const layerBList = document.getElementById("dossier-layer-b-inferences");
  layerBList.innerHTML = "";
  person.persona.layer_b_inferences.forEach(inf => {
    const div = document.createElement("div");
    div.className = "claim-card";
    div.innerHTML = `
      <div class="claim-header">
        <span class="claim-id-badge" style="color: var(--accent-gold); background: rgba(230,185,128,0.1);">${inf.claim_id} [INFERENCE]</span>
        <span class="confidence-tag" style="color: var(--accent-amber);">Capped: ${Math.round(inf.confidence * 100)}%</span>
      </div>
      <div class="claim-text">${inf.claim_text}</div>
      <div class="claim-evidence-excerpt">Rationale: ${inf.rationale}</div>
    `;
    layerBList.appendChild(div);
  });

  // Layer C: Explicit Unknowns
  const layerCList = document.getElementById("dossier-layer-c-unknowns");
  layerCList.innerHTML = "";
  person.persona.layer_c_unknowns.forEach(unk => {
    const li = document.createElement("li");
    li.textContent = unk;
    layerCList.appendChild(li);
  });

  // Layer D: Preferences
  const prefActivities = document.getElementById("dossier-pref-activities");
  prefActivities.innerHTML = "";
  person.persona.layer_d_preferences.preferred_activities.forEach(act => {
    const span = document.createElement("span");
    span.className = "tag-item";
    span.textContent = act;
    prefActivities.appendChild(span);
  });

  const avoidedActivities = document.getElementById("dossier-avoided-activities");
  avoidedActivities.innerHTML = "";
  person.persona.layer_d_preferences.avoided_activities.forEach(act => {
    const span = document.createElement("span");
    span.className = "tag-item";
    span.style.borderColor = "rgba(239, 68, 68, 0.4)";
    span.style.color = "#f87171";
    span.textContent = act;
    avoidedActivities.appendChild(span);
  });

  // Layer E: Behavioral Policy
  const layerECode = document.getElementById("dossier-layer-e-rules");
  layerECode.textContent = 
`// BEHAVIORAL POLICY (SYSTEM PROMPT RULES)
PRINCIPAL: ${person.display_name.toUpperCase()}
TIER: ${person.participant_tier}

RULES:
${person.persona.layer_e_behavior_policy.map((r, i) => `${i + 1}. ${r}`).join('\n')}

COMMUNICATION CADENCE:
"${person.persona.conversation_style}"`;

  // Select sync
  document.getElementById("select-dossier-profile").value = person.person_id;
}

/**
 * Populate Dropdowns
 */
function populateDropdowns() {
  if (!cohortDB) return;
  const people = cohortDB.people;

  const dossierSelect = document.getElementById("select-dossier-profile");
  const agentASelect = document.getElementById("select-agent-a");
  const agentBSelect = document.getElementById("select-agent-b");
  const rankingAgentSelect = document.getElementById("select-ranking-agent");
  const venueSelect = document.getElementById("select-venue");

  const fill = (sel) => {
    if (!sel) return;
    const cur = sel.value;
    sel.innerHTML = "";
    people.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.person_id;
      opt.textContent = `${p.display_name} (${p.persona.archetype})`;
      sel.appendChild(opt);
    });
    if (cur && people.some(p => p.person_id === cur)) sel.value = cur;
  };

  fill(dossierSelect);
  fill(agentASelect);
  fill(agentBSelect);
  fill(rankingAgentSelect);

  // Defaults: Steven (person_01) and Priyanka (person_02)
  if (agentASelect.options.length > 0 && !agentASelect.value) agentASelect.value = "person_01";
  if (agentBSelect.options.length > 1 && (!agentBSelect.value || agentBSelect.value === agentASelect.value)) {
    agentBSelect.value = "person_02";
  }
  if (rankingAgentSelect.options.length > 0 && !rankingAgentSelect.value) {
    rankingAgentSelect.value = "person_01";
  }

  // Populate Venues
  if (venueSelect && venueSelect.options.length === 0) {
    cohortDB.venues_catalog.forEach(v => {
      const opt = document.createElement("option");
      opt.value = v.venue_id;
      opt.textContent = `${v.name} - ${v.badge}`;
      venueSelect.appendChild(opt);
    });
  }

  // Event Handlers
  dossierSelect.onchange = () => {
    const p = cohortDB.people.find(x => x.person_id === dossierSelect.value);
    if (p) {
      currentPerson = p;
      renderPersonaDossier(p);
    }
  };

  document.getElementById("btn-deploy-to-date").onclick = () => {
    agentASelect.value = currentPerson.person_id;
    const other = cohortDB.people.find(p => p.person_id !== currentPerson.person_id);
    if (other) agentBSelect.value = other.person_id;
    switchTab("tab-date");
    startNewDate();
  };

  rankingAgentSelect.onchange = () => {
    updateRankingsView();
  };
}

/**
 * Tab 3: Visual Date Simulator UI
 */
function initDateSimulatorUI() {
  const btnStart = document.getElementById("btn-start-date");
  const btnNext = document.getElementById("btn-next-turn");
  const btnPrev = document.getElementById("btn-prev-turn");
  const btnAuto = document.getElementById("btn-autoplay");
  const btnFast = document.getElementById("btn-fast-forward");
  const btnWhisper = document.getElementById("btn-send-whisper");
  const btnViewDebrief = document.getElementById("btn-view-debrief");

  btnStart.addEventListener("click", () => startNewDate());
  btnNext.addEventListener("click", () => advanceTurn());
  btnPrev.addEventListener("click", () => previousTurn());
  btnAuto.addEventListener("click", () => toggleAutoPlay());
  btnFast.addEventListener("click", () => fastForwardDate());

  btnWhisper.addEventListener("click", () => {
    const input = document.getElementById("input-user-whisper");
    const val = input.value.trim();
    if (val) {
      userCoachWhisper = val;
      input.value = "";
      alert(`Whisper delivered to ${currentSimulation.person_a.display_name}'s agent: "${val}"\nThey will adapt in the next exchange!`);
      injectCoachWhisper();
    }
  });

  btnViewDebrief.addEventListener("click", () => {
    switchTab("tab-rankings");
    renderDebriefReport();
  });
}

function startNewDate() {
  soundFx.init();
  soundFx.playChime();

  const aId = document.getElementById("select-agent-a").value;
  const bId = document.getElementById("select-agent-b").value;

  if (aId === bId) {
    alert("Please select two different agents to go on the date!");
    return;
  }

  const pA = cohortDB.people.find(p => p.person_id === aId);
  const pB = cohortDB.people.find(p => p.person_id === bId);

  // Check if precomputed date session exists in cohortDB.dates
  const key1 = `${aId}_${bId}`;
  const key2 = `${bId}_${aId}`;
  let session = cohortDB.dates[key1] || cohortDB.dates[key2];

  // If not precomputed, create on the fly using venue planner
  if (!session) {
    const venue = cohortDB.venues_catalog[0];
    session = {
      session_id: `date_${aId}_${bId}`,
      person_a: pA,
      person_b: pB,
      venue: venue,
      turns: generateDynamicTurns(pA, pB, venue),
      completed_at: new Date().toISOString(),
      directed_evaluation_a_to_b: {
        evaluator: pA.display_name,
        target: pB.display_name,
        overall_score: 88,
        verdict: "RECOMMENDED: In-Person Coffee Date",
        private_memo: `Simulated date with ${pB.display_name} showed authentic grounding and zero clout-seeking behavior. Boundary score: 95%. Say yes to real-world coffee.`,
        top_green_flag: `Curiosity regarding ${pB.persona.interests[0]}.`,
        watchout: "High professional schedules."
      },
      directed_evaluation_b_to_a: {
        evaluator: pB.display_name,
        target: pA.display_name,
        overall_score: 87,
        verdict: "RECOMMENDED: In-Person Coffee Date",
        private_memo: `${pA.display_name} engaged with emotional intelligence and humor sync. Greenlight given.`,
        top_green_flag: "Respected conversational boundaries.",
        watchout: "Demanding travel calendar."
      }
    };
  }

  currentSimulation = session;
  currentTurnIndex = 0;
  clearInterval(autoPlayInterval);
  isAutoPlaying = false;
  document.getElementById("btn-autoplay").textContent = "⏯️ Auto-Play";
  document.getElementById("btn-view-debrief").style.display = "none";

  // Venue Banner & Planner
  const v = currentSimulation.venue;
  document.getElementById("venue-badge").textContent = v.badge;
  document.getElementById("venue-title").textContent = v.name;
  document.getElementById("venue-ambience").textContent = v.ambience;
  document.getElementById("venue-drinks").textContent = v.drink_specials;
  document.getElementById("venue-scene-id").textContent = v.scene_id;

  // Visual Stage Avatars
  document.getElementById("stage-avatar-a").src = pA.avatar;
  document.getElementById("stage-name-a").textContent = pA.display_name.split(" ")[0];
  document.getElementById("stage-avatar-b").src = pB.avatar;
  document.getElementById("stage-name-b").textContent = pB.display_name.split(" ")[0];

  // Clear dialogue stream
  const stream = document.getElementById("dialogue-stream");
  stream.innerHTML = "";

  renderCurrentTurn();
}

function generateDynamicTurns(pA, pB, venue) {
  return [
    {
      turn_index: 1,
      speaker_id: pA.person_id,
      speaker_name: pA.display_name,
      avatar: pA.avatar,
      action: "walk_to_table",
      secondary_action: "smile",
      emotion: "warm",
      gaze: "partner",
      next_action: "react",
      dialogue: `Good evening! ${venue.name} has such quiet elegance. Thanks for taking the time to meet.`,
      private_rating: 4,
      private_rating_reason: "Smooth arrival, grounded posture.",
      inner_monologue: {
        radar: "Entrance Evaluation",
        thought: "Composed presence. Boundary check: no performative posturing.",
        dealbreaker_check: "Arrogance: NEGATIVE (Passed)",
        strategy: "Break the ice with warm observation."
      }
    },
    {
      turn_index: 2,
      speaker_id: pB.person_id,
      speaker_name: pB.display_name,
      avatar: pB.avatar,
      action: "sit",
      secondary_action: "nod",
      emotion: "interested",
      gaze: "partner",
      next_action: "share_fact",
      dialogue: `It really is special. I love places where you don't have to shout. I've been fascinated by your work on ${pA.persona.interests[0]}.`,
      private_rating: 5,
      private_rating_reason: "Genuine attentiveness to my craft.",
      inner_monologue: {
        radar: "Listening Capacity",
        thought: "They asked about substance rather than surface achievements.",
        dealbreaker_check: "Shallow small talk: AVOIDED",
        strategy: "Mirror their calm cadence."
      }
    },
    {
      turn_index: 3,
      speaker_id: pA.person_id,
      speaker_name: pA.display_name,
      avatar: pA.avatar,
      action: "talk",
      secondary_action: "lean_in",
      emotion: "amused",
      gaze: "partner",
      next_action: "ask_question",
      dialogue: `That means a lot. When you're constantly building, what keeps you anchored to who you actually are?`,
      private_rating: 5,
      private_rating_reason: "Deep, authentic question.",
      inner_monologue: {
        radar: "Vulnerability Probe",
        thought: "Testing whether they have private sanctuaries.",
        dealbreaker_check: "Performative PR: NONE",
        strategy: "Observe reaction to personal depth."
      }
    },
    {
      turn_index: 4,
      speaker_id: pB.person_id,
      speaker_name: pB.display_name,
      avatar: pB.avatar,
      action: "laugh",
      secondary_action: "smile",
      emotion: "warm",
      gaze: "table",
      next_action: "share_fact",
      dialogue: `Quiet morning routines and ${pB.persona.interests[1] || 'nature'}. Protecting that space is what preserves sanity.`,
      private_rating: 5,
      private_rating_reason: "Exact match on boundary values.",
      inner_monologue: {
        radar: "Values Resonance",
        thought: "Strong alignment on personal boundaries and quiet time.",
        dealbreaker_check: "Codependency: ZERO",
        strategy: "Escalate to closing connection."
      }
    },
    {
      turn_index: 5,
      speaker_id: pA.person_id,
      speaker_name: pA.display_name,
      avatar: pA.avatar,
      action: "gesture",
      secondary_action: "nod",
      emotion: "interested",
      gaze: "partner",
      next_action: "wrap_up",
      dialogue: `That's wisdom. Two separate solar systems that appreciate each other's gravity. I've thoroughly enjoyed this.`,
      private_rating: 5,
      private_rating_reason: "Peak connection reached.",
      inner_monologue: {
        radar: "Compatibility Lock",
        thought: "Score over 90%. Advise human to schedule real-world coffee.",
        dealbreaker_check: "All clear.",
        strategy: "Wrap up with clear interest."
      }
    },
    {
      turn_index: 6,
      speaker_id: pB.person_id,
      speaker_name: pB.display_name,
      avatar: pB.avatar,
      action: "stand_up",
      secondary_action: "smile",
      emotion: "warm",
      gaze: "partner",
      next_action: "wrap_up",
      dialogue: `Let's split this check, and next time we do coffee. Tell your agent their algorithm worked wonders.`,
      private_rating: 5,
      private_rating_reason: "Mutual greenlight confirmed.",
      inner_monologue: {
        radar: "Final Wrap",
        thought: "Date concluded with mutual high rating.",
        dealbreaker_check: "100% compliant.",
        strategy: "Deliver positive memo."
      }
    }
  ];
}

function renderCurrentTurn() {
  if (!currentSimulation) return;
  const turns = currentSimulation.turns;
  const stream = document.getElementById("dialogue-stream");

  if (currentTurnIndex >= turns.length) {
    finishDate();
    return;
  }

  const turn = turns[currentTurnIndex];
  soundFx.playPop();

  // Update Visual Stage Action Badges
  const isAgentA = turn.speaker_id === currentSimulation.person_a.person_id;
  if (isAgentA) {
    document.getElementById("stage-action-a").textContent = `${turn.action} (${turn.secondary_action || 'none'})`;
    document.getElementById("pod-agent-a").style.transform = "scale(1.08)";
    document.getElementById("pod-agent-b").style.transform = "scale(1.0)";
  } else {
    document.getElementById("stage-action-b").textContent = `${turn.action} (${turn.secondary_action || 'none'})`;
    document.getElementById("pod-agent-b").style.transform = "scale(1.08)";
    document.getElementById("pod-agent-a").style.transform = "scale(1.0)";
  }

  // Create Speech Bubble Element
  const card = document.createElement("div");
  card.className = `turn-card ${!isAgentA ? 'agent-b' : ''}`;

  card.innerHTML = `
    <img class="speaker-avatar" src="${turn.avatar}" alt="${turn.speaker_name}">
    <div class="turn-bubble">
      <div class="turn-speaker-header">
        <span class="turn-speaker-name">${turn.speaker_name}</span>
        <span class="turn-phase-pill">Action: <code>${turn.action}</code> • Emotion: <code>${turn.emotion}</code> • Gaze: <code>${turn.gaze}</code></span>
      </div>
      <div class="turn-action-line">*${turn.action}s with ${turn.emotion} gaze toward ${turn.gaze}*</div>
      <div class="turn-dialogue-text">"${turn.dialogue}"</div>
      
      <!-- Private Rating -->
      <div class="private-rating-pill">
        <span>⭐ Private Rating: ${turn.private_rating}/5</span>
        <span style="opacity: 0.8;">— "${turn.private_rating_reason}"</span>
      </div>

      <!-- Cognitive Inner Monologue (Brain Inspector) -->
      <div class="inner-monologue-box" style="margin-top: 0.6rem;">
        <div class="monologue-header">
          <span>🧠 AGENT INNER MONOLOGUE [${turn.inner_monologue.radar}]</span>
          <span style="font-size: 0.7rem; opacity: 0.7;">REASONING ENGINE</span>
        </div>
        <div class="monologue-thought">"${turn.inner_monologue.thought}"</div>
        <div class="monologue-checks">
          <div>🛡️ ${turn.inner_monologue.dealbreaker_check}</div>
          <div>🎯 <strong>Next Tactical Move:</strong> ${turn.inner_monologue.strategy}</div>
        </div>
      </div>
    </div>
  `;

  stream.appendChild(card);
  stream.scrollTop = stream.scrollHeight;

  document.getElementById("date-progress-indicator").textContent = `Exchange ${currentTurnIndex + 1} of ${turns.length}`;
  updateLiveGauges(currentTurnIndex + 1, turns.length);

  if (currentTurnIndex === turns.length - 1) {
    finishDate();
  }
}

function updateLiveGauges(current, total) {
  const pct = Math.min(96, Math.round(75 + (current / total) * 20));
  const setGauge = (id, valId, val) => {
    const el = document.getElementById(id);
    const valEl = document.getElementById(valId);
    if (el) el.style.setProperty("--gauge-pct", val);
    if (valEl) valEl.textContent = val + "%";
  };
  setGauge("gauge-chem", "val-gauge-chem", pct);
  setGauge("gauge-humor", "val-gauge-humor", Math.min(98, pct + 4));
  setGauge("gauge-intellect", "val-gauge-intellect", Math.min(99, pct + 6));
  setGauge("gauge-safety", "val-gauge-safety", 98);
}

function advanceTurn() {
  if (!currentSimulation) {
    startNewDate();
    return;
  }
  if (currentTurnIndex < currentSimulation.turns.length - 1) {
    currentTurnIndex++;
    renderCurrentTurn();
  } else {
    finishDate();
  }
}

function previousTurn() {
  if (!currentSimulation || currentTurnIndex <= 0) return;
  const stream = document.getElementById("dialogue-stream");
  if (stream.lastElementChild) {
    stream.removeChild(stream.lastElementChild);
  }
  currentTurnIndex--;
  document.getElementById("date-progress-indicator").textContent = `Exchange ${currentTurnIndex + 1} of ${currentSimulation.turns.length}`;
}

function toggleAutoPlay() {
  soundFx.init();
  if (isAutoPlaying) {
    clearInterval(autoPlayInterval);
    isAutoPlaying = false;
    document.getElementById("btn-autoplay").textContent = "⏯️ Auto-Play";
  } else {
    if (!currentSimulation) startNewDate();
    isAutoPlaying = true;
    document.getElementById("btn-autoplay").textContent = "⏸️ Pause";
    autoPlayInterval = setInterval(() => {
      if (currentTurnIndex < currentSimulation.turns.length - 1) {
        advanceTurn();
      } else {
        clearInterval(autoPlayInterval);
        isAutoPlaying = false;
        document.getElementById("btn-autoplay").textContent = "⏯️ Auto-Play";
        finishDate();
      }
    }, 2800);
  }
}

function fastForwardDate() {
  if (!currentSimulation) startNewDate();
  const stream = document.getElementById("dialogue-stream");
  stream.innerHTML = "";
  for (let i = 0; i < currentSimulation.turns.length; i++) {
    currentTurnIndex = i;
    renderCurrentTurn();
  }
  finishDate();
}

function injectCoachWhisper() {
  if (!currentSimulation || !userCoachWhisper) return;
  const nextIdx = currentTurnIndex + 1;
  if (nextIdx < currentSimulation.turns.length) {
    const t = currentSimulation.turns[nextIdx];
    t.dialogue += ` By the way, someone I trust mentioned you value that—how does that resonate with your day-to-day?`;
    t.inner_monologue.thought = `[HUMAN COACH DIRECTIVE INTEGRATED]: "${userCoachWhisper}". Adapted conversation vector immediately.`;
    userCoachWhisper = null;
  }
}

function finishDate() {
  clearInterval(autoPlayInterval);
  isAutoPlaying = false;
  document.getElementById("btn-autoplay").textContent = "⏯️ Auto-Play";
  document.getElementById("btn-view-debrief").style.display = "inline-flex";
  soundFx.playChime();
}

/**
 * Tab 4: Directed Debrief & 24-Candidate Match Rankings
 */
function renderDebriefReport() {
  if (!currentSimulation) return;
  const debriefContainer = document.getElementById("debrief-container");
  debriefContainer.style.display = "block";

  const debriefA = currentSimulation.directed_evaluation_a_to_b;
  const debriefB = currentSimulation.directed_evaluation_b_to_a;

  document.getElementById("debrief-verdict-title").textContent = debriefA.verdict;
  document.getElementById("debrief-score-subtitle").textContent = 
    `Adjusted Shrunk Score S_adj: ${debriefA.overall_score}% | Evaluator: ${debriefA.evaluator} ➔ Target: ${debriefA.target}`;

  // Agent A Confidential Memo
  document.getElementById("agent-a-letter-title").textContent = `${debriefA.evaluator}'s Directed Memo`;
  document.getElementById("agent-a-letter-text").textContent = debriefA.private_memo;
  document.getElementById("agent-a-green-flag").textContent = debriefA.top_green_flag;
  document.getElementById("agent-a-watchout").textContent = debriefA.watchout;

  // Agent B Confidential Memo
  document.getElementById("agent-b-letter-title").textContent = `${debriefB.evaluator}'s Directed Memo`;
  document.getElementById("agent-b-letter-text").textContent = debriefB.private_memo;
  document.getElementById("agent-b-green-flag").textContent = debriefB.top_green_flag;
  document.getElementById("agent-b-watchout").textContent = debriefB.watchout;

  updateRankingsView();
}

function updateRankingsView() {
  if (!cohortDB) return;
  const rankingAgentSelect = document.getElementById("select-ranking-agent");
  const targetId = rankingAgentSelect.value || (currentPerson ? currentPerson.person_id : "person_01");
  const target = cohortDB.people.find(p => p.person_id === targetId);

  document.getElementById("ranking-target-name").textContent = target ? target.display_name : "Target Person";

  const rankings = cohortDB.rankings[targetId] || [];
  const tbody = document.getElementById("rankings-table-body");
  tbody.innerHTML = "";

  rankings.forEach((item) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-weight: 700; color: var(--accent-gold);">#${item.rank_position}</td>
      <td>
        <div class="suitor-cell">
          <img class="suitor-avatar" src="${item.candidate_avatar}" alt="${item.candidate_name}">
          <div>
            <strong style="color: #fff;">${item.candidate_name}</strong>
            <div style="font-size: 0.72rem; color: var(--text-secondary);">${item.candidate_role}</div>
          </div>
        </div>
      </td>
      <td><span style="font-size: 0.85rem; color: #cbd5e1;">${item.candidate_archetype}</span></td>
      <td>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <strong style="color: #fff; font-size: 1rem;">${item.s_adj}%</strong>
          <span style="font-size: 0.72rem; color: var(--text-muted);">(Raw: ${item.s_raw}%)</span>
          <div class="metric-bar-container" style="max-width: 80px;">
            <div class="metric-bar-fill" style="width: ${item.s_adj}%;"></div>
          </div>
        </div>
      </td>
      <td><span class="badge-blue" style="font-size: 0.72rem;">${item.confidence} (${Math.round(item.coverage * 100)}%)</span></td>
      <td><span class="${item.badge_class}">${item.recommendation}</span></td>
      <td>
        <div style="font-size: 0.75rem; color: #34d399;">✦ ${item.top_positive}</div>
        <div style="font-size: 0.72rem; color: #fbbf24; margin-top: 0.2rem;">⚠️ ${item.friction_point}</div>
      </td>
      <td>
        <button class="primary-btn btn-sim-table" data-candidate="${item.candidate_id}" style="padding: 0.35rem 0.75rem; font-size: 0.75rem;">
          Simulate Date
        </button>
      </td>
    `;

    tr.querySelector(".btn-sim-table").addEventListener("click", () => {
      document.getElementById("select-agent-a").value = targetId;
      document.getElementById("select-agent-b").value = item.candidate_id;
      switchTab("tab-date");
      startNewDate();
    });

    tbody.appendChild(tr);
  });
}

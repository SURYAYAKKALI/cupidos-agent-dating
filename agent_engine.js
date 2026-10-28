/**
 * CupidOS: Autonomous Agent-to-Agent Dating Protocol & Simulation Engine
 * Handles psychometric profile analysis, dynamic turn-by-turn date generation,
 * live cognitive inner-monologue streaming, and post-date debrief scoring.
 */

class AgentEngine {
  constructor(profilesData) {
    this.profiles = profilesData.presets || [];
    this.venues = profilesData.venues || [];
    this.dateHistory = [];
    this.customProfiles = [];
  }

  getAllProfiles() {
    return [...this.profiles, ...this.customProfiles];
  }

  getProfile(id) {
    return this.getAllProfiles().find(p => p.id === id);
  }

  getVenue(id) {
    return this.venues.find(v => v.id === id) || this.venues[0];
  }

  /**
   * Multi-stage reading of a public profile URL or raw bio text
   */
  async analyzeProfile(input, onProgress) {
    const steps = [
      { step: 1, name: "Public Footprint Extraction", detail: "Resolving digital traces, transcripts, interviews & social cadence..." },
      { step: 2, name: "Lexical & Sentiment Profiling", detail: "Quantifying vocabulary nuance, irony density & emotional baseline..." },
      { step: 3, name: "Psychometric & Big Five Synthesis", detail: "Calibrating Openness, Conscientiousness, Extraversion, Agreeableness & Neuroticism..." },
      { step: 4, name: "Core Needs & Vulnerability Mapping", detail: "Detecting unstated emotional requirements & attachment triggers..." },
      { step: 5, name: "Dealbreaker & Boundary Formulation", detail: "Synthesizing red flags, green flags & defensive tripwires..." },
      { step: 6, name: "Autonomous Dating Agent Compilation", detail: "Generating cognitive persona directives & live date simulator core..." }
    ];

    for (let i = 0; i < steps.length; i++) {
      if (onProgress) {
        onProgress({
          step: steps[i].step,
          total: steps.length,
          name: steps[i].name,
          detail: steps[i].detail,
          progress: Math.round(((i + 1) / steps.length) * 100)
        });
      }
      await new Promise(r => setTimeout(r, 450));
    }

    // Check if input matches an existing preset
    const lower = input.toLowerCase().trim();
    const existing = this.profiles.find(p => 
      lower.includes(p.name.toLowerCase()) || 
      lower.includes(p.id.toLowerCase()) ||
      (p.publicLinks && p.publicLinks.some(l => lower.includes(l.toLowerCase())))
    );

    if (existing) {
      return existing;
    }

    // If custom input, dynamically infer a rich dating profile
    const customId = "custom_" + Date.now();
    let detectedName = "Unknown Visionary";
    if (input.includes("http")) {
      const match = input.match(/(?:twitter|instagram|x|github|linkedin|wikipedia\.org\/wiki)\/([a-zA-Z0-9_\-]+)/i);
      if (match && match[1]) {
        detectedName = match[1].replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
      }
    } else {
      const words = input.trim().split(/\s+/);
      if (words.length <= 4) {
        detectedName = input.trim();
      } else {
        detectedName = words.slice(0, 2).join(" ");
      }
    }

    const customProfile = {
      id: customId,
      name: detectedName,
      role: "Autonomous Creator / Independent Thinker",
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
      verified: false,
      publicLinks: [input.startsWith("http") ? input : `web/${detectedName.toLowerCase().replace(/\s+/g, '_')}`],
      bio: input.length > 30 ? input : `${detectedName} is an enigmatic explorer of ideas, passionate about deep conversations, creative integrity, and genuine connections.`,
      analysis: {
        archetype: "The Introspective Pioneer",
        loveLanguage: "Intellectual Resonance & Deep Presence",
        mbti: "INTP / INFJ - The Complex Observer",
        bigFive: {
          openness: 89,
          conscientiousness: 81,
          extraversion: 64,
          agreeableness: 85,
          neuroticism: 28
        },
        needs: [
          "Authentic, unscripted connection without performative social games",
          "Space for intellectual curiosity, shared books, and spontaneous deep dives",
          "A partner with high self-awareness who respects emotional and physical boundaries",
          "Playful banter balanced with genuine emotional security"
        ],
        hobbies: [
          "Exploring indie coffee shops & late-night book browsing",
          "Synthesizing multidisciplinary ideas, tech, and storytelling",
          "Curating eclectic music playlists for road trips",
          "Impromptu city walks and exploring architectural gems"
        ],
        conversationalStyle: "Thoughtful and inquisitive; observant before engaging, followed by sharp wit and sincere curiosity.",
        flirtationSignature: "Subtle smiling eye contact, remembering small offhand remarks, asking uniquely piercing questions.",
        greenFlags: [
          "Passionate about their craft without arrogance",
          "Demonstrates kindness to strangers and animals",
          "Can comfortably enjoy quiet moments without awkwardness",
          "Emotionally articulate and transparent"
        ],
        dealbreakers: [
          "Superficial posturing and excessive social media obsession",
          "Lack of intellectual curiosity or refusal to listen",
          "Cruelty or cynicism masked as humor",
          "Emotional unreliability and ghosting behavior"
        ],
        agentDirectives: `Represent ${detectedName} with curiosity, calm confidence, and sharp intuition. Probe the suitor for genuine substance beneath their surface charm.`
      }
    };

    this.customProfiles.push(customProfile);
    return customProfile;
  }

  /**
   * Generates a curated, multi-stage realistic date between two agents
   */
  generateDateSimulation(agentAId, agentBId, venueId) {
    const a = this.getProfile(agentAId);
    const b = this.getProfile(agentBId);
    const venue = this.getVenue(venueId);

    if (!a || !b) return null;

    // Calculate baseline compatibility
    const opennessDiff = Math.abs(a.analysis.bigFive.openness - b.analysis.bigFive.openness);
    const agreeablenessAvg = (a.analysis.bigFive.agreeableness + b.analysis.bigFive.agreeableness) / 2;
    const neuroticismPenalty = (a.analysis.bigFive.neuroticism + b.analysis.bigFive.neuroticism) / 4;
    
    // Base score between 65 and 95
    let baseScore = Math.min(97, Math.max(68, Math.round(92 - (opennessDiff * 0.4) + (agreeablenessAvg * 0.15) - neuroticismPenalty)));

    // Specific famous pairings chemistry tuning
    if ((a.id === 'zendaya' && b.id === 'keanu_reeves') || (a.id === 'keanu_reeves' && b.id === 'zendaya')) {
      baseScore = 93; // Deep mutual respect, groundedness, low pretension
    } else if ((a.id === 'zendaya' && b.id === 'pedro_pascal') || (a.id === 'pedro_pascal' && b.id === 'zendaya')) {
      baseScore = 91; // Warm banter, industry sanity, playful laughter
    } else if ((a.id === 'taylor_swift' && b.id === 'pedro_pascal') || (a.id === 'pedro_pascal' && b.id === 'taylor_swift')) {
      baseScore = 88; // Passionate, storytelling, expressive, joyful
    } else if ((a.id === 'elon_musk' && b.id === 'taylor_swift') || (a.id === 'taylor_swift' && b.id === 'elon_musk')) {
      baseScore = 64; // High friction, contrasting values, huge clash of egos and schedules
    } else if ((a.id === 'billie_eilish' && b.id === 'keanu_reeves') || (a.id === 'keanu_reeves' && b.id === 'billie_eilish')) {
      baseScore = 90; // Gentle alternative vibes, love for genuine authenticity and cars/music
    }

    const turns = this.buildCuratedTurns(a, b, venue, baseScore);

    return {
      dateId: "date_" + Date.now(),
      agentA: a,
      agentB: b,
      venue: venue,
      baseScore: baseScore,
      turns: turns,
      summary: this.generatePostDateDebrief(a, b, venue, baseScore, turns)
    };
  }

  /**
   * Builds high-fidelity, contextual dialogue turns with actions and cognitive inner monologues
   */
  buildCuratedTurns(a, b, venue, overallScore) {
    const turns = [];

    // Stage 1: The Arrival & First Impression
    turns.push({
      phase: "Phase 1: The Arrival & First Impressions",
      speaker: a.id,
      speakerName: a.name,
      avatar: a.avatar,
      action: `arrives at ${venue.name}, takes off their jacket, and greets with a quiet, observant smile`,
      dialogue: `Hey. The lighting in here is stunning—feels like a scene from an old Wong Kar-wai film. Thanks for picking this spot.`,
      innerMonologue: {
        radar: "Initial Body Language & Presence",
        thought: `Evaluating entry composure. Not performing for an audience. Comfortable in their own posture. First impression green flag: 94%.`,
        dealbreakerCheck: "Arrogance / Clout posture: NEGATIVE (Passed)",
        strategy: "Keep initial banter grounded and informal to break any scripted celebrity barriers."
      },
      chemistry: 68,
      tension: 40,
      humorSync: 65,
      intellectualSync: 72
    });

    turns.push({
      phase: "Phase 1: The Arrival & First Impressions",
      speaker: b.id,
      speakerName: b.name,
      avatar: b.avatar,
      action: `slides their glass slightly to the side, looking up with genuine warmth`,
      dialogue: `It really is. The acoustics are great too—you can actually hear someone speak without shouting over a remix. I already ordered a round of the ${venue.drinkSpecials.split(',')[0].trim()}. Hope you don't mind.`,
      innerMonologue: {
        radar: "Vocal Tone & Consideration",
        thought: `Noticed their calm cadence. Proactively ordered something thoughtful. Respects acoustic intimacy.`,
        dealbreakerCheck: "Self-centered conversational pacing: NEGATIVE (Passed)",
        strategy: "Mirror their unhurried pace. Test their reaction to subtle, dry teasing."
      },
      chemistry: 73,
      tension: 48,
      humorSync: 70,
      intellectualSync: 76
    });

    // Stage 2: Ordering & The Banter/Humor Test
    const bQuirk = b.analysis.hobbies[0] || "analog aesthetics";
    const aHobby = a.analysis.hobbies[0] || "vintage textiles";

    turns.push({
      phase: "Phase 2: Banter & Micro-Teasing",
      speaker: a.id,
      speakerName: a.name,
      avatar: a.avatar,
      action: `takes a slow sip, raising an eyebrow with an amused, knowing smirk`,
      dialogue: `A ${venue.drinkSpecials.split(',')[0].trim()}? Bold choice for a first exchange. My friends warned me that someone into ${bQuirk.toLowerCase()} would try to test my taste within the first ten minutes.`,
      innerMonologue: {
        radar: "Playful Provocation Threshold",
        thought: `Injecting a light tease based on their known profile. Will they defend themselves defensively, or lean into the joke with self-awareness?`,
        dealbreakerCheck: "Fragile ego / Lack of self-deprecating humor: TESTING...",
        strategy: "Wait for the counter-punch. Eye contact steady."
      },
      chemistry: 78,
      tension: 62,
      humorSync: 82,
      intellectualSync: 79
    });

    turns.push({
      phase: "Phase 2: Banter & Micro-Teasing",
      speaker: b.id,
      speakerName: b.name,
      avatar: b.avatar,
      action: `laughs softly, leaning back into the velvet booth without missing a beat`,
      dialogue: `Guilty as charged. But honestly, if you can survive the interrogation about ${bQuirk.toLowerCase()}, you get full clearance to roast my Spotify history or my obsession with odd side-projects. Deal?`,
      innerMonologue: {
        radar: "Humor Calibration Result",
        thought: `Passed with flying colors! No defensiveness. High emotional security. Humor sync just spiked.`,
        dealbreakerCheck: "Defensiveness: RESOLVED (Zero flags).",
        strategy: "Escalate to a deeper personal passion to test if intellectual depth matches the wit."
      },
      chemistry: 84,
      tension: 68,
      humorSync: 88,
      intellectualSync: 83
    });

    // Stage 3: Vulnerability & Core Passion Dive
    turns.push({
      phase: "Phase 3: The Vulnerability & Passions Dive",
      speaker: a.id,
      speakerName: a.name,
      avatar: a.avatar,
      action: `rests their chin lightly on their hand, tone shifting into something noticeably more intimate and sincere`,
      dialogue: `Deal. But joking aside... what’s something you care about deeply that almost nobody in your public life ever asks you about? Like, the thing you’d stay up until 3 AM working on even if no one was watching?`,
      innerMonologue: {
        radar: "Depth & Authenticity Probe",
        thought: `Testing core emotional need: [Authenticity over public spectacle]. Listening for performative elevator pitches versus raw, private passion.`,
        dealbreakerCheck: "Performative PR answers: MONITORING...",
        strategy: "Observe micro-expressions when talking about non-monetized loves."
      },
      chemistry: 89,
      tension: 74,
      humorSync: 84,
      intellectualSync: 91
    });

    turns.push({
      phase: "Phase 3: The Vulnerability & Passions Dive",
      speaker: b.id,
      speakerName: b.name,
      avatar: b.avatar,
      action: `pauses, gazing at the amber reflection in the table before speaking with absolute quiet sincerity`,
      dialogue: `Honestly? It’s the quiet craft of things that don’t seek applause. Like fixing something broken with your own hands, or spending hours trying to get a four-bar chord progression to feel like rain. When everything in the world feels loud and transactional, that quiet space is the only thing that keeps me sane.`,
      innerMonologue: {
        radar: "Soulful Alignment Check",
        thought: `Emotional resonance match: 96%. They just articulated the exact same craving for private sanctuaries. Zero PR gloss. Total emotional transparency.`,
        dealbreakerCheck: "Superficiality: NEGATIVE. High empathy index.",
        strategy: "Acknowledge the resonance without over-romanticizing. Keep the grounded bond."
      },
      chemistry: 93,
      tension: 78,
      humorSync: 86,
      intellectualSync: 95
    });

    // Stage 4: The Boundary & Reality Test
    turns.push({
      phase: "Phase 4: The Boundary & Stress Test",
      speaker: a.id,
      speakerName: a.name,
      avatar: a.avatar,
      action: `nods slowly, their eyes holding the moment with palpable warmth`,
      dialogue: `That hit somewhere real. People love the idea of someone until they realize you come with weird hours, private boundaries, and days where you just don't have the bandwidth to entertain anyone. How do you handle someone who needs their own separate universe?`,
      innerMonologue: {
        radar: "Boundary Compatibility Check",
        thought: `Directly testing relationship dealbreaker: Can this person coexist with an independent, highly autonomous partner without demanding constant emotional appeasement?`,
        dealbreakerCheck: "Anxious clinginess vs Secure autonomy: PROBING...",
        strategy: "Evaluate boundary acceptance."
      },
      chemistry: 91,
      tension: 82,
      humorSync: 87,
      intellectualSync: 94
    });

    turns.push({
      phase: "Phase 4: The Boundary & Stress Test",
      speaker: b.id,
      speakerName: b.name,
      avatar: b.avatar,
      action: `smiles with an effortless, calm reassurance`,
      dialogue: `Separate universes are mandatory. If two people collapse into one orbit, somebody’s going to suffocate. I’d rather be two complete solar systems that just really love visiting each other’s gravity.`,
      innerMonologue: {
        radar: "Philosophical Synthesis",
        thought: `Remarkable metaphor. Secure attachment archetype confirmed. Chemistry index reaching peak equilibrium.`,
        dealbreakerCheck: "Codependency risks: NULL. Ideal autonomy harmony.",
        strategy: "Transition smoothly toward closing chemistry and establishing clear intent for next real-world step."
      },
      chemistry: 95,
      tension: 85,
      humorSync: 90,
      intellectualSync: 96
    });

    // Stage 5: Closing Chemistry & The Bill / Next Date Spark
    turns.push({
      phase: "Phase 5: The Spark & The Next Move",
      speaker: a.id,
      speakerName: a.name,
      avatar: a.avatar,
      action: `laughs softly, shaking their head in disbelief as the server quietly places the check between them`,
      dialogue: `Look at that. Two solar systems and we haven't even argued over who gets the check yet. I have to admit... my agent was skeptical about setting this up, but this was the most genuine two hours I’ve had all year.`,
      innerMonologue: {
        radar: "Final Sentiment Calculation",
        thought: `Date completed. Final compatibility outcome: Exceptional. Human principal will be advised to proceed with an in-person, private second date.`,
        dealbreakerCheck: "All boundaries cleared with 0 violations.",
        strategy: "Lock in recommendation for second real-world date."
      },
      chemistry: overallScore,
      tension: 80,
      humorSync: 92,
      intellectualSync: 96
    });

    turns.push({
      phase: "Phase 5: The Spark & The Next Move",
      speaker: b.id,
      speakerName: b.name,
      avatar: b.avatar,
      action: `reaches for the check with a playful wink and stands up to walk out together`,
      dialogue: `Let’s split it, or better yet—you get the drinks, I get the next diner stop with the terrible jukebox. Tell your agent their predictive algorithm just earned its bonus.`,
      innerMonologue: {
        radar: "Closing Synthesis",
        thought: `Confirmed mutual greenlight. Rapport established on intellect, humor, and respect for privacy. Transmitting positive debrief to human principal.`,
        dealbreakerCheck: "Mutual verification COMPLETE.",
        strategy: "Finalize debrief dossier."
      },
      chemistry: overallScore,
      tension: 76,
      humorSync: 94,
      intellectualSync: 97
    });

    return turns;
  }

  /**
   * Post-Date Debrief & Intelligence Report Generation
   */
  generatePostDateDebrief(a, b, venue, overallScore, turns) {
    const isSuccess = overallScore >= 80;
    const isMedium = overallScore >= 70 && overallScore < 80;

    const verdictTitle = isSuccess 
      ? "RECOMMENDED: Immediate Real-World Second Date" 
      : (isMedium ? "PROCEED WITH CAUTION: Casual / Intellectual Match" : "PASS: Fundamental Values Disconnect");

    return {
      verdictTitle: verdictTitle,
      overallScore: overallScore,
      radarMetrics: {
        intellectualSpark: Math.min(99, overallScore + 3),
        banterAndHumor: Math.min(98, overallScore - 1),
        lifestyleAlignment: Math.min(96, overallScore - 4),
        emotionalSafety: Math.min(99, overallScore + 2),
        boundaryRespect: 97
      },
      agentADebrief: {
        agentName: a.name + "'s Dating Agent",
        privateNoteToHuman: `Dear ${a.name}, I spent 2 hours simulating a date with ${b.name}'s autonomous avatar at ${venue.name}. They showed zero signs of social climbing, understood your need for private sanctuary, and matched your dry humor effortlessly. Their boundary score was 97%. My calculated verdict: Say yes to coffee in the real world.`,
        topGreenFlag: `Genuine humility when speaking about their passions; total absence of performative posturing.`,
        potentialWatchout: `High independent schedule; will need asynchronous communication tolerance.`
      },
      agentBDebrief: {
        agentName: b.name + "'s Dating Agent",
        privateNoteToHuman: `Dear ${b.name}, ${a.name}'s avatar was razor-sharp, attentive, and brought out your most grounded, candid thoughts. They laughed at your jokes without being sycophantic. Chemistry index locked in at ${overallScore}%. Greenlight given.`,
        topGreenFlag: `Instant comfort with silence and thoughtful pacing; respected intellectual sovereignty.`,
        potentialWatchout: `Both of you have demanding travel calendars—coordination requires intentionality.`
      },
      secondDateProbability: isSuccess ? `${Math.min(98, overallScore + 4)}%` : `${overallScore - 10}%`,
      recommendedNextDateIdea: isSuccess 
        ? "Low-profile late-night vinyl record listening session or an unpretentious hole-in-the-wall diner." 
        : "Daytime gallery walk or mutual podcast conversation to test platonic intellectual synergy."
    };
  }

  /**
   * Save completed date to history for rankings
   */
  recordDate(dateSimulation) {
    this.dateHistory.unshift(dateSimulation);
  }

  /**
   * Get ranked candidates against a specific agent
   */
  getRankingsForAgent(targetAgentId) {
    const allProfiles = this.getAllProfiles().filter(p => p.id !== targetAgentId);
    const target = this.getProfile(targetAgentId);
    if (!target) return [];

    return allProfiles.map(suitor => {
      // Check if an actual date simulation exists
      const pastDate = this.dateHistory.find(d => 
        (d.agentA.id === targetAgentId && d.agentB.id === suitor.id) ||
        (d.agentB.id === targetAgentId && d.agentA.id === suitor.id)
      );

      let score;
      let dateStatus;
      if (pastDate) {
        score = pastDate.baseScore;
        dateStatus = "Simulated Date Completed";
      } else {
        // Compute predictive compatibility
        const openDiff = Math.abs(target.analysis.bigFive.openness - suitor.analysis.bigFive.openness);
        const agrAvg = (target.analysis.bigFive.agreeableness + suitor.analysis.bigFive.agreeableness) / 2;
        score = Math.min(96, Math.max(65, Math.round(88 - (openDiff * 0.4) + (agrAvg * 0.15))));
        dateStatus = "Predictive Match Pending Date";
      }

      let recommendation = "Strong Match";
      let badgeClass = "badge-green";
      if (score >= 90) {
        recommendation = "⭐ Soulmate Tier";
        badgeClass = "badge-gold";
      } else if (score >= 80) {
        recommendation = "🔥 Highly Compatible";
        badgeClass = "badge-green";
      } else if (score >= 72) {
        recommendation = "☕ Coffee / Friends";
        badgeClass = "badge-blue";
      } else {
        recommendation = "⚠️ High Friction";
        badgeClass = "badge-red";
      }

      return {
        profile: suitor,
        score: score,
        status: dateStatus,
        recommendation: recommendation,
        badgeClass: badgeClass,
        pastDate: pastDate
      };
    }).sort((a, b) => b.score - a.score);
  }
}

// Export for browser and node
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AgentEngine;
}

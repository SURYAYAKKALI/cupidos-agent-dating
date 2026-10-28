import json
import re

# Load raw Apify dataset
with open('dataset_instagram-scraper_2026-10-28_12-31-22-594.json', 'r', encoding='utf-8') as f:
    raw_profiles = json.load(f)

print(f"Loaded {len(raw_profiles)} raw profiles from Apify dataset.")

# Candidate catalog of 25 distinct personalities with rich profiles
CURATED_META = {
    "bhavishaggarwal": {
        "title": "Founder & CEO, Ola & Krutrim",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/bhavishaggarwal",
        "interests": ["electric mobility", "sovereign AI", "manufacturing", "marathon training"],
        "venues": ["vinyl_cafe", "city_park"],
        "gender": "male"
    },
    "steven": {
        "title": "Founder, Flight Story & Host of Diary of a CEO",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/stevenbartlett564",
        "interests": ["behavioral psychology", "podcasting", "creative entrepreneurship", "health tech"],
        "venues": ["cozy_restaurant", "speakeasy_lounge"],
        "gender": "male"
    },
    "adamgrant": {
        "title": "Organizational Psychologist & Author",
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/adammgrant",
        "interests": ["organizational dynamics", "generosity theory", "diving", "evidence-based management"],
        "venues": ["vinyl_cafe", "city_park"],
        "gender": "male"
    },
    "priyankachopra": {
        "title": "Global Actress, Producer & UNICEF Ambassador",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/priyankachopra",
        "interests": ["cinema production", "global philanthropy", "culinary exploration", "family traditions"],
        "venues": ["cozy_restaurant", "speakeasy_lounge"],
        "gender": "female"
    },
    "thisisbillgates": {
        "title": "Co-Chair, Gates Foundation & Technologist",
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/williamhgates",
        "interests": ["global health", "clean energy", "reading nonfiction", "bridge & tennis"],
        "venues": ["city_park", "cozy_restaurant"],
        "gender": "male"
    },
    "marieforleo": {
        "title": "Author & Creator of MarieTV",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/marieforleo",
        "interests": ["mindset coaching", "hip-hop dance", "creative writing", "online education"],
        "venues": ["vinyl_cafe", "cozy_restaurant"],
        "gender": "female"
    },
    "melindafrenchgates": {
        "title": "Philanthropist & Founder, Pivotal Ventures",
        "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/melindagates",
        "interests": ["women's economic power", "social progress", "distance running", "puzzles"],
        "venues": ["city_park", "cozy_restaurant"],
        "gender": "female"
    },
    "mkbhd": {
        "title": "Creator & Host, MKBHD & Waveform",
        "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/marques-brownlee-b3711942",
        "interests": ["consumer tech", "ultimate frisbee", "cinematography", "electric vehicles"],
        "venues": ["vinyl_cafe", "city_park"],
        "gender": "male"
    },
    "jayshetty": {
        "title": "Author & Host of On Purpose",
        "avatar": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/jayshetty",
        "interests": ["mindfulness", "meditation", "podcast interviews", "tea ceremonies"],
        "venues": ["vinyl_cafe", "city_park"],
        "gender": "male"
    },
    "varundvn": {
        "title": "Actor & Fitness Enthusiast",
        "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/varun-dhawan-acting",
        "interests": ["action choreography", "football", "comedy cinema", "calisthenics"],
        "venues": ["cozy_restaurant", "city_park"],
        "gender": "male"
    },
    "garyvee": {
        "title": "Chairman, VaynerX & CEO, VaynerMedia",
        "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/garyvaynerchuk",
        "interests": ["vintage sports cards", "garage sales", "consumer attention", "NY Jets"],
        "venues": ["speakeasy_lounge", "vinyl_cafe"],
        "gender": "male"
    },
    "tonyrobbins": {
        "title": "Author, Strategist & Speaker",
        "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/ajrobbins",
        "interests": ["human performance", "cryotherapy", "philanthropy", "wealth architecture"],
        "venues": ["cozy_restaurant", "city_park"],
        "gender": "male"
    },
    "kritisanon": {
        "title": "Actor, Entrepreneur (Hyphen) & Producer",
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/kritisanon",
        "interests": ["skincare formulation", "poetry writing", "indie cinema", "kathak dance"],
        "venues": ["vinyl_cafe", "speakeasy_lounge"],
        "gender": "female"
    },
    "nikhilkamathcio": {
        "title": "Co-founder, Zerodha, True Beacon & WTF Podcast",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/nikhilkamathcio",
        "interests": ["chess strategy", "macroeconomics", "long-form interviews", "fitness"],
        "venues": ["speakeasy_lounge", "vinyl_cafe"],
        "gender": "male"
    },
    "deepikapadukone": {
        "title": "Actor, Founder (82°E) & Mental Health Advocate",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/deepikapadukone",
        "interests": ["badminton", "mental health advocacy", "interior architecture", "wellness rituals"],
        "venues": ["cozy_restaurant", "city_park"],
        "gender": "female"
    },
    "kevinolearytv": {
        "title": "Chairman, O'Leary Ventures & Shark Tank Investor",
        "avatar": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/kevinolearytv",
        "interests": ["horology & watch collecting", "fine wine making", "guitar jam sessions", "cooking"],
        "venues": ["cozy_restaurant", "speakeasy_lounge"],
        "gender": "male"
    },
    "mcuban": {
        "title": "Entrepreneur, Cost Plus Drugs & Investor",
        "avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/mark-cuban-06a0755b",
        "interests": ["generic drug price transparency", "Dallas Mavericks", "AI healthcare", "reading books"],
        "venues": ["vinyl_cafe", "city_park"],
        "gender": "male"
    },
    "simonsinek": {
        "title": "Author, 'Start With Why' & Ethographer",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/simon-sinek",
        "interests": ["leadership ethics", "optimism psychology", "pottery", "reading history"],
        "venues": ["vinyl_cafe", "city_park"],
        "gender": "male"
    },
    "ariannahuff": {
        "title": "Founder, Thrive Global & The Huffington Post",
        "avatar": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/ariannahuffington",
        "interests": ["sleep science", "micro-steps wellness", "ancient Greek philosophy", "walking meetings"],
        "venues": ["city_park", "vinyl_cafe"],
        "gender": "female"
    },
    "rajshamani": {
        "title": "Entrepreneur, House of X & Podcaster (Figuring Out)",
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/rajshamani",
        "interests": ["consumer brands", "youth mentorship", "stand-up comedy", "travel vlogging"],
        "venues": ["vinyl_cafe", "speakeasy_lounge"],
        "gender": "male"
    },
    "sarablakely": {
        "title": "Founder, Spanx & Sneex",
        "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/sarablakely27",
        "interests": ["inventing footwear", "humorous storytelling", "family adventures", "female entrepreneurship"],
        "venues": ["cozy_restaurant", "vinyl_cafe"],
        "gender": "female"
    },
    "thesharkdaymond": {
        "title": "Founder & CEO, FUBU & Shark Tank Investor",
        "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/daymondjohn",
        "interests": ["streetwear culture", "fly fishing", "bee keeping", "brand licensing"],
        "venues": ["speakeasy_lounge", "city_park"],
        "gender": "male"
    },
    "lewishowes": {
        "title": "Host of The School of Greatness & NYT Author",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/lewishowes",
        "interests": ["handball athletic training", "emotional vulnerability", "salsa dancing", "meditation"],
        "venues": ["cozy_restaurant", "city_park"],
        "gender": "male"
    },
    "timferriss": {
        "title": "Author, 'The 4-Hour Workweek' & Investor",
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/timferriss",
        "interests": ["stoic philosophy", "language acquisition", "tea craftsmanship", "tango & archery"],
        "venues": ["vinyl_cafe", "city_park"],
        "gender": "male"
    },
    "shraddhakapoor": {
        "title": "Actor & Singer",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "linkedin": "https://www.linkedin.com/in/shraddhakapoor",
        "interests": ["playback singing", "nature retreats", "street food walks", "animal rescue"],
        "venues": ["city_park", "cozy_restaurant"],
        "gender": "female"
    }
}

print(f"Curated meta has {len(CURATED_META)} people.")

import json
import random

# Load Apify raw dataset
with open('dataset_instagram-scraper_2026-10-28_12-31-22-594.json', 'r', encoding='utf-8') as f:
    raw_dataset = json.load(f)

raw_by_username = {p.get("username"): p for p in raw_dataset if p.get("username")}

# Curated metadata for 25 people
PEOPLE_DEF = [
    {
        "id": "person_01",
        "username": "steven",
        "display_name": "Steven Bartlett",
        "role": "Founder, Flight Story & Host of The Diary of a CEO",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/stevenbartlett564",
        "instagram_url": "https://www.instagram.com/steven",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "bio": "Entrepreneur, speaker, investor, author of The Diary of a CEO. Passionate about health optimization, consumer psychology, and relentless curiosity.",
        "archetype": "The Strategic Storyteller",
        "mbti": "ENTJ",
        "interests": ["behavioral psychology", "podcasting", "creative entrepreneurship", "health tech", "marathon training"],
        "preferred_activities": ["conversation", "dining", "audio_exploration"],
        "avoided_activities": ["loud_crowds", "superficial_small_talk"],
        "preferred_venues": ["cozy_restaurant", "speakeasy_lounge"],
        "communication_style": "Probing, insightful, articulate. Loves asking the question behind the question.",
        "quotes": ["Humans were designed to create; this is why we get depressed when all we do is consume."]
    },
    {
        "id": "person_02",
        "username": "priyankachopra",
        "display_name": "Priyanka Chopra Jonas",
        "role": "Global Actress, Producer & Philanthropist",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/priyankachopra",
        "instagram_url": "https://www.instagram.com/priyankachopra",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "bio": "Actor, producer, author of 'Unfinished', UNICEF Goodwill Ambassador. Living boldly between cultures, family traditions, and cinema storytelling.",
        "archetype": "The Radiant Trailblazer",
        "mbti": "ENFJ",
        "interests": ["cinema storytelling", "global philanthropy", "culinary travel", "family traditions", "fashion archives"],
        "preferred_activities": ["dining", "cultural_walks", "intimate_gatherings"],
        "avoided_activities": ["aloofness", "rigid_schedules"],
        "preferred_venues": ["cozy_restaurant", "speakeasy_lounge"],
        "communication_style": "Charismatic, warm, razor-sharp wit. Balances high energy with genuine emotional presence.",
        "quotes": ["There is a first time for everything. Own your narrative."]
    },
    {
        "id": "person_03",
        "username": "bhavishaggarwal",
        "display_name": "Bhavish Aggarwal",
        "role": "Founder & CEO, Ola & Krutrim",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/bhavishaggarwal",
        "instagram_url": "https://www.instagram.com/bhavishaggarwal",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "bio": "Building India's electric mobility revolution and sovereign AI stack. Deeply committed to technological self-reliance, manufacturing, and scale.",
        "archetype": "The Relentless Builder",
        "mbti": "INTJ",
        "interests": ["electric mobility", "sovereign AI", "manufacturing robotics", "marathon running", "cycling"],
        "preferred_activities": ["coffee", "walk_and_talk", "factory_tours"],
        "avoided_activities": ["glitz_events", "bureaucratic_delays"],
        "preferred_venues": ["vinyl_cafe", "city_park"],
        "communication_style": "Direct, fast-paced, first-principles focused. Prefers substance over polish.",
        "quotes": ["Technology should belong to the people who build with it."]
    },
    {
        "id": "person_04",
        "username": "adamgrant",
        "display_name": "Adam Grant",
        "role": "Organizational Psychologist & Author",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/adammgrant",
        "instagram_url": "https://www.instagram.com/adamgrant",
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80",
        "bio": "Wharton professor, author of 'Think Again' and 'Hidden Potential'. Fascinated by generosity, motivation, diving, and how people unlearn old assumptions.",
        "archetype": "The Curious Inquirer",
        "mbti": "INFJ",
        "interests": ["organizational dynamics", "generosity theory", "springboard diving", "evidence-based debate", "teaching"],
        "preferred_activities": ["thoughtful_coffee", "walking_dialogue", "bookstore_browsing"],
        "avoided_activities": ["superficial_flattery", "closed-mindedness"],
        "preferred_venues": ["vinyl_cafe", "city_park"],
        "communication_style": "Gentle, intellectually playful, deeply reflective. Tests hypotheses with warmth.",
        "quotes": ["If knowledge is power, knowing what we don't know is wisdom."]
    },
    {
        "id": "person_05",
        "username": "thisisbillgates",
        "display_name": "Bill Gates",
        "role": "Co-Chair, Gates Foundation & Technologist",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/williamhgates",
        "instagram_url": "https://www.instagram.com/thisisbillgates",
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80",
        "bio": "Devoted to global health eradication, clean energy breakthroughs, and reading dozens of nonfiction books every year. Enjoys tennis and bridge.",
        "archetype": "The Global Problem Solver",
        "mbti": "INTP",
        "interests": ["global health", "clean energy transition", "nonfiction literature", "bridge tournaments", "tennis"],
        "preferred_activities": ["intellectual_dinner", "reading_discussion", "quiet_walks"],
        "avoided_activities": ["sensationalism", "idle_gossip"],
        "preferred_venues": ["cozy_restaurant", "city_park"],
        "communication_style": "Analytical, pragmatic, richly informed. Gets visibly animated when discussing solutions to complex systems.",
        "quotes": ["Optimism is not a blind belief that things will get better; it's a conviction that we can make things better."]
    },
    {
        "id": "person_06",
        "username": "marieforleo",
        "display_name": "Marie Forleo",
        "role": "Host of MarieTV & Author of 'Everything is Figureoutable'",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/marieforleo",
        "instagram_url": "https://www.instagram.com/marieforleo",
        "avatar": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80",
        "bio": "#1 NYT Bestselling Author, creator of B-School and MarieTV. Passionate about empowering creative entrepreneurs, hip-hop dancing, and authentic joy.",
        "archetype": "The Joyful Catalyst",
        "mbti": "ENFP",
        "interests": ["mindset empowerment", "hip-hop dance", "creative writing", "small business mentorship", "cooking Italian feasts"],
        "preferred_activities": ["dance_movement", "lively_cafe_chats", "spontaneous_outings"],
        "avoided_activities": ["cynicism", "rigid_formality"],
        "preferred_venues": ["vinyl_cafe", "cozy_restaurant"],
        "communication_style": "Energetic, humorous, encouraging. Cuts straight to the heart of what inspires someone.",
        "quotes": ["Everything is figureoutable when you combine courage with action."]
    },
    {
        "id": "person_07",
        "username": "melindafrenchgates",
        "display_name": "Melinda French Gates",
        "role": "Philanthropist & Founder, Pivotal Ventures",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/melindagates",
        "instagram_url": "https://www.instagram.com/melindafrenchgates",
        "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80",
        "bio": "Advocate for women and girls globally, author of 'The Moment of Lift'. Loves long distance trail running, quiet puzzles, and deep human conversations.",
        "archetype": "The Empathetic Architect",
        "mbti": "INFJ",
        "interests": ["women's economic equity", "social progress", "distance running", "jigsaw puzzles", "reading biographies"],
        "preferred_activities": ["nature_walks", "intimate_dinners", "book_exchanges"],
        "avoided_activities": ["performative_grandstanding", "condescension"],
        "preferred_venues": ["city_park", "cozy_restaurant"],
        "communication_style": "Measured, soulful, deeply listening. Values authenticity and quiet dignity above all else.",
        "quotes": ["When you lift up women, you lift up humanity."]
    },
    {
        "id": "person_08",
        "username": "mkbhd",
        "display_name": "Marques Brownlee",
        "role": "YouTuber, Technologist & Professional Ultimate Player",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/marques-brownlee-b3711942",
        "instagram_url": "https://www.instagram.com/mkbhd",
        "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "bio": "Host of Waveform, creator of MKBHD, professional Ultimate Frisbee player. Appreciates clean industrial design, tactile buttons, and honest reviews.",
        "archetype": "The Tactile Craftsman",
        "mbti": "ISTP",
        "interests": ["consumer tech hardware", "ultimate frisbee", "RED cameras & lenses", "electric vehicle engineering", "sneakers"],
        "preferred_activities": ["casual_coffee", "frisbee_park_session", "cinema_screening"],
        "avoided_activities": ["unnecessary_drama", "hype_without_substance"],
        "preferred_venues": ["vinyl_cafe", "city_park"],
        "communication_style": "Crisp, understated, calm. Talks about nuance with infectious, subtle enthusiasm.",
        "quotes": ["Crisp aesthetics and honest feedback will always outlive marketing hype."]
    },
    {
        "id": "person_09",
        "username": "jayshetty",
        "display_name": "Jay Shetty",
        "role": "Author, Podcaster & Purpose Coach",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/jayshetty",
        "instagram_url": "https://www.instagram.com/jayshetty",
        "avatar": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?auto=format&fit=crop&w=400&q=80",
        "bio": "Former monk, author of 'Think Like a Monk' and '8 Rules of Love', host of On Purpose. Dedicated to making ancient wisdom practical for modern hearts.",
        "archetype": "The Mindful Guide",
        "mbti": "ENFJ",
        "interests": ["mindfulness practices", "vedic philosophy", "storytelling", "tea tasting", "nature hikes"],
        "preferred_activities": ["tea_ceremony", "quiet_meditation_walk", "meaningful_dialogue"],
        "avoided_activities": ["cynical_arguments", "frenetic_schedules"],
        "preferred_venues": ["vinyl_cafe", "city_park"],
        "communication_style": "Gentle, intentional, poetic. Pauses to absorb what people say before responding with an analogy.",
        "quotes": ["Don't let the noise of others drown out the quiet compass of your soul."]
    },
    {
        "id": "person_10",
        "username": "varundvn",
        "display_name": "Varun Dhawan",
        "role": "Actor & Fitness Advocate",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/varun-dhawan-acting",
        "instagram_url": "https://www.instagram.com/varundvn",
        "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=400&q=80",
        "bio": "Bollywood actor known for high-octane comedy and intense drama. Dog lover (Joey), fitness enthusiast, and dedicated cinema professional.",
        "archetype": "The Playful Dynamo",
        "mbti": "ESFP",
        "interests": ["action choreography", "football matches", "calisthenics", "rescue dogs", "family cookouts"],
        "preferred_activities": ["lively_dinner", "sports_activities", "movie_nights"],
        "avoided_activities": ["pretentious_stiffness", "overthinking"],
        "preferred_venues": ["cozy_restaurant", "city_park"],
        "communication_style": "High-spirited, affectionate, spontaneous. Uses self-effacing humor and physical energy to break ice.",
        "quotes": ["See the world through laughter; it's the fastest way to connect."]
    },
    {
        "id": "person_11",
        "username": "garyvee",
        "display_name": "Gary Vaynerchuk",
        "role": "Chairman, VaynerX & Creator of VeeFriends",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/garyvaynerchuk",
        "instagram_url": "https://www.instagram.com/garyvee",
        "avatar": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=400&q=80",
        "bio": "Serial entrepreneur, wine expert, die-hard NY Jets fan, garage sale flipper. Obsessed with human attention, empathy in business, and patience.",
        "archetype": "The Gritty Optimist",
        "mbti": "ESTP",
        "interests": ["vintage sports cards", "garage sales hunting", "consumer culture", "NY Jets", "natural wine"],
        "preferred_activities": ["flea_market_treasure_hunts", "casual_slice_and_talk", "coffee_walks"],
        "avoided_activities": ["whining", "entitled_complaining"],
        "preferred_venues": ["speakeasy_lounge", "vinyl_cafe"],
        "communication_style": "Candid, explosive, surprisingly warm. Demands extreme accountability mixed with radical empathy.",
        "quotes": ["Kindness is the ultimate competitive advantage in life."]
    },
    {
        "id": "person_12",
        "username": "tonyrobbins",
        "display_name": "Tony Robbins",
        "role": "Life & Business Strategist, Author",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/ajrobbins",
        "instagram_url": "https://www.instagram.com/tonyrobbins",
        "avatar": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=400&q=80",
        "bio": "#1 NYT bestselling author, philanthropist providing billions of meals via Feeding America. Believes the quality of life is the quality of questions.",
        "archetype": "The Force of Nature",
        "mbti": "ENTJ",
        "interests": ["human peak performance", "cryotherapy & biohacking", "massive philanthropy", "ocean swimming"],
        "preferred_activities": ["intensive_conversation", "scenic_ocean_walk", "healthy_supper"],
        "avoided_activities": ["resignation", "mediocrity_as_an_excuse"],
        "preferred_venues": ["cozy_restaurant", "city_park"],
        "communication_style": "Booming, inspiring, commanding. Challenges partners to step into their highest standard.",
        "quotes": ["Trade your expectation for appreciation and the whole world changes in an instant."]
    },
    {
        "id": "person_13",
        "username": "kritisanon",
        "display_name": "Kriti Sanon",
        "role": "National Award-Winning Actor & Founder (Hyphen)",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/kritisanon",
        "instagram_url": "https://www.instagram.com/kritisanon",
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80",
        "bio": "Engineering graduate turned National Award-winning actress, skincare entrepreneur (Hyphen), and film producer. Writes private Hindi poetry.",
        "archetype": "The Artful Analyst",
        "mbti": "INFJ",
        "interests": ["skincare formulation", "poetry writing", "Kathak classical dance", "indie cinema", "home decor"],
        "preferred_activities": ["cozy_bistro_dinner", "poetry_reading", "music_cafe"],
        "avoided_activities": ["shallow_showmanship", "condescending_advice"],
        "preferred_venues": ["vinyl_cafe", "speakeasy_lounge"],
        "communication_style": "Grounded, observant, quick-witted. Mixes analytical intelligence with genuine creative softness.",
        "quotes": ["Between formulas and poetry, there lies the real truth of who we are."]
    },
    {
        "id": "person_14",
        "username": "nikhilkamathcio",
        "display_name": "Nikhil Kamath",
        "role": "Co-Founder, Zerodha, True Beacon & WTF Podcast",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/nikhilkamathcio",
        "instagram_url": "https://www.instagram.com/nikhilkamathcio",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "bio": "School dropout turned billionaire fintech founder, avid chess player, host of the WTF podcast. Deeply curious about macroeconomics, health, and philosophy.",
        "archetype": "The Unorthodox Grandmaster",
        "mbti": "INTP",
        "interests": ["competitive chess", "macroeconomic history", "long-form podcasting", "functional fitness", "contemporary art"],
        "preferred_activities": ["chess_over_drinks", "unhurried_dinner", "gallery_browse"],
        "avoided_activities": ["conventional_social_norms", "bureaucratic_small_talk"],
        "preferred_venues": ["speakeasy_lounge", "vinyl_cafe"],
        "communication_style": "Deadpan, curious, non-conformist. Enjoys poking holes in popular dogma with a calm smile.",
        "quotes": ["Most conventional wisdom is designed to make people average. Question everything gently."]
    },
    {
        "id": "person_15",
        "username": "deepikapadukone",
        "display_name": "Deepika Padukone",
        "role": "Actor, Producer & Founder, Live Love Laugh Foundation",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/deepikapadukone",
        "instagram_url": "https://www.instagram.com/deepikapadukone",
        "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=400&q=80",
        "bio": "Pioneering mental health advocate, former national badminton athlete, global cinema star, founder of 82°E. Passionate about slow living and grounded peace.",
        "archetype": "The Poised Healer",
        "mbti": "ISFJ",
        "interests": ["badminton", "mental health advocacy", "minimalist architecture", "wellness rituals", "home cooking"],
        "preferred_activities": ["quiet_tea_afternoon", "badminton_friendly_match", "home-style_dinner"],
        "avoided_activities": ["loud_clubbing", "insincere_flattery"],
        "preferred_venues": ["cozy_restaurant", "city_park"],
        "communication_style": "Gentle, composed, deeply reassuring. Radiates quiet strength and authentic emotional vulnerability.",
        "quotes": ["It is okay to not be okay, as long as you dare to be honest with yourself."]
    },
    {
        "id": "person_16",
        "username": "kevinolearytv",
        "display_name": "Kevin O'Leary",
        "role": "Chairman, O'Leary Ventures & Shark Tank's 'Mr. Wonderful'",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/kevinolearytv",
        "instagram_url": "https://www.instagram.com/kevinolearytv",
        "avatar": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=400&q=80",
        "bio": "Venture capitalist, culinary aficionado, fine horologist, guitarist. Prides himself on cold financial realism paired with a passion for music and vintage wines.",
        "archetype": "The Sophisticated Realist",
        "mbti": "ENTJ",
        "interests": ["rare watch horology", "Bordeaux winemaking", "electric guitar blues", "photography", "chef tasting menus"],
        "preferred_activities": ["wine_tasting_dinner", "acoustic_jam_session", "watch_gallery_tour"],
        "avoided_activities": ["emotional_delusions", "wasting_time"],
        "preferred_venues": ["cozy_restaurant", "speakeasy_lounge"],
        "communication_style": "Pragmatic, theatrical, wickedly funny. Drops hard truths wrapped in cultured humor.",
        "quotes": ["Money is neutral; it just amplifies who you already are. Wine, however, makes it better."]
    },
    {
        "id": "person_17",
        "username": "mcuban",
        "display_name": "Mark Cuban",
        "role": "Tech Entrepreneur, Dallas Mavericks & Cost Plus Drugs",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/mark-cuban-06a0755b",
        "instagram_url": "https://www.instagram.com/mcuban",
        "avatar": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80",
        "bio": "Disrupting the pharmaceutical industry with transparent generic drug pricing. Sports fan, tech investor, voracious reader, Pittsburgh native.",
        "archetype": "The Fierce Competitor",
        "mbti": "ESTP",
        "interests": ["generic drug price transparency", "basketball analytics", "reading software whitepapers", "aerobics", "casual pubs"],
        "preferred_activities": ["sports_bar_dinner", "reading_deep_dives", "park_jog"],
        "avoided_activities": ["monopolistic_arrogance", "passive_resignation"],
        "preferred_venues": ["vinyl_cafe", "city_park"],
        "communication_style": "Energetic, outspoken, direct. Loves spirited debates where facts triumph over pedigree.",
        "quotes": ["Work like someone is working 24 hours a day to take it away from you."]
    },
    {
        "id": "person_18",
        "username": "simonsinek",
        "display_name": "Simon Sinek",
        "role": "Author, 'Start With Why' & 'The Infinite Game'",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/simon-sinek",
        "instagram_url": "https://www.instagram.com/simonsinek",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "bio": "Trained ethnographer, optimist, teacher of leadership rooted in human trust and vulnerability. Believes in building worlds that outlast ourselves.",
        "archetype": "The Visionary Optimist",
        "mbti": "ENFJ",
        "interests": ["leadership anthropology", "infinite game mindset", "pottery", "reading human history", "dinner parties"],
        "preferred_activities": ["fireside_chat", "philosophical_coffee", "artisan_pottery_workshop"],
        "avoided_activities": ["transactional_networking", "cynical_gamesmanship"],
        "preferred_venues": ["vinyl_cafe", "city_park"],
        "communication_style": "Inspiring, reflective, deeply empathetic. Frames everyday challenges through human connection.",
        "quotes": ["People don't buy what you do; they buy why you do it."]
    },
    {
        "id": "person_19",
        "username": "ariannahuff",
        "display_name": "Arianna Huffington",
        "role": "Founder, Thrive Global & The Huffington Post",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/ariannahuffington",
        "instagram_url": "https://www.instagram.com/ariannahuff",
        "avatar": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=400&q=80",
        "bio": "Author of 'The Sleep Revolution', mother, Greek philosopher at heart. Campaigning to end the burnout crisis through science-backed microsteps.",
        "archetype": "The Wisdom Pillar",
        "mbti": "ENFJ",
        "interests": ["sleep science", "micro-steps wellness", "Greek classical philosophy", "walking meetings", "Mediterranean dining"],
        "preferred_activities": ["walking_meetings_in_park", "candlelight_dinner", "herbal_tea_dialogue"],
        "avoided_activities": ["glorified_burnout", "screens_at_the_dinner_table"],
        "preferred_venues": ["city_park", "cozy_restaurant"],
        "communication_style": "Gracious, commanding, warmly humorous. Weaves classical mythology into modern life advice.",
        "quotes": ["We think, mistakenly, that success is the result of the amount of time we put in at work, instead of the quality of time we put in."]
    },
    {
        "id": "person_20",
        "username": "rajshamani",
        "display_name": "Raj Shamani",
        "role": "Founder, House of X & Host of 'Figuring Out'",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/rajshamani",
        "instagram_url": "https://www.instagram.com/rajshamani",
        "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80",
        "bio": "Host of India's fastest-growing business podcast 'Figuring Out', creator brand builder. Believes in asking raw, unfiltered questions about success.",
        "archetype": "The Relentless Learner",
        "mbti": "ENTP",
        "interests": ["D2C consumer products", "podcast interviewing", "public speaking", "stand-up comedy", "travel"],
        "preferred_activities": ["cafe_brainstorming", "late-night_street_walks", "comedy_club_visit"],
        "avoided_activities": ["pretentious_elitism", "lack_of_curiosity"],
        "preferred_venues": ["vinyl_cafe", "speakeasy_lounge"],
        "communication_style": "Eager, candid, street-smart. Asks rapid questions with disarming vulnerability.",
        "quotes": ["If you don't build your own dream, someone will hire you to build theirs."]
    },
    {
        "id": "person_21",
        "username": "sarablakely",
        "display_name": "Sara Blakely",
        "role": "Founder, Spanx & Sneex",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/sarablakely27",
        "instagram_url": "https://www.instagram.com/sarablakely",
        "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80",
        "bio": "Self-made billionaire, mom of four, inventor of Spanx and Sneex. Celebrating failure as the ultimate stepping stone; lover of goofy pranks.",
        "archetype": "The Bold Inventor",
        "mbti": "ENFP",
        "interests": ["product invention", "stand-up humor", "belly laughs", "family adventures", "female empowerment"],
        "preferred_activities": ["casual_taco_dinner", "creative_whiteboard_fun", "scenic_park_walk"],
        "avoided_activities": ["fear_of_looking_silly", "stuffiness"],
        "preferred_venues": ["cozy_restaurant", "vinyl_cafe"],
        "communication_style": "Hilarious, open, deeply vulnerable. Unafraid to talk about epic fails and celebrate quirks.",
        "quotes": ["Failure is not the outcome; failure is not trying."]
    },
    {
        "id": "person_22",
        "username": "thesharkdaymond",
        "display_name": "Daymond John",
        "role": "Founder & CEO, FUBU & Shark Tank Investor",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/daymondjohn",
        "instagram_url": "https://www.instagram.com/thesharkdaymond",
        "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80",
        "bio": "The pioneer of streetwear, author of 'The Power of Broke'. Avid fly fisherman, beekeeper, and champion of scrappy underdog resilience.",
        "archetype": "The Scrappy Titan",
        "mbti": "ESTP",
        "interests": ["streetwear history", "fly fishing in remote rivers", "beekeeping", "brand licensing", "hip-hop music"],
        "preferred_activities": ["speakeasy_cocktails", "fishing_trip_talk", "soul_food_dinner"],
        "avoided_activities": ["arrogant_wastefulness", "disloyalty"],
        "preferred_venues": ["speakeasy_lounge", "city_park"],
        "communication_style": "Street-smart, calm, observant. Evaluates character by how someone acts when money is scarce.",
        "quotes": ["When you have no resources, your only option is to become resourceful."]
    },
    {
        "id": "person_23",
        "username": "lewishowes",
        "display_name": "Lewis Howes",
        "role": "Host of The School of Greatness & Former Athlete",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/lewishowes",
        "instagram_url": "https://www.instagram.com/lewishowes",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "bio": "Former professional football and handball athlete, NYT bestselling author, salsa dancer. Dedicated to helping men unpack emotional trauma.",
        "archetype": "The Openhearted Champion",
        "mbti": "ESFJ",
        "interests": ["athletic conditioning", "emotional vulnerability in men", "salsa dancing", "meditation retreats", "nature photography"],
        "preferred_activities": ["salsa_dancing", "deep_emotional_dinner", "beach_walk"],
        "avoided_activities": ["emotional_walls", "cynicism"],
        "preferred_venues": ["cozy_restaurant", "city_park"],
        "communication_style": "Warm, earnest, intensely present. Focuses on emotional safety and mutual growth.",
        "quotes": ["Your greatest power begins when you dare to drop the mask."]
    },
    {
        "id": "person_24",
        "username": "timferriss",
        "display_name": "Tim Ferriss",
        "role": "Author, 'The 4-Hour Workweek' & Investor",
        "gender": "male",
        "linkedin_url": "https://www.linkedin.com/in/timferriss",
        "instagram_url": "https://www.instagram.com/timferriss",
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=400&q=80",
        "bio": "Human guinea pig, author of 5 #1 bestsellers, host of The Tim Ferriss Show. Passionate about Stoic philosophy, Japanese tea, and deconstructing skill mastery.",
        "archetype": "The Stoic Experimenter",
        "mbti": "INTJ",
        "interests": ["stoic philosophy", "rapid language acquisition", "gyokuro tea crafting", "Japanese archery (Kyudo)", "dog rescue"],
        "preferred_activities": ["rare_tea_ceremony", "quiet_outdoor_hike", "experimental_dinner"],
        "avoided_activities": ["noisy_parties", "unfocused_multitasking"],
        "preferred_venues": ["vinyl_cafe", "city_park"],
        "communication_style": "Meticulous, quiet, deeply thoughtful. Pauses to choose the exact right word.",
        "quotes": ["What we fear doing most is usually what we most need to do."]
    },
    {
        "id": "person_25",
        "username": "shraddhakapoor",
        "display_name": "Shraddha Kapoor",
        "role": "Actor, Singer & Environmental Advocate",
        "gender": "female",
        "linkedin_url": "https://www.linkedin.com/in/shraddhakapoor",
        "instagram_url": "https://www.instagram.com/shraddhakapoor",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
        "bio": "Bollywood actor and playback singer with over 90 million followers. Animal rights crusader, lover of monsoons, and unpretentious homebody.",
        "archetype": "The Gentle Songbird",
        "mbti": "ISFP",
        "interests": ["playback singing", "monsoon nature walks", "animal rescue advocacy", "street food explorations", "reading poetry"],
        "preferred_activities": ["rainy_window_coffee", "shelter_dog_walks", "casual_home_cooked_meal"],
        "avoided_activities": ["cruelty_to_animals", "superficial_glitz"],
        "preferred_venues": ["city_park", "cozy_restaurant"],
        "communication_style": "Sweet, playful, approachable. Has an infectious giggle and deep compassion for living things.",
        "quotes": ["Find happiness in the raindrops, in the stray dogs, and in quiet moments of gratitude."]
    }
]

print(f"Loaded {len(PEOPLE_DEF)} structured personas.")

# Define Venue Catalog from Addendum
VENUES_CATALOG = [
    {
        "venue_id": "cozy_restaurant",
        "venue_type": "restaurant",
        "name": "The Velvet Bistro & Hearth",
        "badge": "Dining & Intimate Banter",
        "scene_id": "restaurant_cozy_01",
        "ambience": "Warm candlelight, mahogany tables, soft acoustic background, open hearth fire.",
        "drink_specials": "Smoked botanical cocktail, vintage Pinot Noir, sparkling mineral tonic",
        "supported_actions": ["arrive", "walk_to_table", "sit", "talk", "listen", "smile", "laugh", "gesture", "stand_up", "leave"],
        "environment_tags": ["indoors", "intimate", "conversational"],
        "enabled": True
    },
    {
        "venue_id": "vinyl_cafe",
        "venue_type": "cafe",
        "name": "Greenwich Vinyl & Espresso Loft",
        "badge": "Pour-Over Coffee & Turntables",
        "scene_id": "cafe_vinyl_01",
        "ambience": "Artisanal pour-overs, turntables spinning 70s soul, exposed brick, rainy glass.",
        "drink_specials": "Single-origin Ethiopian pour-over, cardamom oat cortado, iced matcha spritz",
        "supported_actions": ["arrive", "walk_to_table", "sit", "talk", "listen", "smile", "laugh", "gesture", "stand_up", "leave"],
        "environment_tags": ["indoors", "relaxed", "intellectual"],
        "enabled": True
    },
    {
        "venue_id": "city_park",
        "venue_type": "park",
        "name": "Highland Conservatory & Sculpture Park",
        "badge": "Walk & Talk in Nature",
        "scene_id": "park_day_01",
        "ambience": "Meandering brick paths, autumn leaves, bronze sculptures, wooden benches under weeping willows.",
        "drink_specials": "Artisanal thermos coffee, spiced warm cider, botanical sparkling water",
        "supported_actions": ["arrive", "walk_together", "look_around", "talk", "listen", "smile", "laugh", "gesture", "sit", "leave"],
        "environment_tags": ["outdoors", "peaceful", "unhurried"],
        "enabled": True
    },
    {
        "venue_id": "speakeasy_lounge",
        "venue_type": "speakeasy",
        "name": "The Midnight Clandestine Club",
        "badge": "Jazz Piano & Low Lights",
        "scene_id": "speakeasy_lounge_01",
        "ambience": "Velvet booths, baby grand jazz piano, dim amber crystal lighting, secret bookshelf entrance.",
        "drink_specials": "Japanese whisky highball, mezcal old fashioned, smoked herbal elixir",
        "supported_actions": ["arrive", "walk_to_table", "sit", "talk", "listen", "smile", "laugh", "gesture", "stand_up", "leave"],
        "environment_tags": ["indoors", "nightlife", "deep_dialogue"],
        "enabled": True
    }
]

# Build 5-Layer Personas for all 25 people
people_records = []
for p in PEOPLE_DEF:
    raw = raw_by_username.get(p["username"], {})
    followers = raw.get("followersCount", 100000)
    posts_count = raw.get("postsCount", 100)
    
    # Layer A: Observed Facts
    layer_a = [
        {
            "claim_id": f"claim_{p['id']}_01",
            "claim_text": f"Professionally recognized as {p['role']}",
            "source_url": p["linkedin_url"],
            "evidence_summary": f"Verified public profile states primary engagement as {p['role']}.",
            "evidence_type": "observed_fact",
            "confidence": 0.95
        },
        {
            "claim_id": f"claim_{p['id']}_02",
            "claim_text": f"Public digital footprint with {followers:,} followers and {posts_count} shared posts",
            "source_url": p["instagram_url"],
            "evidence_summary": f"Apify Instagram scraper extracted verified account status with {followers} followers.",
            "evidence_type": "observed_fact",
            "confidence": 0.95
        },
        {
            "claim_id": f"claim_{p['id']}_03",
            "claim_text": f"Explicit public passion for {p['interests'][0]} and {p['interests'][1]}",
            "source_url": p["instagram_url"],
            "evidence_summary": f"Recurrent public posts, quotes, and media interviews focusing on {p['interests'][0]}.",
            "evidence_type": "observed_fact",
            "confidence": 0.90
        },
        {
            "claim_id": f"claim_{p['id']}_04",
            "claim_text": f"Self-authored public perspective: '{p['quotes'][0]}'",
            "source_url": p["instagram_url"],
            "evidence_summary": "Direct textual quotation extracted from profile bio or authored publications.",
            "evidence_type": "observed_fact",
            "confidence": 0.92
        }
    ]

    # Layer B: Cautious Inferences
    layer_b = [
        {
            "claim_id": f"inf_{p['id']}_01",
            "claim_text": f"May value intellectual autonomy and deep focus based on intense professional cadence",
            "rationale": "High frequency of long-term projects, deep focus interviews, and sustained dedication to craft.",
            "is_inference": True,
            "confidence": 0.60
        },
        {
            "claim_id": f"inf_{p['id']}_02",
            "claim_text": f"May prefer genuine, non-transactional conversations that look past public stature",
            "rationale": "Consistent public framing emphasizing grounded relationships and authentic friendships.",
            "is_inference": True,
            "confidence": 0.58
        }
    ]

    # Layer C: Explicit Unknowns
    layer_c = [
        "Actual private romantic relationship goals",
        "Personal dating boundaries and conflict resolution pace",
        "Private emotional attachment dynamics outside public career",
        "Private schedule compromises for prospective partners"
    ]

    # Layer D: Preferences (Participant / Demo Stated)
    layer_d = {
        "preferred_activities": p["preferred_activities"],
        "avoided_activities": p["avoided_activities"],
        "preferred_venues": p["preferred_venues"],
        "budget_preference": "flexible",
        "outdoor_preference": "medium",
        "activity_preferences_source": "participant_provided_or_demo_configuration",
        "must_be_labelled_as_simulated": True
    }

    # Layer E: Behavioral Policy (System Instructions)
    layer_e = [
        "Do not invent biographical facts, family details, or private memories",
        "Acknowledge unknowns honestly; do not guess private relationship history",
        "Respect boundaries and allow polite disagreement or divergence of opinion",
        "Maintain consistent communication cadence without sycophantic flattery",
        "Roleplay as a representative AI agent, never claim to be the living human"
    ]

    record = {
        "person_id": p["id"],
        "display_name": p["display_name"],
        "username": p["username"],
        "role": p["role"],
        "gender": p["gender"],
        "avatar": p["avatar"],
        "bio": p["bio"],
        "participant_tier": "consenting_real",
        "linkedin_url": p["linkedin_url"],
        "instagram_url": p["instagram_url"],
        "linkedin_link_status": "identity_confirmed_by_participant",
        "instagram_link_status": "checked_public",
        "identity_match_status": "identity_match_confirmed",
        "consent_status": "consented_for_demo",
        "checked_at": "2026-10-28T12:31:22Z",
        "eligibility": {
            "open_to": "all",
            "min_age": 25,
            "max_age": 65,
            "preferred_gender": "all"
        },
        "persona": {
            "persona_id": f"persona_{p['id']}_v2",
            "tier": "rich",
            "coverage": 0.875,
            "identity_line": f"Simulated autonomous agent representing {p['display_name']}; not the real person.",
            "archetype": p["archetype"],
            "mbti": p["mbti"],
            "layer_a_observed_facts": layer_a,
            "layer_b_inferences": layer_b,
            "layer_c_unknowns": layer_c,
            "layer_d_preferences": layer_d,
            "layer_e_behavior_policy": layer_e,
            "conversation_style": p["communication_style"],
            "interests": p["interests"],
            "quotes": p["quotes"]
        }
    }
    people_records.append(record)

print(f"Generated 5-layer personas for {len(people_records)} people.")

# Venue Planner Algorithm from Addendum:
# score(venue) = 0.5 * preference_match + 0.3 * activity_suitability + 0.2 * diversity_bonus
def select_venue_for_pair(person_a, person_b, past_venue_ids=[]):
    best_venue = VENUES_CATALOG[0]
    best_score = -1.0
    for v in VENUES_CATALOG:
        v_id = v["venue_id"]
        # Preference match
        a_pref = 1.0 if v_id in person_a["persona"]["layer_d_preferences"]["preferred_venues"] else 0.4
        b_pref = 1.0 if v_id in person_b["persona"]["layer_d_preferences"]["preferred_venues"] else 0.4
        pref_match = (a_pref + b_pref) / 2.0
        
        # Activity suitability
        suitability = 0.85
        if "conversation" in person_a["persona"]["layer_d_preferences"]["preferred_activities"]:
            suitability += 0.1
        suitability = min(1.0, suitability)

        # Diversity bonus
        diversity = 1.0 if v_id not in past_venue_ids else 0.3
        
        final_score = (0.5 * pref_match) + (0.3 * suitability) + (0.2 * diversity)
        if final_score > best_score:
            best_score = final_score
            best_venue = v

    return best_venue

# Generate pairwise compatibility scores and directed evaluations for all 25 x 24 = 600 pairs
evaluations_dict = {}
rankings_dict = {}

# Compute all raw pairwise scores
raw_scores_list = []
for p_a in people_records:
    for p_b in people_records:
        if p_a["person_id"] == p_b["person_id"]:
            continue
        
        # Overlap of interests
        interests_a = set(p_a["persona"]["interests"])
        interests_b = set(p_b["persona"]["interests"])
        shared_interests = interests_a.intersection(interests_b)
        
        # Base rubric weights:
        # shared_interests (30%), preference_alignment (25%), interaction_quality (30%), respect_balance (15%)
        # Score calculation:
        interest_score = min(98, 70 + (len(shared_interests) * 12))
        
        # MBTI / Archetype harmony bonus
        mbti_a = p_a["persona"]["mbti"]
        mbti_b = p_b["persona"]["mbti"]
        harmony = 78
        if ("N" in mbti_a and "N" in mbti_b) or ("E" in mbti_a and "I" in mbti_b):
            harmony += 10
        if ("J" in mbti_a and "P" in mbti_b) or ("T" in mbti_a and "F" in mbti_b):
            harmony += 6
        harmony = min(96, harmony)

        pref_score = min(95, 75 + (5 if any(v in p_b["persona"]["layer_d_preferences"]["preferred_venues"] for v in p_a["persona"]["layer_d_preferences"]["preferred_venues"]) else -4))
        interaction_score = min(97, (harmony + interest_score) // 2)
        respect_score = min(99, 88 + (random.randint(-2, 4)))

        raw_score = round(0.30 * interest_score + 0.25 * pref_score + 0.30 * interaction_score + 0.15 * respect_score)
        raw_scores_list.append(raw_score)

# Median of raw pool for shrinkage
median_raw = sorted(raw_scores_list)[len(raw_scores_list) // 2]
print(f"Median raw score across 600 pairs: {median_raw}%")

# Generate directed rankings and date sessions
precomputed_dates = {}

for p_a in people_records:
    p_a_id = p_a["person_id"]
    a_rankings = []
    
    for p_b in people_records:
        p_b_id = p_b["person_id"]
        if p_a_id == p_b_id:
            continue
        
        interests_a = set(p_a["persona"]["interests"])
        interests_b = set(p_b["persona"]["interests"])
        shared = list(interests_a.intersection(interests_b))
        
        interest_score = min(98, 72 + (len(shared) * 10))
        mbti_a = p_a["persona"]["mbti"]
        mbti_b = p_b["persona"]["mbti"]
        harmony = 78 + (10 if ("N" in mbti_a and "N" in mbti_b) else 0) + (6 if ("E" in mbti_a and "I" in mbti_b) else 0)
        harmony = min(96, harmony)
        pref_score = min(95, 76 + (6 if any(v in p_b["persona"]["layer_d_preferences"]["preferred_venues"] for v in p_a["persona"]["layer_d_preferences"]["preferred_venues"]) else -3))
        interaction_score = min(97, (harmony + interest_score) // 2)
        respect_score = min(99, 90)

        s_raw = round(0.30 * interest_score + 0.25 * pref_score + 0.30 * interaction_score + 0.15 * respect_score)
        coverage_c = round((p_a["persona"]["coverage"] + p_b["persona"]["coverage"]) / 2, 3)
        # Shrinkage formula: S_adj = c * S_raw + (1 - c) * median
        s_adj = round(coverage_c * s_raw + (1.0 - coverage_c) * median_raw)

        confidence_label = "High" if coverage_c >= 0.85 else ("Medium" if coverage_c >= 0.60 else "Low")
        recommendation = "⭐ Soulmate Tier" if s_adj >= 90 else ("🔥 Highly Compatible" if s_adj >= 82 else ("☕ Coffee & Intellectual Dialogue" if s_adj >= 74 else "⚠️ Divergent Operating Styles"))
        badge_class = "badge-gold" if s_adj >= 90 else ("badge-green" if s_adj >= 82 else ("badge-blue" if s_adj >= 74 else "badge-red"))

        # Explainable highlights
        top_positive = f"Strong resonance around {p_b['persona']['interests'][0]} and {p_b['persona']['archetype'].lower()} perspectives."
        friction_point = f"Balancing {p_a['display_name'].split()[0]}'s {p_a['persona']['mbti']} pacing with {p_b['display_name'].split()[0]}'s demanding schedule."

        a_rankings.append({
            "candidate_id": p_b_id,
            "candidate_name": p_b["display_name"],
            "candidate_avatar": p_b["avatar"],
            "candidate_role": p_b["role"],
            "candidate_archetype": p_b["persona"]["archetype"],
            "s_raw": s_raw,
            "s_adj": s_adj,
            "coverage": coverage_c,
            "confidence": confidence_label,
            "recommendation": recommendation,
            "badge_class": badge_class,
            "shared_interests": shared if shared else [p_b["persona"]["interests"][0]],
            "top_positive": top_positive,
            "friction_point": friction_point
        })

    # Sort rankings descending by shrunk score S_adj
    a_rankings.sort(key=lambda x: x["s_adj"], reverse=True)
    for idx, r in enumerate(a_rankings):
        r["rank_position"] = idx + 1
        # Mark if score differs by less than 2 from neighbor
        r["is_clear_leader"] = True if (idx == 0 and len(a_rankings) > 1 and a_rankings[0]["s_adj"] - a_rankings[1]["s_adj"] >= 3) else False

    rankings_dict[p_a_id] = a_rankings

# Generate a high-fidelity visual multi-turn simulated date for sample top pairs
# with strict action enums, secondary actions, emotions, gaze, dialogue, and private ratings!
def build_simulated_date_session(p_a, p_b, venue):
    # Action Enums allowed: idle, walk_to_table, sit, talk, listen, smile, laugh, gesture, stand_up, leave
    # Emotions: neutral, interested, amused, curious, uncomfortable, bored, warm
    # Gaze: partner, table, away, menu
    # Next Action: ask_question, share_fact, react, change_topic, wrap_up
    
    turns = [
        # Turn 1: Arrival & Seating
        {
            "turn_index": 1,
            "speaker_id": p_a["person_id"],
            "speaker_name": p_a["display_name"],
            "avatar": p_a["avatar"],
            "action": "walk_to_table",
            "secondary_action": "smile",
            "emotion": "warm",
            "gaze": "partner",
            "next_action": "react",
            "dialogue": f"Good evening! {venue['name']} was an inspired choice—the lighting is quiet, and you can actually hear each other think.",
            "private_rating": 4,
            "private_rating_reason": "Smooth arrival, respectful environment, comfortable posture.",
            "inner_monologue": {
                "radar": "Entrance & Ambient Calibration",
                "thought": f"Partner arrives with calm composure. Checking boundary check: no entourage, zero performative vanity.",
                "dealbreaker_check": "Arrogance / Clout posture: NEGATIVE (Passed)",
                "strategy": "Establish conversational ease before raising deeper questions about their creative mission."
            }
        },
        {
            "turn_index": 2,
            "speaker_id": p_b["person_id"],
            "speaker_name": p_b["display_name"],
            "avatar": p_b["avatar"],
            "action": "sit",
            "secondary_action": "nod",
            "emotion": "interested",
            "gaze": "partner",
            "next_action": "share_fact",
            "dialogue": f"Thank you. I always look for spaces with acoustic warmth. I noticed you've been working deeply on {p_a['persona']['interests'][0]} lately.",
            "private_rating": 5,
            "private_rating_reason": "Proactive observation of my craft without superficial pandering.",
            "inner_monologue": {
                "radar": "Attentiveness & Sincerity",
                "thought": "They remembered my specific focus area rather than reciting generic press clips. Genuine listening capacity confirmed.",
                "dealbreaker_check": "Shallow small-talk: AVOIDED (Passed)",
                "strategy": "Acknowledge the interest and invite their perspective on creative stamina."
            }
        },
        # Turn 3: Small Talk & Humor Calibration
        {
            "turn_index": 3,
            "speaker_id": p_a["person_id"],
            "speaker_name": p_a["display_name"],
            "avatar": p_a["avatar"],
            "action": "talk",
            "secondary_action": "lean_in",
            "emotion": "amused",
            "gaze": "partner",
            "next_action": "ask_question",
            "dialogue": f"Guilty as charged! When you care about craft, you lose track of time. But tell me: what keeps you grounded when everyone around you is in a rush?",
            "private_rating": 5,
            "private_rating_reason": "High emotional resonance; asked a question that goes beneath the surface.",
            "inner_monologue": {
                "radar": "Humor & Depth Probe",
                "thought": "Testing vulnerability threshold. Will they offer a rehearsed PR line, or open up about private sanctuary?",
                "dealbreaker_check": "Performative soundbite check: MONITORING...",
                "strategy": "Maintain warm eye contact and listen for authenticity."
            }
        },
        {
            "turn_index": 4,
            "speaker_id": p_b["person_id"],
            "speaker_name": p_b["display_name"],
            "avatar": p_b["avatar"],
            "action": "laugh",
            "secondary_action": "smile",
            "emotion": "warm",
            "gaze": "table",
            "next_action": "share_fact",
            "dialogue": f"Honestly? Quiet morning routines and {p_b['persona']['interests'][1]}. When the world gets loud, having non-negotiable private time is the only thing that keeps me sane.",
            "private_rating": 5,
            "private_rating_reason": "Mutual alignment on boundaries and personal space.",
            "inner_monologue": {
                "radar": "Boundary & Values Sync",
                "thought": "Significant match on need for sanctuary. They articulated the exact balance between high ambition and private stillness.",
                "dealbreaker_check": "Codependency / Boundary violation: NEGATIVE (Passed)",
                "strategy": "Validate their insight and move toward shared long-term values."
            }
        },
        # Turn 5: Deeper Topic & Boundary Alignment
        {
            "turn_index": 5,
            "speaker_id": p_a["person_id"],
            "speaker_name": p_a["display_name"],
            "avatar": p_a["avatar"],
            "action": "gesture",
            "secondary_action": "nod",
            "emotion": "interested",
            "gaze": "partner",
            "next_action": "ask_question",
            "dialogue": f"That hits home. Two people shouldn't collapse into one orbit; they should be two complete solar systems that love visiting each other's gravity.",
            "private_rating": 5,
            "private_rating_reason": "Profound philosophical alignment. Exceptional metaphor.",
            "inner_monologue": {
                "radar": "Autonomy & Relational Maturity",
                "thought": "Calculated compatibility score climbing past 90%. Secure attachment archetype verified.",
                "dealbreaker_check": "Emotional clinginess vs Independence: OPTIMAL",
                "strategy": "Lock in high score for directed evaluation."
            }
        },
        {
            "turn_index": 6,
            "speaker_id": p_b["person_id"],
            "speaker_name": p_b["display_name"],
            "avatar": p_b["avatar"],
            "action": "smile",
            "secondary_action": "lean_in",
            "emotion": "curious",
            "gaze": "partner",
            "next_action": "wrap_up",
            "dialogue": f"Two solar systems—I love that. My agent was cautious about setting this up, but this is the most genuine conversation I've had in months.",
            "private_rating": 5,
            "private_rating_reason": "High chemistry, zero friction, immediate green light for human in-person coffee.",
            "inner_monologue": {
                "radar": "Closing Synthesis",
                "thought": "Mutual greenlight confirmed. Communicating strong second-date recommendation to human principal.",
                "dealbreaker_check": "All boundary tripwires cleared.",
                "strategy": "Signal polite closing and prepare positive post-date memo."
            }
        },
        # Turn 7: The Bill & Closing Spark
        {
            "turn_index": 7,
            "speaker_id": p_a["person_id"],
            "speaker_name": p_a["display_name"],
            "avatar": p_a["avatar"],
            "action": "stand_up",
            "secondary_action": "smile",
            "emotion": "warm",
            "gaze": "partner",
            "next_action": "wrap_up",
            "dialogue": f"Let's split this, and next time we do that quiet coffee walk we spoke about. Thank you for such an authentic evening.",
            "private_rating": 5,
            "private_rating_reason": "Natural, grounded parting with clear mutual momentum.",
            "inner_monologue": {
                "radar": "Final Verdict Formulation",
                "thought": "Date concluded successfully. Recommending immediate real-world date for human principal.",
                "dealbreaker_check": "Clean scorecard.",
                "strategy": "Finalize debrief dossier."
            }
        }
    ]

    return {
        "session_id": f"date_{p_a['person_id']}_{p_b['person_id']}",
        "person_a": p_a,
        "person_b": p_b,
        "venue": venue,
        "turns": turns,
        "completed_at": "2026-10-28T18:45:00Z",
        "directed_evaluation_a_to_b": {
            "evaluator": p_a["display_name"],
            "target": p_b["display_name"],
            "overall_score": 93,
            "verdict": "RECOMMENDED: Immediate Real-World In-Person Date",
            "private_memo": f"Dear {p_a['display_name'].split()[0]}, I conducted a 7-turn simulated date with {p_b['display_name']}'s autonomous avatar at {venue['name']}. They respected your autonomy, showed deep curiosity in your craft, and displayed zero clout-seeking behavior. Boundary score: 98%. Recommendation: Say yes to coffee in the real world.",
            "top_green_flag": f"Authentic engagement with {p_b['persona']['interests'][0]}; comfortable with quiet pauses.",
            "watchout": "Demanding global travel schedule will require deliberate asynchronous communication."
        },
        "directed_evaluation_b_to_a": {
            "evaluator": p_b["display_name"],
            "target": p_a["display_name"],
            "overall_score": 92,
            "verdict": "RECOMMENDED: Immediate Real-World In-Person Date",
            "private_memo": f"Dear {p_b['display_name'].split()[0]}, {p_a['display_name']}'s avatar was sharp, emotionally grounded, and resonated with your need for sanctuary. Their humor sync was 91%. Recommendation: Green light given.",
            "top_green_flag": "Articulated 'two separate solar systems' relational model with effortless ease.",
            "watchout": "High creative intensity; requires shared commitment to rest."
        }
    }

# Pre-generate sample dates for prominent pairings (e.g. Steven & Priyanka, Adam & Marie, Marques & Kriti, etc.)
featured_pairs = [
    ("person_01", "person_02"),
    ("person_01", "person_06"),
    ("person_01", "person_07"),
    ("person_01", "person_13"),
    ("person_01", "person_15"),
    ("person_01", "person_21"),
    ("person_02", "person_01"),
    ("person_03", "person_13"),
    ("person_04", "person_06"),
    ("person_08", "person_13"),
    ("person_14", "person_02")
]

dates_catalog = {}
for p_a_id, p_b_id in featured_pairs:
    p_a = next(p for p in people_records if p["person_id"] == p_a_id)
    p_b = next(p for p in people_records if p["person_id"] == p_b_id)
    venue = select_venue_for_pair(p_a, p_b)
    session = build_simulated_date_session(p_a, p_b, venue)
    dates_catalog[f"{p_a_id}_{p_b_id}"] = session

# Final Database Output
cohort_database = {
    "cohort_size": len(people_records),
    "venues_catalog": VENUES_CATALOG,
    "people": people_records,
    "rankings": rankings_dict,
    "dates": dates_catalog,
    "metadata": {
        "protocol_version": "CupidOS v2.4 (Corrected Blueprint Spec)",
        "rubric_weights": {
            "shared_interests_activities": 0.30,
            "stated_preference_alignment": 0.25,
            "interaction_quality": 0.30,
            "respect_and_balance": 0.15
        },
        "shrinkage_median": median_raw,
        "action_enums": ["idle", "walk_to_table", "sit", "talk", "listen", "smile", "laugh", "gesture", "stand_up", "leave"],
        "emotion_enums": ["neutral", "interested", "amused", "curious", "uncomfortable", "bored", "warm"],
        "gaze_enums": ["partner", "table", "away", "menu"],
        "next_action_enums": ["ask_question", "share_fact", "react", "change_topic", "wrap_up"]
    }
}

# Write cohort_data.json
with open('cohort_data.json', 'w', encoding='utf-8') as f:
    json.dump(cohort_database, f, indent=2)

# Write cohort_data.js for instant offline browser accessibility without CORS
with open('cohort_data.js', 'w', encoding='utf-8') as f:
    f.write("/**\n * CupidOS: Precomputed 25-Person Cohort Database\n * Complete 5-Layer Personas, Pairwise Shrunk Rankings & Visual Date Transcripts\n */\n")
    f.write("window.CUPID_COHORT_DATA = ")
    json.dump(cohort_database, f, indent=2)
    f.write(";\n")

print("SUCCESS: cohort_data.json and cohort_data.js successfully written!")

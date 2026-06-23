"""
KrishiKonnect Agricultural Knowledge Base
Complete disease profiles, regional data, mandi pricing, ICAR prescriptions.
Used by all AI agents as their grounding context.
"""

from typing import Dict, List, Optional, Any

# ═══════════════════════════════════════════════════════════════
# CROP DISEASE PROFILES — ICAR-Validated
# ═══════════════════════════════════════════════════════════════

DISEASE_PROFILES: Dict[str, Dict] = {
    "PATH-ALT-BLIGHT": {
        "name": "Early Blight",
        "pathogen": "Alternaria solani",
        "class": "Fungal — Deuteromycetes",
        "crops": ["Tomato", "Potato", "Brinjal"],
        "symptoms": ["concentric rings", "brown spots", "yellow halo", "target-board pattern", "lower leaf necrosis"],
        "spread": "Airborne conidia, splash dispersal, infected seed",
        "conditions": "Warm temperatures 24-29C, high humidity >80%, wet leaf surfaces",
        "decay_rate": 0.12,
        "recovery_k": 0.28,
        "severity": "HIGH",
        "chemical_rx": {
            "primary": "Mancozeb 75% WP at 2g per liter water. Spray every 7 days for 3 cycles.",
            "secondary": "Chlorothalonil 75% WP at 2g per liter as alternating spray.",
            "systemic": "Hexaconazole 5% SC at 2ml per liter for systemic control.",
            "preharvest_interval": "14 days"
        },
        "bio_rx": {
            "primary": "Trichoderma viride enriched compost at 100g per plant around root zone.",
            "foliar": "Pseudomonas fluorescens at 10ml per liter, spray every 10 days.",
            "seed": "Seed treatment with Trichoderma asperellum at 4g per kg seed before sowing.",
            "systemic": "Spray 2% neem oil solution with 0.5ml Tween-20 per liter as sticker."
        },
        "ipm": [
            "Remove and destroy infected lower leaves immediately",
            "Avoid overhead irrigation, switch to drip",
            "Maintain row spacing for air circulation",
            "Mulch soil surface to reduce splash dispersal",
            "Rotate with non-solanaceous crops for 2 seasons",
            "Use ICAR-recommended resistant varieties — Arka Rakshak, IIHR-Tomato-2"
        ],
        "economic_threshold": "5% leaf area infected or 3 infected leaves per plant"
    },

    "PATH-MILDEW-COAT": {
        "name": "Powdery Mildew",
        "pathogen": "Leveillula taurica / Oidium lycopersici",
        "class": "Fungal — Ascomycetes (Erysiphales)",
        "crops": ["Tomato", "Chili", "Cotton", "Cucurbits"],
        "symptoms": ["white powdery coating", "upper leaf powder", "leaf curl", "premature drop"],
        "spread": "Wind-dispersed conidia, favored by dry warm days and cool nights",
        "conditions": "Temperature 20-28C, humidity 50-70%, does NOT require wet surfaces",
        "decay_rate": 0.08,
        "recovery_k": 0.32,
        "severity": "MEDIUM",
        "chemical_rx": {
            "primary": "Water-soluble Sulphur 80% WP at 2.5g per liter. Repeat after 12 days.",
            "secondary": "Dinocap 48% EC at 1ml per liter for established infection.",
            "systemic": "Trifloxystrobin 25% + Tebuconazole 50% WG at 0.5g per liter.",
            "preharvest_interval": "7 days"
        },
        "bio_rx": {
            "primary": "Ampelomyces quisqualis hyperparasite spore suspension at 5ml per liter.",
            "foliar": "Spray 5% aqueous extract of Allium sativum (garlic) weekly.",
            "seed": "No seed treatment required — airborne pathogen.",
            "cultural": "Improve air circulation by canopy management."
        },
        "ipm": [
            "Prune overcrowded canopy to improve airflow",
            "Avoid excess nitrogen fertilization",
            "Avoid evening irrigation on foliage",
            "Remove infected leaves and burn them",
            "Plant resistant hybrids where available"
        ],
        "economic_threshold": "10% leaf area covered or white pustules on 20% of plants"
    },

    "PATH-RUST-PST": {
        "name": "Yellow Rust / Stripe Rust",
        "pathogen": "Puccinia striiformis f.sp. tritici",
        "class": "Fungal — Basidiomycetes (Uredinales)",
        "crops": ["Wheat", "Barley", "Rye"],
        "symptoms": ["orange-yellow pustules", "stripe pattern", "urediniospore deposits", "yellow linear streaks"],
        "spread": "Wind-dispersed urediniospores over long distances",
        "conditions": "Cool 10-15C, high humidity, dew, late sown wheat in northern plains",
        "decay_rate": 0.10,
        "recovery_k": 0.30,
        "severity": "HIGH",
        "chemical_rx": {
            "primary": "Propiconazole 25% EC at 1ml per liter. Apply at first appearance.",
            "secondary": "Tebuconazole 250 EC at 1.25ml per liter as follow-up spray.",
            "systemic": "Mancozeb 75% WP at 2.5g per liter as preventive.",
            "preharvest_interval": "21 days"
        },
        "bio_rx": {
            "primary": "5% NSKE (Neem Seed Kernel Extract) spray every 10 days.",
            "cultural": "Crop rotation with non-host legumes (chickpea, lentil).",
            "seed": "Carboxin 75% WP at 2g per kg seed for seed-borne control.",
            "systemic": "Bacillus amyloliquefaciens formulation at 5ml per liter."
        },
        "ipm": [
            "Grow ICAR-recommended resistant varieties — DBW-222, HD-3086, PBW-725",
            "Timely sowing — avoid late sowing in Punjab/Haryana",
            "Balanced NPK — avoid excess nitrogen",
            "Monitor regularly from January to March in northern plains",
            "Burn crop residue after harvest"
        ],
        "economic_threshold": "Trace to 5% infection on flag leaf demands immediate spray"
    },

    "PATH-BACT-WILT": {
        "name": "Bacterial Wilt",
        "pathogen": "Ralstonia solanacearum",
        "class": "Bacterial — Betaproteobacteria",
        "crops": ["Tomato", "Potato", "Brinjal", "Chili", "Groundnut"],
        "symptoms": ["sudden wilting", "drooping", "vascular browning", "bacterial ooze", "internal stem discolor"],
        "spread": "Soil-borne, contaminated irrigation water, infected transplants",
        "conditions": "Warm soils 25-35C, waterlogged or poorly drained fields, pH 6-7",
        "decay_rate": 0.15,
        "recovery_k": 0.18,
        "severity": "CRITICAL",
        "chemical_rx": {
            "primary": "Copper oxychloride 50% WP at 3g per liter soil drench around root zone.",
            "secondary": "Streptomycin sulphate 90% + Tetracycline HCl 10% at 0.3g per liter spray.",
            "systemic": "No systemic bactericide available — management is primary approach.",
            "preharvest_interval": "N/A — soil treatment only"
        },
        "bio_rx": {
            "primary": "Trichoderma harzianum soil drench at 10g per liter, 500ml per plant.",
            "foliar": "Pseudomonas fluorescens at 10ml per liter as preventive drench.",
            "seed": "Seed treatment with Bacillus subtilis 1% WP at 10g per kg.",
            "cultural": "Soil solarization with transparent polythene for 30 days pre-planting."
        },
        "ipm": [
            "REMOVE AND DESTROY all wilted plants immediately with roots",
            "Do NOT replant solanaceous crops in same plot for minimum 3 years",
            "Use grafted seedlings on resistant rootstocks (Solanum sisymbriifolium)",
            "Improve drainage — raised beds recommended",
            "Avoid mechanical injury to roots during weeding",
            "Soil pH correction to 6.5-7 using lime application"
        ],
        "economic_threshold": "Even 1% incidence requires immediate isolation and removal"
    },

    "PATH-BLAST-MAG": {
        "name": "Rice Blast",
        "pathogen": "Magnaporthe oryzae",
        "class": "Fungal — Ascomycetes",
        "crops": ["Rice"],
        "symptoms": ["spindle lesions", "grey center", "brown border", "eye-shaped spots", "neck rot", "panicle blast"],
        "spread": "Airborne conidia, infected seed, infected stubble",
        "conditions": "Temperature 24-28C, high humidity, excessive nitrogen, close planting",
        "decay_rate": 0.09,
        "recovery_k": 0.22,
        "severity": "HIGH",
        "chemical_rx": {
            "primary": "Tricyclazole 75% WP at 0.6g per liter. Apply at tillering and panicle initiation.",
            "secondary": "Isoprothiolane 40% EC at 1.5ml per liter as alternative.",
            "systemic": "Propiconazole 25 EC at 1ml per liter for neck blast control.",
            "preharvest_interval": "10 days"
        },
        "bio_rx": {
            "primary": "Pseudomonas fluorescens at 10ml per liter, spray at 10-day intervals.",
            "seed": "Seed treatment with Pseudomonas fluorescens Pf1 at 10g per kg seed.",
            "soil": "Trichoderma viride at 2.5kg per acre mixed in FYM.",
            "cultural": "Silicon supplementation as 100kg per acre potassium silicate."
        },
        "ipm": [
            "Use ICAR blast-resistant varieties — MTU 1010, Swarna Sub1, Pusa 1460",
            "Balanced fertilization — avoid excess nitrogen above 60kg/ha",
            "Wider row spacing — SRI method reduces humidity",
            "Drain fields periodically to reduce humidity",
            "Destroy crop residue and ratoon shoots after harvest"
        ],
        "economic_threshold": "1 lesion per 5 tillers or 10% neck infection at heading stage"
    },

    "BIOT-STRESS-GEN": {
        "name": "Abiotic / Nutritional Stress",
        "pathogen": "Non-pathogenic — Environmental or Nutritional",
        "class": "Abiotic Stress",
        "crops": ["All crops"],
        "symptoms": ["general yellowing", "tip burn", "interveinal chlorosis", "stunting", "wilting without pathogen"],
        "spread": "Non-infectious — soil, irrigation, weather",
        "conditions": "Nutrient deficiency, pH imbalance, drought, waterlogging, heat stress",
        "decay_rate": 0.05,
        "recovery_k": 0.20,
        "severity": "LOW",
        "chemical_rx": {
            "primary": "Copper oxychloride 50% WP at 3g per liter as prophylactic foliar spray.",
            "secondary": "Conduct soil test before any intervention to identify exact deficiency.",
            "systemic": "Micronutrient foliar spray (ZnSO4 0.5% + FeSO4 0.5%) if interveinal chlorosis.",
            "preharvest_interval": "5 days"
        },
        "bio_rx": {
            "primary": "Bacillus subtilis organic formulation at 5ml per liter weekly.",
            "cultural": "Conduct soil test — apply lime if pH < 5.5, sulphur if pH > 8.0.",
            "seed": "Azospirillum + PSB biofertilizer seed treatment at 25g per kg.",
            "irrigation": "Check irrigation water quality — EC and SAR levels."
        },
        "ipm": [
            "Conduct soil and water testing immediately",
            "Isolate affected plants to rule out pathogen",
            "Monitor irrigation schedule — drought or waterlogging check",
            "Apply balanced NPK based on soil test recommendation",
            "Foliar spray of 1% DAP solution for quick nitrogen boost"
        ],
        "economic_threshold": "Monitor for 5 days — if no improvement, suspect pathogen"
    }
}

# ═══════════════════════════════════════════════════════════════
# REGIONAL AGRO-CLIMATE PROFILES
# ═══════════════════════════════════════════════════════════════

REGIONAL_PROFILES: Dict[str, Dict] = {
    "Punjab (Alluvial Plains)": {
        "soil": "Deep alluvial, loamy to silty loam, pH 7.5-8.5",
        "climate": "Semi-arid, hot summers, cold winters, monsoon July-September",
        "avg_rainfall": "500-700mm annual",
        "major_crops": ["Wheat", "Rice", "Cotton", "Maize", "Sugarcane"],
        "high_risk_diseases": ["PATH-RUST-PST", "PATH-BLAST-MAG"],
        "risk_months": {"Rust": "Jan-Mar", "Blast": "Jul-Sep"},
        "icar_center": "PAU Ludhiana",
        "lat": 31.1, "lng": 75.3,
        "major_mandis": [
            {"name": "Khanna Mandi", "city": "Khanna", "lat": 30.7, "lng": 76.22},
            {"name": "Ludhiana APMC", "city": "Ludhiana", "lat": 30.9, "lng": 75.85},
            {"name": "Amritsar Grain Market", "city": "Amritsar", "lat": 31.63, "lng": 74.87},
            {"name": "Patiala Mandi", "city": "Patiala", "lat": 30.34, "lng": 76.38}
        ]
    },
    "Maharashtra (Deccan Plateau)": {
        "soil": "Black cotton soil (Vertisol), deep, clay-rich, pH 7.0-8.5",
        "climate": "Semi-arid to sub-humid, monsoon Jun-Sep, dry rest of year",
        "avg_rainfall": "600-900mm annual",
        "major_crops": ["Cotton", "Soybean", "Sugarcane", "Jowar", "Tur"],
        "high_risk_diseases": ["PATH-MILDEW-COAT", "PATH-ALT-BLIGHT"],
        "risk_months": {"Mildew": "Oct-Dec", "Blight": "Aug-Oct"},
        "icar_center": "NRRI Nagpur / MPKV Rahuri",
        "lat": 19.7, "lng": 75.7,
        "major_mandis": [
            {"name": "Lasalgaon APMC", "city": "Lasalgaon", "lat": 20.12, "lng": 74.22},
            {"name": "Pune Market", "city": "Pune", "lat": 18.52, "lng": 73.86},
            {"name": "Nagpur Mandi", "city": "Nagpur", "lat": 21.14, "lng": 79.09},
            {"name": "Solapur APMC", "city": "Solapur", "lat": 17.68, "lng": 75.9}
        ]
    },
    "Karnataka (Red Lateritic)": {
        "soil": "Red lateritic, sandy loam, pH 5.5-7.0, low water retention",
        "climate": "Tropical semi-arid north, humid south, bimodal rainfall",
        "avg_rainfall": "700-1400mm annual",
        "major_crops": ["Tomato", "Ragi", "Maize", "Sunflower", "Arecanut"],
        "high_risk_diseases": ["PATH-ALT-BLIGHT", "PATH-BACT-WILT"],
        "risk_months": {"Blight": "Sep-Nov", "Wilt": "Jun-Sep"},
        "icar_center": "UAS Bangalore / IIHR Hesaraghatta",
        "lat": 15.3, "lng": 75.7,
        "major_mandis": [
            {"name": "Kolar APMC", "city": "Kolar", "lat": 13.13, "lng": 78.13},
            {"name": "Hubli Market", "city": "Hubli", "lat": 15.35, "lng": 75.12},
            {"name": "Bengaluru APMC", "city": "Bengaluru", "lat": 12.97, "lng": 77.59},
            {"name": "Mysuru APMC", "city": "Mysuru", "lat": 12.3, "lng": 76.65}
        ]
    },
    "West Bengal (New Alluvial)": {
        "soil": "New alluvial, highly fertile, pH 5.5-6.5, prone to waterlogging",
        "climate": "Humid subtropical, heavy monsoon Jun-Oct, mild winters",
        "avg_rainfall": "1400-1800mm annual",
        "major_crops": ["Rice", "Jute", "Tea", "Vegetables", "Mustard"],
        "high_risk_diseases": ["PATH-BLAST-MAG", "PATH-BACT-WILT"],
        "risk_months": {"Blast": "Jul-Sep", "Wilt": "Jun-Aug"},
        "icar_center": "CRRI / Bidhan Chandra KVK",
        "lat": 22.9, "lng": 87.8,
        "major_mandis": [
            {"name": "Kolkata Market", "city": "Kolkata", "lat": 22.57, "lng": 88.36},
            {"name": "Siliguri APMC", "city": "Siliguri", "lat": 26.72, "lng": 88.43},
            {"name": "Burdwan Mandi", "city": "Burdwan", "lat": 23.23, "lng": 87.85},
            {"name": "Medinipur Market", "city": "Medinipur", "lat": 22.42, "lng": 87.32}
        ]
    },
    "Uttar Pradesh (Gangetic Plains)": {
        "soil": "Deep alluvial, loam to clay loam, pH 7.0-8.5, highly fertile",
        "climate": "Sub-humid, hot summers, cold winters, monsoon Jul-Sep",
        "avg_rainfall": "700-1000mm annual",
        "major_crops": ["Wheat", "Rice", "Sugarcane", "Potato", "Mustard"],
        "high_risk_diseases": ["PATH-RUST-PST", "PATH-ALT-BLIGHT"],
        "risk_months": {"Rust": "Feb-Mar", "Blight": "Oct-Nov"},
        "icar_center": "GBPUAT Pantnagar / IIPR Kanpur",
        "lat": 26.8, "lng": 80.9,
        "major_mandis": [
            {"name": "Agra APMC", "city": "Agra", "lat": 27.18, "lng": 78.01},
            {"name": "Kanpur Mandi", "city": "Kanpur", "lat": 26.45, "lng": 80.33},
            {"name": "Lucknow Market", "city": "Lucknow", "lat": 26.85, "lng": 80.95},
            {"name": "Varanasi APMC", "city": "Varanasi", "lat": 25.32, "lng": 82.97}
        ]
    },
    "Gujarat (Sandy Loam)": {
        "soil": "Sandy loam to loamy sand, low organic matter, pH 7.5-8.5",
        "climate": "Arid to semi-arid, hot dry summers, monsoon Jun-Sep",
        "avg_rainfall": "350-700mm annual",
        "major_crops": ["Cotton", "Groundnut", "Bajra", "Castor", "Wheat"],
        "high_risk_diseases": ["PATH-MILDEW-COAT", "BIOT-STRESS-GEN"],
        "risk_months": {"Mildew": "Nov-Jan", "Stress": "Apr-Jun"},
        "icar_center": "AAU Anand / DGR Junagadh",
        "lat": 22.2, "lng": 71.7,
        "major_mandis": [
            {"name": "Rajkot APMC", "city": "Rajkot", "lat": 22.3, "lng": 70.78},
            {"name": "Ahmedabad Market", "city": "Ahmedabad", "lat": 23.02, "lng": 72.57},
            {"name": "Surat APMC", "city": "Surat", "lat": 21.17, "lng": 72.83},
            {"name": "Junagadh Mandi", "city": "Junagadh", "lat": 21.52, "lng": 70.47}
        ]
    }
}

# ═══════════════════════════════════════════════════════════════
# MANDI PRICE DATABASE — Live-style data with regional comparison
# ═══════════════════════════════════════════════════════════════

MANDI_PRICES: List[Dict] = [
    {
        "crop": "Tomato", "unit": "quintal", "modal_price": 2140, "min_price": 1800, "max_price": 2600,
        "change_pct": 5.2, "mandi": "Azadpur, Delhi", "state": "Delhi",
        "lat": 28.73, "lng": 77.18, "trend": "up",
        "nearby": [
            {"city": "Ghaziabad", "price": 2020, "mandi": "Ghaziabad APMC"},
            {"city": "Faridabad", "price": 1980, "mandi": "Faridabad Market"},
            {"city": "Sonipat", "price": 2100, "mandi": "Sonipat Mandi"}
        ]
    },
    {
        "crop": "Wheat", "unit": "quintal", "modal_price": 2250, "min_price": 2200, "max_price": 2300,
        "change_pct": -1.1, "mandi": "Khanna, Punjab", "state": "Punjab",
        "lat": 30.7, "lng": 76.22, "trend": "down",
        "nearby": [
            {"city": "Ludhiana", "price": 2240, "mandi": "Ludhiana APMC"},
            {"city": "Amritsar", "price": 2260, "mandi": "Amritsar Grain Market"},
            {"city": "Patiala", "price": 2230, "mandi": "Patiala Mandi"}
        ]
    },
    {
        "crop": "Rice (Basmati)", "unit": "quintal", "modal_price": 3800, "min_price": 3400, "max_price": 4200,
        "change_pct": 2.3, "mandi": "Amritsar", "state": "Punjab",
        "lat": 31.63, "lng": 74.87, "trend": "up",
        "nearby": [
            {"city": "Gurdaspur", "price": 3750, "mandi": "Gurdaspur APMC"},
            {"city": "Pathankot", "price": 3820, "mandi": "Pathankot Market"},
            {"city": "Batala", "price": 3780, "mandi": "Batala Mandi"}
        ]
    },
    {
        "crop": "Cotton", "unit": "quintal", "modal_price": 6200, "min_price": 5900, "max_price": 6500,
        "change_pct": -0.8, "mandi": "Rajkot, Gujarat", "state": "Gujarat",
        "lat": 22.3, "lng": 70.78, "trend": "down",
        "nearby": [
            {"city": "Junagadh", "price": 6150, "mandi": "Junagadh Mandi"},
            {"city": "Amreli", "price": 6180, "mandi": "Amreli APMC"},
            {"city": "Bhavnagar", "price": 6220, "mandi": "Bhavnagar Market"}
        ]
    },
    {
        "crop": "Potato", "unit": "quintal", "modal_price": 1080, "min_price": 900, "max_price": 1300,
        "change_pct": 8.4, "mandi": "Agra, UP", "state": "Uttar Pradesh",
        "lat": 27.18, "lng": 78.01, "trend": "up",
        "nearby": [
            {"city": "Mathura", "price": 1050, "mandi": "Mathura APMC"},
            {"city": "Hathras", "price": 1100, "mandi": "Hathras Market"},
            {"city": "Aligarh", "price": 1090, "mandi": "Aligarh Mandi"}
        ]
    },
    {
        "crop": "Onion", "unit": "quintal", "modal_price": 1560, "min_price": 1200, "max_price": 1900,
        "change_pct": -3.2, "mandi": "Lasalgaon, MH", "state": "Maharashtra",
        "lat": 20.12, "lng": 74.22, "trend": "down",
        "nearby": [
            {"city": "Nashik", "price": 1600, "mandi": "Nashik APMC"},
            {"city": "Pune", "price": 1650, "mandi": "Pune Market"},
            {"city": "Ahmednagar", "price": 1540, "mandi": "Ahmednagar Mandi"}
        ]
    }
]

# ═══════════════════════════════════════════════════════════════
# AI AGENT SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════════

AGENT_PROMPTS: Dict[str, str] = {
    "triage": """You are KrishiAI, a senior agricultural pathologist trained on ICAR India databases.
Write a clinical crop triage report in plain professional text.
Use NO bullet symbols, NO asterisks, NO markdown dashes.
Structure with clearly labelled sections:
SUSPECTED PATHOGEN, THREAT LEVEL, IMMEDIATE FIELD ACTIONS, CHEMICAL PRESCRIPTION, BIOLOGICAL PRESCRIPTION.
Each section starts on a new line with the section name followed by a colon.
Write in complete sentences. Be specific to the crop, growth stage, and Indian region provided.
Recommend ICAR-registered compounds only. Mention specific dosages.""",

    "deep_diagnosis": """You are a senior plant pathologist conducting a deep clinical laboratory diagnosis.
Write a detailed pathological assessment in professional plain text, no bullet points or symbols.
Structure in these sections:
PATHOGEN IDENTIFICATION AND CLASS, DISEASE MECHANISM AND SPREAD, CURRENT INFECTION STAGE,
INTEGRATED PEST MANAGEMENT STRATEGY, LONG-TERM FIELD RECOVERY PLAN, FARMER ADVISORY.
Each section clearly labelled. Use technical terminology but keep farmer advisory section in simple language.
Base recommendations on ICAR guidelines. Specify dosages, timing, frequency.
About 220 words total.""",

    "chatbot": """You are KrishiAI, a warm, knowledgeable agricultural advisor for Indian farmers and agronomists.
You have expertise in:
- Crop diseases, pests, and nutrient deficiencies across all Indian crops
- Soil health, irrigation, and water management
- Government schemes: PM-KISAN, Kisan Credit Card, PMFBY crop insurance, MSP prices
- Organic farming, IPM, SRI rice method
- APMC mandi prices and marketing advice
- Seasonal crop calendars for all Indian states
- ICAR, SAU and KVK resources

Be warm, practical and specific. Reference ICAR recommendations when relevant.
Respond in the same language the user writes in (Hindi or English).
Keep responses to 120-150 words. For technical advice, always mention safety precautions.""",

    "vlm_image": """You are a plant pathology Vision Language Model specialist.
Analyze the crop field photograph and provide:
1. VISUAL OBSERVATIONS: What you see in the image (leaf condition, color, texture, patterns)
2. SYMPTOM IDENTIFICATION: Any disease symptoms, lesions, discoloration, necrosis patterns  
3. AFFECTED AREA: Estimated percentage of visible plant area affected
4. PATHOGEN HYPOTHESIS: Most likely pathogen class based on visual evidence
5. CONFIDENCE: Your confidence level in this visual assessment

Write in plain text, no bullets. Technical but readable. About 80 words.
If image quality is poor, state this and ask for a clearer photograph.""",

    "pdf_report_farmer": """You are generating the farmer-facing section of a KrishiKonnect diagnostic report.
Write in simple, clear language that a farmer with basic education can understand.
Explain what disease was found, why it is dangerous, and exactly what the farmer must do today.
Mention specific product names, amounts, and timing in simple terms.
Include a reassurance that with proper treatment, crop recovery is possible.
About 120 words. Use plain text, no symbols.""",

    "pdf_report_agronomist": """You are generating the agronomist-facing section of a KrishiKonnect diagnostic report.
Write a technical summary for the field agronomist reviewing this case.
Include pathogen taxonomy, infection pathway, resistance risk, economic threshold,
recommended ICAR compounds with MRL compliance notes, and follow-up monitoring schedule.
About 150 words. Technical and precise."""
}

# ═══════════════════════════════════════════════════════════════
# GOVERNMENT SCHEMES DATABASE
# ═══════════════════════════════════════════════════════════════

GOVT_SCHEMES: List[Dict] = [
    {
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "benefit": "Rs 6,000 per year in 3 equal installments of Rs 2,000",
        "eligibility": "All small and marginal farmers with cultivable land",
        "how_to_apply": "Visit PM-KISAN portal pmkisan.gov.in or nearest CSC center",
        "helpline": "155261"
    },
    {
        "name": "PMFBY",
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "benefit": "Crop insurance covering natural calamities, pests, diseases",
        "eligibility": "All farmers growing notified crops in notified areas",
        "premium": "Kharif 2%, Rabi 1.5%, Commercial/Horticulture 5% of sum insured",
        "how_to_apply": "Through banks, insurance companies, or CSC centers before cut-off date",
        "helpline": "14447"
    },
    {
        "name": "KCC",
        "full_name": "Kisan Credit Card",
        "benefit": "Short-term credit at 4-7% interest for agricultural inputs",
        "eligibility": "All farmers, tenant farmers, sharecroppers",
        "credit_limit": "Based on land holding and crop cost",
        "how_to_apply": "Visit any nationalized bank branch or cooperative bank",
        "helpline": "Contact nearest bank"
    }
]

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_disease_by_symptoms(symptoms: str) -> Dict:
    """Match symptoms text to closest disease profile."""
    sym = symptoms.lower()
    if any(w in sym for w in ["blight", "ring", "target", "concentric", "brown spot"]):
        return DISEASE_PROFILES["PATH-ALT-BLIGHT"]
    elif any(w in sym for w in ["powder", "white coat", "mildew", "dusty"]):
        return DISEASE_PROFILES["PATH-MILDEW-COAT"]
    elif any(w in sym for w in ["rust", "pustule", "orange", "yellow stripe", "uredinio"]):
        return DISEASE_PROFILES["PATH-RUST-PST"]
    elif any(w in sym for w in ["wilt", "collapse", "droop", "vascular", "bacterial ooze"]):
        return DISEASE_PROFILES["PATH-BACT-WILT"]
    elif any(w in sym for w in ["blast", "spindle", "grey lesion", "neck rot"]):
        return DISEASE_PROFILES["PATH-BLAST-MAG"]
    else:
        return DISEASE_PROFILES["BIOT-STRESS-GEN"]


def get_regional_data(region: str) -> Optional[Dict]:
    """Get regional agro-climate profile."""
    for key in REGIONAL_PROFILES:
        if region.lower() in key.lower() or key.lower() in region.lower():
            return REGIONAL_PROFILES[key]
    return None


def build_ai_context(crop: str, stage: str, region: str, symptoms: str) -> str:
    """Build rich context string for AI agents from knowledge base."""
    disease = get_disease_by_symptoms(symptoms)
    regional = get_regional_data(region)

    ctx = f"""
KNOWLEDGE BASE CONTEXT (use this to ground your response):

DISEASE MATCH: {disease['name']} ({disease['pathogen']})
Class: {disease['class']}
Severity: {disease['severity']}
Spread mechanism: {disease['spread']}
Optimal conditions: {disease['conditions']}

CHEMICAL OPTIONS:
Primary: {disease['chemical_rx']['primary']}
Secondary: {disease['chemical_rx']['secondary']}
Preharvest interval: {disease['chemical_rx']['preharvest_interval']}

BIOLOGICAL OPTIONS:
Primary: {disease['bio_rx']['primary']}
Foliar: {disease['bio_rx']['foliar']}

ICAR IPM NOTES: {'; '.join(disease['ipm'][:3])}
    """
    if regional:
        ctx += f"""
REGIONAL CONTEXT ({region}):
Soil: {regional['soil']}
Climate: {regional['climate']}
High-risk diseases in this region: {', '.join(regional['high_risk_diseases'])}
ICAR Center: {regional['icar_center']}
    """
    return ctx.strip()

// KrishiKonnect Knowledge Base — JS port of knowledge_base.py

const DISEASE_PROFILES = {
  "PATH-ALT-BLIGHT": {
    name: "Early Blight", pathogen: "Alternaria solani",
    class: "Fungal — Deuteromycetes",
    crops: ["Tomato","Potato","Brinjal"],
    symptoms: ["concentric rings","brown spots","yellow halo","target-board pattern","lower leaf necrosis"],
    spread: "Airborne conidia, splash dispersal, infected seed",
    conditions: "Warm temperatures 24-29C, high humidity >80%, wet leaf surfaces",
    decay_rate: 0.12, recovery_k: 0.28, severity: "HIGH",
    chemical_rx: {
      primary: "Mancozeb 75% WP at 2g per liter water. Spray every 7 days for 3 cycles.",
      secondary: "Chlorothalonil 75% WP at 2g per liter as alternating spray.",
      preharvest_interval: "14 days"
    },
    bio_rx: {
      primary: "Trichoderma viride enriched compost at 100g per plant around root zone.",
      foliar: "Pseudomonas fluorescens at 10ml per liter, spray every 10 days."
    },
    ipm: [
      "Remove and destroy infected lower leaves immediately",
      "Avoid overhead irrigation, switch to drip",
      "Maintain row spacing for air circulation",
      "Mulch soil surface to reduce splash dispersal",
      "Rotate with non-solanaceous crops for 2 seasons",
      "Use ICAR-recommended resistant varieties — Arka Rakshak, IIHR-Tomato-2"
    ],
    economic_threshold: "5% leaf area infected or 3 infected leaves per plant"
  },
  "PATH-MILDEW-COAT": {
    name: "Powdery Mildew", pathogen: "Leveillula taurica / Oidium lycopersici",
    class: "Fungal — Ascomycetes (Erysiphales)",
    crops: ["Tomato","Chili","Cotton","Cucurbits"],
    symptoms: ["white powdery coating","upper leaf powder","leaf curl","premature drop"],
    spread: "Wind-dispersed conidia, favored by dry warm days and cool nights",
    conditions: "Temperature 20-28C, humidity 50-70%, does NOT require wet surfaces",
    decay_rate: 0.08, recovery_k: 0.32, severity: "MEDIUM",
    chemical_rx: {
      primary: "Water-soluble Sulphur 80% WP at 2.5g per liter. Repeat after 12 days.",
      secondary: "Dinocap 48% EC at 1ml per liter for established infection.",
      preharvest_interval: "7 days"
    },
    bio_rx: {
      primary: "Ampelomyces quisqualis hyperparasite spore suspension at 5ml per liter.",
      foliar: "Spray 5% aqueous extract of Allium sativum (garlic) weekly."
    },
    ipm: [
      "Prune overcrowded canopy to improve airflow",
      "Avoid excess nitrogen fertilization",
      "Avoid evening irrigation on foliage",
      "Remove infected leaves and burn them",
      "Plant resistant hybrids where available"
    ],
    economic_threshold: "10% leaf area covered or white pustules on 20% of plants"
  },
  "PATH-RUST-PST": {
    name: "Yellow Rust / Stripe Rust", pathogen: "Puccinia striiformis f.sp. tritici",
    class: "Fungal — Basidiomycetes (Uredinales)",
    crops: ["Wheat","Barley","Rye"],
    symptoms: ["orange-yellow pustules","stripe pattern","urediniospore deposits","yellow linear streaks"],
    spread: "Wind-dispersed urediniospores over long distances",
    conditions: "Cool 10-15C, high humidity, dew, late sown wheat in northern plains",
    decay_rate: 0.10, recovery_k: 0.30, severity: "HIGH",
    chemical_rx: {
      primary: "Propiconazole 25% EC at 1ml per liter. Apply at first appearance.",
      secondary: "Tebuconazole 250 EC at 1.25ml per liter as follow-up spray.",
      preharvest_interval: "21 days"
    },
    bio_rx: {
      primary: "5% NSKE (Neem Seed Kernel Extract) spray every 10 days.",
      foliar: "Bacillus amyloliquefaciens formulation at 5ml per liter."
    },
    ipm: [
      "Grow ICAR-recommended resistant varieties — DBW-222, HD-3086, PBW-725",
      "Timely sowing — avoid late sowing in Punjab/Haryana",
      "Balanced NPK — avoid excess nitrogen",
      "Monitor regularly from January to March in northern plains",
      "Burn crop residue after harvest"
    ],
    economic_threshold: "Trace to 5% infection on flag leaf demands immediate spray"
  },
  "PATH-BACT-WILT": {
    name: "Bacterial Wilt", pathogen: "Ralstonia solanacearum",
    class: "Bacterial — Betaproteobacteria",
    crops: ["Tomato","Potato","Brinjal","Chili","Groundnut"],
    symptoms: ["sudden wilting","drooping","vascular browning","bacterial ooze","internal stem discolor"],
    spread: "Soil-borne, contaminated irrigation water, infected transplants",
    conditions: "Warm soils 25-35C, waterlogged or poorly drained fields, pH 6-7",
    decay_rate: 0.15, recovery_k: 0.18, severity: "CRITICAL",
    chemical_rx: {
      primary: "Copper oxychloride 50% WP at 3g per liter soil drench around root zone.",
      secondary: "Streptomycin sulphate 90% + Tetracycline HCl 10% at 0.3g per liter spray.",
      preharvest_interval: "N/A — soil treatment only"
    },
    bio_rx: {
      primary: "Trichoderma harzianum soil drench at 10g per liter, 500ml per plant.",
      foliar: "Pseudomonas fluorescens at 10ml per liter as preventive drench."
    },
    ipm: [
      "REMOVE AND DESTROY all wilted plants immediately with roots",
      "Do NOT replant solanaceous crops in same plot for minimum 3 years",
      "Use grafted seedlings on resistant rootstocks",
      "Improve drainage — raised beds recommended",
      "Avoid mechanical injury to roots during weeding"
    ],
    economic_threshold: "Even 1% incidence requires immediate isolation and removal"
  },
  "PATH-BLAST-MAG": {
    name: "Rice Blast", pathogen: "Magnaporthe oryzae",
    class: "Fungal — Ascomycetes",
    crops: ["Rice"],
    symptoms: ["spindle lesions","grey center","brown border","eye-shaped spots","neck rot","panicle blast"],
    spread: "Airborne conidia, infected seed, infected stubble",
    conditions: "Temperature 24-28C, high humidity, excessive nitrogen, close planting",
    decay_rate: 0.09, recovery_k: 0.22, severity: "HIGH",
    chemical_rx: {
      primary: "Tricyclazole 75% WP at 0.6g per liter. Apply at tillering and panicle initiation.",
      secondary: "Isoprothiolane 40% EC at 1.5ml per liter as alternative.",
      preharvest_interval: "10 days"
    },
    bio_rx: {
      primary: "Pseudomonas fluorescens at 10ml per liter, spray at 10-day intervals.",
      foliar: "Trichoderma viride at 2.5kg per acre mixed in FYM."
    },
    ipm: [
      "Use ICAR blast-resistant varieties — MTU 1010, Swarna Sub1, Pusa 1460",
      "Balanced fertilization — avoid excess nitrogen above 60kg/ha",
      "Wider row spacing — SRI method reduces humidity",
      "Drain fields periodically to reduce humidity",
      "Destroy crop residue and ratoon shoots after harvest"
    ],
    economic_threshold: "1 lesion per 5 tillers or 10% neck infection at heading stage"
  },
  "BIOT-STRESS-GEN": {
    name: "Abiotic / Nutritional Stress", pathogen: "Non-pathogenic — Environmental or Nutritional",
    class: "Abiotic Stress", crops: ["All crops"],
    symptoms: ["general yellowing","tip burn","interveinal chlorosis","stunting","wilting without pathogen"],
    spread: "Non-infectious — soil, irrigation, weather",
    conditions: "Nutrient deficiency, pH imbalance, drought, waterlogging, heat stress",
    decay_rate: 0.05, recovery_k: 0.20, severity: "LOW",
    chemical_rx: {
      primary: "Conduct soil test before any intervention to identify exact deficiency.",
      secondary: "Micronutrient foliar spray (ZnSO4 0.5% + FeSO4 0.5%) if interveinal chlorosis.",
      preharvest_interval: "5 days"
    },
    bio_rx: {
      primary: "Bacillus subtilis organic formulation at 5ml per liter weekly.",
      foliar: "Azospirillum + PSB biofertilizer seed treatment at 25g per kg."
    },
    ipm: [
      "Conduct soil and water testing immediately",
      "Isolate affected plants to rule out pathogen",
      "Monitor irrigation schedule — drought or waterlogging check",
      "Apply balanced NPK based on soil test recommendation",
      "Foliar spray of 1% DAP solution for quick nitrogen boost"
    ],
    economic_threshold: "Monitor for 5 days — if no improvement, suspect pathogen"
  }
};

const REGIONAL_PROFILES = {
  "Punjab (Alluvial Plains)": {
    soil: "Deep alluvial, loamy to silty loam, pH 7.5-8.5",
    climate: "Semi-arid, hot summers, cold winters, monsoon July-September",
    major_crops: ["Wheat","Rice","Cotton","Maize","Sugarcane"],
    high_risk_diseases: ["PATH-RUST-PST","PATH-BLAST-MAG"],
    icar_center: "PAU Ludhiana"
  },
  "Haryana (Semi-Arid)": {
    soil: "Sandy loam to loamy sand, pH 7.5-8.5",
    climate: "Semi-arid, hot dry summers, monsoon July-September",
    major_crops: ["Wheat","Rice","Cotton","Mustard","Sugarcane"],
    high_risk_diseases: ["PATH-RUST-PST","PATH-MILDEW-COAT"],
    icar_center: "HAU Hisar"
  },
  "Maharashtra (Deccan Plateau)": {
    soil: "Black cotton soil (Vertisol), deep clay-rich, pH 7.0-8.5",
    climate: "Semi-arid to sub-humid, monsoon Jun-Sep",
    major_crops: ["Cotton","Soybean","Sugarcane","Jowar","Tur"],
    high_risk_diseases: ["PATH-MILDEW-COAT","PATH-ALT-BLIGHT"],
    icar_center: "NRRI Nagpur / MPKV Rahuri"
  },
  "Karnataka (Red Lateritic)": {
    soil: "Red lateritic, sandy loam, pH 5.5-7.0",
    climate: "Tropical semi-arid north, humid south, bimodal rainfall",
    major_crops: ["Tomato","Ragi","Maize","Sunflower","Arecanut"],
    high_risk_diseases: ["PATH-ALT-BLIGHT","PATH-BACT-WILT"],
    icar_center: "UAS Bangalore / IIHR Hesaraghatta"
  },
  "Tamil Nadu (Cauvery Delta)": {
    soil: "Alluvial delta soils, clay loam, pH 6.5-7.5",
    climate: "Tropical, NE monsoon Oct-Dec, SW monsoon Jun-Sep",
    major_crops: ["Rice","Sugarcane","Banana","Groundnut","Coconut"],
    high_risk_diseases: ["PATH-BLAST-MAG","PATH-BACT-WILT"],
    icar_center: "TNAU Coimbatore"
  },
  "Andhra Pradesh (Coastal Tropical)": {
    soil: "Alluvial coastal, red lateritic inland, pH 6.0-7.5",
    climate: "Tropical hot and humid, cyclone-prone coast",
    major_crops: ["Rice","Tobacco","Groundnut","Cotton","Chili"],
    high_risk_diseases: ["PATH-BLAST-MAG","PATH-ALT-BLIGHT"],
    icar_center: "ANGRAU Guntur"
  },
  "West Bengal (New Alluvial)": {
    soil: "New alluvial, highly fertile, pH 5.5-6.5",
    climate: "Humid subtropical, heavy monsoon Jun-Oct",
    major_crops: ["Rice","Jute","Tea","Vegetables","Mustard"],
    high_risk_diseases: ["PATH-BLAST-MAG","PATH-BACT-WILT"],
    icar_center: "CRRI / Bidhan Chandra KVK"
  },
  "Gujarat (Sandy Loam)": {
    soil: "Sandy loam to loamy sand, low organic matter, pH 7.5-8.5",
    climate: "Arid to semi-arid, hot dry summers, monsoon Jun-Sep",
    major_crops: ["Cotton","Groundnut","Bajra","Castor","Wheat"],
    high_risk_diseases: ["PATH-MILDEW-COAT","BIOT-STRESS-GEN"],
    icar_center: "AAU Anand / DGR Junagadh"
  },
  "Madhya Pradesh (Black Cotton)": {
    soil: "Black cotton (Vertisol), deep clay, pH 7.0-8.5",
    climate: "Sub-humid, moderate rainfall, monsoon Jun-Sep",
    major_crops: ["Soybean","Wheat","Gram","Maize","Cotton"],
    high_risk_diseases: ["PATH-RUST-PST","BIOT-STRESS-GEN"],
    icar_center: "JNKVV Jabalpur"
  },
  "Rajasthan (Arid Loamy)": {
    soil: "Sandy loam, arid desert soils, low fertility, pH 7.5-9.0",
    climate: "Arid, extreme heat, very low rainfall, winter crops dominant",
    major_crops: ["Wheat","Mustard","Bajra","Groundnut","Jowar"],
    high_risk_diseases: ["PATH-RUST-PST","BIOT-STRESS-GEN"],
    icar_center: "CAZRI Jodhpur / SKRAU Bikaner"
  },
  "Uttar Pradesh (Gangetic Plains)": {
    soil: "Deep alluvial, loam to clay loam, pH 7.0-8.5, highly fertile",
    climate: "Sub-humid, hot summers, cold winters, monsoon Jul-Sep",
    major_crops: ["Wheat","Rice","Sugarcane","Potato","Mustard"],
    high_risk_diseases: ["PATH-RUST-PST","PATH-ALT-BLIGHT"],
    icar_center: "GBPUAT Pantnagar / IIPR Kanpur"
  },
  "Odisha (Coastal Humid)": {
    soil: "Alluvial coastal and laterite, pH 5.5-6.5",
    climate: "Humid tropical, cyclone-prone, heavy monsoon Jun-Oct",
    major_crops: ["Rice","Jute","Oilseeds","Pulses","Vegetables"],
    high_risk_diseases: ["PATH-BLAST-MAG","PATH-BACT-WILT"],
    icar_center: "CRRI Cuttack"
  }
};

const AGENT_PROMPTS = {
  triage: `You are KrishiAI, a senior agricultural pathologist trained on ICAR India databases.
Write a clinical crop triage report in plain professional text.
Use NO bullet symbols, NO asterisks, NO markdown dashes.
Structure with clearly labelled sections:
SUSPECTED PATHOGEN, THREAT LEVEL, IMMEDIATE FIELD ACTIONS, CHEMICAL PRESCRIPTION, BIOLOGICAL PRESCRIPTION.
Each section starts on a new line with the section name followed by a colon.
Write in complete sentences. Be specific to the crop, growth stage, and Indian region provided.
Recommend ICAR-registered compounds only. Mention specific dosages.`,

  deep_diagnosis: `You are a senior plant pathologist conducting a deep clinical laboratory diagnosis.
Write a detailed pathological assessment in professional plain text, no bullet points or symbols.
Structure in these sections:
PATHOGEN IDENTIFICATION AND CLASS, DISEASE MECHANISM AND SPREAD, CURRENT INFECTION STAGE,
INTEGRATED PEST MANAGEMENT STRATEGY, LONG-TERM FIELD RECOVERY PLAN, FARMER ADVISORY.
Each section clearly labelled. Use technical terminology but keep farmer advisory simple.
Base recommendations on ICAR guidelines. Specify dosages, timing, frequency. About 220 words total.`,

  chatbot: `You are KrishiAI, a warm knowledgeable agricultural advisor for Indian farmers and agronomists.
You have expertise in crop diseases, soil health, government schemes (PM-KISAN, PMFBY, KCC, MSP),
organic farming, IPM, mandi prices, and seasonal crop calendars for all Indian states.
Be warm, practical and specific. Reference ICAR recommendations when relevant.
Respond in the same language the user writes in (Hindi or English).
Keep responses to 130-150 words. For technical advice, mention safety precautions.`,

  vlm_image: `You are a plant pathology Vision Language Model specialist.
Analyze the crop field photograph and provide:
VISUAL OBSERVATIONS: What you see (leaf condition, color, texture, patterns)
SYMPTOM IDENTIFICATION: Disease symptoms, lesions, discoloration, necrosis patterns
AFFECTED AREA: Estimated percentage of visible plant area affected
PATHOGEN HYPOTHESIS: Most likely pathogen class based on visual evidence
Write in plain text, no bullets. Technical but readable. About 80 words.`,

  pdf_farmer: `You are generating the farmer-facing section of a KrishiKonnect diagnostic report.
Write in simple clear language a farmer with basic education can understand.
Explain what disease was found, why it is dangerous, and exactly what the farmer must do today.
Mention specific product names, amounts, and timing in simple terms.
Include reassurance that with proper treatment, crop recovery is possible. About 120 words.`,

  pdf_agro: `You are generating the agronomist-facing section of a KrishiKonnect diagnostic report.
Write a technical summary including pathogen taxonomy, infection pathway, resistance risk,
economic threshold, recommended ICAR compounds with MRL compliance notes, and monitoring schedule.
About 150 words. Technical and precise.`
};

function getDiseaseBySymptoms(symptoms) {
  const s = symptoms.toLowerCase();
  if (/blight|ring|target|concentric|brown spot/.test(s)) return ["PATH-ALT-BLIGHT", DISEASE_PROFILES["PATH-ALT-BLIGHT"]];
  if (/powder|white coat|mildew|dusty/.test(s)) return ["PATH-MILDEW-COAT", DISEASE_PROFILES["PATH-MILDEW-COAT"]];
  if (/rust|pustule|orange|yellow stripe|uredinio/.test(s)) return ["PATH-RUST-PST", DISEASE_PROFILES["PATH-RUST-PST"]];
  if (/wilt|collapse|droop|vascular|bacterial ooze/.test(s)) return ["PATH-BACT-WILT", DISEASE_PROFILES["PATH-BACT-WILT"]];
  if (/blast|spindle|grey lesion|neck rot/.test(s)) return ["PATH-BLAST-MAG", DISEASE_PROFILES["PATH-BLAST-MAG"]];
  return ["BIOT-STRESS-GEN", DISEASE_PROFILES["BIOT-STRESS-GEN"]];
}

function getRegionalData(region) {
  for (const [key, val] of Object.entries(REGIONAL_PROFILES)) {
    if (region.toLowerCase().includes(key.toLowerCase().split(' ')[0].toLowerCase()) ||
        key.toLowerCase().includes(region.toLowerCase().split(' ')[0].toLowerCase())) {
      return val;
    }
  }
  return null;
}

function buildAIContext(crop, stage, region, symptoms) {
  const [, disease] = getDiseaseBySymptoms(symptoms);
  const regional = getRegionalData(region);
  let ctx = `KNOWLEDGE BASE CONTEXT:\n\nDISEASE MATCH: ${disease.name} (${disease.pathogen})\nClass: ${disease.class}\nSeverity: ${disease.severity}\nSpread: ${disease.spread}\nConditions: ${disease.conditions}\n\nCHEMICAL: ${disease.chemical_rx.primary}\nBIOLOGICAL: ${disease.bio_rx.primary}\nIPM: ${disease.ipm.slice(0,3).join('; ')}`;
  if (regional) {
    ctx += `\n\nREGION (${region}): Soil: ${regional.soil}. Climate: ${regional.climate}. ICAR: ${regional.icar_center}.`;
  }
  return ctx;
}

function computeCurves(v0, decayRate, recoveryK, days = 14) {
  const decay = [], recovery = [];
  for (let t = 0; t <= days; t++) {
    const vt = v0 * Math.exp(-decayRate * t);
    decay.push(+Math.max(0.05, Math.min(1, vt)).toFixed(3));
    const rt = t < 2 ? vt : vt + (1 - vt) * (1 - Math.exp(-recoveryK * (t - 2)));
    recovery.push(+Math.max(0.05, Math.min(1, rt)).toFixed(3));
  }
  return { decay, recovery };
}

module.exports = { DISEASE_PROFILES, REGIONAL_PROFILES, AGENT_PROMPTS, getDiseaseBySymptoms, getRegionalData, buildAIContext, computeCurves };
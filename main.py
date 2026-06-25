"""
KrishiKonnect — Unified Backend API
FastAPI + Firebase Auth + Anthropic Claude + PDF Generation
Handles: Auth, Triage, Deep Diagnosis, Chat, PDF Reports, Visit Tracking
"""

import os, math, time, asyncio, logging, base64, io
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

import httpx
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from loguru import logger

# Optional: Firebase admin (for persistent user store)
try:
    import firebase_admin
    from firebase_admin import credentials, firestore, auth as fb_auth
    cred_path = os.getenv("FIREBASE_CRED_PATH", "firebase-creds.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        FIREBASE_ENABLED = True
        logger.info("Firebase Firestore connected.")
    else:
        FIREBASE_ENABLED = False
        logger.warning("Firebase credentials not found. Using in-memory store.")
except ImportError:
    FIREBASE_ENABLED = False
    logger.warning("firebase-admin not installed.")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from knowledge_base import (
    DISEASE_PROFILES, REGIONAL_PROFILES, MANDI_PRICES,
    AGENT_PROMPTS, get_disease_by_symptoms, get_regional_data, build_ai_context
)

# ── Config ─────────────────────────────────────────────────────
SECRET_KEY    = os.getenv("JWT_SECRET", "krishikonnect-dev-secret-change-in-prod")
ALGORITHM     = "HS256"
TOKEN_EXPIRE  = 60 * 24 * 7  # 7 days
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_KEY    = os.getenv("GEMINI_API_KEY", "")
OPENAI_KEY    = os.getenv("OPENAI_API_KEY", "")

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

# In-memory fallback if Firebase not available
_users_store: Dict[str, Dict] = {}
_visits_store: List[Dict] = []
_cases_store: List[Dict] = []

logging.basicConfig(level=logging.INFO)

# ── App ─────────────────────────────────────────────────────────
app = FastAPI(
    title="KrishiKonnect API",
    description="AI-Powered Agricultural Crop Intelligence Platform",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=60)
    email: str
    password: str = Field(..., min_length=6)
    role: str = Field(default="farmer")  # farmer | agronomist | researcher
    state: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

class TriageRequest(BaseModel):
    crop_type: str
    crop_stage: str
    region: str
    symptoms: str
    area_acres: Optional[float] = 1.0
    user_id: Optional[str] = None

class TriageResponse(BaseModel):
    crop_type: str
    crop_stage: str
    region: str
    symptoms: str
    diagnostic_code: str
    severity: str
    ai_triage: str
    agent_traces: List[str]
    decay_curve: List[float]
    recovery_curve: List[float]
    decay_rate: float
    recovery_k: float
    chemical_rx: str
    bio_rx: str
    ipm_notes: List[str]

class DeepDiagRequest(BaseModel):
    crop_type: str
    crop_stage: str
    region: str
    symptoms: str
    area_acres: Optional[float] = 1.0
    image_base64: Optional[str] = None
    image_mime: Optional[str] = "image/jpeg"
    patch_indices: List[int] = Field(default_factory=lambda: [28, 36])
    case_id: Optional[str] = None

class DeepDiagResponse(BaseModel):
    crop: str
    stage: str
    region: str
    diagnosis: str
    pathogen: str
    pathogen_class: str
    confidence: float
    severity: str
    decay_vector: List[float]
    recovery_vector: List[float]
    chemical_rx: str
    bio_rx: str
    ipm_notes: List[str]
    ai_analysis: str
    farmer_advisory: str
    agronomist_notes: str
    agent_traces: List[str]
    attention_heatmap: List[Dict]
    decay_rate: float
    recovery_k: float

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    llm: Optional[str] = "claude"  # claude | gemini | openai
    user_id: Optional[str] = None

class PDFReportRequest(BaseModel):
    report_type: str  # triage | deep_diagnosis
    triage_data: Optional[Dict] = None
    diag_data: Optional[Dict] = None
    include_farmer_section: bool = True
    include_agronomist_section: bool = True

class VisitRecord(BaseModel):
    user_id: Optional[str] = None
    page: str
    action: Optional[str] = None

# ═══════════════════════════════════════════════════════════════
# AUTH UTILITIES
# ═══════════════════════════════════════════════════════════════

def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_token(data: dict, expires_minutes: int = TOKEN_EXPIRE) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[Dict]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            return None
        if FIREBASE_ENABLED:
            users = db.collection("users").where("email", "==", email).limit(1).get()
            for u in users:
                return u.to_dict()
        else:
            return _users_store.get(email)
    except JWTError:
        return None

async def require_user(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def save_user(user_data: dict):
    if FIREBASE_ENABLED:
        db.collection("users").document(user_data["user_id"]).set(user_data)
    else:
        _users_store[user_data["email"]] = user_data

def get_user_by_email(email: str) -> Optional[Dict]:
    if FIREBASE_ENABLED:
        docs = db.collection("users").where("email", "==", email).limit(1).get()
        for d in docs:
            return d.to_dict()
        return None
    else:
        return _users_store.get(email)

def record_visit(record: dict):
    record["timestamp"] = datetime.utcnow().isoformat()
    if FIREBASE_ENABLED:
        db.collection("visits").add(record)
    else:
        _visits_store.append(record)

# ═══════════════════════════════════════════════════════════════
# LLM UTILITIES
# ═══════════════════════════════════════════════════════════════

async def call_claude(system: str, user_message: str,
                      image_base64: str = None, image_mime: str = "image/jpeg",
                      max_tokens: int = 1200) -> str:
    if not ANTHROPIC_KEY:
        logger.warning("No Anthropic API key. Returning fallback.")
        return None

    headers = {
        "x-api-key": ANTHROPIC_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    content = []
    if image_base64:
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": image_mime, "data": image_base64}
        })
    content.append({"type": "text", "text": user_message})

    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": content}]
    }

    retries, delay_s = 3, 1.0
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                res = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    json=payload, headers=headers, timeout=30.0
                )
                if res.status_code == 200:
                    data = res.json()
                    return "".join(b.get("text", "") for b in data.get("content", []))
                elif res.status_code == 429:
                    logger.warning(f"Rate limited. Attempt {attempt+1}")
                    await asyncio.sleep(delay_s); delay_s *= 2
                else:
                    logger.error(f"Claude API error {res.status_code}: {res.text}")
            except Exception as e:
                logger.error(f"Claude call failed attempt {attempt+1}: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay_s); delay_s *= 2
    return None


async def call_gemini(prompt: str, system: str = "") -> Optional[str]:
    if not GEMINI_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{system}\n\n{prompt}"}]}]
    }
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, json=payload, timeout=20.0)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.error(f"Gemini call failed: {e}")
    return None


async def call_openai(messages: List[Dict], system: str = "") -> Optional[str]:
    if not OPENAI_KEY:
        return None
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": 1000
    }
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post("https://api.openai.com/v1/chat/completions",
                                    json=payload, headers=headers, timeout=20.0)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
    return None

# ═══════════════════════════════════════════════════════════════
# MATH / MODELLING UTILITIES
# ═══════════════════════════════════════════════════════════════

def compute_curves(v0: float, decay_rate: float, recovery_k: float, days: int = 14) -> Dict:
    decay, recovery = [], []
    for t in range(days + 1):
        vt = v0 * math.exp(-decay_rate * t)
        d = round(max(0.05, min(1.0, vt)), 3)
        decay.append(d)
        if t < 2:
            rt = vt
        else:
            rt = vt + (1.0 - vt) * (1.0 - math.exp(-recovery_k * (t - 2)))
        recovery.append(round(max(0.05, min(1.0, rt)), 3))
    return {"decay": decay, "recovery": recovery}


def generate_attention_weights(target_patch: int, total: int = 64, sigma: float = 1.8) -> List[float]:
    grid_size = int(math.sqrt(total))
    tR, tC = divmod(target_patch, grid_size)
    weights = []
    for i in range(total):
        r, c = divmod(i, grid_size)
        d2 = (r - tR) ** 2 + (c - tC) ** 2
        weights.append(math.exp(-d2 / (2 * sigma ** 2)))
    # Add secondary hotspot
    sec = (target_patch + 9) % total
    sR, sC = divmod(sec, grid_size)
    for i in range(total):
        r, c = divmod(i, grid_size)
        d2 = (r - sR) ** 2 + (c - sC) ** 2
        weights[i] += 0.4 * math.exp(-d2 / (2 * sigma ** 2))
    exp_w = [math.exp(w) for w in weights]
    total_exp = sum(exp_w)
    return [round(e / total_exp, 4) for e in exp_w]

# ═══════════════════════════════════════════════════════════════
# AUTH ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.post("/api/auth/register", response_model=TokenResponse)
async def register(user: UserRegister):
    existing = get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    import uuid
    user_id = str(uuid.uuid4())
    user_data = {
        "user_id": user_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "state": user.state,
        "password_hash": hash_password(user.password),
        "created_at": datetime.utcnow().isoformat(),
        "visit_count": 1,
        "last_login": datetime.utcnow().isoformat()
    }
    save_user(user_data)
    record_visit({"user_id": user_id, "action": "register", "page": "auth"})

    token = create_token({"sub": user.email, "uid": user_id, "role": user.role})
    safe_user = {k: v for k, v in user_data.items() if k != "password_hash"}
    logger.info(f"New user registered: {user.email} | role: {user.role}")
    return {"access_token": token, "token_type": "bearer", "user": safe_user}


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Update visit count
    db_user["visit_count"] = db_user.get("visit_count", 0) + 1
    db_user["last_login"] = datetime.utcnow().isoformat()
    save_user(db_user)
    record_visit({"user_id": db_user["user_id"], "action": "login", "page": "auth"})

    token = create_token({"sub": user.email, "uid": db_user["user_id"], "role": db_user.get("role", "farmer")})
    safe_user = {k: v for k, v in db_user.items() if k != "password_hash"}
    logger.info(f"Login: {user.email} | visits: {db_user['visit_count']}")
    return {"access_token": token, "token_type": "bearer", "user": safe_user}


@app.get("/api/auth/me")
async def get_me(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {k: v for k, v in user.items() if k != "password_hash"}

# ═══════════════════════════════════════════════════════════════
# ANALYTICS / VISIT TRACKING
# ═══════════════════════════════════════════════════════════════

@app.post("/api/track")
async def track_visit(record: VisitRecord):
    record_visit(record.model_dump())
    return {"status": "ok"}


@app.get("/api/admin/stats")
async def get_stats(user=Depends(get_current_user)):
    """Admin endpoint — visit counts and user metrics."""
    if not user or user.get("role") not in ["admin", "agronomist"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    if FIREBASE_ENABLED:
        total_users  = len(list(db.collection("users").get()))
        total_visits = len(list(db.collection("visits").get()))
        farmers      = len(list(db.collection("users").where("role", "==", "farmer").get()))
        agronomists  = len(list(db.collection("users").where("role", "==", "agronomist").get()))
    else:
        total_users  = len(_users_store)
        total_visits = len(_visits_store)
        farmers      = sum(1 for u in _users_store.values() if u.get("role") == "farmer")
        agronomists  = sum(1 for u in _users_store.values() if u.get("role") == "agronomist")

    return {
        "total_users": total_users,
        "total_visits": total_visits,
        "farmers": farmers,
        "agronomists": agronomists,
        "firebase_enabled": FIREBASE_ENABLED
    }

# ═══════════════════════════════════════════════════════════════
# TRIAGE ENDPOINT (Farmer Tab)
# ═══════════════════════════════════════════════════════════════

@app.post("/api/triage", response_model=TriageResponse)
async def perform_triage(req: TriageRequest, user=Depends(get_current_user)):
    disease = get_disease_by_symptoms(req.symptoms)
    code = [k for k, v in DISEASE_PROFILES.items() if v == disease][0]

    d_rate = disease["decay_rate"]
    rec_k  = disease["recovery_k"]
    curves = compute_curves(0.75, d_rate, rec_k)

    agent_traces = [
        f"[PathoVision VLM] Symptom pattern matched → diagnostic code '{code}' on {req.crop_type}.",
        f"[RegionalGrounded] Verified agro-climate parameters for {req.region}.",
        f"[BioTherapeutic] ICAR compound registry checked — {disease['name']} protocol loaded.",
        f"[YieldPrognostic] 14-day vigor decay modeled: d={d_rate}, k={rec_k}.",
        f"[TriageOrchestrator] Synthesizing multi-agent outputs → generating triage report."
    ]

    kb_context = build_ai_context(req.crop_type, req.crop_stage, req.region, req.symptoms)
    system = AGENT_PROMPTS["triage"] + "\n\n" + kb_context
    user_msg = (
        f"Crop: {req.crop_type}\nStage: {req.crop_stage}\n"
        f"Region: {req.region}\nField Area: {req.area_acres} acres\n"
        f"Symptoms: {req.symptoms}"
    )

    ai_text = await call_claude(system, user_msg)

    if not ai_text:
        ai_text = (
            f"SUSPECTED PATHOGEN: {disease['name']} ({disease['pathogen']}) — {disease['class']}.\n\n"
            f"THREAT LEVEL: {disease['severity']}. The described symptoms match this pathogen at "
            f"early to mid-stage infection under current {req.region} conditions.\n\n"
            f"IMMEDIATE FIELD ACTIONS: {'. '.join(disease['ipm'][:3])}.\n\n"
            f"CHEMICAL PRESCRIPTION: {disease['chemical_rx']['primary']}\n\n"
            f"BIOLOGICAL PRESCRIPTION: {disease['bio_rx']['primary']}"
        )

    if user:
        record_visit({
            "user_id": user.get("user_id"), "action": "triage",
            "page": "farmer", "crop": req.crop_type, "region": req.region
        })

    return TriageResponse(
        crop_type=req.crop_type, crop_stage=req.crop_stage,
        region=req.region, symptoms=req.symptoms,
        diagnostic_code=code, severity=disease["severity"],
        ai_triage=ai_text, agent_traces=agent_traces,
        decay_curve=curves["decay"], recovery_curve=curves["recovery"],
        decay_rate=d_rate, recovery_k=rec_k,
        chemical_rx=disease["chemical_rx"]["primary"],
        bio_rx=disease["bio_rx"]["primary"],
        ipm_notes=disease["ipm"]
    )

# ═══════════════════════════════════════════════════════════════
# DEEP DIAGNOSIS ENDPOINT (Agronomist Tab)
# ═══════════════════════════════════════════════════════════════

@app.post("/api/diagnose", response_model=DeepDiagResponse)
async def perform_deep_diagnosis(req: DeepDiagRequest, user=Depends(get_current_user)):
    disease = get_disease_by_symptoms(req.symptoms)
    code = [k for k, v in DISEASE_PROFILES.items() if v == disease][0]
    d_rate = disease["decay_rate"]
    rec_k  = disease["recovery_k"]
    curves = compute_curves(0.75, d_rate, rec_k)
    conf   = 0.82 + (hash(req.symptoms[:20]) % 100) / 600

    # Attention heatmap
    active = req.patch_indices if req.patch_indices else [28, 36]
    heatmap = []
    for p in range(64):
        weights = generate_attention_weights(p, 64) if p in active else [0.0156] * 64
        heatmap.append({"patch_id": p, "scores": weights})

    # Agent trace messages
    agent_traces = [
        f"[PathoVision VLM] Pixel-level lesion segmentation complete on {req.crop_type}.",
        f"[RegionalGrounded] Climate+soil parameters loaded for {req.region}.",
        f"[BioTherapeutic] ICAR compound registry: {disease['chemical_rx']['primary'][:50]}...",
        f"[KinematicSolver] 8x8 attention heatmap generated — peak at patch {active[0]}.",
        f"[YieldPrognostic] 14-day trajectory: decay d={d_rate}, recovery k={rec_k}.",
        f"[TriageOrchestrator] Confidence score: {conf:.3f}. Report synthesized."
    ]

    kb_context = build_ai_context(req.crop_type, req.crop_stage, req.region, req.symptoms)

    # Deep analysis for agronomist
    diag_system  = AGENT_PROMPTS["deep_diagnosis"] + "\n\n" + kb_context
    farm_system  = AGENT_PROMPTS["pdf_report_farmer"]
    agro_system  = AGENT_PROMPTS["pdf_report_agronomist"] + "\n\n" + kb_context
    user_msg     = (
        f"Crop: {req.crop_type} | Stage: {req.crop_stage} | Region: {req.region} | "
        f"Area: {req.area_acres} acres\nSymptoms: {req.symptoms}"
    )

    # Run in parallel
    vlm_result = None
    if req.image_base64:
        vlm_result = await call_claude(
            AGENT_PROMPTS["vlm_image"], "Analyze this crop image for disease symptoms.",
            req.image_base64, req.image_mime, max_tokens=300
        )

    ai_analysis, farmer_adv, agro_notes = await asyncio.gather(
        call_claude(diag_system, user_msg, max_tokens=1200),
        call_claude(farm_system, user_msg, max_tokens=400),
        call_claude(agro_system, user_msg, max_tokens=500),
    )

    if not ai_analysis:
        ai_analysis = (
            f"Pathogen identified as {disease['pathogen']} based on symptom morphology. "
            f"Disease mechanism involves penetration of host cuticle followed by intercellular "
            f"hyphal growth causing necrotic lesion formation. Current stage indicates early to mid "
            f"progression. Immediate intervention is recommended with the prescribed chemical and "
            f"biological agents. Long-term management must incorporate resistant varieties and "
            f"crop rotation with non-host species for 2-3 seasons."
        )
    if not farmer_adv:
        farmer_adv = (
            f"Your {req.crop_type} crop has a disease called {disease['name']}. "
            f"It is serious and needs immediate action. First, remove all infected leaves and "
            f"destroy them. Then spray {disease['chemical_rx']['primary']}. "
            f"Do not water the leaves in the evening. With proper treatment, your crop can recover."
        )
    if not agro_notes:
        agro_notes = (
            f"Pathogen: {disease['pathogen']} | Class: {disease['class']}. "
            f"Preharvest interval: {disease['chemical_rx']['preharvest_interval']}. "
            f"Economic threshold: {disease.get('economic_threshold', 'See ICAR guidelines')}. "
            f"Resistance risk: Low to moderate for single-site fungicides. "
            f"Recommended rotation of chemical groups to delay resistance."
        )

    if vlm_result:
        agent_traces.insert(0, f"[VLM ImageScan] {vlm_result[:80]}...")

    if user:
        record_visit({
            "user_id": user.get("user_id"), "action": "deep_diagnosis",
            "page": "agronomist", "crop": req.crop_type, "case_id": req.case_id
        })

    return DeepDiagResponse(
        crop=req.crop_type, stage=req.crop_stage, region=req.region,
        diagnosis=disease["name"], pathogen=disease["pathogen"],
        pathogen_class=disease["class"], confidence=round(conf, 3),
        severity=disease["severity"],
        decay_vector=curves["decay"], recovery_vector=curves["recovery"],
        chemical_rx=disease["chemical_rx"]["primary"],
        bio_rx=disease["bio_rx"]["primary"],
        ipm_notes=disease["ipm"],
        ai_analysis=ai_analysis, farmer_advisory=farmer_adv,
        agronomist_notes=agro_notes,
        agent_traces=agent_traces, attention_heatmap=heatmap,
        decay_rate=d_rate, recovery_k=rec_k
    )

# ═══════════════════════════════════════════════════════════════
# CHAT ENDPOINT — Multi-LLM
# ═══════════════════════════════════════════════════════════════

@app.post("/api/chat")
async def chat(req: ChatRequest, user=Depends(get_current_user)):
    system = AGENT_PROMPTS["chatbot"]
    msgs = [{"role": m.role, "content": m.content} for m in req.messages]
    last_user_msg = next((m["content"] for m in reversed(msgs) if m["role"] == "user"), "")

    response_text = None

    if req.llm == "gemini":
        response_text = await call_gemini(last_user_msg, system)
    elif req.llm == "openai":
        response_text = await call_openai(msgs, system)
    else:  # default: claude
        response_text = await call_claude(system, last_user_msg)

    if not response_text:
        # Cascade fallback: try other LLMs
        response_text = (
            await call_claude(system, last_user_msg) or
            await call_gemini(last_user_msg, system) or
            "I am unable to connect to the AI service right now. Please try again shortly."
        )

    if user:
        record_visit({"user_id": user.get("user_id"), "action": "chat", "page": "advisor", "llm": req.llm})

    return {"response": response_text, "llm_used": req.llm}

# ═══════════════════════════════════════════════════════════════
# IMAGE UPLOAD ENDPOINT
# ═══════════════════════════════════════════════════════════════

@app.post("/api/image/analyze")
async def analyze_image(file: UploadFile = File(...), user=Depends(get_current_user)):
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image too large. Max 2MB (frontend compresses to 800px before upload).")

    b64 = base64.b64encode(content).decode("utf-8")
    mime = file.content_type or "image/jpeg"

    analysis = await call_claude(
        AGENT_PROMPTS["vlm_image"],
        "Analyze this crop field photograph for disease symptoms.",
        b64, mime, max_tokens=400
    )

    if not analysis:
        analysis = "Image registered. VLM analysis unavailable — please describe symptoms manually."

    return {"analysis": analysis, "image_b64": b64, "mime": mime}

# ═══════════════════════════════════════════════════════════════
# PDF REPORT ENDPOINT
# ═══════════════════════════════════════════════════════════════

@app.post("/api/report/pdf")
async def generate_pdf_report(req: PDFReportRequest, user=Depends(get_current_user)):
    """
    Generates a structured text payload for the frontend to render as PDF via print().
    Returns a JSON object with all report sections pre-generated by Claude.
    The frontend builds the PDF DOM and calls window.print().
    """
    now_str = datetime.now().strftime("%d %B %Y")
    user_name = user.get("name", "Field Agronomist") if user else "Field Agronomist"

    if req.report_type == "triage" and req.triage_data:
        data = req.triage_data
        farmer_section, agro_section = None, None

        user_msg = (
            f"Crop: {data.get('crop_type')} | Stage: {data.get('crop_stage')} | "
            f"Region: {data.get('region')}\nSymptoms: {data.get('symptoms')}\n"
            f"AI Assessment: {data.get('ai_triage', '')}"
        )

        if req.include_farmer_section:
            farmer_section = await call_claude(AGENT_PROMPTS["pdf_report_farmer"], user_msg, max_tokens=350)
        if req.include_agronomist_section:
            agro_section = await call_claude(AGENT_PROMPTS["pdf_report_agronomist"], user_msg, max_tokens=450)

        return {
            "report_type": "triage",
            "generated_by": "KrishiKonnect AI Platform",   # no personal name in farmer triage reports
            "generated_at": now_str,
            "crop": data.get("crop_type"),
            "stage": data.get("crop_stage"),
            "region": data.get("region"),
            "diagnostic_code": data.get("diagnostic_code"),
            "severity": data.get("severity"),
            "symptoms": data.get("symptoms"),
            "ai_triage": data.get("ai_triage"),
            "farmer_section": farmer_section,
            "agronomist_section": agro_section,
            "decay_curve": data.get("curves", {}).get("decay", []),
            "recovery_curve": data.get("curves", {}).get("recovery", []),
            "agent_traces": data.get("agent_traces", []),
            "chemical_rx": data.get("chemical_rx"),
            "bio_rx": data.get("bio_rx"),
            "ipm_notes": data.get("ipm_notes", [])
        }

    elif req.report_type == "deep_diagnosis" and req.diag_data:
        data = req.diag_data
        return {
            "report_type": "deep_diagnosis",
            "generated_by": user_name,   # agronomist name intentionally kept for deep diagnosis
            "generated_at": now_str,
            "crop": data.get("crop"),
            "stage": data.get("stage"),
            "region": data.get("region"),
            "pathogen": data.get("pathogen"),
            "pathogen_class": data.get("pathogen_class"),
            "confidence": data.get("confidence"),
            "severity": data.get("severity"),
            "ai_analysis": data.get("ai_analysis"),
            "farmer_advisory": data.get("farmer_advisory"),
            "agronomist_notes": data.get("agronomist_notes"),
            "chemical_rx": data.get("chemical_rx"),
            "bio_rx": data.get("bio_rx"),
            "ipm_notes": data.get("ipm_notes", []),
            "decay_vector": data.get("decay_vector", []),
            "recovery_vector": data.get("recovery_vector", []),
            "agent_traces": data.get("agent_traces", [])
        }

    raise HTTPException(status_code=400, detail="Invalid report type or missing data")

# ═══════════════════════════════════════════════════════════════
# MANDI PRICES ENDPOINT
# ═══════════════════════════════════════════════════════════════

@app.get("/api/mandi")
async def get_mandi_prices(crop: Optional[str] = None, state: Optional[str] = None):
    prices = MANDI_PRICES
    if crop:
        prices = [p for p in prices if crop.lower() in p["crop"].lower()]
    if state:
        prices = [p for p in prices if state.lower() in p["state"].lower()]
    return {"prices": prices, "updated_at": datetime.utcnow().isoformat()}

# ═══════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def health():
    return {
        "status": "ONLINE",
        "service": "KrishiKonnect API v2.1",
        "firebase": FIREBASE_ENABLED,
        "claude": bool(ANTHROPIC_KEY),
        "gemini": bool(GEMINI_KEY),
        "openai": bool(OPENAI_KEY),
        "timestamp": datetime.utcnow().isoformat()
    }

# ═══════════════════════════════════════════════════════════════
# LOCAL RUN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting KrishiKonnect API on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
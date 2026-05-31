import streamlit as st
from groq import Groq
import json
import PyPDF2
import io
import random
import plotly.graph_objects as go
from datetime import date
from fpdf import FPDF

import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MOTIVATIONAL_QUOTES = [
    "The more that you read, the more things you will know.",
    "An investment in knowledge pays the best interest.",
    "Live as if you were to die tomorrow. Learn as if you were to live forever.",
    "The beautiful thing about learning is nobody can take it away from you.",
    "Knowledge is power. Information is liberating.",
    "Education is the passport to the future.",
    "The expert in anything was once a beginner.",
    "Push yourself, because no one else is going to do it for you.",
]

def export_pdf(cards):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(40, 20, 0)
    pdf.cell(170, 12, "Memoria - Flashcard Export", ln=True, align="C")
    pdf.ln(4)
    pdf.set_draw_color(180, 140, 60)
    pdf.set_line_width(0.4)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(6)
    for i, card in enumerate(cards):
        q = card['question'].encode('latin-1', 'replace').decode('latin-1')[:300]
        a = card['answer'].encode('latin-1', 'replace').decode('latin-1')[:300]
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(100, 70, 20)
        pdf.cell(170, 7, f"Card {i+1}", ln=True)
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 20, 10)
        pdf.multi_cell(170, 6, f"Q: {q}")
        pdf.ln(1)
        pdf.set_text_color(70, 50, 120)
        pdf.multi_cell(170, 6, f"A: {a}")
        pdf.ln(3)
        pdf.set_draw_color(200, 170, 100)
        pdf.set_line_width(0.2)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(4)
    return bytes(pdf.output())

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #080808 !important;
    color: #e8e0d0 !important;
}

.stApp {
    background: #080808 !important;
    background-image:
        radial-gradient(ellipse at 15% 15%, rgba(212,184,120,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(120,80,200,0.03) 0%, transparent 50%) !important;
}

h1,h2,h3 { font-family: 'Cormorant Garamond', serif !important; }

.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(212,184,120,0.2) !important;
    color: #c8a860 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2.5px !important;
    padding: 12px 28px !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    border-radius: 4px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

.stButton > button:hover {
    background: rgba(212,184,120,0.06) !important;
    border-color: rgba(212,184,120,0.45) !important;
    color: #e8c878 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,184,120,0.15) !important;
    color: #f0e8d8 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
    padding: 16px !important;
    caret-color: #d4b878 !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(212,184,120,0.35) !important;
    box-shadow: 0 0 0 1px rgba(212,184,120,0.1) !important;
    outline: none !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(200,180,140,0.3) !important;
}

div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(212,184,120,0.15) !important;
    color: #f0e8d8 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    caret-color: #d4b878 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: rgba(212,184,120,0.35) !important;
    box-shadow: 0 0 0 1px rgba(212,184,120,0.1) !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(200,180,140,0.3) !important;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(212,184,120,0.15) !important;
    border-radius: 10px !important;
    padding: 8px !important;
    transition: border-color 0.3s !important;
}

div[data-testid="stFileUploader"]:hover {
    border-color: rgba(212,184,120,0.3) !important;
}

div[data-testid="stFileUploader"] * {
    color: #a09070 !important;
}

div[data-testid="stRadio"] label {
    color: #a09070 !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    font-family: 'Inter', sans-serif !important;
}

div[data-testid="stRadio"] > div {
    gap: 16px !important;
}

div[data-testid="stSelectSlider"] {
    color: #c8a860 !important;
}

div[data-testid="stSelectSlider"] > div > div {
    color: #e8e0d0 !important;
}

hr { border-color: rgba(212,184,120,0.06) !important; }

div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}

.element-container { animation: fadeUp 0.4s ease forwards; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #f8f5f0 !important;
    color: #1a1410 !important;
}

.stApp {
    background: #f8f5f0 !important;
    background-image:
        radial-gradient(ellipse at 15% 15%, rgba(180,140,60,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(100,60,160,0.02) 0%, transparent 50%) !important;
}

h1,h2,h3 { font-family: 'Cormorant Garamond', serif !important; }

.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(120,90,30,0.25) !important;
    color: #7a5a20 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2.5px !important;
    padding: 12px 28px !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    border-radius: 4px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

.stButton > button:hover {
    background: rgba(120,90,30,0.06) !important;
    border-color: rgba(120,90,30,0.45) !important;
    color: #5a3a10 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important;
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(120,90,30,0.2) !important;
    color: #1a1410 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.8 !important;
    padding: 16px !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(120,90,30,0.4) !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(80,60,30,0.35) !important;
}

div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(120,90,30,0.2) !important;
    color: #1a1410 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(80,60,30,0.35) !important;
}

div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.6) !important;
    border: 1px dashed rgba(120,90,30,0.2) !important;
    border-radius: 10px !important;
    padding: 8px !important;
}

div[data-testid="stRadio"] label {
    color: #6a4a20 !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
}

hr { border-color: rgba(120,90,30,0.08) !important; }

.element-container { animation: fadeUp 0.4s ease forwards; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
"""

SHARED_CSS = """
<style>
/* ── Logo ── */
.mem-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(3.5rem, 10vw, 6rem);
    font-weight: 300;
    text-align: center;
    letter-spacing: 16px;
    line-height: 1;
    margin-bottom: 6px;
}

.mem-logo.dark { color: #e8e0d0; }
.mem-logo.light { color: #1a1410; }

.mem-tag {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    text-align: center;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

.mem-tag.dark { color: rgba(212,184,120,0.35); }
.mem-tag.light { color: rgba(100,70,20,0.4); }

/* ── Gold divider ── */
.g-div {
    width: 48px;
    height: 1px;
    margin: 1.2rem auto;
}

.g-div.dark { background: linear-gradient(90deg, transparent, rgba(212,184,120,0.4), transparent); }
.g-div.light { background: linear-gradient(90deg, transparent, rgba(120,90,30,0.4), transparent); }

/* ── Section label ── */
.sec-label {
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    letter-spacing: 4px;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 1.5rem;
}

.sec-label.dark { color: rgba(212,184,120,0.3); }
.sec-label.light { color: rgba(100,70,20,0.35); }

/* ── Quote ── */
.quote-box {
    padding: 1rem 1.5rem;
    border-radius: 0 8px 8px 0;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 17px;
    line-height: 1.7;
    margin: 0.5rem 0 1.5rem;
}

.quote-box.dark {
    background: rgba(255,255,255,0.02);
    border-left: 2px solid rgba(212,184,120,0.2);
    color: rgba(220,200,160,0.55);
}

.quote-box.light {
    background: rgba(255,255,255,0.5);
    border-left: 2px solid rgba(120,90,30,0.25);
    color: rgba(60,40,10,0.5);
}

/* ── Stat cards ── */
.stat-card {
    border-radius: 10px;
    padding: 1.1rem 0.8rem;
    text-align: center;
    transition: transform 0.2s ease;
}

.stat-card:hover { transform: translateY(-2px); }

.stat-card.dark {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(212,184,120,0.08);
}

.stat-card.light {
    background: rgba(255,255,255,0.6);
    border: 1px solid rgba(120,90,30,0.1);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.stat-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 300;
    line-height: 1;
    margin-bottom: 4px;
}

.stat-num.dark { color: #d4b878; }
.stat-num.light { color: #8a6020; }

.stat-lbl {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}

.stat-lbl.dark { color: rgba(212,184,120,0.35); }
.stat-lbl.light { color: rgba(100,70,20,0.4); }

/* ── Flip card ── */
.flip-wrap {
    perspective: 1400px;
    width: 100%;
    height: 280px;
    margin: 1.5rem 0;
}

.flip-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s cubic-bezier(0.4,0.2,0.2,1);
    transform-style: preserve-3d;
}

.flip-wrap.flipped .flip-inner { transform: rotateY(180deg); }

.flip-f, .flip-b {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 14px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2.5rem;
    text-align: center;
}

.flip-f {
    background: rgba(18,14,8,0.96);
    border: 1px solid rgba(212,184,120,0.12);
    box-shadow: 0 4px 32px rgba(0,0,0,0.5);
}

.flip-f::before {
    content: '';
    position: absolute;
    top: 0; left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,184,120,0.25), transparent);
}

.flip-b {
    background: rgba(12,10,20,0.96);
    border: 1px solid rgba(130,90,210,0.18);
    box-shadow: 0 4px 32px rgba(60,20,120,0.2);
    transform: rotateY(180deg);
}

.flip-b::before {
    content: '';
    position: absolute;
    top: 0; left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(130,90,210,0.25), transparent);
}

.flip-f.light-card {
    background: rgba(255,252,245,0.98);
    border: 1px solid rgba(120,90,30,0.12);
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}

.flip-b.light-card {
    background: rgba(248,244,255,0.98);
    border: 1px solid rgba(110,80,200,0.15);
    box-shadow: 0 4px 24px rgba(80,40,160,0.06);
}

.c-tag {
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 18px;
    color: rgba(212,184,120,0.3);
}

.c-q {
    font-family: 'Cormorant Garamond', serif;
    font-size: 23px;
    font-weight: 400;
    line-height: 1.6;
    color: #e8dcc8;
}

.c-q.light { color: #1a1410; }

.c-a {
    font-family: 'Cormorant Garamond', serif;
    font-size: 21px;
    font-style: italic;
    line-height: 1.6;
    color: #b898e8;
}

.c-a.light { color: #5030a0; }

.c-hint {
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 18px;
    color: rgba(212,184,120,0.15);
}

/* ── Progress dots ── */
.p-dots {
    display: flex;
    justify-content: center;
    gap: 7px;
    margin: 1rem 0;
}

.dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.dot-u { background: rgba(212,184,120,0.12); }
.dot-k { background: #6aaa7a; }
.dot-x { background: #aa6a6a; }
.dot-a { background: #d4b878; transform: scale(1.4); }

/* ── Progress bar ── */
.p-track {
    border-radius: 10px;
    height: 3px;
    overflow: hidden;
    margin: 6px 0;
}

.p-track.dark { background: rgba(212,184,120,0.06); }
.p-track.light { background: rgba(120,90,30,0.08); }

.p-fill {
    height: 3px;
    border-radius: 10px;
    background: linear-gradient(90deg, #c8a050, #e8c878);
    transition: width 0.5s cubic-bezier(0.4,0,0.2,1);
}

/* ── Quiz card ── */
.q-card {
    border-radius: 14px;
    padding: 2.5rem;
    text-align: center;
    margin: 1rem 0;
}

.q-card.dark {
    background: rgba(18,14,8,0.96);
    border: 1px solid rgba(212,184,120,0.1);
    box-shadow: 0 4px 32px rgba(0,0,0,0.4);
}

.q-card.light {
    background: rgba(255,252,245,0.98);
    border: 1px solid rgba(120,90,30,0.1);
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
}

.q-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    line-height: 1.7;
    margin-bottom: 2rem;
}

.q-text.dark { color: #e8dcc8; }
.q-text.light { color: #1a1410; }

/* ── Badges ── */
.badge-hard {
    display: inline-block;
    background: rgba(180,60,60,0.1);
    border: 1px solid rgba(180,60,60,0.2);
    color: #b06060;
    font-size: 9px;
    letter-spacing: 2px;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    margin-left: 8px;
    vertical-align: middle;
}

.badge-easy {
    display: inline-block;
    background: rgba(60,140,80,0.1);
    border: 1px solid rgba(60,140,80,0.2);
    color: #60a070;
    font-size: 9px;
    letter-spacing: 2px;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    margin-left: 8px;
    vertical-align: middle;
}

/* ── Theme toggle ── */
.theme-btn {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 999;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(212,184,120,0.15);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
    backdrop-filter: blur(8px);
}

.theme-btn:hover {
    background: rgba(212,184,120,0.08);
    border-color: rgba(212,184,120,0.3);
}

/* ── Particles ── */
#mem-particles {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
}
</style>

<canvas id="mem-particles"></canvas>
<script>
(function(){
    const c = document.getElementById('mem-particles');
    if(!c) return;
    const ctx = c.getContext('2d');
    function resize(){ c.width=window.innerWidth; c.height=window.innerHeight; }
    resize();
    window.addEventListener('resize', resize);
    const pts = Array.from({length:40}, ()=>({
        x: Math.random()*window.innerWidth,
        y: Math.random()*window.innerHeight,
        r: Math.random()*1.2+0.2,
        vy: -(Math.random()*0.3+0.05),
        vx: (Math.random()-0.5)*0.1,
        o: Math.random()*0.25+0.05,
        t: Math.random()*Math.PI*2
    }));
    function draw(){
        ctx.clearRect(0,0,c.width,c.height);
        pts.forEach(p=>{
            p.y+=p.vy; p.x+=p.vx; p.t+=0.015;
            if(p.y<-5){p.y=c.height+5;p.x=Math.random()*c.width;}
            const a=p.o*(0.5+0.5*Math.sin(p.t));
            ctx.beginPath();
            ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
            ctx.fillStyle=`rgba(212,180,100,${a})`;
            ctx.fill();
        });
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
"""

st.set_page_config(
    page_title="Memoria",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

defaults = {
    "page": "home",
    "flashcards": [],
    "card_index": 0,
    "flipped": False,
    "results": {},
    "difficulty": {},
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_answers": {},
    "weak_cards": [],
    "streak": 0,
    "last_study_date": None,
    "total_sessions": 0,
    "dark_mode": True,
    "quote": random.choice(MOTIVATIONAL_QUOTES),
    "shuffled": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

th = "dark" if st.session_state.dark_mode else "light"
st.markdown((DARK_CSS if st.session_state.dark_mode else LIGHT_CSS) + SHARED_CSS, unsafe_allow_html=True)

def go_home():
    keep = ["streak","last_study_date","total_sessions","weak_cards","dark_mode","quote"]
    for k,v in defaults.items():
        if k not in keep:
            st.session_state[k] = v

def update_streak():
    today = date.today()
    last = st.session_state.last_study_date
    if last is None or (today-last).days > 1:
        st.session_state.streak = 1
    elif (today-last).days == 1:
        st.session_state.streak += 1
    st.session_state.last_study_date = today
    st.session_state.total_sessions += 1

def dots_html(cards, idx, results):
    d = ""
    for i in range(len(cards)):
        if i == idx: cls = "dot dot-a"
        elif i in results: cls = "dot dot-k" if results[i]=="known" else "dot dot-x"
        else: cls = "dot dot-u"
        d += f"<div class='{cls}'></div>"
    return f"<div class='p-dots'>{d}</div>"

# ── Theme toggle ──
_, tcol = st.columns([8,1])
with tcol:
    if st.button("☀️" if st.session_state.dark_mode else "🌙", key="theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ════════════════════════════════
# HOME
# ════════════════════════════════
if st.session_state.page == "home":
    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='mem-logo {th}'>Memoria</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='mem-tag {th}'>Intelligent Flashcard Learning</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-div {th}'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='quote-box {th}'>{st.session_state.quote}</div>", unsafe_allow_html=True)

    if st.session_state.total_sessions > 0:
        streak = st.session_state.streak
        flame = "🔥" * min(streak, 5)
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{st.session_state.total_sessions}</div><div class='stat-lbl {th}'>Sessions</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{streak}</div><div class='stat-lbl {th}'>Streak {flame}</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{len(st.session_state.weak_cards)}</div><div class='stat-lbl {th}'>Weak Cards</div></div>", unsafe_allow_html=True)
        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='sec-label {th}'>How would you like to add your notes?</div>", unsafe_allow_html=True)

    method = st.radio("", ["✍️  Write notes","📁  Upload file"], horizontal=True, label_visibility="collapsed")

    notes = ""
    if "Write" in method:
        notes = st.text_area("", height=200, placeholder="Paste your study notes here — any subject, any length...", label_visibility="collapsed")
    else:
        up = st.file_uploader("", type=["txt","pdf"], label_visibility="collapsed")
        if up:
            ft = getattr(up,"type","")
            if "pdf" in ft:
                r = PyPDF2.PdfReader(io.BytesIO(up.read()))
                for pg in r.pages: notes += pg.extract_text() or ""
                st.success("✦ PDF loaded")
            else:
                notes = up.read().decode("utf-8")
                st.success("✦ File loaded")
            if notes:
                with st.expander("Preview"):
                    st.text(notes[:500]+("..." if len(notes)>500 else ""))

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    num = st.select_slider("Number of flashcards", options=[3,5,7,10], value=5)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    _,mid,_ = st.columns([1,2,1])
    with mid:
        if st.button("Generate Flashcards", use_container_width=True):
            if not notes.strip():
                st.warning("Please add some notes first.")
            else:
                with st.spinner("Generating your flashcards..."):
                    try:
                        resp = client.chat.completions.create(
                            model=model_name,
                            messages=[{"role":"user","content":f"""You are an expert at creating flashcards from study notes.
Generate exactly {num} flashcards ONLY from the notes below.
Do NOT use outside knowledge.
Return ONLY a JSON array, no extra text, no backticks:
[
  {{"question":"...","answer":"..."}},
  {{"question":"...","answer":"..."}}
]
Notes:
{notes[:6000]}"""}],
                            temperature=0.3
                        )
                        raw = resp.choices[0].message.content.strip()
                        if raw.startswith("```"):
                            raw = raw.split("```")[1]
                            if raw.startswith("json"): raw = raw[4:]
                        st.session_state.flashcards = json.loads(raw.strip())
                        st.session_state.card_index = 0
                        st.session_state.results = {}
                        st.session_state.difficulty = {}
                        st.session_state.flipped = False
                        st.session_state.shuffled = False
                        st.session_state.page = "flashcard"
                        st.session_state.quote = random.choice(MOTIVATIONAL_QUOTES)
                        update_streak()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

    if st.session_state.weak_cards:
        st.markdown(f"<div class='g-div {th}'></div>", unsafe_allow_html=True)
        _,mid,_ = st.columns([1,2,1])
        with mid:
            if st.button("Review Weak Cards", use_container_width=True):
                st.session_state.flashcards = st.session_state.weak_cards.copy()
                st.session_state.card_index = 0
                st.session_state.results = {}
                st.session_state.flipped = False
                st.session_state.page = "flashcard"
                update_streak()
                st.rerun()

# ════════════════════════════════
# FLASHCARD
# ════════════════════════════════
elif st.session_state.page == "flashcard":
    cards = st.session_state.flashcards
    idx = st.session_state.card_index
    total = len(cards)
    known = sum(1 for v in st.session_state.results.values() if v=="known")
    unknown = sum(1 for v in st.session_state.results.values() if v=="unknown")

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([1,2,1])
    with c1:
        if st.button("← Back"):
            go_home(); st.rerun()
    with c2:
        pct = int((len(st.session_state.results)/total)*100)
        st.markdown(f"<div style='text-align:center;font-size:9px;letter-spacing:4px;color:rgba(212,184,120,0.35);text-transform:uppercase;margin-bottom:6px;font-family:Inter,sans-serif;'>Progress</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='p-track {th}'><div class='p-fill' style='width:{pct}%'></div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='text-align:right;font-size:12px;color:rgba(212,184,120,0.4);font-family:Inter,sans-serif;'>{idx+1}/{total}</div>", unsafe_allow_html=True)

    sb1,sb2 = st.columns(2)
    with sb1:
        if st.button("🔀 Shuffle", use_container_width=True):
            s = st.session_state.flashcards.copy()
            random.shuffle(s)
            st.session_state.flashcards = s
            st.session_state.card_index = 0
            st.session_state.results = {}
            st.session_state.flipped = False
            st.rerun()
    with sb2:
        pdf_bytes = export_pdf(cards)
        st.download_button("📄 Export PDF", data=pdf_bytes, file_name="memoria.pdf", mime="application/pdf", use_container_width=True)

    st.markdown(dots_html(cards, idx, st.session_state.results), unsafe_allow_html=True)

    card = cards[idx]
    fc = "flip-wrap flipped" if st.session_state.flipped else "flip-wrap"
    diff = st.session_state.difficulty.get(idx,"")
    badge = f"<span class='badge-hard'>Hard</span>" if diff=="hard" else f"<span class='badge-easy'>Easy</span>" if diff=="easy" else ""
    lc = "light-card" if not st.session_state.dark_mode else ""
    qc = "light" if not st.session_state.dark_mode else ""

    st.markdown(f"""
    <div class='{fc}'>
        <div class='flip-inner'>
            <div class='flip-f {lc}'>
                <div class='c-tag'>Question {idx+1} of {total}{badge}</div>
                <div class='c-q {qc}'>{card['question']}</div>
                <div class='c-hint'>— tap to reveal —</div>
            </div>
            <div class='flip-b {lc}'>
                <div class='c-tag'>Answer</div>
                <div class='c-a {qc}'>{card['answer']}</div>
                <div class='c-hint'>— how did you do? —</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.flipped:
        _,mid,_ = st.columns([1,2,1])
        with mid:
            if st.button("Reveal Answer", use_container_width=True):
                st.session_state.flipped = True; st.rerun()
    else:
        st.markdown(f"<div style='text-align:center;font-size:9px;letter-spacing:3px;color:rgba(212,184,120,0.25);text-transform:uppercase;margin-bottom:12px;font-family:Inter,sans-serif;'>How did you do?</div>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("😓  Hard", use_container_width=True):
                st.session_state.results[idx] = "unknown"
                st.session_state.difficulty[idx] = "hard"
                if card not in st.session_state.weak_cards:
                    st.session_state.weak_cards.append(card)
                if idx+1 < total:
                    st.session_state.card_index += 1
                    st.session_state.flipped = False
                else:
                    st.session_state.page = "summary"
                st.rerun()
        with c2:
            if st.button("🤔  Medium", use_container_width=True):
                st.session_state.results[idx] = "unknown"
                st.session_state.difficulty[idx] = "medium"
                if idx+1 < total:
                    st.session_state.card_index += 1
                    st.session_state.flipped = False
                else:
                    st.session_state.page = "summary"
                st.rerun()
        with c3:
            if st.button("✓  Easy", use_container_width=True):
                st.session_state.results[idx] = "known"
                st.session_state.difficulty[idx] = "easy"
                if card in st.session_state.weak_cards:
                    st.session_state.weak_cards.remove(card)
                if idx+1 < total:
                    st.session_state.card_index += 1
                    st.session_state.flipped = False
                else:
                    st.session_state.page = "summary"
                st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;justify-content:center;gap:20px;font-size:11px;font-family:Inter,sans-serif;color:rgba(212,184,120,0.35);'><span>✓ {known} known</span><span>✗ {unknown} needs work</span></div>", unsafe_allow_html=True)

# ════════════════════════════════
# SUMMARY
# ════════════════════════════════
elif st.session_state.page == "summary":
    cards = st.session_state.flashcards
    total = len(cards)
    known = sum(1 for v in st.session_state.results.values() if v=="known")
    unknown = total - known
    acc = int((known/total)*100) if total > 0 else 0

    if acc == 100: st.balloons()

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='mem-logo {th}' style='font-size:2rem;letter-spacing:6px;'>Session Complete</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-div {th}'></div>", unsafe_allow_html=True)

    if acc==100: st.success("🎉 Perfect score! Outstanding work!")
    elif acc>=80: st.info("✦ Excellent — you're nearly there!")
    elif acc>=60: st.warning("Keep going — review the hard cards!")
    else: st.error("Don't give up — every attempt builds your knowledge!")

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{acc}%</div><div class='stat-lbl {th}'>Accuracy</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{known}</div><div class='stat-lbl {th}'>Mastered</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{unknown}</div><div class='stat-lbl {th}'>Needs Work</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    fig = go.Figure(go.Pie(
        values=[known, unknown] if known+unknown > 0 else [1,0],
        labels=["Mastered","Needs Work"],
        hole=0.72,
        marker=dict(colors=["#6aaa7a","#aa6a6a"]),
        textinfo="none",
        hovertemplate="%{label}: %{value}<extra></extra>"
    ))
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10,b=10,l=10,r=10),
        height=180,
        annotations=[dict(
            text=f"<b>{acc}%</b>",
            x=0.5,y=0.5,
            font=dict(size=22,color="#d4b878",family="Cormorant Garamond"),
            showarrow=False
        )]
    )
    st.plotly_chart(fig, use_container_width=True)

    if unknown > 0:
        st.info(f"✦ {unknown} card{'s' if unknown>1 else ''} added to your Weak Deck")

    hard = [cards[i] for i,d in st.session_state.difficulty.items() if d=="hard"]
    if hard:
        with st.expander(f"Cards to review ({len(hard)})"):
            for c in hard:
                st.markdown(f"**Q:** {c['question']}")
                st.markdown(f"*A: {c['answer']}*")
                st.markdown("---")

    pdf_bytes = export_pdf(cards)
    st.download_button("📄 Export as PDF", data=pdf_bytes, file_name="memoria.pdf", mime="application/pdf")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("Try Quiz Mode", use_container_width=True):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
            st.session_state.page = "quiz"
            st.rerun()
    with c2:
        if st.button("Study Again", use_container_width=True):
            st.session_state.card_index = 0
            st.session_state.results = {}
            st.session_state.difficulty = {}
            st.session_state.flipped = False
            st.session_state.page = "flashcard"
            st.rerun()
    with c3:
        if st.button("Home", use_container_width=True):
            go_home(); st.rerun()

# ════════════════════════════════
# QUIZ
# ════════════════════════════════
elif st.session_state.page == "quiz":
    cards = st.session_state.flashcards
    idx = st.session_state.quiz_index
    total = len(cards)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c1:
        if st.button("← Back"):
            st.session_state.page = "summary"; st.rerun()
    with c2:
        pct = int((idx/total)*100)
        st.markdown(f"<div style='text-align:center;font-size:9px;letter-spacing:4px;color:rgba(212,184,120,0.35);text-transform:uppercase;margin-bottom:6px;font-family:Inter,sans-serif;'>Quiz</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='p-track {th}'><div class='p-fill' style='width:{pct}%'></div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='text-align:right;font-size:12px;color:rgba(212,184,120,0.4);font-family:Inter,sans-serif;'>{idx+1}/{total}</div>", unsafe_allow_html=True)

    if idx < total:
        card = cards[idx]
        answered = idx in st.session_state.quiz_answers

        st.markdown(f"""
        <div class='q-card {th}'>
            <div class='c-tag'>Question {idx+1} of {total}</div>
            <div class='q-text {th}'>{card['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        mode = st.radio("", ["✍️  Type answer","🔤  Multiple choice"], horizontal=True, key=f"qm_{idx}", label_visibility="collapsed")

        if "Type" in mode:
            ans = st.text_input("", placeholder="Type your answer...", key=f"a_{idx}", label_visibility="collapsed", disabled=answered)
            if not answered:
                _,mid,_ = st.columns([1,2,1])
                with mid:
                    if st.button("Submit", use_container_width=True):
                        if ans.strip():
                            with st.spinner("Checking..."):
                                try:
                                    j = client.chat.completions.create(
                                        model=model_name,
                                        messages=[{"role":"user","content":f"Is this answer correct or close enough?\nQuestion: {card['question']}\nCorrect: {card['answer']}\nGiven: {ans}\nReply ONLY 'correct' or 'incorrect'."}],
                                        temperature=0.1
                                    )
                                    ok = "correct" in j.choices[0].message.content.strip().lower()
                                    st.session_state.quiz_answers[idx] = {"correct":ok,"user":ans,"right":card['answer']}
                                    if ok: st.session_state.quiz_score += 1
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
        else:
            others = [c['answer'] for i,c in enumerate(cards) if i!=idx]
            wrong = random.sample(others, min(3,len(others)))
            opts = wrong + [card['answer']]
            random.shuffle(opts)
            if not answered:
                for opt in opts:
                    if st.button(opt, key=f"o_{idx}_{opt[:20]}", use_container_width=True):
                        ok = opt == card['answer']
                        st.session_state.quiz_answers[idx] = {"correct":ok,"user":opt,"right":card['answer']}
                        if ok: st.session_state.quiz_score += 1
                        st.rerun()

        if answered:
            d = st.session_state.quiz_answers[idx]
            if d["correct"]: st.success("✦ Correct!")
            else: st.error(f"✗ Answer: {d['right']}")
            _,mid,_ = st.columns([1,2,1])
            with mid:
                if idx+1 < total:
                    if st.button("Next →", use_container_width=True):
                        st.session_state.quiz_index += 1; st.rerun()
                else:
                    if st.button("See Results →", use_container_width=True):
                        st.session_state.page = "quiz_results"; st.rerun()

# ════════════════════════════════
# QUIZ RESULTS
# ════════════════════════════════
elif st.session_state.page == "quiz_results":
    cards = st.session_state.flashcards
    total = len(cards)
    score = st.session_state.quiz_score
    acc = int((score/total)*100) if total > 0 else 0

    if acc == 100: st.balloons()

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='mem-logo {th}' style='font-size:2rem;letter-spacing:6px;'>Quiz Complete</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='g-div {th}'></div>", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{score}/{total}</div><div class='stat-lbl {th}'>Score</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{acc}%</div><div class='stat-lbl {th}'>Accuracy</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card {th}'><div class='stat-num {th}'>{st.session_state.streak}</div><div class='stat-lbl {th}'>Streak</div></div>", unsafe_allow_html=True)

    if acc==100: st.success("🎉 Perfect! You've mastered this material!")
    elif acc>=80: st.info("✦ Great work! A little more practice needed.")
    elif acc>=60: st.warning("Getting there — review weak cards and retry.")
    else: st.error("Keep studying — every attempt builds knowledge!")

    wrong = [(cards[i],d) for i,d in st.session_state.quiz_answers.items() if not d["correct"]]
    if wrong:
        with st.expander(f"Review incorrect answers ({len(wrong)})"):
            for card,d in wrong:
                st.markdown(f"**Q:** {card['question']}")
                st.markdown(f"*Your answer:* {d['user']}")
                st.markdown(f"*Correct:* {d['right']}")
                st.markdown("---")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.button("Retake Quiz", use_container_width=True):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
            st.session_state.page = "quiz"
            st.rerun()
    with c2:
        if st.button("Back to Home", use_container_width=True):
            go_home(); st.rerun()
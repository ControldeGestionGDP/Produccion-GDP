import base64
import hmac
import html
import io
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None

# =========================================================
# RUTAS Y CONFIGURACIÓN
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

icon_image = Image.open(LOGO_PATH) if LOGO_PATH.exists() else "🐔"

st.set_page_config(
    page_title="Gestión Producción • GDP",
    page_icon=icon_image,
    layout="wide",
    initial_sidebar_state="collapsed",
)

COLOR1 = "#ed701b"
CTID = "42fc96b3-c018-482d-8ada-cab81720489e"
URL_PENDIENTE = "https://app.powerbi.com"


def pbi(link_id, extra=""):
    return f"https://app.powerbi.com/links/{link_id}?ctid={CTID}&pbi_source=linkShare{extra}"


# =========================================================
# CLAVES DE ACCESO
# Recomendado: definirlas en .streamlit/secrets.toml (o en los
# Secrets de Streamlit Cloud) para que no queden en GitHub:
#   [passwords]
#   "Administración de Personal" = "..."
# =========================================================
PASSWORDS_DEFAULT = {
    "Pollo Carne": "pollo2026",
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Cerdos": "cerdos2026",
    "Planta de Beneficio": "beneficio2026",
    "Comité Operacional": "comite2026",
    "Gerencia": "gerencia2026",
}


def get_passwords():
    try:
        return {**PASSWORDS_DEFAULT, **dict(st.secrets["passwords"])}
    except Exception:
        return PASSWORDS_DEFAULT


PASSWORDS = get_passwords()

# =========================================================
# CATÁLOGO DE REPORTES (única fuente de verdad)
# Gerencia ve automáticamente TODOS los reportes de la lista
# =========================================================
AREAS = {
    "Reproductoras": ("Producción de huevo fértil", "repro.jpg"),
    "Incubación": ("Gestión de nacimientos", "incubacion.jpg"),
    "Pollo Carne": ("Producción de engorde", "pollo.jpg"),
    "Cerdos": ("Producción porcina", "cerdos.jpg"),
    "Planta de Beneficio": ("Procesamiento", "beneficio.jpg"),
    "Comité Operacional": ("Seguimiento estratégico", "comite.jpg"),
}

REP, INC, PC, CER, PB, CO = list(AREAS)
GER = "Gerencia"

REPORTES = [
    # ---- Reproductoras ----
    dict(area=REP, title="Tablero Reproductoras", desc="Indicadores clave",
         img="repro.jpg", url=pbi("MTKKKyrmOC")),
    dict(area=REP, title="Temperatura de Almacén de Huevos", desc="Monitoreo térmico de huevos",
         img="temp_huevos.jpg", url=pbi("0fi95g4HTJ")),
    dict(area=REP, title="Temperatura de Vacunas", desc="Monitoreo de conservación",
         img="temp_vacunas.jpg", url=pbi("fC-cGaZZEX")),
    dict(area=REP, title="Proyección de Lotes a 65 Semanas", desc="Simulación y escenarios de cierre",
         img="proyeccion_65_semanas.jpg", url=pbi("emcxo7s7Yy")),
    # ---- Incubación ----
    dict(area=INC, title="Tablero Incubación", desc="Performance de planta",
         img="incubacion.jpg",
         url=pbi("FvBE6glv0p", "&bookmarkGuid=eb3a6db3-05d1-4d87-8b75-e55208fa6824")),
    dict(area=INC, title="Seguimiento Log Tag", desc="Trazabilidad",
         img="logtag.jpg", url=pbi("ZRsbRrhCSk")),
    dict(area=INC, title="Análisis Días de Almacenamiento", desc="Evaluación de almacenamiento de huevos",
         img="dias_almacenamiento.jpg", url=pbi("tNUMx0BO14")),
    # ---- Pollo Carne ----
    dict(area=PC, title="Seguimiento de Lotes Activos", desc="Control en tiempo real",
         img="lotes.jpg",
         url=pbi("g2lIM309oY", "&bookmarkGuid=b43e89fd-62e5-4778-aaab-8915d510ba46")),
    dict(area=PC, title="Pollo Carne", desc="Indicadores productivos",
         img="pollo.jpg", url=pbi("FlfN0CCJ4H")),
    dict(area=PC, title="Faltantes y Sobrantes", desc="Control de diferencias",
         img="faltantes.jpg", url=pbi("IEWsDiPysE")),
    dict(area=PC, title="JSA Loreto", desc="Seguimiento JSA",
         img="loreto.jpg", url=pbi("X0jy7jd1vs")),
    dict(area=PC, title="JSA Pucallpa", desc="Seguimiento JSA",
         img="pucallpa.jpg", url=pbi("2uz6wNBWep")),
    dict(area=PC, title="JSA Calzada", desc="Seguimiento JSA",
         img="calzada.jpg", url=pbi("-0gJXo1gss")),
    dict(area=PC, title="JSA Picota", desc="Seguimiento JSA",
         img="picota.jpg", url=pbi("MqnHkulYmd")),
    dict(area=PC, title="Análisis Ombligo y Tarso", desc="Pollo Bebé",
         img="ombligo_tarso.jpg",
         url=pbi("zuRKkFX2eS", "&bookmarkGuid=b12eb673-757b-4d68-a842-43d8098e93c4")),
    # ---- Cerdos ----
    dict(area=CER, title="Reporte General", desc="Producción porcina",
         img="cerdos.jpg",
         url=pbi("a_19Nuy4nY", "&bookmarkGuid=a90f008c-b27a-4034-b71c-2214e8f7c251")),
    dict(area=CER, title="Evaluacion de Nacimientos", desc="Control de nacimientos",
         img="cerdosnacimiento.jpg", url=pbi("hEx6l1PkFt")),
    dict(area=CER, title="Litter Scatter", desc="Analítica de camadas",
         img="litterscatter.jpg", url=pbi("uc_hQHv1GM")),
    # ---- Planta de Beneficio ----
    dict(area=PB, title="Reporte Diario", desc="Operación diaria",
         img="diario.jpg",
         url=pbi("VlI_Pqq3rS", "&bookmarkGuid=53e6330f-bc0c-4549-b247-0f0a729bb3ec")),
    dict(area=PB, title="Reporte General", desc="Visión consolidada",
         img="general.jpg", url=pbi("qBUR10mRm3")),
    # ---- Comité Operacional ----
    dict(area=CO, title="Incubación", desc="Performance de planta",
         img="incubacion.jpg",
         url=pbi("i0vEmizvmC", "&bookmarkGuid=51869a31-aa63-4cef-b59d-c7a23e3a9560")),
    dict(area=CO, title="Pollo Carne", desc="Indicadores productivos",
         img="pollo.jpg", url=pbi("gFrq9kBwfI")),
    dict(area=CO, title="Planeamiento", desc="Proyección y control",
         img="planeamiento.jpg", url=pbi("EWURfVV_Ae")),
    dict(area=CO, title="Resultados Generales - PAB", desc="Visión consolidada y PAB",
         img="pab.jpg", url=pbi("kMBXBLnFJs")),
]

# =========================================================
# SESSION STATE
# =========================================================
st.session_state.setdefault("area", None)
st.session_state.setdefault("auth", False)

# =========================================================
# ESTILOS
# =========================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root{--blue:#ed701b;--blue-d:#d95d0b;--navy:#2a1103;--ink:#0f172a;--mute:#64748b;
--line:#e2e8f0;--bg:#ffffff;--ok:#12a150;--warn:#d98e04;}
html,body,[class*="css"]{font-family:'Plus Jakarta Sans',-apple-system,sans-serif !important;}
.stApp,[data-testid="stAppViewContainer"]{background:var(--bg) !important;}
[data-testid="stHeader"]{background:transparent !important;}
[data-testid="stSidebar"],[data-testid="stSidebarCollapseButton"],[data-testid="stToolbar"],
[data-testid="stDecoration"],#MainMenu,footer{display:none !important;}
.block-container{max-width:1180px;padding-top:1.4rem !important;}

/* ---------- HERO ---------- */
.hero{position:relative;overflow:hidden;border-radius:28px;padding:44px 48px;margin:10px 0 30px;
background:linear-gradient(120deg,#2a1103 0%,#7a3308 55%,#ed701b 120%);color:#fff;
display:flex;justify-content:space-between;align-items:center;gap:24px;
box-shadow:0 30px 60px -28px rgba(42,17,3,.6);}
.hero::before{content:"";position:absolute;inset:0;opacity:.35;
background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),
linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:44px 44px;
mask-image:radial-gradient(ellipse at 80% 20%,#000 0%,transparent 70%);}
.orb{position:absolute;border-radius:50%;filter:blur(60px);opacity:.55;animation:drift 14s ease-in-out infinite alternate;}
.o1{width:340px;height:340px;background:#ff9a3c;top:-120px;right:8%;}
.o2{width:280px;height:280px;background:#d95d0b;bottom:-140px;left:30%;animation-delay:-6s;}
@keyframes drift{to{transform:translate(-60px,40px) scale(1.15);}}
.hero-in{position:relative;z-index:1;max-width:720px;}
.kicker{font-size:.86rem;font-weight:600;color:#ffcfa8;margin-bottom:10px;}
.hero h1{font-size:2.5rem;line-height:1.12;font-weight:800;letter-spacing:-.035em;margin:0 0 10px;color:#fff;}
.hero p{font-size:1rem;color:#ffe3cc;margin:0 0 26px;font-weight:500;}
.stats{display:flex;gap:12px;flex-wrap:wrap;}
.stat{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(8px);
border-radius:16px;padding:12px 20px;min-width:118px;}
.stat b{display:block;font-size:1.65rem;font-weight:800;line-height:1.1;}
.stat span{font-size:.78rem;color:#ffd9bd;font-weight:600;}
.hero-logo{position:relative;z-index:1;background:#fff;border-radius:24px;padding:16px;width:120px;height:120px;
display:flex;align-items:center;justify-content:center;box-shadow:0 20px 40px -12px rgba(0,0,0,.45);flex-shrink:0;}
.hero-logo img{max-width:100%;max-height:100%;}

/* ---------- TARJETAS ---------- */
.rcard{position:relative;display:block;text-decoration:none !important;background:#fff;border:1px solid var(--line);
border-radius:22px;overflow:hidden;margin-bottom:14px;color:var(--ink) !important;
box-shadow:0 12px 30px -18px rgba(15,23,42,.14);transition:transform .4s cubic-bezier(.16,1,.3,1),box-shadow .4s,border-color .4s;
animation:rise .7s cubic-bezier(.16,1,.3,1) both;animation-delay:var(--d,0ms);}
@keyframes rise{from{opacity:0;transform:translateY(22px);}to{opacity:1;transform:none;}}
.rcard:hover{transform:translateY(-8px);border-color:rgba(237,112,27,.4);box-shadow:0 30px 50px -22px rgba(237,112,27,.4);}
.media{position:relative;aspect-ratio:16/9;overflow:hidden;background:#7a3308;}
.rcard .media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;
border-radius:0 !important;margin:0;transition:transform .8s cubic-bezier(.16,1,.3,1);}
.cover{position:absolute;inset:0;z-index:3;border-radius:22px;}
.tt .t{min-height:2.75em;}.td .d{min-height:2.7em;}
.media::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(42,17,3,.5));}
.rcard:hover .media img{transform:scale(1.08);}
.badge{position:absolute;z-index:2;top:14px;left:14px;display:inline-flex;align-items:center;gap:7px;
padding:5px 12px;border-radius:99px;font-size:.72rem;font-weight:700;background:rgba(255,255,255,.94);
box-shadow:0 4px 12px rgba(0,0,0,.12);}
.badge i{width:7px;height:7px;border-radius:50%;background:var(--ok);animation:pulse 1.9s infinite;}
.badge.wip{color:#8a5a00;}.badge.wip i{background:var(--warn);}
.badge.live{color:#0b6b38;}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(18,161,80,.55);}70%{box-shadow:0 0 0 8px rgba(18,161,80,0);}100%{box-shadow:0 0 0 0 rgba(18,161,80,0);}}
.body{padding:20px 22px 20px;}
.t{font-weight:700;font-size:1.05rem;line-height:1.35;}
.d{color:var(--mute);font-size:.88rem;font-weight:500;margin-top:4px;min-height:2.4em;}
.go{display:flex;align-items:center;justify-content:space-between;margin-top:14px;padding-top:14px;
border-top:1px solid var(--line);font-weight:700;font-size:.9rem;color:var(--blue);}
.go svg{transition:transform .35s cubic-bezier(.16,1,.3,1);}
.rcard:hover .go svg{transform:translateX(6px);}
.rcard.wide{display:grid;grid-template-columns:1.1fr 1fr;}
.rcard.wide .media{aspect-ratio:auto;min-height:280px;}
.rcard.wide .body{display:flex;flex-direction:column;justify-content:center;padding:28px 34px;}
.rcard.wide .t{font-size:1.45rem;}

/* ---------- BOTONES ---------- */
.stButton,[data-testid="stButton"],[data-testid="stFormSubmitButton"]{width:100% !important;}
div.stButton>button,[data-testid="stFormSubmitButton"]>button{display:flex;align-items:center;justify-content:center;}
div.stButton>button,[data-testid="stFormSubmitButton"]>button{width:100%;height:48px;border:none !important;
border-radius:14px !important;color:#fff !important;font-weight:700 !important;font-size:.95rem !important;
background:linear-gradient(135deg,var(--blue),var(--blue-d)) !important;
box-shadow:0 8px 18px -8px rgba(237,112,27,.6) !important;transition:all .3s cubic-bezier(.16,1,.3,1) !important;}
div.stButton>button:hover,[data-testid="stFormSubmitButton"]>button:hover{transform:translateY(-2px);
box-shadow:0 14px 26px -10px rgba(237,112,27,.7) !important;}
.st-key-btn_open_modal button,.st-key-btn_back button,.st-key-btn_login_volver button{background:#fff !important;
color:#334155 !important;border:1.5px solid #cbd5e1 !important;border-radius:99px !important;height:42px !important;
box-shadow:none !important;}
.st-key-btn_open_modal button:hover,.st-key-btn_back button:hover,.st-key-btn_login_volver button:hover{
background:#f1f5f9 !important;border-color:#94a3b8 !important;}

/* ---------- OTROS ---------- */
[data-testid="stForm"]{border:none !important;padding:0 !important;background:transparent !important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--blue) !important;}
div[data-baseweb="input"]{border-radius:14px !important;background:#fff !important;border:1.5px solid var(--line) !important;}
div[data-baseweb="input"]:focus-within{border-color:var(--blue) !important;box-shadow:0 0 0 4px rgba(237,112,27,.14);}
.stTabs [data-baseweb="tab-list"]{gap:6px;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{font-weight:700;color:var(--mute);padding:10px 18px;}
.stTabs [aria-selected="true"]{color:var(--blue) !important;}
.sect{font-weight:800;font-size:1.15rem;margin:22px 0 14px;color:var(--ink);}
.login-card{background:#fff;border:1px solid var(--line);border-radius:24px;padding:34px 30px 18px;text-align:center;
box-shadow:0 30px 60px -30px rgba(237,112,27,.35);position:relative;overflow:hidden;margin-bottom:14px;}
.login-card::before{content:"";position:absolute;inset:0 0 auto 0;height:5px;background:linear-gradient(90deg,#2a1103,#ed701b,#ff9a3c);}
.login-ico{width:58px;height:58px;margin:0 auto 14px;border-radius:18px;background:#fdeee2;color:var(--blue);
display:flex;align-items:center;justify-content:center;}
div[data-testid="stDialog"]>div{border-radius:28px !important;}
@media (max-width:760px){.hero{flex-direction:column;align-items:flex-start;padding:30px 24px;}
.hero h1{font-size:1.8rem;}.rcard.wide{grid-template-columns:1fr;}.hero-logo{display:none;}}
@media (prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important;}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================================================
# UTILIDADES
# =========================================================
ARROW = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def img_uri(name, width=900):
    for p in (ASSETS_DIR / name, ASSETS_DIR / "default.jpg"):
        if p.exists():
            try:
                im = Image.open(p).convert("RGB")
                im.thumbnail((width, width))
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=82, optimize=True)
                return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
            except Exception:
                pass
    return ""


@st.cache_data(show_spinner=False)
def logo_uri():
    if LOGO_PATH.exists():
        return "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return ""


def saludo():
    try:
        now = datetime.now(ZoneInfo("America/Lima"))
    except Exception:
        now = datetime.now()
    s = "Buenos días" if now.hour < 12 else "Buenas tardes" if now.hour < 19 else "Buenas noches"
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{s} · {dias[now.weekday()]} {now.day} de {meses[now.month - 1]} de {now.year}"


def hero(kicker, title, sub, stats):
    chips = "".join(f'<div class="stat"><b>{v}</b><span>{l}</span></div>' for v, l in stats)
    logo = logo_uri()
    logo_html = f'<div class="hero-logo"><img src="{logo}" alt="logo"></div>' if logo else ""
    st.markdown(
        f'<div class="hero"><div class="orb o1"></div><div class="orb o2"></div>'
        f'<div class="hero-in"><div class="kicker">{kicker}</div><h1>{title}</h1><p>{sub}</p>'
        f'<div class="stats">{chips}</div></div>{logo_html}</div>',
        unsafe_allow_html=True,
    )


def card_html(r, i=0, wide=False, tall=(False, False)):
    img = img_uri(r["img"])
    media = f'<img src="{img}" alt="">' if img else ""
    badge = ('<span class="badge wip"><i></i>En construcción</span>' if r.get("wip")
             else '<span class="badge live"><i></i>Disponible</span>')
    cls = "rcard" + (" wide" if wide else "") + (" tt" if tall[0] else "") + (" td" if tall[1] else "")
    return (f'<div class="{cls}" style="--d:{i * 70}ms"><div class="media">{media}{badge}</div>'
            f'<div class="body"><div class="t">{r["title"]}</div><div class="d">{r["desc"]}</div>'
            f'<div class="go"><span>Abrir dashboard</span>{ARROW}</div></div>'
            f'<a class="cover" href="{html.escape(r["url"])}" target="_blank" rel="noopener" '
            f'aria-label="Abrir {html.escape(r["title"])}"></a></div>')


def grid(items, cols=3):
    if not items:
        st.info("No hay reportes que coincidan con tu búsqueda. Prueba con otra palabra o borra el filtro.")
        return
    if len(items) == 1:
        st.markdown(card_html(items[0], 0, wide=True), unsafe_allow_html=True)
        return
    for s in range(0, len(items), cols):
        row = items[s:s + cols]
        tall = (any(len(r["title"]) > 26 for r in row), any(len(r["desc"]) > 30 for r in row))
        for c, (j, r) in zip(st.columns(cols), enumerate(row)):
            with c:
                st.markdown(card_html(r, s + j, tall=tall), unsafe_allow_html=True)


def area_card(name, i):
    desc, img = AREAS[name]
    n = sum(1 for r in REPORTES if r["area"] == name)
    uri = img_uri(img)
    media = f'<img src="{uri}" alt="">' if uri else ""
    st.markdown(
        f'<div class="rcard" style="--d:{i * 90}ms"><div class="media">{media}'
        f'<span class="badge live"><i></i>{n} dashboard{"s" if n != 1 else ""}</span></div>'
        f'<div class="body"><div class="t">{name}</div><div class="d">{desc}</div></div></div>',
        unsafe_allow_html=True,
    )


def go_home():
    st.session_state.area = None
    st.session_state.auth = False
    st.session_state.pop("q", None)
    st.rerun()


def check_pwd(area, pwd):
    return hmac.compare_digest(pwd.encode(), PASSWORDS[area].encode())


# =========================================================
# MODAL GERENCIA
# =========================================================
@st.dialog(" ")
def modal_gerencia():
    st.markdown(
        '<div style="text-align:center"><div style="font-weight:800;font-size:1.3rem;color:var(--blue);">'
        'Panel Ejecutivo</div><span class="badge live" style="position:static;display:inline-flex;margin:10px 0;">'
        '<i></i>Acceso gerencial</span><p style="color:#64748b;font-size:.9rem;">Ingresa tu clave para ver '
        'el panel consolidado de todas las áreas.</p></div>',
        unsafe_allow_html=True,
    )
    with st.form("form_gerencia"):
        pwd = st.text_input("Contraseña gerencial", type="password", placeholder="••••••••")
        if st.form_submit_button("Ingresar al panel", use_container_width=True):
            if check_pwd(GER, pwd):
                st.session_state.area, st.session_state.auth = GER, True
                st.rerun()
            else:
                st.error("Clave incorrecta. Verifica e intenta de nuevo.")


# =========================================================
# VISTAS
# =========================================================
def portal():
    total = len(REPORTES)
    wip = sum(1 for r in REPORTES if r.get("wip"))
    c1, c2 = st.columns([2.6, 1.4], vertical_alignment="center")
    with c1:
        st.markdown('<div style="font-weight:800;color:#0f172a;font-size:1.02rem;">Grupo Don Pollo '
                    '<span style="color:var(--blue)">•</span> Gerencia de Planeamiento Estratégico</div>',
                    unsafe_allow_html=True)
    with c2:
        if st.button("Acceso Gerencial", key="btn_open_modal", use_container_width=True):
            modal_gerencia()

    stats = [(total - wip, "dashboards disponibles"), (len(AREAS), "áreas estratégicas")]
    if wip:
        stats.append((wip, "en construcción"))
    hero(saludo(), "Ecosistema Digital • Producción",
         "Todos tus reportes en un solo lugar. Elige un área para ver sus indicadores.", stats)

    names = list(AREAS)
    for s in range(0, len(names), 3):
        for c, (j, name) in zip(st.columns(3), enumerate(names[s:s + 3])):
            i = s + j
            with c:
                area_card(name, i)
                if st.button("Ingresar", key=f"go_{i}", use_container_width=True):
                    st.session_state.area, st.session_state.auth = name, False
                    st.rerun()


def login(area):
    _, mid, _ = st.columns([1, 1.3, 1])
    with mid:
        st.markdown(
            f'<div class="login-card"><div class="login-ico"><svg width="26" height="26" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></div>'
            f'<div style="font-size:1.4rem;font-weight:800;color:var(--blue);">{area}</div>'
            f'<div style="color:#64748b;font-size:.9rem;margin:6px 0 4px;">Ingresa tu clave de acceso</div></div>',
            unsafe_allow_html=True,
        )
        with st.form("form_login"):
            pwd = st.text_input("Contraseña", type="password", placeholder="••••••••")
            if st.form_submit_button("Ingresar", use_container_width=True):
                if check_pwd(area, pwd):
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Acceso denegado: clave incorrecta.")
        if st.button("Volver", key="btn_login_volver", use_container_width=True):
            go_home()


def dashboard(area):
    ger = area == GER
    items = REPORTES if ger else [r for r in REPORTES if r["area"] == area]

    # Diagnóstico visible si falta la fotografía del reporte nuevo.
    if any(r["img"] == "dias_almacenamiento.jpg" for r in items):
        foto = ASSETS_DIR / "dias_almacenamiento.jpg"
        if not foto.is_file():
            st.warning("No se encontró assets/dias_almacenamiento.jpg en el servidor. Verifica que el archivo esté en la misma rama que app.py.")
        else:
            try:
                with Image.open(foto) as prueba:
                    prueba.verify()
            except Exception:
                st.warning("El archivo assets/dias_almacenamiento.jpg existe, pero no es una imagen válida. Vuelve a subirlo como JPG.")

    back, _ = st.columns([1.4, 4.6])
    with back:
        if st.button("← Cambiar área", key="btn_back", use_container_width=True):
            go_home()

    if ger:
        hero(saludo(), "Panel Gerencial", "Vista consolidada de Producción: todas las áreas en un solo lugar.",
             [(len(items), "dashboards"), (len(AREAS), "áreas")])
    else:
        hero(saludo(), area, "Módulos e indicadores disponibles para esta área.", [(len(items), "dashboards")])

    q = st.text_input("Buscar", key="q", placeholder="🔎  Buscar reporte por nombre o tema…",
                      label_visibility="collapsed").strip().lower()

    def filt(lst):
        return [r for r in lst if q in f'{r["title"]} {r["desc"]}'.lower()]

    if ger:
        tabs = st.tabs(["Todas las áreas"] + list(AREAS))
        with tabs[0]:
            hubo = False
            for name in AREAS:
                lst = filt([r for r in items if r["area"] == name])
                if lst:
                    hubo = True
                    st.markdown(f'<div class="sect">{name}</div>', unsafe_allow_html=True)
                    grid(lst)
            if not hubo:
                grid([])
        for tab, name in zip(tabs[1:], AREAS):
            with tab:
                grid(filt([r for r in items if r["area"] == name]))
    else:
        grid(filt(items))


# =========================================================
# ENRUTADOR
# =========================================================
if st.session_state.area is None:
    portal()
elif not st.session_state.auth:
    login(st.session_state.area)
else:
    dashboard(st.session_state.area)

# =========================================================
# FOOTER
# =========================================================
st.markdown(f"""
<div style="margin-top:70px;padding:24px 0 30px;border-top:1px solid #e1e8f0;text-align:center;">
<div style="font-size:.88rem;font-weight:700;color:#334155;margin-bottom:4px;">
Grupo Don Pollo <span style="color:{COLOR1};font-weight:800;">•</span> Gerencia de Planeamiento Estratégico</div>
<div style="font-size:.78rem;color:#94a3b8;font-weight:500;">© 2026 Ecosistema Digital de Reportes. Todos los derechos reservados.</div>
</div>
""", unsafe_allow_html=True)

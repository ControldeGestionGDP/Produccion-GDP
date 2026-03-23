import streamlit as st
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Producción • GDP",
    page_icon="🐥",
    layout="wide"
)

# Paleta de Producción
COLOR1 = "#8dbf44"
COLOR2 = "#0d897d"
COLOR3 = "#129b94"

# =========================================================
# RUTA BASE
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# =========================================================
# PASSWORDS
# =========================================================
PASSWORDS = {
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Producción Pollo Carne": "pollo2026",
    "Gerencia": "gerencia2026"
}

# =========================================================
# SESSION STATE
# =========================================================
if "area" not in st.session_state:
    st.session_state.area = None

if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================================================
# 🔐 SIDEBAR GERENCIA
# =========================================================
with st.sidebar:
    st.markdown(f"""
    <style>
    .executive-card-sidebar {{
        background: white; border-radius: 18px; padding: 20px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 20px;
    }}
    .exe-title-sidebar {{ font-weight: 800; color: {COLOR2}; margin-bottom: 5px; font-size: 1.1rem; text-transform: uppercase; }}
    .exe-status-sidebar {{ display: inline-block; padding: 3px 12px; background: #FEE2E2; color: #EF4444; border-radius: 12px; font-size: 0.7rem; font-weight: 700; margin-bottom: 12px; }}
    </style>
    <div class="executive-card-sidebar">
        <div style="font-size: 2.2rem; margin-bottom: 10px;">🐣</div>
        <div class="exe-title-sidebar">Panel Ejecutivo</div>
        <div class="exe-status-sidebar">● ACCESO RESTRINGIDO</div>
        <p style="color: #64748b; font-size: 0.85rem; line-height: 1.4; margin-top: 5px;">
            Ecosistema de Producción consolidado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("INGRESAR", use_container_width=True):
        st.session_state.area = "Gerencia"
        st.session_state.auth = False
        st.rerun()
    
    st.markdown("---")
    st.caption("© 2026 • Grupo Don Pollo")

# =========================================================
# ESTILOS (TU LÓGICA + FIX DE TAMAÑO IMAGEN)
# =========================================================
st.markdown(f"""
<style>
html, body {{ font-family: "Segoe UI", sans-serif; background: #f4f6fb; }}
.main-title {{ font-size: 2.6rem; font-weight: 800; color: {COLOR2}; }}
.subtitle {{ color: #6b7280; margin-bottom: 12px; }}
.title-accent {{ height: 4px; width: 120px; background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3}); border-radius: 4px; margin-bottom: 28px; }}
.card {{
    border-radius: 18px; overflow: hidden; box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    margin-bottom: 8px; background: white; transition: all 0.35s ease;
}}
.card:hover {{ transform: translateY(-8px); box-shadow: 0 25px 55px rgba(0,0,0,0.18); }}

/* --- FIX PARA TAMAÑO DE IMAGEN IGUALES --- */
.stImage > img {{
    height: 200px !important;
    object-fit: cover !important;
    border-radius: 18px 18px 0 0;
}}

.card-title {{ padding: 15px; font-weight: 700; font-size: 1.1rem; min-height: 95px; }}
div.stButton > button {{
    width: 100%; background: linear-gradient(90deg, {COLOR1}, {COLOR2}, {COLOR3});
    color: white; border-radius: 10px; border: none; font-weight: 700; height: 45px;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIONES
# =========================================================
def report_card(titulo, desc, img_relative_path):
    img_path = ASSETS_DIR / img_relative_path
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if img_path.exists():
        st.image(img_path.read_bytes(), use_container_width=True)
    else:
        st.image("https://via.placeholder.com/800x400.png?text=Don+Pollo", use_container_width=True)
    
    st.markdown(f'<div class="card-title">{titulo}<br><span style="font-weight:400;color:#6b7280;font-size:0.95rem;">{desc}</span></div></div>', unsafe_allow_html=True)

def open_panel_button(url, key):
    st.markdown(f"""
    <a href="{url}" target="_blank" style="text-decoration:none;">
        <div style="width:100%; text-align:center; padding:12px; border-radius:10px; font-weight:700; color:white;
            background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3}); box-shadow: 0 6px 14px rgba(0,0,0,0.15);">
            Abrir Dashboard
        </div>
    </a>""", unsafe_allow_html=True)

# =========================================================
# PORTAL
# =========================================================
if st.session_state.area is None:
    st.markdown('<div class="main-title">Ecosistema Digital • Producción</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Seleccione el área de interés</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        report_card("Reproductoras", "Gestión de lotes y huevos fértiles", "Reproductoras.jpg")
        if st.button("Ingresar", key="repro"):
            st.session_state.area = "Reproductoras"; st.rerun()
    with col2:
        report_card("Incubación", "Control de nacimientos y planta", "Incubacion.jpg")
        if st.button("Ingresar", key="inc"):
            st.session_state.area = "Incubación"; st.rerun()
    with col3:
        report_card("Producción Pollo Carne", "Engorde y salida a venta", "PolloCarne.jpg")
        if st.button("Ingresar", key="pollo"):
            st.session_state.area = "Producción Pollo Carne"; st.rerun()

else:
    area = st.session_state.area
    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f'<div class="login-box"><div style="font-size:1.4rem;font-weight:700;color:{COLOR2};text-align:center;">{area}</div><div style="text-align:center;color:#6b7280;margin-bottom:20px;">Ingrese su contraseña</div></div>', unsafe_allow_html=True)
            pwd = st.text_input("Contraseña", type="password")
            if st.button("Ingresar"):
                if pwd == PASSWORDS[area]: st.session_state.auth = True; st.rerun()
                else: st.error("Contraseña incorrecta")
            if st.button("Volver"): st.session_state.area = None; st.rerun()
    else:
        st.markdown(f'<div class="main-title">{area}</div>', unsafe_allow_html=True)
        st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)
        if st.button("Cambiar área"): st.session_state.area = None; st.session_state.auth = False; st.rerun()
        st.divider()

        if area == "Gerencia":
            st.subheader("Reproductoras e Incubación")
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("Postura Semanal", "Resumen de lotes", "Reproductoras.jpg")
                open_panel_button("https://app.powerbi.com", "g1")
            with col2:
                report_card("Nacimientos", "Efectividad de planta", "Incubacion.jpg")
                open_panel_button("https://app.powerbi.com", "g2")
            with col3:
                report_card("Calidad de Pollito", "Descarte y primera", "Pollito.jpg")
                open_panel_button("https://app.powerbi.com", "g3")
            
            st.divider()
            st.subheader("Producción Carne")
            col_g4, col_g5, _ = st.columns(3)
            with col_g4:
                report_card("Engorde", "Conversión alimenticia", "PolloCarne.jpg")
                open_panel_button("https://app.powerbi.com", "g4")
            with col_g5:
                report_card("Ventas", "Programación comercial", "Ventas.jpg")
                open_panel_button("https://app.powerbi.com", "g5")

        elif area == "Reproductoras":
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("Postura", "Control diario", "Reproductoras.jpg")
                open_panel_button("https://app.powerbi.com", "r1")

        elif area == "Incubación":
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("Nacimientos", "Efectividad de planta", "Incubacion.jpg")
                open_panel_button("https://app.powerbi.com", "i1")

        elif area == "Producción Pollo Carne":
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("Engorde", "Conversión alimenticia", "PolloCarne.jpg")
                open_panel_button("https://app.powerbi.com", "p1")

st.markdown("<center style='color:#9ca3af;margin-top:40px;'>Gerencia de Control de Gestión • Grupo Don Pollo</center>", unsafe_allow_html=True)

import streamlit as st
from pathlib import Path

# =========================================================
# CONFIGURACIÓN (ESTILO CORPORATIVO PRODUCCIÓN)
# =========================================================
st.set_page_config(
    page_title="Producción • Grupo Don Pollo",
    page_icon="🐣",
    layout="wide"
)

# Colores extraídos de la paleta enviada
COLOR1 = "#8dbf44"  # Verde Claro
COLOR2 = "#0d897d"  # Esmeralda
COLOR3 = "#129b94"  # Turquesa

# =========================================================
# RUTA BASE
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# =========================================================
# PASSWORDS (ACCESOS POR UNIDAD)
# =========================================================
PASSWORDS = {
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Producción Pollo Carne": "pollo2026",
    "Cerdos": "cerdos2026",
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
# 🔐 SIDEBAR GERENCIA (ESTILO UNIFICADO PRODUCCIÓN)
# =========================================================
with st.sidebar:
    st.markdown(f"""
    <style>
    .executive-card-sidebar {{
        background: white;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }}
    .exe-title-sidebar {{
        font-weight: 800;
        color: {COLOR2};
        margin-bottom: 5px;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .exe-status-sidebar {{
        display: inline-block;
        padding: 3px 12px;
        background: #FEE2E2;
        color: #EF4444;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-bottom: 12px;
    }}
    </style>
    
    <div class="executive-card-sidebar">
        <div style="font-size: 2.2rem; margin-bottom: 10px;">🚜</div>
        <div class="exe-title-sidebar">Panel Producción</div>
        <div class="exe-status-sidebar">● ACCESO RESTRINGIDO</div>
        <p style="color: #64748b; font-size: 0.85rem; line-height: 1.4; margin-top: 5px;">
            Control estratégico de todas las unidades biológicas del Grupo Don Pollo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("INGRESAR GERENCIA", use_container_width=True, help="Solo directores"):
        st.session_state.area = "Gerencia"
        st.session_state.auth = False
        st.rerun()
    
    st.markdown("---")
    st.caption("© 2026 • Grupo Don Pollo")

# =========================================================
# ESTILOS CSS (BLOQUE PREMIUM)
# =========================================================
st.markdown(f"""
<style>
html, body {{
    font-family: "Segoe UI", sans-serif;
    background: #f4f6fb;
    animation: fadeInBody 0.6s ease-in-out;
}}
@keyframes fadeInBody {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.main-title {{
    font-size: 2.6rem;
    font-weight: 800;
    color: {COLOR2};
    animation: slideInTitle 0.7s ease;
}}
@keyframes slideInTitle {{
    from {{ opacity: 0; transform: translateX(-10px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}
.subtitle {{
    color: #6b7280;
    margin-bottom: 12px;
}}
.title-accent {{
    height: 4px;
    width: 120px;
    background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3});
    border-radius: 4px;
    margin-bottom: 28px;
    animation: expandBar 0.8s ease forwards;
}}
@keyframes expandBar {{
    from {{ width: 0; }}
    to {{ width: 120px; }}
}}
.login-box {{
    background: white;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0 25px 55px rgba(0,0,0,0.12);
    border-top: 5px solid {COLOR2};
    animation: fadeInCard 0.5s ease;
}}
.card {{
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    margin-bottom: 8px;
    background: white;
    transition: all 0.35s cubic-bezier(.4,0,.2,1);
}}
.card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 25px 55px rgba(0,0,0,0.18);
}}
.card img {{
    border-radius: 18px;
    transition: transform 0.4s ease;
}}
.card:hover img {{
    transform: scale(1.04);
}}
.card-title {{
    padding: 15px;
    font-weight: 700;
    font-size: 1.1rem;
}}
div.stButton > button {{
    width: 100%;
    background: linear-gradient(90deg, {COLOR1}, {COLOR2}, {COLOR3});
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
    height: 45px;
    transition: all 0.25s ease;
}}
div.stButton > button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 22px rgba(0,0,0,0.2);
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIONES MAESTRAS
# =========================================================
def report_card(titulo, desc, img_relative_path):
    img_path = ASSETS_DIR / img_relative_path
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if img_path.exists():
        st.image(img_path.read_bytes(), use_container_width=True)
    else:
        st.image("https://via.placeholder.com/800x400.png?text=PRODUCCION+IMAGE", use_container_width=True)
    st.markdown(f"""
        <div class="card-title">
            {titulo}<br>
            <span style="font-weight:400;color:#6b7280;font-size:0.95rem;">{desc}</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def open_panel_button(url, key):
    st.markdown(f"""
    <a href="{url}" target="_blank" style="text-decoration:none;">
        <div style="width:100%; text-align:center; padding:12px; border-radius:10px; font-weight:700; color:white;
            background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3}); box-shadow: 0 6px 14px rgba(0,0,0,0.15);">
            Abrir Reporte Power BI
        </div>
    </a>
    """, unsafe_allow_html=True)

# =========================================================
# PORTAL DE PRODUCCIÓN
# =========================================================
if st.session_state.area is None:
    st.markdown('<div class="main-title">Ecosistema • Producción</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Gestión estratégica de unidades biológicas</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        report_card("Reproductoras", "Gestión de lotes y producción de huevos", "Repro_Main.jpg")
        if st.button("Entrar a Reproductoras", key="btn_repro"):
            st.session_state.area = "Reproductoras"; st.session_state.auth = False; st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        report_card("Producción Pollo Carne", "Monitoreo de engorde y sanidad", "Pollo_Main.jpg")
        if st.button("Entrar a Pollo Carne", key="btn_pollo"):
            st.session_state.area = "Producción Pollo Carne"; st.session_state.auth = False; st.rerun()

    with col2:
        report_card("Incubación", "Control de planta y nacimientos", "Incuba_Main.jpg")
        if st.button("Entrar a Incubación", key="btn_inc"):
            st.session_state.area = "Incubación"; st.session_state.auth = False; st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        report_card("Cerdos", "Indicadores de unidad porcina", "Cerdos_Main.jpg")
        if st.button("Entrar a Cerdos", key="btn_cerdos"):
            st.session_state.area = "Cerdos"; st.session_state.auth = False; st.rerun()

else:
    area = st.session_state.area

    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f"""<div class="login-box">
                <div style="font-size:1.4rem;font-weight:700;color:{COLOR2};text-align:center;">{area}</div>
                <div style="text-align:center;color:#6b7280;margin-bottom:20px;">Seguridad de Producción</div>
            </div>""", unsafe_allow_html=True)
            pwd = st.text_input("Ingrese Contraseña", type="password")
            if st.button("Validar Acceso", use_container_width=True):
                if pwd == PASSWORDS[area]:
                    st.session_state.auth = True; st.rerun()
                else: st.error("Contraseña incorrecta")
            if st.button("Regresar", use_container_width=True):
                st.session_state.area = None; st.rerun()

    else:
        st.markdown(f'<div class="main-title">{area}</div>', unsafe_allow_html=True)
        st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)
        if st.button("← Cambiar Unidad"):
            st.session_state.area = None; st.session_state.auth = False; st.rerun()
        st.divider()

        # ================= VISTA GERENCIAL (TODO) =================
        if area == "Gerencia":
            # REPRO E INCUBA
            st.subheader("🧬 Ciclo Biológico Inicial")
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("Reproductoras", "KPI General", "Repro_General.jpg")
                open_panel_button("https://app.powerbi.com", "g1")
            with col2:
                report_card("Incubación", "KPI General", "Incuba_General.jpg")
                open_panel_button("https://app.powerbi.com", "g2")
            with col3:
                report_card("Cerdos", "KPI General", "Cerdos_General.jpg")
                open_panel_button("https://app.powerbi.com", "g3")
            
            st.divider()
            # POLLO CARNE FULL
            st.subheader("🍗 Producción Pollo Carne")
            c1, c2, c3 = st.columns(3)
            with c1:
                report_card("JSA Pollo", "Seguimiento Administrativo", "Pollo_JSA.jpg")
                open_panel_button("https://app.powerbi.com", "g4")
            with c2:
                report_card("Comité Técnico", "Sanidad y Nutrición", "Pollo_Comite.jpg")
                open_panel_button("https://app.powerbi.com", "g5")
            with c3:
                report_card("Rep. General Pollo", "Consolidado Engorde", "Pollo_General.jpg")
                open_panel_button("https://app.powerbi.com", "g6")
            
            st.markdown("#### Detalle Operativo Pollo Carne")
            c4, c5, _ = st.columns(3)
            with c4:
                report_card("Sobrantes y Faltantes", "Control de Mermas", "Pollo_Sobrantes.jpg")
                open_panel_button("https://app.powerbi.com", "g7")
            with c5:
                report_card("Seguimiento de Lotes", "Trazabilidad Campo", "Pollo_Lotes.jpg")
                open_panel_button("https://app.powerbi.com", "g8")

        # ================= REPRODUCTORAS / INCUBACION / CERDOS =================
        elif area in ["Reproductoras", "Incubación", "Cerdos"]:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                report_card(f"Reporte General {area}", f"Panel consolidado de {area}", f"{area}_General.jpg")
                open_panel_button("https://app.powerbi.com", f"btn_{area}")

        # ================= POLLO CARNE (VISTA AREA) =================
        elif area == "Producción Pollo Carne":
            st.subheader("Dashboard Principal")
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("JSA", "Junta Seguimiento Administrativo", "Pollo_JSA.jpg")
                open_panel_button("https://app.powerbi.com", "p1")
            with col2:
                report_card("Comité Técnico", "Análisis Sanitario", "Pollo_Comite.jpg")
                open_panel_button("https://app.powerbi.com", "p2")
            with col3:
                report_card("Reporte General", "KPI Maestro", "Pollo_General.jpg")
                open_panel_button("https://app.powerbi.com", "p3")
            
            st.divider()
            st.subheader("Sub-Reportes de Gestión")
            col_s1, col_s2, _ = st.columns(3)
            with col_s1:
                report_card("Sobrantes y Faltantes", "Consolidado de mermas", "Pollo_Sobrantes.jpg")
                open_panel_button("https://app.powerbi.com", "p4")
            with col_s2:
                report_card("Seguimiento de Lotes", "Trazabilidad por Galpón", "Pollo_Lotes.jpg")
                open_panel_button("https://app.powerbi.com", "p5")

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    f"<center style='color:#9ca3af;margin-top:40px;border-top: 1px solid #e2e8f0; padding-top:20px;'>"
    f"Gerencia de Control de Gestión • <b>Dirección de Producción</b> • Grupo Don Pollo</center>",
    unsafe_allow_html=True
)

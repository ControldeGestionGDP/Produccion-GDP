import streamlit as st
from pathlib import Path

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Producción • Grupo Don Pollo",
    page_icon="🐣",
    layout="wide"
)

# Colores extraídos de la paleta de Producción
COLOR1 = "#8dbf44"  # Verde Claro
COLOR2 = "#0d897d"  # Esmeralda
COLOR3 = "#129b94"  # Turquesa

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
    "Cerdos": "cerdos2026",
    "Gerencia": "gerencia2026"
}

if "area" not in st.session_state: st.session_state.area = None
if "auth" not in st.session_state: st.session_state.auth = False

# =========================================================
# ESTILOS CSS (BLOQUE UNIFICADO)
# =========================================================
st.markdown(f"""
<style>
html, body {{ font-family: "Segoe UI", sans-serif; background: #f4f6fb; }}
.main-title {{ font-size: 2.6rem; font-weight: 800; color: {COLOR2}; }}
.title-accent {{ height: 4px; width: 120px; background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3}); border-radius: 4px; margin-bottom: 28px; }}

/* Tarjeta y Ajuste de Imagen */
.card {{
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    margin-bottom: 15px;
    background: white;
    transition: all 0.35s ease;
}}
.card img {{
    width: 100%;
    height: 220px; /* Altura fija para uniformidad */
    object-fit: cover; /* Recorta la imagen para llenar el espacio sin deformar */
}}
.card-title {{ padding: 15px; font-weight: 700; font-size: 1.1rem; }}

/* Botones estilo original - Ancho Completo */
div.stButton > button {{
    width: 100%;
    background: linear-gradient(90deg, {COLOR1}, {COLOR2}, {COLOR3});
    color: white;
    border-radius: 0px 0px 18px 18px; /* Redondeado solo abajo para unir a la card */
    border: none;
    font-weight: 700;
    height: 50px;
    margin-top: -15px; /* Une el botón a la tarjeta superior */
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
        st.image("https://via.placeholder.com/800x400.png?text=Don+Pollo+Produccion", use_container_width=True)
    st.markdown(f"""
        <div class="card-title">
            {titulo}<br>
            <span style="font-weight:400;color:#6b7280;font-size:0.95rem;">{desc}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def open_panel_button(url, key):
    st.markdown(f"""
    <a href="{url}" target="_blank" style="text-decoration:none;">
        <div style="width:100%; text-align:center; padding:15px; border-radius:10px; font-weight:700; color:white;
            background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3}); box-shadow: 0 6px 14px rgba(0,0,0,0.15);">
            Abrir Dashboard
        </div>
    </a>
    """, unsafe_allow_html=True)

# =========================================================
# PORTAL DE PRODUCCIÓN
# =========================================================
if st.session_state.area is None:
    st.markdown('<div class="main-title">Ecosistema Digital • Producción</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        report_card("Reproductoras", "Gestión de lotes y huevos", "Repro_Main.jpg")
        if st.button("Ingresar", key="btn_repro"):
            st.session_state.area = "Reproductoras"; st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        report_card("Cerdos", "Unidad de porcinos", "Cerdos_Main.jpg")
        if st.button("Ingresar", key="btn_cerdos"):
            st.session_state.area = "Cerdos"; st.rerun()

    with col2:
        report_card("Incubación", "Control de nacimientos", "Incuba_Main.jpg")
        if st.button("Ingresar", key="btn_inc"):
            st.session_state.area = "Incubación"; st.rerun()

    with col3:
        report_card("Producción Pollo Carne", "Monitoreo de engorde", "Pollo_Main.jpg")
        if st.button("Ingresar", key="btn_pollo"):
            st.session_state.area = "Producción Pollo Carne"; st.rerun()

else:
    area = st.session_state.area
    if not st.session_state.auth:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f'<div class="login-box"><div style="font-size:1.4rem;font-weight:700;color:{COLOR2};text-align:center;">{area}</div><div style="text-align:center;color:#6b7280;margin-bottom:20px;">Ingrese su contraseña</div></div>', unsafe_allow_html=True)
            pwd = st.text_input("Contraseña", type="password")
            if st.button("Validar Acceso", use_container_width=True):
                if pwd == PASSWORDS[area]:
                    st.session_state.auth = True; st.rerun()
                else: st.error("Contraseña incorrecta")
    else:
        st.markdown(f'<div class="main-title">{area}</div>', unsafe_allow_html=True)
        st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)
        if st.button("← Cambiar área"):
            st.session_state.area = None; st.session_state.auth = False; st.rerun()
        st.divider()

        # Lógica de sub-niveles para Pollo Carne
        if area == "Producción Pollo Carne":
            c1, c2, c3 = st.columns(3)
            with c1:
                report_card("JSA", "Seguimiento Administrativo", "Pollo_JSA.jpg")
                open_panel_button("https://app.powerbi.com", "u1")
            with c2:
                report_card("Comité Técnico", "Sanidad y Nutrición", "Pollo_Comite.jpg")
                open_panel_button("https://app.powerbi.com", "u2")
            with c3:
                report_card("Reporte General", "Consolidado Engorde", "Pollo_General.jpg")
                open_panel_button("https://app.powerbi.com", "u3")
            
            # Segunda fila para los específicos de Pollo Carne
            c4, c5, _ = st.columns(3)
            with c4:
                report_card("Sobrantes y Faltantes", "Control de mermas", "Pollo_Sobrantes.jpg")
                open_panel_button("https://app.powerbi.com", "u4")
            with c5:
                report_card("Seguimiento de Lotes", "Trazabilidad campo", "Pollo_Lotes.jpg")
                open_panel_button("https://app.powerbi.com", "u5")
        
        elif area == "Gerencia":
            # Vista unificada para Gerencia
            st.subheader("🧬 Gestión Biológica")
            cg1, cg2, cg3 = st.columns(3)
            with cg1: report_card("Reproductoras", "KPI General", "Repro_General.jpg"); open_panel_button("#", "g1")
            with cg2: report_card("Incubación", "KPI General", "Incuba_General.jpg"); open_panel_button("#", "g2")
            with cg3: report_card("Cerdos", "KPI General", "Cerdos_General.jpg"); open_panel_button("#", "g3")
            
            st.divider()
            st.subheader("🍗 Engorde Pollo Carne")
            cg4, cg5, cg6 = st.columns(3)
            with cg4: report_card("JSA", "Adm. Pollo", "Pollo_JSA.jpg"); open_panel_button("#", "g4")
            with cg5: report_card("Comité Técnico", "Sanidad", "Pollo_Comite.jpg"); open_panel_button("#", "g5")
            with cg6: report_card("Reporte General", "Consolidado", "Pollo_General.jpg"); open_panel_button("#", "g6")

        else: # Unidades simples: Reproductoras, Incubación, Cerdos
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card(f"Reporte General", f"Dashboard {area}", f"{area}_General.jpg")
                open_panel_button("https://app.powerbi.com", "simple")

st.markdown("<center style='color:#9ca3af;margin-top:40px;'>Gerencia de Control de Gestión • Grupo Don Pollo</center>", unsafe_allow_html=True)

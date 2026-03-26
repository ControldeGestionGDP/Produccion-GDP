import streamlit as st
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Gerencia de Producción",
    page_icon="🐔",
    layout="wide"
)

COLOR1 = "#1071B8"
COLOR2 = "#2E3788"
COLOR3 = "#C4579B"

# =========================================================
# RUTA BASE
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# =========================================================
# PASSWORDS
# =========================================================
PASSWORDS = {
    "Pollo Carne": "pollo2026",
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Cerdos": "cerdos2026",
    "Planta de Beneficio": "beneficio2026"
}

# =========================================================
# SESSION STATE
# =========================================================
if "area" not in st.session_state:
    st.session_state.area = None

if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================================================
# ESTILOS (MISMO TUYO)
# =========================================================
st.markdown(f"""
<style>
.main-title {{
    font-size: 2.6rem;
    font-weight: 800;
    color: {COLOR2};
}}
.title-accent {{
    height: 4px;
    width: 120px;
    background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3});
    border-radius: 4px;
    margin-bottom: 28px;
}}
.card {{
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    margin-bottom: 8px;
    background: white;
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
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIONES
# =========================================================
def report_card(titulo, desc, img):
    img_path = ASSETS_DIR / img

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if img_path.exists():
        st.image(img_path.read_bytes(), use_container_width=True)

    st.markdown(f"""
        <div class="card-title">
            {titulo}<br>
            <span style="font-weight:400;color:#6b7280;font-size:0.9rem;">
                {desc}
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def open_panel_button(url):
    st.markdown(f"""
    <a href="{url}" target="_blank">
        <div style="
            text-align:center;
            padding:12px;
            border-radius:10px;
            font-weight:700;
            color:white;
            background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3});
        ">
            Abrir Dashboard
        </div>
    </a>
    """, unsafe_allow_html=True)

# =========================================================
# PORTAL PRINCIPAL
# =========================================================
if st.session_state.area is None:

    st.markdown('<div class="main-title">Gerencia de Producción</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        report_card("Pollo Carne", "Producción de engorde", "pollo.jpg")
        if st.button("Ingresar", key="pc"):
            st.session_state.area = "Pollo Carne"
            st.rerun()

    with col2:
        report_card("Reproductoras", "Producción de huevo fértil", "repro.jpg")
        if st.button("Ingresar", key="rep"):
            st.session_state.area = "Reproductoras"
            st.rerun()

    with col3:
        report_card("Incubación", "Gestión de nacimientos", "incubacion.jpg")
        if st.button("Ingresar", key="inc"):
            st.session_state.area = "Incubación"
            st.rerun()

    col4, col5, _ = st.columns(3)

    with col4:
        report_card("Cerdos", "Producción porcina", "cerdos.jpg")
        if st.button("Ingresar", key="cer"):
            st.session_state.area = "Cerdos"
            st.rerun()

    with col5:
        report_card("Planta de Beneficio", "Procesamiento", "beneficio.jpg")
        if st.button("Ingresar", key="pb"):
            st.session_state.area = "Planta de Beneficio"
            st.rerun()

# =========================================================
# LOGIN
# =========================================================
else:

    area = st.session_state.area

    if not st.session_state.auth:

        st.subheader(area)
        pwd = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            if pwd == PASSWORDS[area]:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

        if st.button("Volver"):
            st.session_state.area = None
            st.rerun()

    else:

        st.markdown(f'<div class="main-title">{area}</div>', unsafe_allow_html=True)
        st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

        if st.button("Cambiar área"):
            st.session_state.area = None
            st.session_state.auth = False
            st.rerun()

        st.divider()

        # =========================================================
        # POLLO CARNE
        # =========================================================
        if area == "Pollo Carne":
            col1, col2, col3 = st.columns(3)

            with col1:
                report_card("Seguimiento de Lotes Activos", "Control en tiempo real", "lotes.jpg")
                open_panel_button("URL_AQUI")

            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button("URL_AQUI")

            with col3:
                report_card("Faltantes y Sobrantes", "Control de diferencias", "faltantes.jpg")
                open_panel_button("URL_AQUI")

        # =========================================================
        # REPRODUCTORAS
        # =========================================================
        elif area == "Reproductoras":
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                report_card("Tablero Reproductoras", "Indicadores clave", "repro.jpg")
                open_panel_button("URL_AQUI")

        # =========================================================
        # INCUBACIÓN
        # =========================================================
        elif area == "Incubación":
            col1, col2 = st.columns(2)

            with col1:
                report_card("Tablero Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button("URL_AQUI")

            with col2:
                report_card("Seguimiento Log Tag", "Trazabilidad", "logtag.jpg")
                open_panel_button("URL_AQUI")

        # =========================================================
        # CERDOS
        # =========================================================
        elif area == "Cerdos":
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                report_card("Reporte General", "Producción porcina", "cerdos.jpg")
                open_panel_button("URL_AQUI")

        # =========================================================
        # PLANTA DE BENEFICIO
        # =========================================================
        elif area == "Planta de Beneficio":
            col1, col2 = st.columns(2)

            with col1:
                report_card("Reporte Diario", "Operación diaria", "diario.jpg")
                open_panel_button("URL_AQUI")

            with col2:
                report_card("Reporte General", "Visión consolidada", "general.jpg")
                open_panel_button("URL_AQUI")

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    "<center style='color:#9ca3af;margin-top:40px;'>Gerencia de Producción • Grupo Don Pollo</center>",
    unsafe_allow_html=True
)

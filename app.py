import streamlit as st
import base64
from pathlib import Path
from datetime import datetime

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA (SIDEBAR CONTRAÍDO POR DEFECTO)
# =============================================================================
st.set_page_config(
    page_title="PRODUCCIÓN | GRUPO DON POLLO",
    page_icon="🐥",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# =============================================================================
# 2. DEFINICIÓN DE IDENTIDAD VISUAL
# =============================================================================
COLOR_PRIMARY = "#0d897d"    # Teal Principal
COLOR_SECONDARY = "#8dbf44"  # Verde Don Pollo
COLOR_ACCENT = "#129b94"     # Turquesa Operativo
COLOR_BACKGROUND = "#F1F5F9"
COLOR_CARD = "#FFFFFF"
COLOR_TEXT = "#1E293B"

# =============================================================================
# 3. GESTIÓN DE RUTAS Y ACTIVOS
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def get_base64(file_path):
    """Función de codificación para imágenes"""
    try:
        if file_path.exists():
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error crítico en activo {file_path.name}: {e}")
    return ""

# =============================================================================
# 4. INYECCIÓN DE CSS (HEADER LIMPIO Y BOTONES ANCHO TOTAL)
# =============================================================================
def local_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700;800&display=swap');

    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
    
    [data-testid="stAppViewContainer"] {{
        background-color: {COLOR_BACKGROUND};
    }}

    /* HEADER ELEGANTE (SIN CUADRO) */
    .header-minimal {{
        margin-bottom: 3.5rem;
        padding-left: 0.5rem;
    }}

    .main-title {{
        font-family: 'Segoe UI', sans-serif;
        color: {COLOR_PRIMARY};
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1.5px;
        line-height: 1;
    }}

    .sub-title {{
        font-family: 'Segoe UI', sans-serif;
        color: #64748b;
        font-size: 1.2rem;
        margin-top: 0.8rem;
    }}

    .title-accent {{
        height: 6px; 
        width: 120px; 
        background: {COLOR_SECONDARY}; 
        border-radius: 10px; 
        margin-top: 1.5rem;
    }}

    /* TARJETAS (CARDS) */
    .card-wrapper {{
        background: {COLOR_CARD};
        border-radius: 22px 22px 0 0; 
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        height: 100%;
    }}

    .card-image-box img {{
        width: 100%;
        height: 240px !important;
        object-fit: cover !important;
    }}

    .card-content {{
        padding: 1.8rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }}

    .card-name {{
        font-size: 1.4rem;
        font-weight: 800;
        color: {COLOR_TEXT};
        margin-bottom: 0.6rem;
    }}

    .card-desc {{
        color: #64748b;
        font-size: 1rem;
        line-height: 1.5;
        min-height: 60px;
    }}

    /* BOTONES: ANCHO TOTAL Y PEGADOS A LA BASE */
    div.stButton > button {{
        width: 100% !important;
        height: 60px !important;
        background: linear-gradient(90deg, {COLOR_PRIMARY} 0%, {COLOR_ACCENT} 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 0 0 22px 22px !important; 
        border: none !important;
        margin-top: -10px !important; 
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px rgba(13, 137, 125, 0.15) !important;
    }}

    div.stButton > button:hover {{
        filter: brightness(1.1) !important;
        transform: translateY(2px) !important;
    }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{
        background-color: white;
        border-right: 1px solid #e2e8f0;
    }}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 5. COMPONENTES DE INTERFAZ
# =============================================================================
def header_component(title, subtitle):
    st.markdown(f"""
    <div class="header-minimal">
        <h1 class="main-title">{title}</h1>
        <p class="sub-title">{subtitle}</p>
        <div class="title-accent"></div>
    </div>
    """, unsafe_allow_html=True)

def card_component(title, description, img_name, button_key, is_external=False, url=""):
    img_path = ASSETS_DIR / img_name
    img_b64 = get_base64(img_path)
    src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else "https://via.placeholder.com/400x240"

    st.markdown(f"""
    <div class="card-wrapper">
        <div class="card-image-box">
            <img src="{src}">
        </div>
        <div class="card-content">
            <div class="card-name">{title}</div>
            <div class="card-desc">{description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if is_external:
        st.markdown(f"""
        <a href="{url}" target="_blank" style="text-decoration: none;">
            <div style="width: 100%; background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_ACCENT}); 
            color: white; text-align: center; padding: 18px; border-radius: 0 0 22px 22px; 
            font-weight: 700; margin-top: -10px; margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            text-transform: uppercase; font-size: 1.1rem; letter-spacing: 1px;">
                ABRIR DASHBOARD
            </div>
        </a>
        """, unsafe_allow_html=True)
    else:
        if st.button(f"INGRESAR", key=button_key):
            st.session_state.area = title
            st.session_state.auth = False
            st.rerun()

# =============================================================================
# 6. LÓGICA DE CONTROL DE ACCESO (CORREGIDO)
# =============================================================================
CREDENTIALS = {
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Producción Pollo Carne": "pollo2026",
    "Gerencia": "gerencia2026"
}

def login_screen(area_target):
    local_css()
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:{COLOR_PRIMARY}; text-align:center;'>ACCESO PRIVADO</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Área seleccionada: <b>{area_target}</b></p>", unsafe_allow_html=True)
    
    password = st.text_input("Ingrese PIN de seguridad", type="password")
    
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button("CONFIRMAR"):
            if password == CREDENTIALS.get(area_target):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("PIN Incorrecto")
    with col_r:
        if st.button("REGRESAR"):
            st.session_state.area = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 7. BLOQUE PRINCIPAL
# =============================================================================
def main():
    local_css()
    
    if "area" not in st.session_state: st.session_state.area = None
    if "auth" not in st.session_state: st.session_state.auth = False

    # A. PANEL DE GERENCIA (CONTRAÍDO)
    with st.sidebar:
        st.markdown("### 🛠️ Administración")
        if st.button("Panel Gerencial"):
            st.session_state.area = "Gerencia"
            st.session_state.auth = False
            st.rerun()
        st.divider()
        st.caption("Grupo Don Pollo - Producción 2026")

    # B. VISTA DE SELECCIÓN
    if st.session_state.area is None:
        header_component("Ecosistema Producción", "Plataforma de visualización estratégica para la toma de decisiones.")
        
        c1, c2, c3 = st.columns(3)
        with c1: card_component("Reproductoras", "Monitoreo de lotes y huevo fértil.", "Reproductoras.jpg", "b_repro")
        with c2: card_component("Incubación", "Control de planta y nacimientos.", "Incubacion.jpg", "b_inc")
        with c3: card_component("Producción Pollo Carne", "Eficiencia alimenticia y logística.", "PolloCarne.jpg", "b_pollo")

    # C. FLUJO DE AUTENTICACIÓN
    elif not st.session_state.auth:
        login_screen(st.session_state.area)

    # D. VISTA INTERNA (DASHBOARDS)
    else:
        current_area = st.session_state.area
        header_component(current_area, f"Indicadores clave de {current_area}")
        
        if st.sidebar.button("⬅ CERRAR SESIÓN"):
            st.session_state.area = None
            st.session_state.auth = False
            st.rerun()

        if current_area == "Gerencia":
            g_c1, g_c2, g_c3 = st.columns(3)
            with g_c1: card_component("Postura", "Lotes activos", "Reproductoras.jpg", "g1", True, "URL_PBI_1")
            with g_c2: card_component("Nacimientos", "Eficiencia planta", "Incubacion.jpg", "g2", True, "URL_PBI_2")
            with g_c3: card_component("Engorde", "FCR / Mortalidad", "PolloCarne.jpg", "g3", True, "URL_PBI_3")

if __name__ == "__main__":
    main()

st.markdown("<br><hr><center style='color:#94a3b8; font-size:0.8rem;'>© 2026 GRUPO DON POLLO | GERENCIA DE CONTROL DE GESTIÓN</center>", unsafe_allow_html=True)

import streamlit as st
import base64
from pathlib import Path
from datetime import datetime

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA (ESTRICTO GESTIÓN HUMANA)
# =============================================================================
st.set_page_config(
    page_title="PRODUCCIÓN | GRUPO DON POLLO",
    page_icon="🐥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. DEFINICIÓN DE IDENTIDAD VISUAL (PALETA PRODUCCIÓN)
# =============================================================================
# Colores corporativos extraídos para el área de Producción
COLOR_PRIMARY = "#0d897d"    # Teal Principal
COLOR_SECONDARY = "#8dbf44"  # Verde Don Pollo
COLOR_ACCENT = "#129b94"     # Turquesa Operativo
COLOR_BACKGROUND = "#F1F5F9"
COLOR_CARD = "#FFFFFF"
COLOR_TEXT = "#1E293B"

# =============================================================================
# 3. GESTIÓN DE RUTAS Y ACTIVOS (RECURSIVO)
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def get_base64(file_path):
    """Función de codificación para persistencia visual de imágenes"""
    try:
        if file_path.exists():
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error crítico en activo {file_path.name}: {e}")
    return ""

# =============================================================================
# 4. INYECCIÓN DE CSS (ESTRUCTURA DE ALTO NIVEL)
# =============================================================================
def local_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700;800&display=swap');

    /* Reset de Contenedor */
    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
    
    /* Fondo Global */
    [data-testid="stAppViewContainer"] {{
        background-color: {COLOR_BACKGROUND};
    }}

    /* HEADER TIPO CEO (Rounded Rectangles) */
    .header-container {{
        background: white;
        padding: 2.5rem;
        border-radius: 25px;
        border-left: 10px solid {COLOR_PRIMARY};
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 3rem;
        transition: all 0.3s ease;
    }}
    
    .header-container:hover {{
        border-left-color: {COLOR_SECONDARY};
    }}

    .main-title {{
        font-family: 'Segoe UI', sans-serif;
        color: {COLOR_PRIMARY};
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        line-height: 1;
    }}

    .sub-title {{
        font-family: 'Segoe UI', sans-serif;
        color: #64748b;
        font-size: 1.2rem;
        margin-top: 0.8rem;
    }}

    /* TARJETAS (CARDS) - LÓGICA DE DIMENSIONAMIENTO FIJO */
    .card-wrapper {{
        background: {COLOR_CARD};
        border-radius: 22px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
    }}

    .card-wrapper:hover {{
        transform: translateY(-10px);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        border-color: {COLOR_SECONDARY};
    }}

    /* CONTROL DE IMAGEN: NO SE MUEVE */
    .card-image-box img {{
        width: 100%;
        height: 230px !important;
        object-fit: cover !important;
        border-bottom: 1px solid #f1f5f9;
    }}

    .card-content {{
        padding: 1.5rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }}

    .card-name {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {COLOR_TEXT};
        margin-bottom: 0.5rem;
        min-height: 32px;
     Muse Sans;
    }}

    .card-desc {{
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1.5rem;
        min-height: 60px; /* Alineación de texto */
    }}

    /* BOTONES: MISMO TAMAÑO SIEMPRE */
    div.stButton > button {{
        width: 100% !important;
        height: 54px !important;
        background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, {COLOR_ACCENT} 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border-radius: 14px !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(13, 137, 125, 0.2) !important;
    }}

    div.stButton > button:hover {{
        filter: brightness(1.1) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(13, 137, 125, 0.3) !important;
    }}

    /* LOGIN CONTAINER */
    .login-wrapper {{
        max-width: 500px;
        margin: 5rem auto;
        background: white;
        padding: 3.5rem;
        border-radius: 30px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.15);
        text-align: center;
        border-top: 8px solid {COLOR_PRIMARY};
    }}

    /* SIDEBAR MODERNO */
    [data-testid="stSidebar"] {{
        background-color: white;
        border-right: 1px solid #e2e8f0;
    }}
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 5. FUNCIONES DE RENDERIZADO (COMPONENTES DEL SISTEMA)
# =============================================================================
def header_component(title, subtitle):
    st.markdown(f"""
    <div class="header-container">
        <h1 class="main-title">{title}</h1>
        <p class="sub-title">{subtitle}</p>
        <div style="height: 6px; width: 100px; background: {COLOR_SECONDARY}; border-radius: 10px; margin-top: 1rem;"></div>
    </div>
    """, unsafe_allow_html=True)

def card_component(title, description, img_name, button_key, is_external=False, url=""):
    img_path = ASSETS_DIR / img_name
    img_b64 = get_base64(img_path)
    
    # Manejo de fallback si la imagen no existe
    src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else "https://via.placeholder.com/400x230?text=Don+Pollo+Produccion"

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
            <div style="width: 100%; background: linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_ACCENT}); 
            color: white; text-align: center; padding: 16px; border-radius: 14px; font-weight: 700; 
            margin-top: -25px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
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
# 6. LÓGICA DE CONTROL DE ACCESO
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
    
    # Logo opcional
    logo_path = ASSETS_DIR / "logo_don_pollo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=180)
    
    st.markdown(f"<h2 style='color:{COLOR_PRIMARY}; margin-bottom:0;'>ACCESO PRIVADO</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#64748b;'>Área seleccionada: <b>{area_target}</b></p>", unsafe_allow_html=True)
    
    password = st.text_input("Ingrese PIN de seguridad", type="password", help="Solicite su clave al administrador de BI")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("CONFIRMAR"):
            if password == CREDENTIALS.get(area_target):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("PIN Incorrecto")
    with c2:
        if st.button("REGRESAR"):
            st.session_state.area = None
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 7. BLOQUE PRINCIPAL (MAIN LOOP)
# =============================================================================
def main():
    local_css()
    
    if "area" not in st.session_state: st.session_state.area = None
    if "auth" not in st.session_state: st.session_state.auth = False

    # A. SELECCIÓN DE UNIDAD DE NEGOCIO
    if st.session_state.area is None:
        header_component("Ecosistema Producción", "Plataforma de visualización estratégica para la toma de decisiones en tiempo real.")
        
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            card_component("Reproductoras", "Monitoreo de lotes, sanidad y productividad de huevo fértil.", "Reproductoras.jpg", "btn_repro")
        with col_2:
            card_component("Incubación", "Control de parámetros de incubación y porcentaje de nacimientos.", "Incubacion.jpg", "btn_inc")
        with col_3:
            card_component("Producción Pollo Carne", "Eficiencia alimenticia, mortalidad y logística de engorde.", "PolloCarne.jpg", "btn_pollo")

    # B. FLUJO DE AUTENTICACIÓN
    elif not st.session_state.auth:
        login_screen(st.session_state.area)

    # C. VISTA DE DASHBOARDS (POST-LOGIN)
    else:
        current_area = st.session_state.area
        header_component(current_area, f"Bienvenido al panel centralizado de {current_area}")
        
        if st.sidebar.button("⬅ CERRAR SESIÓN"):
            st.session_state.area = None
            st.session_state.auth = False
            st.rerun()

        # ÁREA GERENCIAL (Múltiples Reportes)
        if current_area == "Gerencia":
            st.markdown("### 📈 Resumen Operativo")
            g_col1, g_col2, g_col3 = st.columns(3)
            with g_col1:
                card_component("Postura Semanal", "Resumen gerencial de lotes", "Reproductoras.jpg", "g1", True, "URL_PBI_1")
            with g_col2:
                card_component("Nacimientos", "Efectividad de planta", "Incubacion.jpg", "g2", True, "URL_PBI_2")
            with g_col3:
                card_component("Despacho", "Salida a campo", "Pollito.jpg", "g3", True, "URL_PBI_3")
            
            st.divider()
            g_col4, g_col5, _ = st.columns(3)
            with g_col4:
                card_component("Engorde", "FCR y Mortalidad", "PolloCarne.jpg", "g4", True, "URL_PBI_4")
            with g_col5:
                card_component("Comercialización", "Proyección de saca", "Ventas.jpg", "g5", True, "URL_PBI_5")

        # ÁREAS OPERATIVAS (Reporte Único)
        else:
            st.markdown(f"### 📑 Dashboard {current_area}")
            op_col1, _, _ = st.columns(3)
            with op_col1:
                card_component(f"Reporte {current_area}", "Acceso completo a métricas", "default.jpg", "op1", True, "URL_ESPECIFICA")

# =============================================================================
# 8. EJECUCIÓN DEL MÓDULO
# =============================================================================
if __name__ == "__main__":
    main()
    
st.markdown("<br><hr><center style='color:#94a3b8; font-size:0.8rem;'>© 2026 GRUPO DON POLLO | GERENCIA DE CONTROL DE GESTIÓN</center>", unsafe_allow_html=True)

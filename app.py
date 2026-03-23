import streamlit as st
from pathlib import Path
import time

# =========================================================
# ⚙️ CONFIGURACIÓN DE PÁGINA (ESTÁNDAR CORPORATIVO)
# =========================================================
st.set_page_config(
    page_title="Portal de Producción | Grupo Don Pollo",
    page_icon="🐥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de Colores Oficial Don Pollo
COLOR_PRIMARY = "#1071B8"    # Azul Principal
COLOR_SECONDARY = "#2E3788"  # Azul Oscuro (Títulos)
COLOR_ACCENT = "#C4579B"     # Magenta (Acentos)
COLOR_BG = "#F4F7FB"         # Fondo Gris Azulado
COLOR_SUCCESS = "#10B981"    # Verde Status

# =========================================================
# 📂 GESTIÓN DE RUTAS Y RECURSOS
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def check_assets():
    """Valida la existencia de la carpeta de recursos"""
    if not ASSETS_DIR.exists():
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)

check_assets()

# =========================================================
# 🔐 SEGURIDAD Y CREDENCIALES (PRODUCCIÓN 2026)
# =========================================================
# Contraseñas segmentadas por unidad de negocio
PASSWORDS = {
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Producción Pollo Carne": "pollo2026",
    "Cerdos": "cerdos2026",
    "Gerencia General": "gerencia2026"
}

# Inicialización de estados de sesión
if "area_activa" not in st.session_state:
    st.session_state.area_activa = None

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "last_login" not in st.session_state:
    st.session_state.last_login = None

# =========================================================
# 🎨 DISEÑO CSS AVANZADO (LÓGICA VISUAL)
# =========================================================
st.markdown(f"""
<style>
    /* Importación de fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Montserrat', sans-serif;
        background-color: {COLOR_BG};
    }}

    /* Contenedor de Animación */
    .main {{
        animation: fadeIn 0.6s ease-in-out;
    }}
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(15px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Títulos Ejecutivos */
    .title-container {{
        padding: 20px 0px;
        margin-bottom: 30px;
    }}
    .main-title {{
        color: {COLOR_SECONDARY};
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -1.5px;
    }}
    .subtitle {{
        color: #64748B;
        font-size: 1.1rem;
        font-weight: 400;
    }}
    .accent-bar {{
        height: 6px;
        width: 150px;
        background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_ACCENT});
        border-radius: 10px;
        margin-top: 15px;
    }}

    /* Tarjetas de Reporte (Efecto Elevación) */
    .report-card {{
        background: white;
        border-radius: 24px;
        padding: 0px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 25px;
        overflow: hidden;
    }}
    .report-card:hover {{
        transform: translateY(-12px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.1);
        border-color: {COLOR_PRIMARY};
    }}
    .card-content {{
        padding: 25px;
    }}
    .card-tag {{
        display: inline-block;
        background: #E0F2FE;
        color: {COLOR_PRIMARY};
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 12px;
    }}

    /* Botones de Acción */
    .stButton > button {{
        width: 100%;
        border-radius: 14px;
        height: 50px;
        background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, {COLOR_SECONDARY} 100%);
        color: white;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        box-shadow: 0 8px 20px rgba(16, 113, 184, 0.4);
        transform: scale(1.02);
    }}

    /* Estilo Sidebar */
    .sidebar-header {{
        text-align: center;
        padding: 10px;
        background: white;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 🛠️ FUNCIONES MAESTRAS (COMPONENTES)
# =========================================================
def render_header(titulo, subtitulo):
    """Genera el encabezado de cada sección"""
    st.markdown(f"""
        <div class="title-container">
            <div class="main-title">{titulo}</div>
            <div class="subtitle">{subtitulo}</div>
            <div class="accent-bar"></div>
        </div>
    """, unsafe_allow_html=True)

def card_display(titulo, descripcion, tag, imagen):
    """Renderiza la tarjeta visual del reporte"""
    img_path = ASSETS_DIR / imagen
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    
    # Manejo inteligente de imágenes
    if img_path.exists():
        st.image(img_path.read_bytes(), use_container_width=True)
    else:
        st.image("https://via.placeholder.com/800x450.png?text=GDP+PRODUCCION", use_container_width=True)
    
    st.markdown(f"""
        <div class="card-content">
            <span class="card-tag">{tag}</span>
            <div style="font-size: 1.25rem; font-weight: 800; color: {COLOR_SECONDARY};">{titulo}</div>
            <div style="color: #64748B; font-size: 0.9rem; margin-top: 8px;">{descripcion}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def open_powerbi_link(url):
    """Crea un botón estilizado para links de Power BI"""
    st.markdown(f"""
        <a href="{url}" target="_blank" style="text-decoration:none;">
            <div style="background: {COLOR_PRIMARY}; color: white; padding: 14px; 
                 border-radius: 12px; text-align: center; font-weight: 700; 
                 box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
                🚀 ABRIR REPORTE EN VIVO
            </div>
        </a>
    """, unsafe_allow_html=True)

# =========================================================
# 🏢 NAVEGACIÓN LATERAL (SIDEBAR)
# =========================================================
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-header">
            <div style="font-size: 3rem;">🚜</div>
            <div style="font-weight: 800; color: {COLOR_SECONDARY};">CONTROL DE PRODUCCIÓN</div>
            <div style="font-size: 0.7rem; color: #EF4444; font-weight: 700; margin-top: 5px;">
                ● SISTEMA DE ALTA PRIORIDAD
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("📈 VISTA GERENCIAL (CEO)", key="btn_gerencia"):
        st.session_state.area_activa = "Gerencia General"
        st.session_state.autenticado = False
        st.rerun()
    
    st.markdown("<br>"*10, unsafe_allow_html=True)
    st.caption("GRUPO DON POLLO - UNIDAD DE TECNOLOGÍA")
    st.caption("Versión: 2.1.0-PROD (2026)")

# =========================================================
# 🏠 VISTA: SELECCIÓN DE UNIDAD (HOME)
# =========================================================
if st.session_state.area_activa is None:
    render_header("Ecosistema de Producción", "Seleccione la unidad de negocio para visualización de KPIs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        card_display("Reproductoras", "Gestión de lotes de reproducción y huevos.", "BIOLOGÍA", "Main_Repro.jpg")
        if st.button("Gestionar Reproductoras", key="main_repro"):
            st.session_state.area_activa = "Reproductoras"; st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        card_display("Producción Pollo Carne", "Monitoreo de engorde, comités y sanidad.", "CARNE", "Main_Pollo.jpg")
        if st.button("Gestionar Pollo Carne", key="main_pollo"):
            st.session_state.area_activa = "Producción Pollo Carne"; st.rerun()

    with col2:
        card_display("Incubación", "Control de planta, nacimientos y mermas.", "PROCESOS", "Main_Incubacion.jpg")
        if st.button("Gestionar Incubación", key="main_inc"):
            st.session_state.area_activa = "Incubación"; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        card_display("Cerdos", "Eficiencia de la unidad de producción porcina.", "PORCINOS", "Main_Cerdos.jpg")
        if st.button("Gestionar Cerdos", key="main_cerdos"):
            st.session_state.area_activa = "Cerdos"; st.rerun()

# =========================================================
# 🛡️ VISTA: LOGIN Y CONTENIDO PRIVADO
# =========================================================
else:
    area = st.session_state.area_activa
    
    if not st.session_state.autenticado:
        _, login_col, _ = st.columns([1, 1.5, 1])
        with login_col:
            st.markdown(f"""
                <div style="background: white; padding: 45px; border-radius: 25px; 
                     box-shadow: 0 20px 60px rgba(0,0,0,0.1); border-left: 8px solid {COLOR_PRIMARY};">
                    <h2 style="color: {COLOR_SECONDARY}; margin-bottom: 0px;">{area}</h2>
                    <p style="color: #64748B;">Portal de Seguridad Biosegura</p>
                </div>
            """, unsafe_allow_html=True)
            
            password_attempt = st.text_input("Credencial de Acceso", type="password")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("VALIDAR"):
                    if password_attempt == PASSWORDS.get(area):
                        st.session_state.autenticado = True
                        st.success("Acceso Concedido")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Credencial Incorrecta")
            with c_btn2:
                if st.button("VOLVER"):
                    st.session_state.area_activa = None
                    st.rerun()
    
    else:
        # PANELES OPERATIVOS TRAS LOGIN
        render_header(area, "Panel de control y reportes estratégicos")
        
        if st.button("← REGRESAR AL MENÚ PRINCIPAL", use_container_width=False):
            st.session_state.area_activa = None
            st.session_state.autenticado = False
            st.rerun()
        
        st.divider()

        # -----------------------------------------------------
        # 🟢 REPRODUCTORAS / INCUBACIÓN / CERDOS (General)
        # -----------------------------------------------------
        if area in ["Reproductoras", "Incubación", "Cerdos"]:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                card_display("Reporte General", f"Dashboard consolidado de {area}", "KPI MASTER", f"{area}_General.jpg")
                open_powerbi_link("https://app.powerbi.com")
            
            # Bloques para futuras expansiones (Mantenemos la simetría)
            with col_b:
                st.info(f"Reportes adicionales de {area} en fase de desarrollo.")

        # -----------------------------------------------------
        # 🟢 PRODUCCIÓN POLLO CARNE (VISTA DETALLADA)
        # -----------------------------------------------------
        elif area == "Producción Pollo Carne":
            st.subheader("📊 DASHBOARDS DE GESTIÓN TÉCNICA")
            row1_1, row1_2, row1_3 = st.columns(3)
            with row1_1:
                card_display("JSA", "Juntas de Seguimiento Administrativo", "ADMIN", "Pollo_JSA.jpg")
                open_powerbi_link("https://app.powerbi.com")
            with row1_2:
                card_display("Comité Técnico", "Análisis sanitario y de nutrición", "TÉCNICO", "Pollo_Comite.jpg")
                open_powerbi_link("https://app.powerbi.com")
            with row1_3:
                card_display("Reporte General", "KPIs de Engorde Consolidados", "MASTER", "Pollo_General.jpg")
                open_powerbi_link("https://app.powerbi.com")
            
            st.divider()
            st.subheader("🔍 CONTROL DE CAMPO Y LOGÍSTICA")
            row2_1, row2_2, row2_3 = st.columns(3)
            with row2_1:
                card_display("Sobrantes y Faltantes", "Gestión de inventarios en granja", "LOGÍSTICA", "Pollo_Sobrantes.jpg")
                open_powerbi_link("https://app.powerbi.com")
            with row2_2:
                card_display("Seguimiento de Lotes", "Trazabilidad detallada por edad", "PRODUCCIÓN", "Pollo_Lotes.jpg")
                open_powerbi_link("https://app.powerbi.com")

        # -----------------------------------------------------
        # 👑 GERENCIA GENERAL (EL "ALL-IN-ONE")
        # -----------------------------------------------------
        elif area == "Gerencia General":
            st.warning("⚠️ VISTA EJECUTIVA: Acceso total a todas las unidades de producción.")
            
            tabs = st.tabs(["🧬 AVÍCOLA", "🐖 PORCINA", "📍 LOGÍSTICA"])
            
            with tabs[0]: # Avícola
                st.markdown("### Consolidado Avícola")
                g_col1, g_col2, g_col3 = st.columns(3)
                with g_col1:
                    card_display("Reproductoras", "KPI General", "REPRO", "Repro_General.jpg")
                    open_powerbi_link("https://app.powerbi.com")
                with g_col2:
                    card_display("Incubación", "KPI General", "INC", "Inc_General.jpg")
                    open_powerbi_link("https://app.powerbi.com")
                with g_col3:
                    card_display("Pollo Carne", "Rendimiento", "POLLO", "Pollo_General.jpg")
                    open_powerbi_link("https://app.powerbi.com")
            
            with tabs[1]: # Porcina
                st.markdown("### Consolidado Cerdos")
                p_col1, _, _ = st.columns(3)
                with p_col1:
                    card_display("Reporte Cerdos", "Productividad", "CERDOS", "Cerdos_General.jpg")
                    open_powerbi_link("https://app.powerbi.com")

            with tabs[2]: # Logística y Otros
                st.markdown("### Operaciones Especiales")
                l_col1, l_col2, _ = st.columns(3)
                with l_col1:
                    card_display("Sobrantes y Faltantes", "Mermas", "LOG", "Pollo_Sobrantes.jpg")
                    open_powerbi_link("https://app.powerbi.com")
                with l_col2:
                    card_display("Trazabilidad Lotes", "Rastreo", "LOTES", "Pollo_Lotes.jpg")
                    open_powerbi_link("https://app.powerbi.com")

# =========================================================
# 🏁 FOOTER CORPORATIVO
# =========================================================
st.markdown(f"""
    <div style="text-align: center; margin-top: 60px; padding: 20px; color: #94A3B8; font-size: 0.8rem;">
        <hr style="opacity: 0.2;">
        CONTROL DE GESTIÓN • GRUPO DON POLLO<br>
        Desarrollado para la Gerencia de Producción © 2026
    </div>
""", unsafe_allow_html=True)

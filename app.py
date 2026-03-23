import streamlit as st
from pathlib import Path

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================
st.set_page_config(
    page_title="Producción • GDP",
    page_icon="🐥",
    layout="wide"
)

# Paleta de colores extraída de la identidad visual de Producción
COLOR1 = "#8dbf44"  # Verde claro
COLOR2 = "#0d897d"  # Turquesa oscuro
COLOR3 = "#129b94"  # Turquesa medio

# =========================================================
# RUTAS DE ACTIVOS
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# =========================================================
# CREDENCIALES DE ACCESO
# =========================================================
PASSWORDS = {
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Producción Pollo Carne": "pollo2026",
    "Gerencia": "gerencia2026"
}

# =========================================================
# CONTROL DE ESTADO DE SESIÓN
# =========================================================
if "area" not in st.session_state:
    st.session_state.area = None

if "auth" not in st.session_state:
    st.session_state.auth = False


# =========================================================
# 🔐 SIDEBAR DE NAVEGACIÓN EJECUTIVA
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
        <div style="font-size: 2.2rem; margin-bottom: 10px;">🐣</div>
        <div class="exe-title-sidebar">Panel Ejecutivo</div>
        <div class="exe-status-sidebar">● ACCESO RESTRINGIDO</div>
        <p style="color: #64748b; font-size: 0.85rem; line-height: 1.4; margin-top: 5px;">
            Todo el ecosistema de Producción consolidado en una sola vista estratégica para la toma de decisiones.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("INGRESAR AL PANEL", use_container_width=True, help="Solo personal directivo"):
        st.session_state.area = "Gerencia"
        st.session_state.auth = False
        st.rerun()
    
    st.markdown("---")
    st.info("Utilice sus credenciales asignadas para cada módulo técnico.")
    st.caption("© 2026 • Grupo Don Pollo")


# =========================================================
# MOTOR DE ESTILOS CSS (DISEÑO Y ALINEACIÓN)
# =========================================================
st.markdown(f"""
<style>
/* Estabilización de fuentes y fondo */
html, body {{
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: #f4f6fb;
}}

/* Animaciones de entrada */
@keyframes fadeInBody {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.stApp {{
    animation: fadeInBody 0.6s ease-out;
}}

/* Títulos y Subtítulos */
.main-title {{
    font-size: 2.6rem;
    font-weight: 800;
    color: {COLOR2};
    letter-spacing: -0.5px;
}}
.subtitle {{
    color: #64748b;
    margin-bottom: 10px;
    font-size: 1.1rem;
}}
.title-accent {{
    height: 5px;
    width: 140px;
    background: linear-gradient(90deg, {COLOR1}, {COLOR2}, {COLOR3});
    border-radius: 5px;
    margin-bottom: 35px;
}}

/* FIX DE TAMAÑO DE TARJETAS (SOLUCIÓN A IMÁGENES DESIGUALES) */
[data-testid="stImage"] img {{
    height: 220px !important;
    object-fit: cover !important;
    border-radius: 18px 18px 0 0;
}}

.card-container {{
    background: white;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    height: 440px; /* Altura fija total */
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
    transition: all 0.3s ease;
    border: 1px solid #f1f5f9;
}}

.card-container:hover {{
    transform: translateY(-10px);
    box-shadow: 0 20px 45px rgba(0,0,0,0.15);
}}

.card-body {{
    padding: 20px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.card-text-title {{
    font-weight: 700;
    font-size: 1.2rem;
    color: #1e293b;
    margin-bottom: 8px;
}}

.card-text-desc {{
    font-weight: 400;
    color: #64748b;
    font-size: 0.95rem;
    line-height: 1.4;
}}

/* Estilo de botones del portal */
div.stButton > button {{
    width: 100%;
    background: linear-gradient(90deg, {COLOR1}, {COLOR2}) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 48px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 15px rgba(13, 137, 125, 0.2) !important;
    transition: all 0.3s ease !important;
}}

div.stButton > button:hover {{
    box-shadow: 0 8px 25px rgba(13, 137, 125, 0.35) !important;
    filter: brightness(1.1);
}}

/* Caja de Login */
.login-box-container {{
    background: white;
    padding: 45px;
    border-radius: 24px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.1);
    border-top: 6px solid {COLOR1};
    margin-top: 20px;
}}
</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCIONES DE RENDERIZADO
# =========================================================
def render_report_card(titulo, descripcion, imagen_nombre, key_id):
    """Genera una tarjeta visualmente estandarizada"""
    img_path = ASSETS_DIR / imagen_nombre
    
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    if img_path.exists():
        st.image(img_path.read_bytes(), use_container_width=True)
    else:
        st.image("https://via.placeholder.com/600x400.png?text=Don+Pollo+Produccion", use_container_width=True)
    
    st.markdown(f"""
        <div class="card-body">
            <div>
                <div class="card-text-title">{titulo}</div>
                <div class="card-text-desc">{descripcion}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # El botón se renderiza dentro del mismo bloque de columna para alineación
    btn_click = st.button("Ingresar", key=f"btn_{key_id}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return btn_click

def render_dashboard_button(url, etiqueta):
    """Botón de acción para Power BI"""
    st.markdown(f"""
    <a href="{url}" target="_blank" style="text-decoration:none;">
        <div style="
            width:100%;
            text-align:center;
            padding:14px;
            border-radius:12px;
            font-weight:700;
            color:white;
            background: linear-gradient(90deg, {COLOR2}, {COLOR3});
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        ">
            Visualizar Reporte
        </div>
    </a>
    """, unsafe_allow_html=True)


# =========================================================
# LÓGICA PRINCIPAL DEL PORTAL
# =========================================================
if st.session_state.area is None:
    # --- PANTALLA DE SELECCIÓN DE ÁREA ---
    st.markdown('<div class="main-title">Ecosistema Digital • Producción</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Gestión estratégica de la cadena productiva</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if render_report_card("Reproductoras", "Control de lotes, sanidad y producción de huevos fértiles.", "Reproductoras.jpg", "main_repro"):
            st.session_state.area = "Reproductoras"
            st.session_state.auth = False
            st.rerun()

    with col2:
        if render_report_card("Incubación", "Seguimiento de procesos de carga, transferencia y nacimientos.", "Incubacion.jpg", "main_incuba"):
            st.session_state.area = "Incubación"
            st.session_state.auth = False
            st.rerun()

    with col3:
        if render_report_card("Producción Pollo Carne", "Monitoreo de engorde, conversión alimenticia y logística.", "PolloCarne.jpg", "main_pollo"):
            st.session_state.area = "Producción Pollo Carne"
            st.session_state.auth = False
            st.rerun()

else:
    # --- FLUJO DE AUTENTICACIÓN Y CONTENIDO ---
    area_activa = st.session_state.area

    if not st.session_state.auth:
        # PANTALLA DE LOGIN
        col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
        with col_l2:
            st.markdown(f"""
            <div class="login-box-container">
                <div style="font-size:1.6rem; font-weight:800; color:{COLOR2}; text-align:center; margin-bottom:10px;">
                    {area_activa.upper()}
                </div>
                <div style="text-align:center; color:#64748b; margin-bottom:25px; font-size:1rem;">
                    Introduzca la clave de acceso departamental
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Espacio para el input de Streamlit
            password_input = st.text_input("Clave de Seguridad", type="password", placeholder="••••••••")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🔓 Validar Acceso", use_container_width=True):
                    if password_input == PASSWORDS[area_activa]:
                        st.session_state.auth = True
                        st.rerun()
                    else:
                        st.error("Credencial inválida")
            with col_b2:
                if st.button("⬅️ Regresar", use_container_width=True):
                    st.session_state.area = None
                    st.rerun()
    
    else:
        # --- PANEL DE DASHBOARDS ACTIVOS ---
        st.markdown(f'<div class="main-title">{area_activa}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="subtitle">Paneles de control de {area_activa}</div>', unsafe_allow_html=True)
        st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

        if st.sidebar.button("🔄 Cambiar de Módulo", use_container_width=True):
            st.session_state.area = None
            st.session_state.auth = False
            st.rerun()

        st.divider()

        # =========================================================
        # VISTA GERENCIAL (CONSOLIDADO)
        # =========================================================
        if area_activa == "Gerencia":
            st.subheader("📊 Producción Aves y Planta")
            
            # Fila 1 - Gerencia
            g_col1, g_col2, g_col3 = st.columns(3)
            with g_col1:
                render_report_card("Reproductoras", "Resumen ejecutivo de lotes.", "Reproductoras.jpg", "g_r")
                render_dashboard_button("https://app.powerbi.com", "Ver Dashboard")
            with g_col2:
                render_report_card("Incubación", "KPIs de nacimiento y calidad.", "Incubacion.jpg", "g_i")
                render_dashboard_button("https://app.powerbi.com", "Ver Dashboard")
            with g_col3:
                render_report_card("Pollo Carne", "Conversión y mortalidad general.", "PolloCarne.jpg", "g_p")
                render_dashboard_button("https://app.powerbi.com", "Ver Dashboard")
            
            st.divider()
            
            # Fila 2 - Gerencia
            st.subheader("🐖 Otras Unidades y Costos")
            g_col4, g_col5, g_col6 = st.columns(3)
            with g_col4:
                render_report_card("Cerdos", "Seguimiento de granjas porcinas.", "Cerdos.jpg", "g_c")
                render_dashboard_button("https://app.powerbi.com", "Ver Dashboard")
            with g_col5:
                render_report_card("Costos Producción", "Análisis financiero operativo.", "Costos.jpg", "g_costos")
                render_dashboard_button("https://app.powerbi.com", "Ver Dashboard")
            with g_col6:
                render_report_card("Inventarios Alimento", "Stock en silos y consumo.", "Alimento.jpg", "g_stock")
                render_dashboard_button("https://app.powerbi.com", "Ver Dashboard")

        # =========================================================
        # VISTA REPRODUCTORAS
        # =========================================================
        elif area_activa == "Reproductoras":
            st.subheader("🐣 Gestión de Lotes y Huevos")
            
            r_col1, r_col2, r_col3 = st.columns(3)
            with r_col1:
                render_report_card("Producción Semanal", "Curva de postura vs estándar.", "Reproductoras.jpg", "r_p")
                render_dashboard_button("https://app.powerbi.com", "Dashboard")
            with r_col2:
                render_report_card("Calidad de Huevo", "Clasificación y descartes.", "Huevos.jpg", "r_h")
                render_dashboard_button("https://app.powerbi.com", "Dashboard")
            with r_col3:
                render_report_card("Levante", "Uniformidad y peso de aves.", "Levante.jpg", "r_l")
                render_dashboard_button("https://app.powerbi.com", "Dashboard")
            
            st.divider()
            
            r_col4, r_col5, _ = st.columns(3)
            with r_col4:
                render_report_card("Sanidad", "Programas de vacunación.", "Sanidad.jpg", "r_s")
                render_dashboard_button("https://app.powerbi.com", "Dashboard")
            with r_col5:
                render_report_card("Alimentación", "Consumo diario por lote.", "Alimento_R.jpg", "r_a")
                render_dashboard_button("https://app.powerbi.com", "Dashboard")

        # =========================================================
        # VISTA INCUBACIÓN
        # =========================================================
        elif area_activa == "Incubación":
            st.subheader("🧪 Control de Planta de Incubación")
            
            i_col1, i_col2, i_col3 = st.columns(3)
            with i_col1:
                render_report_card("Nacimientos", "Efectividad y pollito de primera.", "Incubacion.jpg", "i_n")
                render_dashboard_button("https://app.powerbi.com", "Ver Panel")
            with i_col2:
                render_report_card("Carga de Máquinas", "Ocupación de incubadoras.", "Maquinas.jpg", "i_m")
                render_dashboard_button("https://app.powerbi.com", "Ver Panel")
            with i_col3:
                render_report_card("Pérdida de Humedad", "Monitoreo de procesos térmicos.", "Humedad.jpg", "i_h")
                render_dashboard_button("https://app.powerbi.com", "Ver Panel")

        # =========================================================
        # VISTA POLLO CARNE
        # =========================================================
        elif area_activa == "Producción Pollo Carne":
            st.subheader("🍗 Engorde y Salida a Venta")
            
            p_col1, p_col2, p_col3 = st.columns(3)
            with p_col1:
                render_report_card("Engorde Campo", "Peso proyectado vs real.", "PolloCarne.jpg", "p_e")
                render_dashboard_button("https://app.powerbi.com", "Acceder")
            with p_col2:
                render_report_card("Conversión Alimenticia", "Eficiencia de alimento por kg.", "Conversion.jpg", "p_c")
                render_dashboard_button("https://app.powerbi.com", "Acceder")
            with p_col3:
                render_report_card("Saca y Logística", "Programación de despachos.", "Saca.jpg", "p_s")
                render_dashboard_button("https://app.powerbi.com", "Acceder")

# =========================================================
# PIE DE PÁGINA INSTITUCIONAL
# =========================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; border-top: 1px solid #e2e8f0; padding-top: 25px; margin-top: 50px;">
        <span style="color:#9ca3af; font-size:0.9rem;">
            Gerencia de Control de Gestión • Gestión de Datos de Producción (GDP) • <b>Grupo Don Pollo 2026</b>
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

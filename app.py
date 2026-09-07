from pathlib import Path
import streamlit as st
from PIL import Image

# =========================================================
# RUTAS DE ARCHIVOS
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

# =========================================================
# CARGAR ICONO/LOGO DE LA EMPRESA
# =========================================================
if LOGO_PATH.exists():
    icon_image = Image.open(LOGO_PATH)
else:
    icon_image = "🐔"

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================
st.set_page_config(
    page_title="Gestión Producción • GDP",
    page_icon=icon_image,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Paleta Naranja Corporativa Solicitada
COLOR1 = "#ed701b"

# URL Por defecto para reportes sin enlace aún
URL_PENDIENTE = "https://app.powerbi.com"

# =========================================================
# PASSWORDS
# =========================================================
PASSWORDS = {
    "Pollo Carne": "pollo2026",
    "Reproductoras": "repro2026",
    "Incubación": "incuba2026",
    "Cerdos": "cerdos2026",
    "Planta de Beneficio": "beneficio2026",
    "Gerencia": "gerencia2026",
    "Comité Operacional": "comite2026",
}

# =========================================================
# SESSION STATE
# =========================================================
if "area" not in st.session_state:
    st.session_state.area = None

if "auth" not in st.session_state:
    st.session_state.auth = False

# =========================================================
# OCULTAR BARRA LATERAL Y AJUSTAR CONTENEDOR BLANCO
# =========================================================
st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# ESTILOS VISUALES - FONDO BLANCO PURO (ESTILO APP 24)
# =========================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
}}

/* FONDO COMPLETAMENTE BLANCO */
.stApp, [data-testid="stHeader"], [data-testid="stAppViewContainer"] {{
    background-color: #ffffff !important;
    background-image: none !important;
}}

.main-title {{
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, {COLOR1} 0%, #d95d0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
    line-height: 1.2;
}}

.subtitle {{
    color: #64748b;
    font-size: 0.98rem;
    font-weight: 500;
    margin-top: 4px;
}}

.title-accent {{
    height: 4px;
    width: 80px;
    background: linear-gradient(90deg, {COLOR1}, #f97316);
    border-radius: 99px;
    margin-top: 16px;
    margin-bottom: 28px;
    box-shadow: 0 4px 12px rgba(237, 112, 27, 0.2);
}}

/* TARJETAS ESTÁNDAR */
.card {{
    border-radius: 20px;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
    margin-bottom: 12px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}}

.card:hover {{
    transform: translateY(-8px) scale(1.01);
    background: #ffffff;
    border-color: rgba(237, 112, 27, 0.3);
    box-shadow: 0 25px 40px -12px rgba(237, 112, 27, 0.18);
}}

.card img {{
    border-radius: 20px 20px 0 0;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

.card:hover img {{
    transform: scale(1.06);
}}

.card-title {{
    padding: 20px;
    font-weight: 700;
    font-size: 1.05rem;
    color: #0f172a;
    line-height: 1.4;
}}

/* BOTONES GENERALES (NARANJA DE LA MARCA) */
div.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, {COLOR1} 0%, #d95d0b 100%) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    height: 48px !important;
    box-shadow: 0 6px 16px rgba(237, 112, 27, 0.22) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}

div.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 25px rgba(237, 112, 27, 0.35) !important;
    background: linear-gradient(135deg, #d95d0b 0%, #c24e05 100%) !important;
}}

/* SOBREESCRITURA DIRECTA POR ARIA-LABEL PARA ACCESO GERENCIAL (PLOMO) */
div.stButton > button[aria-label="Acceso Gerencial"] {{
    background: #f1f5f9 !important;
    color: #475569 !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 99px !important;
    height: 42px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
}}

div.stButton > button[aria-label="Acceso Gerencial"]:hover {{
    background: #e2e8f0 !important;
    color: #0f172a !important;
    border-color: #94a3b8 !important;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08) !important;
    transform: translateY(-2px) !important;
}}

/* SOBREESCRITURA DIRECTA POR ARIA-LABEL PARA CAMBIAR ÁREA */
div.stButton > button[aria-label="← Cambiar área"] {{
    background: transparent !important;
    color: #64748b !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 99px !important;
    height: 40px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}

div.stButton > button[aria-label="← Cambiar área"]:hover {{
    background: #f1f5f9 !important;
    color: #0f172a !important;
    border-color: #94a3b8 !important;
    transform: translateY(-1px) !important;
}}

/* ESTILIZACIÓN DEL MODAL */
div[data-testid="stDialog"] > div {{
    background: #ffffff !important;
    border-radius: 28px !important;
    border: 1px solid rgba(237, 112, 27, 0.15) !important;
    box-shadow: 0 30px 60px -12px rgba(237, 112, 27, 0.25) !important;
    padding: 32px !important;
}}

div[data-testid="stDialog"] header {{
    background: transparent !important;
}}

.exe-modal-header {{
    text-align: center;
    padding-bottom: 8px;
}}

.exe-title-modal {{
    font-weight: 800;
    color: {COLOR1};
    font-size: 1.35rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 10px;
    margin-bottom: 6px;
}}

.exe-badge-modal {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    background: rgba(254, 226, 226, 0.85);
    color: #dc2626;
    border: 1px solid rgba(252, 165, 165, 0.6);
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    margin-bottom: 12px;
}}

.pulse-dot {{
    width: 6px;
    height: 6px;
    background-color: #dc2626;
    border-radius: 50%;
    animation: pulse 1.8s infinite;
}}

@keyframes pulse {{
    0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }}
    70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(220, 38, 38, 0); }}
    100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }}
}}

div[data-baseweb="input"] {{
    border-radius: 12px !important;
    background-color: #f8fafc !important;
    border: 1.5px solid #e2e8f0 !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def report_card(titulo, desc, img_relative_path):
    img_path = ASSETS_DIR / img_relative_path
    fallback = ASSETS_DIR / "default.jpg"

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if img_path.exists():
        st.image(img_path.read_bytes(), use_container_width=True)
    elif fallback.exists():
        st.image(fallback.read_bytes(), use_container_width=True)
    else:
        st.image("https://via.placeholder.com/800x400.png?text=Imagen+no+disponible",
                 use_container_width=True)

    st.markdown(f"""
        <div class="card-title">
            {titulo}<br>
            <span style="font-weight:500;color:#64748b;font-size:0.88rem;display:inline-block;margin-top:4px;">
                {desc}
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def open_panel_button(url, key):
    st.markdown(f"""
    <a href="{url}" target="_blank" style="text-decoration:none;">
        <div style="
            width:100%;
            text-align:center;
            padding:13px 18px;
            border-radius:12px;
            font-weight:700;
            font-size:0.92rem;
            color:white;
            background: linear-gradient(135deg, {COLOR1} 0%, #d95d0b 100%);
            box-shadow: 0 6px 16px rgba(237, 112, 27, 0.2);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            margin-top: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        " onmouseover="this.style.transform='translateY(-3px)';" onmouseout="this.style.transform='translateY(0)';" >
            <span>Abrir Dashboard</span>
            <span style="font-size: 1.1rem;">→</span>
        </div>
    </a>
    """, unsafe_allow_html=True)


# =========================================================
# MODAL DE ACCESO GERENCIAL
# =========================================================
@st.dialog(" ")
def modal_gerencia():
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if LOGO_PATH.exists():
            st.image(LOGO_PATH.read_bytes(), use_container_width=True)
        else:
            st.markdown("<div style='text-align:center;font-size:3rem;'>🐔</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="exe-modal-header">
            <div class="exe-title-modal">Panel Ejecutivo</div>
            <div class="exe-badge-modal"><span class="pulse-dot"></span> ACCESO GERENCIAL</div>
            <p style="color: #64748b; font-size: 0.88rem; margin-top: 4px; font-weight: 500;">
                Ingrese su clave restringida para desplegar el panel consolidado.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    pwd = st.text_input("Contraseña Gerencial", type="password", placeholder="••••••••", key="modal_pwd_input")

    if st.button("INGRESAR AL PANEL", use_container_width=True, key="btn_confirmar_modal"):
        if pwd == PASSWORDS["Gerencia"]:
            st.session_state.area = "Gerencia"
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")


# =========================================================
# PORTAL PRINCIPAL
# =========================================================
if st.session_state.area is None:

    # ENCABEZADO TIPO NAVBAR CON BOTÓN ALINEADO
    nav_col1, nav_col2 = st.columns([3.8, 1.2], vertical_alignment="center")
    
    with nav_col1:
        st.markdown('<div class="main-title">Ecosistema Digital • Producción</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Seleccione el área estratégica para desplegar indicadores</div>', unsafe_allow_html=True)
    
    with nav_col2:
        # Botón estilo Pill/Badge plomo
        if st.button("Acceso Gerencial", key="btn_open_modal", use_container_width=True):
            modal_gerencia()

    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    # GRILLA DE TARJETAS DE PRODUCCIÓN
    col1, col2, col3 = st.columns(3)

    with col1:
        report_card("Reproductoras", "Producción de huevo fértil", "repro.jpg")
        if st.button("Ingresar", key="rep", use_container_width=True):
            st.session_state.area = "Reproductoras"
            st.session_state.auth = False
            st.rerun()

    with col2:
        report_card("Incubación", "Gestión de nacimientos", "incubacion.jpg")
        if st.button("Ingresar", key="inc", use_container_width=True):
            st.session_state.area = "Incubación"
            st.session_state.auth = False
            st.rerun()

    with col3:
        report_card("Pollo Carne", "Producción de engorde", "pollo.jpg")
        if st.button("Ingresar", key="pc", use_container_width=True):
            st.session_state.area = "Pollo Carne"
            st.session_state.auth = False
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        report_card("Cerdos", "Producción porcina", "cerdos.jpg")
        if st.button("Ingresar", key="cer", use_container_width=True):
            st.session_state.area = "Cerdos"
            st.session_state.auth = False
            st.rerun()

    with col5:
        report_card("Planta de Beneficio", "Procesamiento", "beneficio.jpg")
        if st.button("Ingresar", key="pb", use_container_width=True):
            st.session_state.area = "Planta de Beneficio"
            st.session_state.auth = False
            st.rerun()

    with col6:
        report_card("Comité Operacional", "Seguimiento estratégico", "comite.jpg")
        if st.button("Ingresar", key="comite", use_container_width=True):
            st.session_state.area = "Comité Operacional"
            st.session_state.auth = False
            st.rerun()

else:

    area = st.session_state.area

    if not st.session_state.auth:

        col1, col2, col3 = st.columns([1,2,1])
        with col2:

            st.markdown(f"""
            <div style="background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.05); text-align: center;">
                <div style="font-size:1.5rem;font-weight:800;color:{COLOR1};margin-bottom:8px;">
                    {area}
                </div>
                <div style="color:#64748b;margin-bottom:20px;font-size:0.9rem;">
                    Ingrese su clave de acceso
                </div>
            </div>
            """, unsafe_allow_html=True)

            pwd = st.text_input("Contraseña", type="password", placeholder="••••••••")

            if st.button("Ingresar", use_container_width=True, key="btn_login_auth"):
                if pwd == PASSWORDS[area]:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Acceso denegado: Contraseña incorrecta")

            if st.button("Volver", use_container_width=True, key="btn_login_volver"):
                st.session_state.area = None
                st.rerun()

    else:

        # ENCABEZADO SUPERIOR CON NAVEGACIÓN LIMPIA
        head_col1, head_col2 = st.columns([3.8, 1.2], vertical_alignment="center")
        
        with head_col1:
            st.markdown(f'<div class="main-title">{area}</div>', unsafe_allow_html=True)
            st.markdown('<div class="subtitle">Módulos e indicadores disponibles para esta área</div>', unsafe_allow_html=True)
            
        with head_col2:
            if st.button("← Cambiar área", key="btn_cambiar_area", use_container_width=True):
                st.session_state.area = None
                st.session_state.auth = False
                st.rerun()

        st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

        # ================= GERENCIA VE TODO =================
        if area == "Gerencia":

            st.subheader("Reproductoras")
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                report_card("Tablero Reproductoras", "Indicadores clave", "repro.jpg")
                open_panel_button("https://app.powerbi.com/links/MTKKKyrmOC?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g4")

            st.divider()

            st.subheader("Incubación")
            col1, col2 = st.columns(2)
            with col1:
                report_card("Tablero Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button("https://app.powerbi.com/links/FvBE6glv0p?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=eb3a6db3-05d1-4d87-8b75-e55208fa6824", "g5")
            with col2:
                report_card("Seguimiento Log Tag", "Trazabilidad", "logtag.jpg")
                open_panel_button("https://app.powerbi.com/links/ZRsbRrhCSk?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g6")

            st.divider()

            # ================= POLLO CARNE =================
            st.subheader("Pollo Carne")

            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("Seguimiento de Lotes Activos", "Control en tiempo real", "lotes.jpg")
                open_panel_button("https://app.powerbi.com/links/g2lIM309oY?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=b43e89fd-62e5-4778-aaab-8915d510ba46", "g1")
            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button("https://app.powerbi.com/links/FlfN0CCJ4H?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g2")
            with col3:
                report_card("Faltantes y Sobrantes", "Control de diferencias", "faltantes.jpg")
                open_panel_button("https://app.powerbi.com/links/IEWsDiPysE?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g3")

            # ===== JSA =====
            st.divider()

            col4, col5, col6 = st.columns(3)
            with col4:
                report_card("JSA Loreto", "Indicadores JSA", "loreto.jpg")
                open_panel_button("https://app.powerbi.com/links/X0jy7jd1vs?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g10")
            with col5:
                report_card("JSA Pucallpa", "Indicadores JSA", "pucallpa.jpg")
                open_panel_button("https://app.powerbi.com/links/2uz6wNBWep?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g11")
            with col6:
                report_card("JSA Calzada", "Indicadores JSA", "calzada.jpg")
                open_panel_button("https://app.powerbi.com/links/-0gJXo1gss?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g12")

            st.divider()

            col7, col8, col9 = st.columns(3)

            with col7:
                st.empty()
            
            with col8:
                report_card("JSA Picota", "Indicadores JSA", "picota.jpg")
                open_panel_button(
                    "https://app.powerbi.com/links/MqnHkulYmd?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare",
                    "g13"
                )
            
            with col9:
                report_card("Análisis Ombligo y Tarso", "Pollo Bebé", "ombligo_tarso.jpg")
                open_panel_button(
                    "https://app.powerbi.com/links/zuRKkFX2eS?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=b12eb673-757b-4d68-a842-43d8098e93c4",
                    "g14"
                )
          
            st.divider()

            st.subheader("Cerdos")
            col1, col2, col3 = st.columns(3)
            with col1:
                report_card("Reporte General", "Producción porcina", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/a_19Nuy4nY?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=a90f008c-b27a-4034-b71c-2214e8f7c251", "g7")
            with col2:
                report_card("Evaluacion de Nacimientos", "Control de nacimientos", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/hEx6l1PkFt?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g_cer_nac")
            with col3:
                report_card("Litter Scatter", "Analítica de camadas", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/uc_hQHv1GM?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g_cer_lit")

            st.divider()

            st.subheader("Planta de Beneficio")
            col1, col2 = st.columns(2)
            with col1:
                report_card("Reporte Diario", "Operación diaria", "diario.jpg")
                open_panel_button("https://app.powerbi.com/links/VlI_Pqq3rS?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=53e6330f-bc0c-4549-b247-0f0a729bb3ec", "g8")
            with col2:
                report_card("Reporte General", "Visión consolidada", "general.jpg")
                open_panel_button("https://app.powerbi.com/links/qBUR10mRm3?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g9")

            st.divider()

            st.subheader("Comité Operacional")
            # BLOQUE 1
            col1, col2 = st.columns(2)

            with col1:
                report_card("Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button(
                    "https://app.powerbi.com/links/i0vEmizvmC?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=51869a31-aa63-4cef-b59d-c7a23e3a9560",
                    "gc1"
                )

            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button(
                    "https://app.powerbi.com/links/gFrq9kBwfI?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare",
                    "gc2"
                )

            st.divider()

            # BLOQUE 2
            col1, col2 = st.columns(2)

            with col1:
                report_card("Planeamiento", "Proyección y control", "planeamiento.jpg")
                open_panel_button(
                    "https://app.powerbi.com/links/EWURfVV_Ae?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare",
                    "gc3"
                )

            with col2:
                report_card("Resultados Generales - PAB", "Visión consolidada y PAB", "pab.jpg")
                open_panel_button(
                    "https://app.powerbi.com/links/kMBXBLnFJs?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare",
                    "gc4"
                )

        # ================= AREAS NORMALES =================

        elif area == "Pollo Carne":

            # ===== BLOQUE 1 =====
            col1, col2, col3 = st.columns(3)

            with col1:
                report_card("Seguimiento de Lotes Activos", "Control en tiempo real", "lotes.jpg")
                open_panel_button("https://app.powerbi.com/links/g2lIM309oY?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=b43e89fd-62e5-4778-aaab-8915d510ba46", "pc1")

            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button("https://app.powerbi.com/links/FlfN0CCJ4H?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "pc2")

            with col3:
                report_card("Faltantes y Sobrantes", "Control de diferencias", "faltantes.jpg")
                open_panel_button("https://app.powerbi.com/links/IEWsDiPysE?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "pc3")

            st.divider()

            # ===== BLOQUE 2 =====
            col1, col2, col3 = st.columns(3)

            with col1:
                report_card("JSA Loreto", "Seguimiento JSA", "loreto.jpg")
                open_panel_button("https://app.powerbi.com/links/X0jy7jd1vs?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "pc4")

            with col2:
                report_card("JSA Pucallpa", "Seguimiento JSA", "pucallpa.jpg")
                open_panel_button("https://app.powerbi.com/links/2uz6wNBWep?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "pc5")

            with col3:
                report_card("JSA Calzada", "Seguimiento JSA", "calzada.jpg")
                open_panel_button("https://app.powerbi.com/links/-0gJXo1gss?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "pc6")

            st.divider()

            # ===== BLOQUE 3 =====
            col1, col2, col3 = st.columns(3)

            with col1:
                report_card("JSA Picota", "Seguimiento JSA", "picota.jpg")
                open_panel_button("https://app.powerbi.com/links/MqnHkulYmd?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "pc7")

            with col2:
                report_card("Análisis Ombligo y Tarso", "Pollo Bebé", "ombligo_tarso.jpg")
                open_panel_button("https://app.powerbi.com/links/zuRKkFX2eS?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=b12eb673-757b-4d68-a842-43d8098e93c4", "pc8")

            with col3:
                st.empty()


        elif area == "Reproductoras":

            col1, col2, col3 = st.columns([1,2,1])

            with col2:
                report_card("Tablero Reproductoras", "Indicadores clave", "repro.jpg")
                open_panel_button("https://app.powerbi.com/links/MTKKKyrmOC?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "rep1")


        elif area == "Incubación":

            col1, col2 = st.columns(2)

            with col1:
                report_card("Tablero Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button("https://app.powerbi.com/links/FvBE6glv0p?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=eb3a6db3-05d1-4d87-8b75-e55208fa6824", "inc1")

            with col2:
                report_card("Seguimiento Log Tag", "Trazabilidad", "logtag.jpg")
                open_panel_button("https://app.powerbi.com/links/ZRsbRrhCSk?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "inc2")


        elif area == "Cerdos":

            col1, col2, col3 = st.columns(3)

            with col1:
                report_card("Reporte General", "Producción porcina", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/a_19Nuy4nY?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=a90f008c-b27a-4034-b71c-2214e8f7c251", "cer1")

            with col2:
                report_card("Evaluacion de Nacimientos", "Control de nacimientos", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/hEx6l1PkFt?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "cer2")

            with col3:
                report_card("Litter Scatter", "Analítica de camadas", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/uc_hQHv1GM?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "cer3")


        elif area == "Planta de Beneficio":

            col1, col2 = st.columns(2)

            with col1:
                report_card("Reporte Diario", "Operación diaria", "diario.jpg")
                open_panel_button("https://app.powerbi.com/links/VlI_Pqq3rS?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=53e6330f-bc0c-4549-b247-0f0a729bb3ec", "pb1")

            with col2:
                report_card("Reporte General", "Visión consolidada", "general.jpg")
                open_panel_button("https://app.powerbi.com/links/qBUR10mRm3?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "pb2")

        
        elif area == "Comité Operacional":

            st.subheader("Pollo Carne e Incubación")

            # BLOQUE 1
            col1, col2 = st.columns(2)

            with col1:
                report_card("Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button("https://app.powerbi.com/links/i0vEmizvmC?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=51869a31-aa63-4cef-b59d-c7a23e3a9560", "co1")

            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button("https://app.powerbi.com/links/gFrq9kBwfI?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "co2")
            st.divider()

            # BLOQUE 2
            col1, col2 = st.columns(2)

            with col1:
                report_card("Planeamiento", "Proyección y control", "planeamiento.jpg")
                open_panel_button("https://app.powerbi.com/links/EWURfVV_Ae?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "co3")

            with col2:
                report_card("Resultados Generales - PAB", "Visión consolidada y PAB", "pab.jpg")
                open_panel_button("https://app.powerbi.com/links/kMBXBLnFJs?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "co4")

# =========================================================
# FOOTER
# =========================================================
st.markdown(f"""
<div style="
    margin-top: 80px;
    padding-top: 24px;
    padding-bottom: 30px;
    border-top: 1px solid #e2e8f0;
    text-align: center;
">
    <div style="
        font-size: 0.88rem;
        font-weight: 700;
        color: #334155;
        letter-spacing: 0.3px;
        margin-bottom: 4px;
    ">
        Gerencia de Control de Gestión <span style="color: {COLOR1}; font-weight: 800;">•</span> Grupo Don Pollo
    </div>
    <div style="
        font-size: 0.78rem;
        color: #94a3b8;
        font-weight: 500;
    ">
        © 2026 Ecosistema Digital de Reportes. Todos los derechos reservados.
    </div>
</div>
""", unsafe_allow_html=True)

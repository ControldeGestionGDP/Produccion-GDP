import streamlit as st
from pathlib import Path

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================
st.set_page_config(
    page_title="Gestión Producción • GDP",
    page_icon="🐔",
    layout="wide"
)

# =========================================================
# PALETA DE COLORES Naranja Premium / Ejecutivo
# =========================================================
COLOR_PRIMARY = "#ed701b"     # Naranja principal solicitado
COLOR_SECONDARY = "#d15c0d"   # Naranja medio/oscuro para degradados
COLOR_DARK = "#a64303"        # Naranja profundo para sombras y contrastes

# =========================================================
# RUTA BASE
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# =========================================================
# CONTRASEÑAS POR ÁREA
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
# ESTADO DE SESIÓN
# =========================================================
if "area" not in st.session_state:
    st.session_state.area = None

if "auth" not in st.session_state:
    st.session_state.auth = False


# =========================================================
# ESTILOS CSS AVANZADOS
# =========================================================
st.markdown(f"""
<style>
/* Reset & Tipografía General */
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #f8fafc;
    color: #1e293b;
}}

/* Transición suave de entrada */
.main .block-container {{
    animation: fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Header Principal */
.main-title {{
    font-size: 2.3rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
}}

.subtitle {{
    color: #64748b;
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 12px;
}}

.title-accent {{
    height: 4px;
    width: 90px;
    background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_SECONDARY});
    border-radius: 4px;
    margin-bottom: 30px;
}}

/* Cards de Reportes / Módulos */
.custom-card {{
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}}

.custom-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 16px 32px rgba(237, 112, 27, 0.12);
    border-color: #fdba74;
}}

.card-title-text {{
    padding: 16px 18px;
    font-weight: 700;
    font-size: 1.1rem;
    color: #0f172a;
    line-height: 1.3;
}}

.card-desc-text {{
    display: block;
    font-weight: 400;
    color: #64748b;
    font-size: 0.88rem;
    margin-top: 4px;
}}

/* Caja de Autenticación */
.login-card {{
    background: #ffffff;
    padding: 35px 30px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.06);
    border-top: 6px solid {COLOR_PRIMARY};
    text-align: center;
    margin-bottom: 20px;
}}

.login-header {{
    font-size: 1.5rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}}

/* Botones Genéricos de Streamlit */
div.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, {COLOR_SECONDARY} 100%);
    color: #ffffff !important;
    border-radius: 12px;
    border: none;
    font-weight: 700;
    font-size: 0.95rem;
    height: 46px;
    box-shadow: 0 4px 12px rgba(237, 112, 27, 0.25);
    transition: all 0.25s ease;
    letter-spacing: 0.3px;
}}

div.stButton > button:hover {{
    background: linear-gradient(135deg, {COLOR_SECONDARY} 0%, {COLOR_DARK} 100%);
    box-shadow: 0 8px 20px rgba(237, 112, 27, 0.35);
    transform: translateY(-2px);
}}

div.stButton > button:active {{
    transform: translateY(0px);
}}

/* Botón de Enlace Externo (Abrir Dashboard) */
.btn-dashboard {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.92rem;
    color: #ffffff !important;
    background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, {COLOR_SECONDARY} 100%);
    box-shadow: 0 4px 12px rgba(237, 112, 27, 0.25);
    text-decoration: none !important;
    transition: all 0.25s ease;
    margin-bottom: 15px;
}}

.btn-dashboard:hover {{
    background: linear-gradient(135deg, {COLOR_SECONDARY} 0%, {COLOR_DARK} 100%);
    box-shadow: 0 8px 20px rgba(237, 112, 27, 0.35);
    transform: translateY(-2px);
}}

/* Panel Lateral (Sidebar) */
.executive-card-sidebar {{
    background: #ffffff;
    border-radius: 18px;
    padding: 22px 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    text-align: center;
    margin-bottom: 20px;
}}

.exe-title-sidebar {{
    font-weight: 800;
    color: {COLOR_PRIMARY};
    margin-bottom: 6px;
    font-size: 1.15rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.exe-status-sidebar {{
    display: inline-block;
    padding: 4px 12px;
    background: #fff7ed;
    color: {COLOR_PRIMARY};
    border: 1px solid #ffedd5;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 800;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
}}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR NAVEGACIÓN
# =========================================================
with st.sidebar:
    st.markdown(f"""
    <div class="executive-card-sidebar">
        <div style="font-size: 2.2rem; margin-bottom: 10px;">🐔</div>
        <div class="exe-title-sidebar">Panel Ejecutivo</div>
        <div class="exe-status-sidebar">● ACCESO RESTRINGIDO</div>
        <p style="color: #64748b; font-size: 0.85rem; line-height: 1.4; margin-top: 5px;">
            Todo el ecosistema de Producción consolidado en una sola vista estratégica.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("INGRESAR GERENCIA", use_container_width=True, help="Solo personal autorizado"):
        st.session_state.area = "Gerencia"
        st.session_state.auth = False
        st.rerun()
    
    st.markdown("---")
    st.caption("© 2026 • Grupo Don Pollo")


# =========================================================
# FUNCIONES AUXILIARES DE RENDERIZADO
# =========================================================
def report_card(titulo, desc, img_relative_path):
    img_path = ASSETS_DIR / img_relative_path
    fallback = ASSETS_DIR / "default.jpg"

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    if img_path.exists():
        st.image(img_path.read_bytes(), use_container_width=True)
    elif fallback.exists():
        st.image(fallback.read_bytes(), use_container_width=True)
    else:
        st.image("https://via.placeholder.com/800x400.png?text=Imagen+no+disponible",
                 use_container_width=True)

    st.markdown(f"""
        <div class="card-title-text">
            {titulo}
            <span class="card-desc-text">
                {desc}
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def open_panel_button(url, key):
    st.markdown(f"""
    <a href="{url}" target="_blank" class="btn-dashboard">
        Abrir Dashboard ↗
    </a>
    """, unsafe_allow_html=True)


# =========================================================
# PORTAL PRINCIPAL / ÁREAS
# =========================================================
if st.session_state.area is None:

    st.markdown('<div class="main-title">Ecosistema Digital • Producción</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Seleccione el área de interés para consultar reportes y dashboards</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        report_card("Reproductoras", "Producción de huevo fértil", "repro.jpg")
        if st.button("Ingresar a Reproductoras", key="rep", use_container_width=True):
            st.session_state.area = "Reproductoras"
            st.session_state.auth = False
            st.rerun()

    with col2:
        report_card("Incubación", "Gestión de nacimientos", "incubacion.jpg")
        if st.button("Ingresar a Incubación", key="inc", use_container_width=True):
            st.session_state.area = "Incubación"
            st.session_state.auth = False
            st.rerun()

    with col3:
        report_card("Pollo Carne", "Producción de engorde", "pollo.jpg")
        if st.button("Ingresar a Pollo Carne", key="pc", use_container_width=True):
            st.session_state.area = "Pollo Carne"
            st.session_state.auth = False
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        report_card("Cerdos", "Producción porcina", "cerdos.jpg")
        if st.button("Ingresar a Cerdos", key="cer", use_container_width=True):
            st.session_state.area = "Cerdos"
            st.session_state.auth = False
            st.rerun()

    with col5:
        report_card("Planta de Beneficio", "Procesamiento industrial", "beneficio.jpg")
        if st.button("Ingresar a Beneficio", key="pb", use_container_width=True):
            st.session_state.area = "Planta de Beneficio"
            st.session_state.auth = False
            st.rerun()

    with col6:
        report_card("Comité Operacional", "Seguimiento estratégico", "comite.jpg")
        if st.button("Ingresar a Comité", key="comite", use_container_width=True):
            st.session_state.area = "Comité Operacional"
            st.session_state.auth = False
            st.rerun()

else:

    area = st.session_state.area

    if not st.session_state.auth:

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="login-card">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🔐</div>
                <div class="login-header">{area}</div>
                <div style="color: #64748b; font-size: 0.9rem; margin-bottom: 20px;">
                    Ingrese la clave de autorización para acceder
                </div>
            </div>
            """, unsafe_allow_html=True)

            pwd = st.text_input("Contraseña del área", type="password", key="pwd_input")

            st.write("")
            if st.button("Ingresar al Panel", use_container_width=True):
                if pwd == PASSWORDS[area]:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("🔒 Contraseña incorrecta. Intente nuevamente.")

            if st.button("← Volver al Portal Main", use_container_width=True):
                st.session_state.area = None
                st.rerun()

    else:

        st.markdown(f'<div class="main-title">{area}</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Módulos e indicadores estratégicos del área</div>', unsafe_allow_html=True)
        st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

        if st.button("← Cambiar de Área", key="btn_back"):
            st.session_state.area = None
            st.session_state.auth = False
            st.rerun()

        st.divider()

        # ================= GERENCIA VE TODO =================
        if area == "Gerencia":

            st.subheader("Reproductoras")
            col1, col2, col3 = st.columns([1, 2, 1])
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
                open_panel_button("https://app.powerbi.com/links/MqnHkulYmd?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g13")
            with col9:
                report_card("Análisis Ombligo y Tarso", "Pollo Bebé", "ombligo_tarso.jpg")
                open_panel_button("https://app.powerbi.com/links/zuRKkFX2eS?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=b12eb673-757b-4d68-a842-43d8098e93c4", "g14")
          
            st.divider()

            st.subheader("Cerdos")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                report_card("Reporte General", "Producción porcina", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/a_19Nuy4nY?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=a90f008c-b27a-4034-b71c-2214e8f7c251", "g7")

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
            col1, col2 = st.columns(2)
            with col1:
                report_card("Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button("https://app.powerbi.com/links/i0vEmizvmC?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=51869a31-aa63-4cef-b59d-c7a23e3a9560", "gc1")
            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button("https://app.powerbi.com/links/gFrq9kBwfI?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "gc2")

            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                report_card("Planeamiento", "Proyección y control", "planeamiento.jpg")
                open_panel_button("https://app.powerbi.com/links/EWURfVV_Ae?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "gc3")
            with col2:
                report_card("Resultados Generales - PAB", "Visión consolidada y PAB", "pab.jpg")
                open_panel_button("https://app.powerbi.com/links/kMBXBLnFJs?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "gc4")

        # ================= ÁREAS INDIVIDUALES =================
        elif area == "Pollo Carne":

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

            col1, col2, col3 = st.columns([1, 2, 1])
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

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                report_card("Reporte General", "Producción porcina", "cerdos.jpg")
                open_panel_button("https://app.powerbi.com/links/a_19Nuy4nY?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=a90f008c-b27a-4034-b71c-2214e8f7c251", "cer1")

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
            col1, col2 = st.columns(2)
            with col1:
                report_card("Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button("https://app.powerbi.com/links/i0vEmizvmC?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=51869a31-aa63-4cef-b59d-c7a23e3a9560", "co1")
            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button("https://app.powerbi.com/links/gFrq9kBwfI?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "co2")

            st.divider()

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
st.markdown(
    "<center style='color:#94a3b8; margin-top:50px; font-size: 0.85rem;'>Gerencia de Control de Gestión • Grupo Don Pollo</center>",
    unsafe_allow_html=True
)

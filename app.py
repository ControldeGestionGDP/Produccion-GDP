import streamlit as st
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Gestión Producción • GDP",
    page_icon="🐔",
    layout="wide"
)

COLOR1 = "#129B94"
COLOR2 = "#0D897D"
COLOR3 = "#8DBF44"

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
# 🔐 SIDEBAR GERENCIA (ESTILO UNIFICADO)
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
        <div style="font-size: 2.2rem; margin-bottom: 10px;">🐔</div>
        <div class="exe-title-sidebar">Panel Ejecutivo</div>
        <div class="exe-status-sidebar">● ACCESO RESTRINGIDO</div>
        <p style="color: #64748b; font-size: 0.85rem; line-height: 1.4; margin-top: 5px;">
            Todo el ecosistema de Producción consolidado en una sola vista estratégica.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("INGRESAR", use_container_width=True, help="Solo personal autorizado"):
        st.session_state.area = "Gerencia"
        st.session_state.auth = False
        st.rerun()
    
    st.markdown("---")
    st.caption("© 2026 • Grupo Don Pollo")


# =========================================================
# ESTILOS (TU MISMO BLOQUE ORIGINAL)
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
    border-top: 5px solid {COLOR1};
    animation: fadeInCard 0.5s ease;
}}
@keyframes fadeInCard {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
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
# FUNCIONES (SIN CAMBIOS)
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
            <span style="font-weight:400;color:#6b7280;font-size:0.95rem;">
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
            padding:12px;
            border-radius:10px;
            font-weight:700;
            color:white;
            background: linear-gradient(90deg,{COLOR1},{COLOR2},{COLOR3});
            box-shadow: 0 6px 14px rgba(0,0,0,0.15);
        ">
            Abrir Dashboard
        </div>
    </a>
    """, unsafe_allow_html=True)

# =========================================================
# PORTAL
# =========================================================
if st.session_state.area is None:

    st.markdown('<div class="main-title">Ecosistema Digital • Producción</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Seleccione el área de interés</div>', unsafe_allow_html=True)
    st.markdown('<div class="title-accent"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col3:
        report_card("Pollo Carne","Producción de engorde","pollo.jpg")
        if st.button("Ingresar", key="pc", use_container_width=True):
            st.session_state.area = "Pollo Carne"
            st.session_state.auth = False
            st.rerun()

    with col1:
        report_card("Reproductoras","Producción de huevo fértil","repro.jpg")
        if st.button("Ingresar", key="rep", use_container_width=True):
            st.session_state.area = "Reproductoras"
            st.session_state.auth = False
            st.rerun()

    with col2:
        report_card("Incubación","Gestión de nacimientos","incubacion.jpg")
        if st.button("Ingresar", key="inc", use_container_width=True):
            st.session_state.area = "Incubación"
            st.session_state.auth = False
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        report_card("Cerdos","Producción porcina","cerdos.jpg")
        if st.button("Ingresar", key="cer", use_container_width=True):
            st.session_state.area = "Cerdos"
            st.session_state.auth = False
            st.rerun()

    with col5:
        report_card("Planta de Beneficio","Procesamiento","beneficio.jpg")
        if st.button("Ingresar", key="pb", use_container_width=True):
            st.session_state.area = "Planta de Beneficio"
            st.session_state.auth = False
            st.rerun()

    with col6:
        report_card("Comité Operacional","Seguimiento estratégico","comite.jpg")
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
            <div class="login-box">
                <div style="font-size:1.4rem;font-weight:700;color:{COLOR2};text-align:center;">
                    {area}
                </div>
                <div style="text-align:center;color:#6b7280;margin-bottom:20px;">
                    Ingrese su contraseña
                </div>
            </div>
            """, unsafe_allow_html=True)

            pwd = st.text_input("Contraseña", type="password")

            if st.button("Ingresar", use_container_width=True):
                if pwd == PASSWORDS[area]:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")

            if st.button("Volver", use_container_width=True):
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

            col7, col8, col9 = st.columns([1,2,1])
            with col8:
                report_card("JSA Picota", "Indicadores JSA", "picota.jpg")
                open_panel_button("https://app.powerbi.com/links/MqnHkulYmd?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "g13")

            st.divider()

            st.subheader("Cerdos")
            col1, col2, col3 = st.columns([1,2,1])
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

            st.subheader("Comité Operacional")
            col1, col2 = st.columns(2)
            with col1:
                report_card("Incubación", "Performance de planta", "incubacion.jpg")
                open_panel_button("https://app.powerbi.com/links/i0vEmizvmC?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare&bookmarkGuid=51869a31-aa63-4cef-b59d-c7a23e3a9560", "gc1")

            with col2:
                report_card("Pollo Carne", "Indicadores productivos", "pollo.jpg")
                open_panel_button("https://app.powerbi.com/links/gFrq9kBwfI?ctid=42fc96b3-c018-482d-8ada-cab81720489e&pbi_source=linkShare", "gc2")
        
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
                st.empty()

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

            col1, col2, col3 = st.columns([1,2,1])

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
st.markdown(
    "<center style='color:#9ca3af;margin-top:40px;'>Gerencia de Control de Gestión • Grupo Don Pollo</center>",
    unsafe_allow_html=True
)

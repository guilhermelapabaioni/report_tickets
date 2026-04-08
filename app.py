import streamlit as st
from src.utils.security import check_password

st.set_page_config(
    page_title="Tickets Monitoring",
    layout="wide",
    page_icon="images/icon_tsystems.png",
)
st.logo("images/logo_tsystems.png")

"""if not check_password():
    st.stop()"""

pages = {
    "Análise de Chamados": [
        st.Page(
            "src/views/report_incidents.py",
            title="Relatório Incidentes",
            icon="📊",
            default=True,
        ),
        st.Page(
            "src/views/report_requests.py", title="Relatório Requisições", icon="📆"
        ),
    ],
}

pg = st.navigation(pages)
pg.run()

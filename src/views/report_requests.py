import streamlit as st
import plotly.express as px
from src.functions.data_wrangling import preprocess_data
from src.functions.analysis import get_incident_reasons
from src.utils.components import create_sidebar
from src.utils.excel_exporter import export_incidents
from src.config.settings import REQUESTS_CONFIG, FONT_STYLE, TITLE_STYLE


@st.cache_data
def load_data():
    return preprocess_data("./data/Reports_Monitoring_Semanal.xlsx", REQUESTS_CONFIG)


df = load_data()

st.set_page_config(layout="wide")
st.title("📊 Relatório Requisições")

if not df.empty:
    df_filtered, _ = create_sidebar(df)

    df_grouped = (
        df_filtered.groupby(["Ano", "Mes", "CI"])
        .size()
        .reset_index(name="Qtd. Tickets")
        .sort_values(by="Qtd. Tickets", ascending=False)
    )

    st.subheader("🔎 Ocorrências por Mês")
    fig_bar = px.bar(
        df_grouped.head(15), 
        x="CI", 
        y="Qtd. Tickets", 
        color="Qtd. Tickets",
        text_auto=True,
        color_continuous_scale="Reds",
        hover_data=["Mes"],
        labels={"Mes": "Mês", "CI": "Hostname (CI)", "Qtd. Tickets": "Tickets"},
    )
    
    fig_bar.update_layout(
        title_text="Incidentes por CI (Intensidade baseada em Volume)",
        margin=dict(b=100),
        coloraxis_showscale=False,
        xaxis=dict(tickfont=FONT_STYLE, title_font=TITLE_STYLE),
        yaxis=dict(tickfont=FONT_STYLE, title_font=TITLE_STYLE),
    )
    
    fig_bar.update_traces(textfont=FONT_STYLE)

    fig_event = st.plotly_chart(
        fig_bar, width="stretch", on_select="rerun", selection_mode="points"
    )
    
    if fig_event and len(fig_event["selection"]["points"]) > 0:
        selected_ci = fig_event["selection"]["points"][0]["x"]

        st.success(f"🔍 Analisando Detalhes: **{selected_ci}**")

        df_detalhes = df_filtered[df_filtered["CI"] == selected_ci]
        
        st.dataframe(
            df_detalhes[['Request ID', 'CI', 'Descricao Request', 'Status', 'Horario de Abertura', 'Horario de Resolucao', 'Grupo de Resolucao']],
            hide_index=True,
            width="stretch",
        )
        export_incidents(
            df_detalhes[
                [
                    "CI",
                    "Request ID",
                    "Descricao Request",
                    "Horario de Abertura",
                    "Horario de Resolucao",
                    "Periodo",
                    "Status",
                    "Grupo de Resolucao",
                ]
            ]
        )

    else:
        st.info("💡 **Dica:** Clique em uma barra para abrir o histórico detalhado.")
        st.dataframe(
            df_grouped[["CI","Qtd. Tickets"]].head(15),
            hide_index=True,
            width="stretch",
        )
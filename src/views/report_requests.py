import streamlit as st
from src.functions.data_wrangling import preprocess_data
from src.utils.sidebar_filters import create_sidebar
from src.utils.excel_exporter import export_incidents
from src.config.settings import REQUESTS_CONFIG
from src.components.charts import plot_bar_chart, plot_pie_chart
from src.components.charts_events import event_bar_plot
from src.functions.analysis import get_incident_reasons


@st.cache_data
def load_data():
    return preprocess_data("./data/Reports_Monitoring_Semanal.xlsx", REQUESTS_CONFIG)


df = load_data()

st.set_page_config(layout="wide")
st.title("📊 Relatório Requisições")

if not df.empty:
    df_filtered = create_sidebar(df)

    df_incident_reasons = get_incident_reasons(df_filtered)

    df_incident_reasons = (
        df_incident_reasons.groupby(["Ano", "Mes", "CI", "Causa Chamado"])
        .size()
        .reset_index(name="Qtd. Tickets")
        .sort_values(by="Qtd. Tickets", ascending=False)
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("🔎 Ocorrências por Mês")
        fig_pie = plot_pie_chart(
            df_incident_reasons,
            names="Causa Chamado",
            values="Qtd. Tickets",
            hole=0.4,
        )

        st.plotly_chart(fig_pie, width="stretch")

    with col2:
        st.markdown("📋 Tabela de Resumo")
        st.dataframe(
            df_incident_reasons[["CI", "Causa Chamado", "Qtd. Tickets"]],
            hide_index=True,
            width="stretch",
        )

    st.divider()

    st.subheader("⚠️ Top 15 Oferensores por Mês")
    fig_bar = plot_bar_chart(
        df_incident_reasons.head(15),
        x_axis="CI",
        y_axis="Qtd. Tickets",
        title="Requests por CI (Intensidade baseada em Volume)",
        hover_data=["Mes"],
        labels={"Mes": "Mês", "CI": "Hostname"},
    )

    fig_bar = st.plotly_chart(
        fig_bar, width="stretch", on_select="rerun", selection_mode="points"
    )

    drill_config = [
        "Request ID",
        "CI",
        "Descricao Chamado",
        "Status",
        "Horario de Abertura",
        "Horario de Resolucao",
    ]
    event_bar_plot(
        fig=fig_bar,
        df_full=df_filtered,
        config=drill_config,
        export_func=export_incidents,
    )

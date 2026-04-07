import streamlit as st
from src.functions.data_wrangling import preprocess_data
from src.utils.sidebar_filters import create_sidebar
from src.utils.excel_exporter import export_incidents
from src.config.settings import REQUESTS_CONFIG
from src.components.charts import plot_bar_chart
from src.components.charts_events import event_bar_plot


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

    col1, col2 = st.columns([2, 1])
    st.subheader("🔎 Ocorrências por Mês")
    with col1:
        fig_bar = plot_bar_chart(
            df_grouped.head(15),
            x_axis="CI",
            y_axis="Qtd. Tickets",
            title="Requests por CI (Intensidade baseada em Volume)",
            hover_data=["Mes"],
            labels={"Mes": "Mês", "CI": "Hostname"},
        )

    with col2:
        st.dataframe(df_grouped, width="stretch", hide_index=True)

    drill_config = [
        "Request ID",
        "CI",
        "Descricao Request",
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

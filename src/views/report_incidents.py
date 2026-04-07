import streamlit as st
import plotly.express as px
from src.functions.data_wrangling import preprocess_data
from src.functions.analysis import get_incident_reasons
from src.utils.components import create_sidebar
from src.utils.excel_exporter import export_incidents
from src.config.settings import INCIDENTS_CONFIG, FONT_STYLE, TITLE_STYLE
from src.components.charts import plot_bar_chat
from src.components.charts_events import event_bar_plot


@st.cache_data
def load_data():
    return preprocess_data(
        "./data/Incidentes_Monitoring_Semanal.xlsx", INCIDENTS_CONFIG
    )


df = load_data()

st.set_page_config(layout="wide")
st.title("📊 Relatório Incidentes")


if not df.empty:
    df_filtered, _ = create_sidebar(df)

    df_processed = get_incident_reasons(df_filtered)

    df_grouped = (
        df_processed.groupby(["Ano", "Mes", "CI", "Causa Incidente"])
        .size()
        .reset_index(name="Qtd. Tickets")
        .sort_values(by="Qtd. Tickets", ascending=False)
    )

    st.subheader("🔎 Ocorrências por Mês")
    col1, col2 = st.columns([1, 1])

    with col1:
        fig_pie = px.pie(
            df_grouped,
            values="Qtd. Tickets",
            names="Causa Incidente",
            hole=0.3,
        )

        fig_pie.update_layout(
            title_text="Incidentes por Causa Raiz",
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(
                font=FONT_STYLE,  # Tamanho 16 e cor preta para os itens
                title_font=TITLE_STYLE,  # Tamanho 20 para o título da legenda
            ),
        )

        fig_pie.update_traces(textfont=FONT_STYLE)

        st.plotly_chart(fig_pie, width="stretch")

    with col2:
        st.markdown("📋 Tabela de Resumo")
        st.dataframe(
            df_grouped[["CI", "Causa Incidente", "Qtd. Tickets"]],
            hide_index=True,
            width="stretch",
        )

    st.divider()
    st.subheader("⚠️ Top 15 Oferensores por Mês")

    fig_bar = plot_bar_chat(
        df_grouped.head(15),
        x_axis="CI",
        y_axis="Qtd. Tickets",
        title="Incidentes por CI (Intensidade baseada em Volume)",
        hover_data=["Mes"],
        labels={"Mes": "Mês", "CI": "Hostname"},
    )

    drill_config = [
        "Ticket ID",
        "CI",
        "Descricao Incidente",
        "Incident Status",
        "Horario de Abertura",
        "Horario de Resolucao",
    ]
    event_bar_plot(
        fig_bar, df_full=df_filtered, config=drill_config, export_func=export_incidents
    )

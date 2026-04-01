import streamlit as st
import plotly.express as px
from src.functions.data_wrangling import preprocess_data
from src.functions.analysis import get_incident_reasons
from src.utils.components import create_sidebar
from src.utils.excel_exporter import export_incidents
from src.config.settings import INCIDENTS_CONFIG, FONT_STYLE, TITLE_STYLE


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

        export_incidents(
            df_detalhes[
                [
                    "CI",
                    "Ticket ID",
                    "Descricao Incidente",
                    "Horario de Abertura",
                    "Horario de Resolucao",
                    "Periodo",
                    "Incident Status",
                    "Grupo de Resolucao",
                ]
            ]
        )

        st.dataframe(
            df_detalhes[
                [
                    "CI",
                    "Ticket ID",
                    "Descricao Incidente",
                    "Horario de Abertura",
                    "Horario de Resolucao",
                    "Periodo",
                    "Incident Status",
                    "Grupo de Resolucao",
                ]
            ],
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("💡 **Dica:** Clique em uma barra para abrir o histórico detalhado.")
        st.dataframe(
            df_grouped[["CI", "Causa Incidente", "Qtd. Tickets"]].head(15),
            hide_index=True,
            width="stretch",
        )

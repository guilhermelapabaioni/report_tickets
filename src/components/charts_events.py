import streamlit as st


def event_bar_plot(fig, df_full, df_data, config, export_func):
    if fig and len(fig["selection"]["points"]) > 0:
        selected_ci = fig["selection"]["points"][0]["x"]

        st.success(f"🔍 Analisando Detalhes: **{selected_ci}**")

        df_detalhes = df_full[df_full["CI"] == selected_ci]

        export_func(df_detalhes[config])

        st.dataframe(
            df_detalhes[config],
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("💡 **Dica:** Clique em uma barra para abrir o histórico detalhado.")
        export_func(df_data)

        st.dataframe(df_data, hide_index=True, width="stretch")

import streamlit as st
import plotly.express as px
from src.config.settings import TITLE_STYLE, FONT_STYLE


def plot_bar_chart(df, x_axis, y_axis, **kwargs):
    """
    Gera um gráfico de barras flexível.
    Qualquer argumento extra passado será enviado diretamente para o px.bar.
    """
    params = {
        "color": kwargs.get("color", y_axis),
        "text_auto": True,
        "color_continuous_scale": "Reds",
        "labels": kwargs.get("labels", {}),
        "hover_data": kwargs.get("hover_data", []),
    }

    for key in params.keys():
        kwargs.pop(key, None)

    fig = px.bar(df, x=x_axis, y=y_axis, **params, **kwargs)

    fig.update_layout(
        margin=dict(b=100),
        coloraxis_showscale=False,
        xaxis=dict(tickfont=FONT_STYLE, title_font=TITLE_STYLE),
        yaxis=dict(tickfont=FONT_STYLE, title_font=TITLE_STYLE),
    )

    fig.update_traces(textfont=FONT_STYLE, textangle=0, textposition="outside")

    fig = st.plotly_chart(
        fig, width="stretch", on_select="rerun", selection_mode="points"
    )

    return fig


def plot_pie_chart(df, names, values, **kwargs):
    fig = px.pie(df, names, values, **kwargs)

    fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            font=FONT_STYLE,
            title_font=TITLE_STYLE,
        ),
    )

    fig.update_traces(textfont=FONT_STYLE)

    return fig

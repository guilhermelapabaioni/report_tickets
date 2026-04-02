import streamlit as st
import plotly.express as px
from src.config.settings import TITLE_STYLE, FONT_STYLE

def plot_bar_chat(df, x_axis, y_axis, title, color_col=None):
    
    color_col = color_col if color_col else y_axis
    
    fig = px.bar(
        df.head(15),
        x=x_axis,
        y=y_axis,
        color=color_col,
        text_auto=True,
        color_continuous_scale='Reds',
        hover_data=["Mes"],
        labels={"Mes": "Mês", "CI": "Hostname (CI)", "Qtd. Tickets": "Tickets"},
    )
    
    fig.update_layout(
        title_text = title,
        margin=dict(b=100),
        coloraxis_showscale=False,
        xaxis=dict(tickfont=FONT_STYLE, title_font=TITLE_STYLE),
        yaxis=dict(tickfont=FONT_STYLE, title_font=TITLE_STYLE),
        
    )
    
    fig.update_traces(
        textfont=FONT_STYLE
    )
    
    return fig
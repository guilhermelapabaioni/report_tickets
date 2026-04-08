import streamlit as st
from datetime import datetime as dt
from src.config.settings import MONTH_MAP, MONTHS_ORDER


def get_year(df):
    available_years = sorted(df["Ano"].unique())

    selected_years = st.sidebar.multiselect(
        "Ano do Incidente",
        available_years,
        default=dt.now().year,
        placeholder="Todos os Anos",
        key="filter_year",
    )

    return selected_years


def get_month(df):
    available_months = sorted(
        df["Mes"].unique(),
        key=lambda m: MONTHS_ORDER.index(m) if m in MONTHS_ORDER else 99,
    )

    selected_months = st.sidebar.multiselect(
        "Mês do Incidente",
        available_months,
        default=(
            MONTH_MAP[dt.now().month]
            if MONTH_MAP[dt.now().month] in df["Mes"].values
            else None
        ),
        placeholder="Todos os Meses",
        key="filter_month",
    )

    return selected_months


def get_ci(df):
    enable_cis = sorted(df["CI"].unique())

    selected_cis = st.sidebar.multiselect(
        "Hostname Devices",
        options=enable_cis,
        placeholder="Pesquisar Equipamentos",
        key="filter_ci",
    )

    return selected_cis


def get_day(df):
    available_dates = sorted(
        df["Dia"].unique(),
    )

    selected_dates = st.sidebar.multiselect(
        "Dia do Incidente",
        options=available_dates,
        placeholder="Todos os Dias",
        key="filter_date",
    )

    return selected_dates


def reset_filters():
    st.session_state["filter_year"] = []
    st.session_state["filter_month"] = []
    st.session_state["filter_ci"] = []
    st.session_state["filter_date"] = []


def create_sidebar(df):
    st.sidebar.header("⚙️ Painel de Filtro")

    years = get_year(df)
    if years:
        df_filtered = df[df["Ano"].isin(years)]

    months = get_month(df_filtered)
    if months:
        df_filtered = df_filtered[df_filtered["Mes"].isin(months)]

    days = get_day(df_filtered)
    if days:
        df_filtered = df_filtered[df_filtered["Dia"].isin(days)]

    cis = get_ci(df_filtered)
    if cis:
        df_filtered = df_filtered[df_filtered["CI"].isin(cis)]

    st.sidebar.button(
        "Limpar Filtros",
        on_click=reset_filters,
    )

    return df_filtered, (years, months, cis)

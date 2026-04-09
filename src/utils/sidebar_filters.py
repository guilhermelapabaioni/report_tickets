import pandas as pd
import streamlit as st
from datetime import datetime as dt
from src.config.settings import MONTH_MAP, MONTHS_ORDER


def get_date_range(df):
    min_date, max_date = (
        df["Horario de Abertura"].min(),
        df["Horario de Abertura"].max(),
    )

    selected_date_range = st.sidebar.date_input(
        "Período de Análise",
        value=[],
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY",
        key="filter_date_range",
    )
    return selected_date_range


def get_year(df, default_val=None):
    available_years = sorted(df["Ano"].unique())

    selected_years = st.sidebar.multiselect(
        "Ano do Incidente",
        available_years,
        default=default_val if default_val else [],
        placeholder="Todos os Anos",
        key="filter_year",
    )
    return selected_years


def get_month(df, default_val=None):
    available_months = sorted(
        df["Mes"].unique(),
        key=lambda m: MONTHS_ORDER.index(m) if m in MONTHS_ORDER else 99,
    )

    selected_months = st.sidebar.multiselect(
        "Mês do Incidente",
        available_months,
        default=default_val if default_val else [],
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


def get_ticket_number(df):
    selected_tickets = st.sidebar.multiselect(
        "N° do Chamado",
        df["N° Chamado"],
        placeholder="Todos os Chamados",
        key="filter_ticket",
    )

    return selected_tickets


def reset_filters():
    st.session_state["filter_date_range"] = []
    st.session_state["filter_year"] = [dt.now().year]
    st.session_state["filter_month"] = [MONTH_MAP[dt.now().month]]
    st.session_state["filter_ci"] = []
    st.session_state["filter_ticket"] = []


def create_sidebar(df):
    st.sidebar.header("⚙️ Painel de Filtro")

    date_range = get_date_range(df)
    is_date_range = len(date_range) == 2

    if is_date_range:
        start_date, end_date = date_range
        df["Data_Aux"] = pd.to_datetime(df["Horario de Abertura"]).dt.date
        df = df[(df["Data_Aux"] >= start_date) & (df["Data_Aux"] <= end_date)]
    else:
        current_year = dt.now().year
        year_default = [current_year] if current_year in df["Ano"].values else None
        years = get_year(df, default_val=year_default)
        if years:
            df = df[df["Ano"].isin(years)]

        current_month = MONTH_MAP[dt.now().month]
        month_default = [current_month] if current_month in df["Mes"].values else None
        months = get_month(df, default_val=month_default)
        if months:
            df = df[df["Mes"].isin(months)]

    cis = get_ci(df)
    if cis:
        df = df[df["CI"].isin(cis)]

    tickets = get_ticket_number(df)
    if tickets:
        df = df[df["N° Chamado"].isin(tickets)]

    st.sidebar.button(
        "Limpar Filtros",
        on_click=reset_filters,
    )

    return df

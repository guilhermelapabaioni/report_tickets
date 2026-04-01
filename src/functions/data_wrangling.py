import pandas as pd
import re


def preprocess_data(PATH, config):
    """
    Carrega o arquivo e aplica as primeiras transformações estruturais.
    """
    try:
        df = (
            pd.read_excel(
                PATH, skiprows=(10 if config.get("id") == "INCIDENTS_CONFIG" else 3)
            )
            .rename(columns=config.get("rename_columns"))
            .drop(columns=config.get("drop_columns"))
        )

        df = recover_generic_ci(df)
        df = extract_time_features(df)

        return df
    except FileNotFoundError:
        raise (f"ERRO: Arquivo não encontrado em {PATH}")


def preprocess_reports_data(PATH):
    """ """
    try:
        df = pd.read_excel(PATH, skiprows=3).rename().drop()

        return df
    except FileExistsError:
        raise (f"ERRO: Arquivo não encontrado em {PATH}")


def extract_time_features(df):
    """
    Extrai componentes temporais para análise de sazonalidade.
    """
    df = df.copy()

    for column in df[
        [
            "Horario de Abertura",
            "Horario de Resolucao",
        ]
    ]:
        df[column] = pd.to_datetime(df[column])

    dt_series = pd.to_datetime(df["Horario de Abertura"], errors="coerce")

    df["Dia"] = dt_series.dt.day
    df["Mes"] = dt_series.dt.month_name(locale="portuguese_brazil")
    df["Ano"] = dt_series.dt.year

    df["Hora"] = dt_series.dt.hour
    df["Dia_Semana"] = dt_series.dt.day_name()

    df["Periodo"] = pd.cut(
        df["Hora"],
        bins=[-1, 6, 12, 18, 24],
        labels=["Madrugada", "Manhã", "Tarde", "Noite"],
    )

    return df


def recover_generic_ci(df):
    """
    Recupera o nome real do Servidor quando o campo CI vem como 'GENERIC'.
    """
    df = df.copy()

    mask_generic = df["CI"].str.contains("GENERIC", na=False, case=False)

    prefixes_ci = [
        "VWBR",
        "VWAR",
        "ADBR",
        "AUBR",
        "UPSAN",
        "BVW",
        "SYN",
        "BRVW",
        "MLBR",
        "VWTB",
        "BRA",
    ]
    regex_pattern = r"((?:" + "|".join(prefixes_ci) + r")[a-zA-Z0-9_-]+)"

    extract_ci = df.loc[mask_generic, "Descricao Incidente"].str.extract(
        regex_pattern, flags=re.IGNORECASE, expand=False
    )

    df.loc[mask_generic, "CI"] = extract_ci.fillna(df.loc[mask_generic, "CI"])

    df["CI"] = df["CI"].str.upper().str.strip()

    return df

from src.config.settings import MONTH_MAP, KEYWORDS
from datetime import datetime as dt

def get_report_date(df, year=dt.now().year, month=MONTH_MAP[dt.now().month]):
    df = df.loc[(df['Ano'] == year) & (df['Mes'] == month)].copy()
    return df

def classify_reason(texto):
    texto = str(texto).lower()
    for categoria, palavras in KEYWORDS.items():
        if any(p in texto for p in palavras):
            return categoria
    return 'Outros/Analisar Manualmente'

def get_incident_reasons(df):
    df = df.copy()
    df['Causa Incidente'] = df['Descricao Incidente'].apply(classify_reason)

    return df

def get_monthly_report(df):
    # Recebe o DF já filtrado
    """Aplica a classificação e gera o resumo consolidado."""
    df = df.copy()

    df = get_incident_reasons(df)

    report = (df.groupby(['CI', 'Causa Incidente'])
                .size()
                .unstack(fill_value=0))
    
    report['Qtd. Incidentes'] = report.sum(axis=1)

    return report.sort_values(by='Qtd. Incidentes', ascending=False).reset_index()


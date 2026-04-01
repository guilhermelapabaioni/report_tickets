import pandas as pd
import streamlit as st


from datetime import datetime as dt
from xlsxwriter.utility import xl_rowcol_to_cell
from io import BytesIO

def save_formatted_report(monthly_report, df_tickets):
    data_str = dt.now().strftime('%d-%m-%Y')
    nome_arquivo = f'relatorio_completo_{data_str}.xlsx'

    with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
        # Novas Abas Gerenciais (Mensais)
        monthly_report.to_excel(writer, sheet_name='1. Incidentes Mensais', index=False)
        df_tickets.to_excel(writer, sheet_name='2. Detalhes Incidentes', index=False)

        workbook = writer.book
        # Definição de estilos
        format_critico = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})

        for nome_aba, dataframe in [('1. Incidentes Mensais', monthly_report)]:
            worksheet = writer.sheets[nome_aba]
            worksheet.freeze_panes(1, 0)

            # Dimensões do DataFrame para a lógica numérica
            num_linhas = len(dataframe)
            num_cols = len(dataframe.columns) - 1  # O índice do pandas vira a coluna 0 no Excel

            # 1. Ajuste de largura: Coluna 0 até a última (num_cols)
            worksheet.set_column(0, num_cols, 20)

            # 2. Formatação Condicional usando Coordenadas Numéricas
            # Sintaxe: worksheet.conditional_format(first_row, first_col, last_row, last_col, options)
            worksheet.conditional_format(1, 0, num_linhas, num_cols, {
                'type': 'formula',
                # Aqui está o segredo: xl_rowcol_to_cell converte (1, num_cols) em "$F$2"
                # Usamos row=1 (linha 2 no Excel) e col=num_cols (coluna do Total)
                'criteria': f'={xl_rowcol_to_cell(1, num_cols, row_abs=False, col_abs=True)} >= 5',
                'format': format_critico
            })

    return nome_arquivo


def export_incidents(df):
    """
    Gera um buffer de memória com o Excel e renderiza o botão de download.
    """
    if df.empty:
        st.warning('Não há dados para exportar. Por gentileza, contate guilherme.baioni@t-systems.com')
        return None

    try:
        # 1. Criação do Buffer (Evita salvar arquivos no servidor)
        output = BytesIO()

        # 2. Nome do arquivo dinâmico
        # Se houver apenas um CI, usamos o nome dele. Se houver vários, usamos 'Multiplos_CIs'
        ci_tag = df['CI'].iloc[0] if df['CI'].nunique() == 1 else "Consolidado"
        file_name = f"relatorio_incidentes_{ci_tag}.xlsx"

        # 3. Escrita do Excel
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='1. Incidentes', index=False)

            # Ajuste automático de largura de colunas (Opcional, mas profissional)
            worksheet = writer.sheets['1. Incidentes']
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.set_column(i, i, column_len)

        # 4. Botão de Download do Streamlit
        st.download_button(
            label="📥 Baixar Relatório Excel",
            data=output.getvalue(),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao gerar o arquivo: {e}")
        st.info("Suporte: guilherme.baioni@t-systems.com")
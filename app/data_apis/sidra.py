import sidrapy
import pandas as pd
from datetime import datetime

def get_pib_data(period_start=None, period_end=None):
    """
    Obtém dados do PIB trimestral do SIDRA/IBGE
    Tabela 1621 - PIB a preços de mercado
    """
    try:
        # Busca os dados do PIB trimestral
        pib_raw = sidrapy.get_table(table_code="1621",  # Tabela do PIB trimestral
                                   territorial_level="1",  # Brasil
                                   ibge_territorial_code="1",
                                   classification = "11255/90707",
                                   #variable="93404",  # PIB a preços de mercado
                                   period="all")  # Toda a série histórica
        
        # Converte para DataFrame
        pib_raw = pd.DataFrame(pib_raw)
        
        # Substitui as colunas pela primeira observação
        pib_raw.columns = pib_raw.iloc[0]
        
        # Retira a primeira observação
        pib_raw = pib_raw.iloc[1:, :]
        
        # Substitui '..' por NaN e converte para float
        pib_raw['Valor'] = pib_raw['Valor'].replace('..', pd.NA)
        pib_raw['Valor'] = pd.to_numeric(pib_raw['Valor'], errors='coerce')
        
        # Remove linhas com valores nulos
        pib_raw = pib_raw.dropna(subset=['Valor'])
        
        # Renomeia e seleciona as colunas
        pib = pib_raw.rename(columns={"Valor": "pib",
                                    "Trimestre (Código)": "date"})[['pib', 'date']]
        
        # Procedimento para lidar com a coluna de trimestre para transformar em data
        pib['date'] = pib['date'].str[:-2] + pib['date'].str[-2:].replace({
            "01": "03",
            "02": "06",
            "03": "09",
            "04": "12"
        })
        
        # Transforma em formato date a coluna de data e insere no índice
        pib.index = pd.to_datetime(pib['date'], format="%Y%m")
        
        # Retira a coluna de data
        pib = pib.drop(columns=['date'])
        
        # Ordena o índice
        pib = pib.sort_index()
        
        # Prepara o resultado para o gráfico
        result = {
            'dates': pib.index.strftime('%Y-%m-%d').tolist(),
            'values': pib['pib'].tolist(),
            'label': 'PIB Trimestral',
            'unit': 'Milhões de Reais'
        }
        
        return result
    
    except Exception as e:
        print(f"Erro ao buscar dados do PIB: {e}")
        print("Dados recebidos:", pib_raw if 'pib_raw' in locals() else None)
        return None

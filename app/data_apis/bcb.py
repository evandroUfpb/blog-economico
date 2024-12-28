import requests
import pandas as pd
from datetime import datetime, date

def get_ipca_data(start_date="2000-01-01", end_date=None):
    """
    Obtém dados do IPCA do Banco Central do Brasil
    Série 433 - IPCA - Variação mensal
    """
    try:
        # Se não foi especificada uma data final, usa a data atual
        if end_date is None:
            end_date = date.today().strftime("%Y-%m-%d")
            
        # Converte as datas para o formato da API
        start = pd.to_datetime(start_date).strftime("%d/%m/%Y")
        end = pd.to_datetime(end_date).strftime("%d/%m/%Y")
            
        # URL da API do BCB
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial={start}&dataFinal={end}"
        
        # Faz a requisição
        response = requests.get(url)
        response.raise_for_status()
        
        # Converte para DataFrame
        df = pd.DataFrame(response.json())
        
        # Converte data e valor
        df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Remove valores nulos
        df = df.dropna()
        
        # Ordena por data
        df = df.sort_values('data')
        
        # Prepara o resultado para o gráfico
        result = {
            'dates': df['data'].dt.strftime('%Y-%m-%d').tolist(),
            'values': df['valor'].tolist(),
            'label': 'IPCA - Variação Mensal',
            'unit': '% ao mês'
        }
        
        return result
    
    except Exception as e:
        print(f"Erro ao buscar dados do IPCA: {str(e)}")
        return {
            'dates': [],
            'values': [],
            'label': 'IPCA - Variação Mensal',
            'unit': '% ao mês'
        }

def get_selic_data(start_date="2000-01-01", end_date=None):
    """
    Obtém dados da Taxa SELIC do Banco Central do Brasil
    Série 432 - Taxa SELIC acumulada no mês
    """
    try:
        # Se não foi especificada uma data final, usa a data atual
        if end_date is None:
            end_date = date.today().strftime("%Y-%m-%d")
            
        # Converte as datas para o formato da API
        start = pd.to_datetime(start_date).strftime("%d/%m/%Y")
        end = pd.to_datetime(end_date).strftime("%d/%m/%Y")
            
        # URL da API do BCB
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json&dataInicial={start}&dataFinal={end}"
        
        # Faz a requisição
        response = requests.get(url)
        response.raise_for_status()
        
        # Converte para DataFrame
        df = pd.DataFrame(response.json())
        
        # Converte data e valor
        df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Remove valores nulos
        df = df.dropna()
        
        # Ordena por data
        df = df.sort_values('data')
        
        # Prepara o resultado para o gráfico
        result = {
            'dates': df['data'].dt.strftime('%Y-%m-%d').tolist(),
            'values': df['valor'].tolist(),
            'label': 'Taxa SELIC',
            'unit': '% ao mês'
        }
        
        return result
    
    except Exception as e:
        print(f"Erro ao buscar dados da SELIC: {str(e)}")
        return {
            'dates': [],
            'values': [],
            'label': 'Taxa SELIC',
            'unit': '% ao mês'
        }

# Fucao para pegar dados do CAMBIO
def get_cambio_data(start_date="2000-01-01", end_date=None):
    """
    Obtém dados da Taxa SELIC do Banco Central do Brasil
    Série 1 - Taxa SELIC acumulada no mês
    """
    try:
        # Se não foi especificada uma data final, usa a data atual
        if end_date is None:
            end_date = date.today().strftime("%Y-%m-%d")
            
        # Converte as datas para o formato da API
        start = pd.to_datetime(start_date).strftime("%d/%m/%Y")
        end = pd.to_datetime(end_date).strftime("%d/%m/%Y")
            
        # URL da API do BCB
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial={start}&dataFinal={end}"
        
        # Faz a requisição
        response = requests.get(url)
        response.raise_for_status()
        
        # Converte para DataFrame
        df = pd.DataFrame(response.json())
        
        # Converte data e valor
        df['data'] = pd.to_datetime(df['data'], format="%d/%m/%Y")
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        
        # Remove valores nulos
        df = df.dropna()
        
        # Ordena por data
        df = df.sort_values('data')
        
        # Prepara o resultado para o gráfico
        result = {
            'dates': df['data'].dt.strftime('%Y-%m-%d').tolist(),
            'values': df['valor'].tolist(),
            'label': 'Taxa de Câmbio Livre - PTAX, diária (venda)',
            'unit': 'R/US'
        }
        
        return result
    
    except Exception as e:
        print(f"Erro ao buscar dados da SELIC: {str(e)}")
        return {
            'dates': [],
            'values': [],
            'label': 'Taxa SELIC',
            'unit': '% ao mês'
        }


# from bcb import sgs
# import pandas as pd
# from datetime import datetime, date

# def get_ipca_data(start_date="2000-01-01", end_date=None):
#     """
#     Obtém dados do IPCA do Banco Central do Brasil
#     Série 433 - IPCA - Variação mensal
#     """
#     try:
#         # Se não foi especificada uma data final, usa a data atual
#         if end_date is None:
#             end_date = date.today().strftime("%Y-%m-%d")
            
#         # Converte as datas para datetime
#         inicial = pd.to_datetime(start_date)
#         final = pd.to_datetime(end_date)
            
#         # Busca os dados do IPCA
#         df = sgs.get(433, inicial, final)  # Código da série IPCA
        
#         if df is None or df.empty:
#             raise ValueError("Nenhum dado retornado pela API")
            
#         # Converte data e valores
#         dates = df.index.strftime('%Y-%m-%d').tolist()
#         values = df[433].tolist()
        
#         if not dates or not values:
#             raise ValueError("Dados vazios ou inválidos")
        
#         # Prepara o resultado para o gráfico
#         result = {
#             'dates': dates,
#             'values': values,
#             'label': 'IPCA - Variação Mensal',
#             'unit': '% ao mês'
#         }
        
#         return result
    
#     except Exception as e:
#         print(f"Erro ao buscar dados do IPCA: {e}")
#         print("Dados recebidos:", df if 'df' in locals() else None)
#         return {
#             'dates': [],
#             'values': [],
#             'label': 'IPCA - Variação Mensal',
#             'unit': '% ao mês'
#         }

# def get_selic_data(start_date="2000-01-01", end_date=None):
#     """
#     Obtém dados da Taxa SELIC do Banco Central do Brasil
#     Série 432 - Taxa SELIC acumulada no mês
#     """
#     try:
#         # Se não foi especificada uma data final, usa a data atual
#         if end_date is None:
#             end_date = date.today().strftime("%Y-%m-%d")
            
#         # Converte as datas para datetime
#         inicial = pd.to_datetime(start_date)
#         final = pd.to_datetime(end_date)
            
#         # Busca os dados da SELIC
#         df = sgs.get(432, inicial, final)  # Código da série SELIC
        
#         if df is None or df.empty:
#             raise ValueError("Nenhum dado retornado pela API")
            
#         # Converte data e valores
#         dates = df.index.strftime('%Y-%m-%d').tolist()
#         values = df[432].tolist()
        
#         if not dates or not values:
#             raise ValueError("Dados vazios ou inválidos")
        
#         # Prepara o resultado para o gráfico
#         result = {
#             'dates': dates,
#             'values': values,
#             'label': 'Taxa SELIC',
#             'unit': '% ao mês'
#         }
        
#         return result
    
#     except Exception as e:
#         print(f"Erro ao buscar dados da SELIC: {e}")
#         print("Dados recebidos:", df if 'df' in locals() else None)
#         return {
#             'dates': [],
#             'values': [],
#             'label': 'Taxa SELIC',
#             'unit': '% ao mês'
#         }
# import requests

# def get_selic_data():
#     try:
#         # Código da Selic no BCB: 432
#         url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json"
#         response = requests.get(url)
#         return response.json()
#     except Exception as e:
#         print(f"Erro ao buscar dados do BCB: {e}")
#         return None
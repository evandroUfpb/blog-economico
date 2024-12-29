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
        return None
        # return {
        #     'dates': [],
        #     'values': [],
        #     'label': 'IPCA - Variação Mensal',
        #     'unit': '% ao mês'
        # }
    #linhas adicionadas
    
    cache_key_str = cache_key('ipca', start=start_date, end=end_date)
    return get_cached_data(cache_key_str, fetch_data, expires_in=3600)    

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
        # return {
        #     'dates': [],
        #     'values': [],
        #     'label': 'Taxa SELIC',
        #     'unit': '% ao mês'
        # }
        return None
        
    #linhas adicionadas
    
    cache_key_str = cache_key('selic', start=start_date, end=end_date)
    return get_cached_data(cache_key_str, fetch_data, expires_in=3600)      

# Fucao para pegar dados do CAMBIO
def get_cambio_data(start_date="2000-01-01", end_date=None): #get_elic_data(start_date="2000-01-01", end_date=None):
    """
    Obtém dados da Taxa de Câmbio do Brasil
    Série 1 - Taxa acumulada no mês
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
        print(f"Erro ao buscar dados da Câmbio {str(e)}")
        # return {
        #     'dates': [],
        #     'values': [],
        #     'label': 'Taxa SELIC',
        #     'unit': '% ao mês'
        # }
        return None
    r
    #linhas adicionadas
    
    cache_key_str = cache_key('cambio', start=start_date, end=end_date), cache_key('ipca', start=start_date, end=end_date)
    return get_cached_data(cache_key_str, fetch_data, expires_in=3600)      


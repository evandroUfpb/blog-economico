import logging
import pandas as pd
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_ipca_data(period_start=None, period_end=None):
    """
    Obtém dados do IPCA do Banco Central do Brasil
    """
    try:
        logging.info("Iniciando busca de dados do IPCA")
        
        # URL para dados do IPCA mensal
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"
        
        # Adicionar headers para evitar bloqueios
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        logging.info(f"Status da resposta IPCA: {response.status_code}")
        logging.info(f"Conteúdo da resposta: {response.text[:500]}...")  # Mostra os primeiros 500 caracteres
        
        if response.status_code != 200:
            logging.error(f"Erro na requisição do IPCA: {response.status_code}")
            return None
        
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as json_err:
            logging.error(f"Erro de decodificação JSON: {json_err}")
            logging.error(f"Conteúdo da resposta: {response.text}")
            return None
        
        # Processamento dos dados
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        
        # Filtrar dados a partir de 2002
        df = df[df['data'] >= '01/01/2002']
        
        df.set_index('data', inplace=True)
        
        # Ordenar por data
        df = df.sort_index()
        
        result = {
            'dates': df.index.strftime('%Y%m').tolist(),  # Formato YYYYMM
            'values': df['valor'].tolist(),
            'label': 'IPCA Mensal',
            'unit': '%'
        }
        
        logging.info(f"Dados do IPCA processados: {len(result['dates'])} registros")
        return result
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados do IPCA: {e}", exc_info=True)
        return None

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_selic_data(period_start=None, period_end=None):
    """
    Obtém dados da Taxa SELIC do Banco Central do Brasil
    """
    try:
        logging.info("Iniciando busca de dados da SELIC")
        
        # URL para dados da SELIC
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json"
        
        # Adicionar headers para evitar bloqueios
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logging.error(f"Erro na requisição da SELIC: {response.status_code}")
            return None
        
        data = response.json()
        
        # Processamento dos dados
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df.set_index('data', inplace=True)
        
        # Ordenar por data
        df = df.sort_index()
        
        result = {
            'dates': df.index.strftime('%Y-%m').tolist(),
            'values': df['valor'].tolist(),
            'label': 'Taxa SELIC Mensal',
            'unit': '%'
        }
        
        logging.info(f"Dados da SELIC processados: {len(result['dates'])} registros")
        return result
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados da SELIC: {e}", exc_info=True)
        return None
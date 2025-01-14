import logging
import requests
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_fixed


#---------------------- Função para pegar o PIB do Brasil ---------------------
def get_pib_data():
    try:
        logging.info("Iniciando busca de dados de PIB")
        
        url = "https://apisidra.ibge.gov.br/values/t/5938/n1/all/v/37/p/all?formato=json"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            logging.error(f"Erro na requisição de PIB: {response.status_code}")
            return None
        
        data = response.json()
        
        if not data:
            logging.error("Dados de PIB retornados estão vazios")
            return None
        
        dates = []
        values = []
        
        for item in data:
            try:
                # Converter ano para datetime
                year_str = item.get('D3N', '')
                
                # Converter valor para float em milhões
                value_str = item.get('V', '')
                value = float(value_str) / 1_000_000_000 if value_str else None
                
                if year_str and value is not None:
                    dates.append(year_str)
                    values.append(round(value, 2))
            except Exception as e:
                logging.error(f"Erro ao processar item de PIB: {e}")
        
        if not dates or not values:
            logging.error("Nenhum dado válido de PIB encontrado")
            return None
        
        return {
            'dates': dates,
            'values': values,
            'label': 'Produto Interno Bruto',
            'unit': ''
        }
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados de PIB: {e}")
        return None



# ------------------------- Função para pegar valores do PIB da Paraíba -----------------
        
def get_pib_data_pb():
    try:
        logging.info("Iniciando busca de dados de PIB da Paraíba")
        
        # Atualizar URL para o formato correto
        url = f"{SIDRA_BASE_URL}/t/5938/v/37/p/all/c1/2607/d/last%201"
        
        logging.info(f"URL da requisição de PIB da Paraíba: {url}")
        
        # Adicionar cabeçalhos para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        logging.info(f"Código de status do PIB da Paraíba: {response.status_code}")
        logging.info(f"Conteúdo da resposta: {response.text[:500]}...")  # Mostrar primeiros 500 caracteres
        
        if response.status_code != 200:
            logging.error(f"Erro na requisição de PIB da Paraíba: {response.status_code}")
            logging.error(f"Conteúdo da resposta completo: {response.text}")
            return None
        
        data = response.json()
        
        if not data:
            logging.error("Dados de PIB da Paraíba retornados estão vazios")
            return None
        
        dates = []
        values = []
        
        for item in data:
            try:
                date_str = item.get('D2N', '')
                value = item.get('V', 0)
                
                if date_str and value is not None:
                    dates.append(date_str)
                    values.append(float(value))
            except Exception as e:
                logging.error(f"Erro ao processar item de PIB da Paraíba: {e}")
        
        logging.info(f"Dados de PIB da Paraíba processados: {len(dates)} registros")
        
        if not dates or not values:
            logging.error("Nenhum dado válido de PIB da Paraíba encontrado")
            return None
        
        return {
            'dates': dates,
            'values': values,
            'label': 'PIB da Paraíba',
            'unit': 'R$ milhões'
        }
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de conexão ao buscar PIB da Paraíba: {e}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao buscar dados de PIB da Paraíba: {e}")
        return None

# --------------- Função para coletar dados da Desocupação do Brasil ----------

def get_desocupacao_data():
    try:
        logging.info("Iniciando busca de dados de Desocupação")
        
        url = "https://apisidra.ibge.gov.br/values/t/4099/n1/all/v/4099/p/all?formato=json"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            logging.error(f"Erro na requisição de Desocupação: {response.status_code}")
            return None
        
        data = response.json()
        
        if not data:
            logging.error("Dados de Desocupação retornados estão vazios")
            return None
        
        dates = []
        values = []
        
        for item in data:
            try:
                # Converter data no formato YYYYMM para datetime
                date_str = item.get('D3C', '')
                
                # Ajustar o mês para o último mês do trimestre
                if date_str.endswith('01'):
                    date_str = date_str[:-2] + '03'
                elif date_str.endswith('02'):
                    date_str = date_str[:-2] + '06'
                elif date_str.endswith('03'):
                    date_str = date_str[:-2] + '09'
                elif date_str.endswith('04'):
                    date_str = date_str[:-2] + '12'
                
                # Converter valor para float
                value_str = item.get('V', '')
                value = float(value_str) if value_str else None
                
                if date_str and value is not None:
                    dates.append(date_str)
                    values.append(value)
            except Exception as e:
                logging.error(f"Erro ao processar item de Desocupação: {e}")
        
        if not dates or not values:
            logging.error("Nenhum dado válido de Desocupação encontrado")
            return None
        
        return {
            'dates': dates,
            'values': values,
            'label': 'Taxa de Desocupação',
            'unit': '%'
        }
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados de Desocupação: {e}")
        return None
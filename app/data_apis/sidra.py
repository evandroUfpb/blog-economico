import sidrapy
import pandas as pd
import logging
import functools
import time

def retry(max_attempts=3, delay_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = func(*args, **kwargs)
                    
                    # Validação adicional dos dados
                    if result is None or (isinstance(result, (list, dict)) and len(result) == 0):
                        raise ValueError("Dados inválidos ou vazios")
                    
                    return result
                
                except Exception as e:
                    attempts += 1
                    logging.warning(f"Tentativa {attempts} falhou para {func.__name__}: {e}")
                    
                    if attempts >= max_attempts:
                        logging.error(f"Falha após {max_attempts} tentativas para {func.__name__}")
                        return None
                    
                    time.sleep(delay_seconds)
        
        return wrapper
    return decorator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='data_fetch.log'  # Log em arquivo
)

@retry(max_attempts=3, delay_seconds=2)
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
                                   period="all")  # Toda a série histórica
        
        # Converte para DataFrame
        pib_raw = pd.DataFrame(pib_raw)
        
        # Validações adicionais
        if pib_raw is None or pib_raw.empty:
            raise ValueError("Dados do PIB não puderam ser obtidos")
        
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
        logging.error(f"Erro ao buscar dados do PIB: {e}")
        return None

@retry(max_attempts=3, delay_seconds=2)
def get_desocupacao_data(period_start=None, period_end=None):
    """
    Obtém dados do Desocupação do SIDRA/IBGE
    Tabela 4099 - Taxa de Desocupação
    """
    try:
        # Busca os dados da taxa de desocupação trimestral
        desocupacao_raw = sidrapy.get_table(table_code="4099",  # Tabela do desocupação trimestral
                                   territorial_level="1",  # Brasil
                                   variable="4099",
                                   ibge_territorial_code="1",
                                   period="all")  # Toda a série histórica
        
        # Converte para DataFrame
        desocupacao_raw = pd.DataFrame(desocupacao_raw)
        
        # Substitui as colunas pela primeira observação
        desocupacao_raw.columns = desocupacao_raw.iloc[0]
        
        # Retira a primeira observação
        desocupacao_raw = desocupacao_raw.iloc[1:, :]
        
        # Substitui '..' por NaN e converte para float
        desocupacao_raw['Valor'] = desocupacao_raw['Valor'].replace('..', pd.NA)
        desocupacao_raw['Valor'] = pd.to_numeric(desocupacao_raw['Valor'], errors='coerce')
        
        # Remove linhas com valores nulos
        desocupacao_raw = desocupacao_raw.dropna(subset=['Valor'])
        
        # Renomeia e seleciona as colunas
        desocupacao = desocupacao_raw.rename(columns={"Valor": "tx_desocupacao",
                                    "Trimestre (Código)": "date"})[['tx_desocupacao', 'date']]
        
        # Procedimento para lidar com a coluna de trimestre para transformar em data
        desocupacao['date'] = desocupacao['date'].str[:-2] + desocupacao['date'].str[-2:].replace({
            "01": "03",
            "02": "06",
            "03": "09",
            "04": "12"
        })
        
        # Transforma em formato date a coluna de data e insere no índice
        desocupacao.index = pd.to_datetime(desocupacao['date'], format="%Y%m")
        
        # Retira a coluna de data
        desocupacao = desocupacao.drop(columns=['date'])
        
        # Ordena o índice
        desocupacao = desocupacao.sort_index()
        
        # Prepara o resultado para o gráfico
        result = {
            'dates': desocupacao.index.strftime('%Y-%m-%d').tolist(),
            'values': desocupacao['tx_desocupacao'].tolist(),
            'label': 'Taxa de Desocupação - Trimestral'
        }
        
        return result
    
    except Exception as e:
        logging.error(f"Erro ao buscar dados do Desocupação: {e}")
        return None

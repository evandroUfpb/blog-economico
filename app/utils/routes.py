from flask import render_template, jsonify
from app.data_apis.sidra import get_pib_data, get_desocupacao_data
from app.data_apis.bcb import get_ipca_data
import logging

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('index.html')
    
    @app.route('/dashboard_pb')
    def dashboard_pb():
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/api/pib')
    def pib_api():
        try:
            logging.info("Iniciando busca de dados do PIB")
            data = get_pib_data()
            
            if data is None:
                logging.error("Dados do PIB retornaram None")
                return jsonify({
                    'error': 'Não foi possível obter os dados do PIB',
                    'dates': [],
                    'values': [],
                    'label': 'PIB Trimestral',
                    'unit': 'Milhões de Reais'
                }), 500
            
            logging.info(f"Dados do PIB obtidos: {len(data.get('dates', []))} registros")
            return jsonify(data)
        except Exception as e:
            logging.error(f"Erro ao buscar dados do PIB: {e}", exc_info=True)
            return jsonify({
                'error': str(e),
                'dates': [],
                'values': [],
                'label': 'PIB Trimestral',
                'unit': 'Milhões de Reais'
            }), 500
    
    @app.route('/api/desocupacao')
    def desocupacao_api():
        try:
            logging.info("Iniciando busca de dados de Desocupação")
            data = get_desocupacao_data()
            
            if data is None:
                logging.error("Dados de Desocupação retornaram None")
                return jsonify({
                    'error': 'Não foi possível obter os dados de Desocupação',
                    'dates': [],
                    'values': [],
                    'label': 'Taxa de Desocupação',
                    'unit': '%'
                }), 500
            
            logging.info(f"Dados de Desocupação obtidos: {len(data.get('dates', []))} registros")
            return jsonify(data)
        except Exception as e:
            logging.error(f"Erro ao buscar dados de Desocupação: {e}", exc_info=True)
            return jsonify({
                'error': str(e),
                'dates': [],
                'values': [],
                'label': 'Taxa de Desocupação',
                'unit': '%'
            }), 500
    
    @app.route('/api/ipca')
    def ipca_api():
        try:
            logging.info("Iniciando busca de dados do IPCA")
            data = get_ipca_data()
            
            if data is None:
                logging.error("Dados do IPCA retornaram None")
                return jsonify({
                    'error': 'Não foi possível obter os dados do IPCA',
                    'dates': [],
                    'values': [],
                    'label': 'IPCA',
                    'unit': '%'
                }), 500
            
            logging.info(f"Dados do IPCA obtidos: {len(data.get('dates', []))} registros")
            logging.info(f"Primeiros 5 registros: {data.get('dates')[:5]}, {data.get('values')[:5]}")
            
            return jsonify(data)
        except Exception as e:
            logging.error(f"Erro ao buscar dados do IPCA: {e}", exc_info=True)
            return jsonify({
                'error': str(e),
                'dates': [],
                'values': [],
                'label': 'IPCA',
                'unit': '%'
            }), 500
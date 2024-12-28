from flask import render_template, jsonify
from app import app
from app.data_apis import sidra, bcb

@app.route('/')
def index():
    return render_template('index.html', title='Blog Econômico')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Dashboard Econômico')

# API endpoints para dados econômicos
@app.route('/api/pib')
def get_pib_data():
    data = sidra.get_pib_data()
    if data is None:
        return jsonify({'message': 'Erro ao obter dados do PIB'})
    return jsonify(data)

@app.route('/api/ipca')
def get_ipca_data():
    data = bcb.get_ipca_data()
    if data is None:
        return jsonify({'message': 'Erro ao obter dados do IPCA'})
    # Implementaremos a lógica do IPEA depois
    return jsonify(data)

@app.route('/api/selic')
def get_selic_data():
    data = bcb.get_selic_data()
    if data is None:
        return jsonify({'message': 'Erro ao obter dados da Selic'})
    return jsonify(data)

@app.route('/about')
def about():
    return render_template('about.html')    
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'

# Importações locais para evitar circular import
from app.utils import routes
routes.init_routes(app)
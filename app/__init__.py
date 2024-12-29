from flask import Flask
#from app.utils.cache import init_cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'

from app import routes
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'

from app import routes
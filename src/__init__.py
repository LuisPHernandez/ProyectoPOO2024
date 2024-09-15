from flask import Flask 
import flask_sqlalchemy

# Se inicializa la aplicación Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Inicializar la base de datos
db = flask_sqlalchemy.SQLAlchemy(app)
import src.model as model  # No mover esta línea.

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def hello_world():
    return 'Hello, World!'
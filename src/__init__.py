from flask import Flask

# Se inicializa la aplicación Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route('/')
def hello_world():
    return 'Hello, World!'
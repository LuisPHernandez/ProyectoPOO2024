from flask import Flask, render_template, url_for, request, redirect, flash 
import flask_sqlalchemy

# Se inicializa la aplicación Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.secret_key = 'KKhdsakhu772*#$#($)'

# Inicializar la base de datos
db = flask_sqlalchemy.SQLAlchemy(app)
import src.model as model  # No mover esta línea.

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def homescreen():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = model.Usuario.query.filter_by(username=username, password=password).first()

        if usuario != None:

            if usuario.tipo == 1:
                return redirect(url_for('admin'))
            elif usuario.tipo == 2:
                return redirect(url_for('maestro'))
            elif usuario.tipo == 3:
                return redirect(url_for('padre'))
        else:
            flash('Usario o password inválido', 'error')

    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/maestro')
def maestro():
    return render_template('maestro.html')

@app.route('/padre')
def padre():
    return render_template('padre.html')
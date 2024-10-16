from flask import Flask, render_template, url_for, request, redirect, flash 
import flask_sqlalchemy
from src import forms
from sqlalchemy.exc import IntegrityError

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
            flash('Usuario o password inválido', 'error')

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

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route("/admin/list", methods=["GET", "POST"])
def user_list():
    data = model.Usuario.query.order_by(model.Usuario.username).all()
    return render_template('user_list.html', data=data)

@app.route("/admin/edit/<int:userid>" , methods=["GET", "POST"])
def user_edit(userid):
    form = forms.UsuarioForm()
    user = model.Usuario.query.filter(model.Usuario.id == userid).first()

    if form.cancel.data:
        flash('Operación cancelada, no se tomó ninguna acción.')
        return redirect(url_for('user_list'))

    if form.delete.data:
        if ((user is None) or (userid == 0)):
            flash('Imposible borrar usuario inexistente.')
        else:
            db.session.delete(user)
            db.session.commit()
            db.session.flush()
        return redirect(url_for('user_list'))

    if form.validate_on_submit():
        user = model.Usuario(None, None, None) if user is None else user
        user.update_from_form(form)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as ex:
            db.session.rollback()
            flash(
                'Nombre de usuario duplicado, imposible insertar', 'error')
        except Exception as ex: 
            db.session.rollback()
            flash(str(ex), 'error')
        else:
            db.session.flush()
            return redirect(url_for('user_list'))

    if user is not None:
        form.username.data = user.username
    return render_template('user_edit.html', form=form)

@app.route('/admin/agregar-alumno', methods=['GET', 'POST'])
def agregar_alumno():
    if request.method == 'POST':
        nombre = request.form['nombre']
        grado = request.form['grado']
        nuevo_alumno = model.Alumno(nombre=nombre, grado=grado)
        db.session.add(nuevo_alumno)
        db.session.commit()
        
        # Recuperar el ID autogenerado del alumno
        id_generado = nuevo_alumno.id

        return render_template('alumno_agregado.html', id=id_generado, nombre=nombre, grado=grado)
    
    return render_template('agregar_alumno.html')

@app.route('/admin/ver-alumnos')
def ver_alumnos():
    alumnos = model.Alumno.query.all()
    return render_template('lista_alumnos.html', alumnos=alumnos)

@app.route("/admin/lista-materia", methods =["GET", "POST"])
def lista_materia():
    data = model.Materia.query.order_by(model.Materia.nombre).all()
    return render_template("lista_materia.html", data = data)

@app.route("/admin/editar-materia/<int:materiaid>", methods =["GET", "POST"])
def editar_materia(materiaid):
    form = forms.MateriaForm()
    materia = model.Materia.query.filter(model.Materia.id == materiaid).first()

    if form.cancel.data:
        flash('Operación cancelada, no se tomó ninguna acción.')
        return redirect(url_for('lista_materia'))
    
    if form.delete.data:
        if ((materia is None) or (materiaid == 0)):
            flash('Imposible borrar materia inexistente.')
        else:
            db.session.delete(materia)
            db.session.commit()
            db.session.flush()
        return redirect(url_for('lista_materia'))
    
    if form.validate_on_submit():
        materia = model.Materia() if materia is None else materia
        materia.update_from_form(form)
        db.session.add(materia)
        try:
            db.session.commit()
        except IntegrityError as ex:
            db.session.rollback()
            flash('Nombre de materia duplicado, imposible insertar', 'error')
        except Exception as ex: 
            db.session.rollback()
            flash(str(ex), 'error')
        else:
            db.session.flush()
            return redirect(url_for('lista_materia'))
        
    if materia is not None:
        form.nombre.data = materia.nombre
    return render_template('editar_materia.html', form=form)



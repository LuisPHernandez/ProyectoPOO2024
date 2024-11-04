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

@app.route('/admin/editar-alumno/<int:id>', methods=['GET', 'POST'])
def editar_alumno(id):
    alumno = model.Alumno.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        grado = request.form['grado']
        
        alumno.nombre = nombre
        alumno.grado = grado
        
        db.session.commit()
        return redirect(url_for('ver_alumnos'))
    
    return render_template('editar_alumno.html', alumno=alumno)

@app.route('/eliminar_alumno/<int:id>', methods=['POST'])
def eliminar_alumno(id):
    alumno = model.Alumno.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return redirect(url_for('lista_alumnos'))

@app.route('/lista_alumnos')
def lista_alumnos():
    alumnos = model.Alumno.query.all()  
    return render_template('lista_alumnos.html', alumnos=alumnos)

@app.route('/materias/listar', methods=['GET'])
def listar_materias():
    materias = model.Materia.query.all()
    return render_template('listar_materias.html', materias=materias)

@app.route('/materias/<int:materia_id>/asignar', methods=['GET', 'POST'])
def asignar_alumno(materia_id):
    materia = model.Materia.query.get(materia_id)
    form = forms.AsignarAlumnoForm()
    alumnos_asignados_ids = [
        relacion.idAlumno for relacion in model.MateriaAlumno.query.filter_by(idMateria=materia_id).all()
    ]
    alumnos_disponibles = model.Alumno.query.filter(~model.Alumno.id.in_(alumnos_asignados_ids)).all()

    form.alumnos.choices = [(alumno.id, alumno.nombre) for alumno in alumnos_disponibles]

    if form.validate_on_submit():
        alumnos_seleccionados = form.alumnos.data
        for alumno_id in alumnos_seleccionados:
            asignacion = model.MateriaAlumno(idMateria=materia_id, idAlumno=alumno_id)
            db.session.add(asignacion)
        db.session.commit()
        return redirect(url_for('listar_materias'))
    return render_template('seleccionar_alumnos.html', form=form, materia=materia)

@app.route('/notas_y_alumnos')
def notas_y_alumnos():
    relaciones = db.session.query(model.MateriaAlumno, model.Alumno, model.Materia) \
        .join(model.Alumno, model.MateriaAlumno.idAlumno == model.Alumno.id) \
        .join(model.Materia, model.MateriaAlumno.idMateria == model.Materia.id) \
        .all()
    
    return render_template("notas_y_alumnos.html", relaciones=relaciones)

@app.route('/admin/ver-padres')
def ver_padres():
    padres = model.Usuario.query.filter_by(tipo=3).all()  # tipo 3 corresponde a los usuarios de tipo "padre"
    return render_template('ver_padres.html', padres=padres)

@app.route('/admin/asignar-alumno-padre/<int:padre_id>')
def asignar_alumno_padre_vista(padre_id):
    # Obtener el padre seleccionado
    padre = model.Usuario.query.get_or_404(padre_id)
    
    # Obtener los alumnos no asignados a un padre
    alumnos_no_asignados = model.Alumno.query.filter(~model.Alumno.id.in_(
        db.session.query(model.PadreAlumno.idAlumno).distinct()
    )).all()

    return render_template('asignar_alumno_padre.html', padre=padre, alumnos=alumnos_no_asignados)

@app.route('/admin/guardar-asignacion-alumno/<int:padre_id>/<int:alumno_id>', methods=['POST'])
def guardar_asignacion_alumno(padre_id, alumno_id):
    padre = model.Usuario.query.get_or_404(padre_id)
    alumno = model.Alumno.query.get_or_404(alumno_id)
    
    # Crear la relación entre el padre y el alumno
    relacion = model.PadreAlumno(idPadre=padre_id, idAlumno=alumno_id)
    db.session.add(relacion)
    db.session.commit()
    
    return redirect(url_for('asignar_alumno_padre_vista', padre_id=padre_id))

@app.route('/editar_nota/<int:relacion_id>', methods=['GET', 'POST'])
def editar_nota(relacion_id):
    relacion = model.MateriaAlumno.query.get_or_404(relacion_id)
    alumno = model.Alumno.query.get_or_404(relacion.idAlumno)
    materia = model.Materia.query.get_or_404(relacion.idMateria)

    if request.method == 'POST':
        nueva_nota = request.form.get('nota')
        relacion.nota = nueva_nota
        db.session.commit()
        
        flash("Nota actualizada con éxito")
        return redirect(url_for('notas_y_alumnos'))

    return render_template('editar_nota.html', alumno=alumno, materia=materia, relacion=relacion)





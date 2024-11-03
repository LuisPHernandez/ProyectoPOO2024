from src import db, app


# Catálogo de tipos de usuario
class UsuarioTipo(db.Model):
    __tablename__ = 'UsuarioTipo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(32), unique=True, nullable=False)

# Tabla de información de usuario
class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    tipo = db.Column(db.Integer, db.ForeignKey(UsuarioTipo.id))

    def __init__(self, username, password, tipo):
        self.username = username
        self.password = password
        self.tipo = tipo

    def update_from_form(self, form):
        self.username = form.username.data.strip()
        if form.password.data.strip() != "": 
            self.password = form.password.data.strip()
        self.tipo = form.type.data

# Tabla de información de alumnos
class Alumno(db.Model):
    __tablename__ = 'Alumno'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(32), nullable=False)
    grado = db.Column(db.Integer, nullable=False)

# Tabla de información de materias
class Materia(db.Model):
    __tablename__ = 'Materia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(32), nullable=False)
    maestro = db.Column(db.Integer, db.ForeignKey(Usuario.id))

    def update_from_form(self, form):
        self.nombre = form.nombre.data.strip()
        self.maestro = int(form.idmaestro.data)

# Tabla de relación entre materias, alumnos y sus notas
class MateriaAlumno(db.Model):
    __tablename__ = 'MateriaAlumno'
    relacion = db.Column(db.Integer, primary_key=True)
    idMateria = db.Column(db.Integer, db.ForeignKey(Materia.id))
    idAlumno = db.Column(db.Integer, db.ForeignKey(Alumno.id))
    nota = db.Column(db.Integer)
    
    
#################################################################################
# Declaración de valores por defecto de base de datos
#################################################################################

def _inicializar_tipos_usuario(*args, **kwargs):
    # Crear tipos de usuario default
    tipo_usuario = UsuarioTipo(tipo='Administrador')
    db.session.add(tipo_usuario)
    tipo_usuario = UsuarioTipo(tipo='Maestro')
    db.session.add(tipo_usuario)
    tipo_usuario = UsuarioTipo(tipo='Padre')
    db.session.add(tipo_usuario)
    db.session.commit()

def _inicializar_usuarios(*args, **kwargs):
    # Crear usuarios default
    admin = Usuario('admin', app.config['ADMIN_PASSWORD'], 1)
    db.session.add(admin)
    db.session.commit()


#################################################################################
# Inicialización de valores por defecto de base de datos
#################################################################################
db.event.listen(UsuarioTipo.__table__, 'after_create', _inicializar_tipos_usuario)
db.event.listen(Usuario.__table__, 'after_create', _inicializar_usuarios)






    





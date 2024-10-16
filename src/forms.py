from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import InputRequired

class UsuarioForm(FlaskForm):
    uid = IntegerField("uuid", default=None)
    username = StringField(
        "Usuario:",
        render_kw={
            "autofocus": True,
        },
        validators=[InputRequired()],
    )
    password = PasswordField("Password:")
    type = RadioField("Tipo:", choices=[(1, 'Admin'), (2, 'Maestro'), (3, 'Padre')])
    save = SubmitField("Guardar")
    cancel = SubmitField("Cancelar")
    delete = SubmitField("Borrar")

class MateriaForm(FlaskForm):
    mid = IntegerField("ID", default=None)
    nombre = StringField(
        "Nombre de la Materia:",
        validators=[InputRequired()],
    )
    idmaestro = IntegerField(
        "ID del Maestro:",
        validators=[InputRequired()],
    )
    save = SubmitField("Guardar")
    cancel = SubmitField("Cancelar")
    delete = SubmitField("Borrar") 
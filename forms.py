"""
Formularios con validación para la Red Social
Usando WTForms y Flask-WTF
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from models import Usuario


class RegistroForm(FlaskForm):
    """Formulario de registro de nuevo usuario"""
    
    username = StringField(
        'Nombre de usuario',
        validators=[
            DataRequired(message='El nombre de usuario es requerido'),
            Length(min=3, max=80, message='El nombre de usuario debe tener entre 3 y 80 caracteres')
        ],
        render_kw={"placeholder": "Nombre de usuario"}
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='El email es requerido'),
            Email(message='Email inválido')
        ],
        render_kw={"placeholder": "tu@email.com"}
    )
    
    nombre = StringField(
        'Nombre completo',
        validators=[Optional(), Length(max=120)],
        render_kw={"placeholder": "Nombre completo (opcional)"}
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message='La contraseña es requerida'),
            Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
        ],
        render_kw={"placeholder": "Contraseña"}
    )
    
    confirmar_password = PasswordField(
        'Confirmar contraseña',
        validators=[
            DataRequired(message='Confirma tu contraseña'),
            EqualTo('password', message='Las contraseñas no coinciden')
        ],
        render_kw={"placeholder": "Confirmar contraseña"}
    )
    
    submit = SubmitField('Registrarse')
    
    def validate_username(self, username):
        """Validar que el username sea único"""
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Ese nombre de usuario ya está en uso. Elige otro.')
    
    def validate_email(self, email):
        """Validar que el email sea único"""
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Ese email ya está registrado. Intenta con otro.')


class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    
    username = StringField(
        'Nombre de usuario',
        validators=[DataRequired(message='El nombre de usuario es requerido')],
        render_kw={"placeholder": "Nombre de usuario"}
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es requerida')],
        render_kw={"placeholder": "Contraseña"}
    )
    
    submit = SubmitField('Iniciar Sesión')


class PostForm(FlaskForm):
    """Formulario para crear publicaciones"""
    
    contenido = TextAreaField(
        'Contenido',
        validators=[
            DataRequired(message='El contenido no puede estar vacío'),
            Length(min=1, max=5000, message='El contenido debe tener entre 1 y 5000 caracteres')
        ],
        render_kw={"placeholder": "¿Qué estás pensando?", "rows": 4}
    )
    
    imagen = FileField(
        'Imagen (opcional)',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes (jpg, jpeg, png, gif)')
        ]
    )
    
    submit = SubmitField('Publicar')


class ComentarioForm(FlaskForm):
    """Formulario para comentarios"""
    
    contenido = TextAreaField(
        'Comentario',
        validators=[
            DataRequired(message='El comentario no puede estar vacío'),
            Length(min=1, max=1000, message='El comentario debe tener entre 1 y 1000 caracteres')
        ],
        render_kw={"placeholder": "Escribe un comentario...", "rows": 2}
    )
    
    submit = SubmitField('Comentar')


class PerfilForm(FlaskForm):
    """Formulario para editar perfil de usuario"""
    
    nombre = StringField(
        'Nombre completo',
        validators=[Optional(), Length(max=120, message='El nombre no puede exceder 120 caracteres')],
        render_kw={"placeholder": "Tu nombre completo"}
    )
    
    biografia = TextAreaField(
        'Biografía',
        validators=[Optional(), Length(max=500, message='La biografía no puede exceder 500 caracteres')],
        render_kw={"placeholder": "Cuéntanos sobre ti...", "rows": 4}
    )
    
    avatar = FileField(
        'Avatar (opcional)',
        validators=[
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes (jpg, jpeg, png, gif)')
        ]
    )
    
    submit = SubmitField('Guardar Cambios')

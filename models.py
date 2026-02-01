"""
Modelos de base de datos para la Red Social
Usando SQLAlchemy ORM
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    """Modelo de usuario para la base de datos"""
    
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(120), nullable=True)
    biografia = db.Column(db.Text, nullable=True, default='')
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True, default='default_avatar.png')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    posts = db.relationship('Post', backref='usuario', lazy=True, cascade='all, delete-orphan')
    comentarios = db.relationship('Comentario', backref='usuario', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='usuario', lazy=True, cascade='all, delete-orphan')
    
    # Relaciones de seguimiento
    seguidos = db.relationship(
        'Seguimiento',
        foreign_keys='Seguimiento.seguidor_id',
        backref='seguidor',
        lazy=True,
        cascade='all, delete-orphan'
    )
    seguidores = db.relationship(
        'Seguimiento',
        foreign_keys='Seguimiento.seguido_id',
        backref='seguido',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def set_password(self, password):
        """Hashear y establecer contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def seguir(self, otro_usuario):
        """Seguir a otro usuario"""
        if not self.esta_siguiendo(otro_usuario):
            seguimiento = Seguimiento(seguidor_id=self.id, seguido_id=otro_usuario.id)
            db.session.add(seguimiento)
            db.session.commit()
    
    def dejar_de_seguir(self, otro_usuario):
        """Dejar de seguir a otro usuario"""
        seguimiento = Seguimiento.query.filter_by(
            seguidor_id=self.id,
            seguido_id=otro_usuario.id
        ).first()
        if seguimiento:
            db.session.delete(seguimiento)
            db.session.commit()
    
    def esta_siguiendo(self, otro_usuario):
        """Verificar si está siguiendo a otro usuario"""
        return Seguimiento.query.filter_by(
            seguidor_id=self.id,
            seguido_id=otro_usuario.id
        ).first() is not None
    
    def __repr__(self):
        return f'<Usuario {self.username}>'


class Post(db.Model):
    """Modelo para publicaciones"""
    
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, index=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    comentarios = db.relationship('Comentario', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    
    # Alias para compatibilidad con templates
    @property
    def autor(self):
        """Alias para usuario (compatibilidad con templates)"""
        return self.usuario
    
    def cantidad_likes(self):
        """Obtener cantidad de likes"""
        return len(self.likes)
    
    def cantidad_comentarios(self):
        """Obtener cantidad de comentarios"""
        return len(self.comentarios)
    
    def __repr__(self):
        return f'<Post {self.id}>'


class Comentario(db.Model):
    """Modelo para comentarios"""
    
    __tablename__ = 'comentario'
    
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Alias para compatibilidad con templates
    @property
    def autor(self):
        """Alias para usuario (compatibilidad con templates)"""
        return self.usuario
    
    def __repr__(self):
        return f'<Comentario {self.id}>'


class Like(db.Model):
    """Modelo para likes en publicaciones"""
    
    __tablename__ = 'like'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Índice único para evitar likes duplicados
    __table_args__ = (db.UniqueConstraint('usuario_id', 'post_id', name='unique_like'),)
    
    def __repr__(self):
        return f'<Like {self.usuario_id} - {self.post_id}>'


class Seguimiento(db.Model):
    """Modelo para relación de seguimiento entre usuarios"""
    
    __tablename__ = 'seguimiento'
    
    id = db.Column(db.Integer, primary_key=True)
    seguidor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, index=True)
    seguido_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, index=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Índice único para evitar seguimientos duplicados
    __table_args__ = (db.UniqueConstraint('seguidor_id', 'seguido_id', name='unique_seguimiento'),)
    
    def __repr__(self):
        return f'<Seguimiento {self.seguidor_id} -> {self.seguido_id}>'

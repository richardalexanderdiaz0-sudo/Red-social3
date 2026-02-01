from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from models import db, Usuario, Post, Comentario, Like, Seguimiento
from forms import RegistroForm, LoginForm, PostForm, ComentarioForm, PerfilForm
import os
from datetime import datetime

app = Flask(__name__)
# Usar variables de entorno en producción, o valores por defecto en desarrollo
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu-clave-secreta-super-segura-cambiar-en-produccion')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///redsocial.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None

def init_db():
    """Inicializa la base de datos y crea las carpetas necesarias"""
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            nombre=form.nombre.data
        )
        usuario.set_password(form.password.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('feed'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

@app.route('/feed')
@login_required
def feed():
    # Obtener posts de usuarios seguidos y del usuario actual
    seguidos_ids = [s.seguido_id for s in Seguimiento.query.filter_by(seguidor_id=current_user.id).all()]
    seguidos_ids.append(current_user.id)
    
    posts = Post.query.filter(Post.usuario_id.in_(seguidos_ids))\
                      .order_by(Post.fecha_creacion.desc())\
                      .limit(50).all()
    
    form = PostForm()
    comentario_form = ComentarioForm()
    
    return render_template('feed.html', posts=posts, post_form=form, comentario_form=comentario_form)

@app.route('/post/crear', methods=['POST'])
@login_required
def crear_post():
    form = PostForm()
    if form.validate_on_submit():
        imagen_filename = None
        if 'imagen' in request.files:
            archivo = request.files['imagen']
            if archivo.filename:
                imagen_filename = save_uploaded_file(archivo)
        
        post = Post(
            contenido=form.contenido.data,
            imagen=imagen_filename,
            usuario_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('¡Publicación creada exitosamente!', 'success')
    
    return redirect(url_for('feed'))

@app.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(usuario_id=current_user.id, post_id=post_id).first()
    
    if like:
        db.session.delete(like)
        accion = 'unliked'
    else:
        like = Like(usuario_id=current_user.id, post_id=post_id)
        db.session.add(like)
        accion = 'liked'
    
    db.session.commit()
    
    return jsonify({
        'accion': accion,
        'cantidad_likes': post.cantidad_likes()
    })

@app.route('/post/<int:post_id>/comentario', methods=['POST'])
@login_required
def crear_comentario(post_id):
    form = ComentarioForm()
    post = Post.query.get_or_404(post_id)
    
    if form.validate_on_submit():
        comentario = Comentario(
            contenido=form.contenido.data,
            usuario_id=current_user.id,
            post_id=post_id
        )
        
        db.session.add(comentario)
        db.session.commit()
        
        flash('Comentario agregado.', 'success')
    else:
        # Si la validación falla, mostrar errores
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error en {field}: {error}', 'error')
    
    return redirect(url_for('feed'))

@app.route('/usuario/<username>')
@login_required
def perfil(username):
    usuario = Usuario.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(usuario_id=usuario.id)\
                      .order_by(Post.fecha_creacion.desc()).all()
    
    # Estadísticas
    cantidad_seguidores = Seguimiento.query.filter_by(seguido_id=usuario.id).count()
    cantidad_seguidos = Seguimiento.query.filter_by(seguidor_id=usuario.id).count()
    es_seguido = False
    
    if current_user.is_authenticated and current_user.id != usuario.id:
        es_seguido = current_user.esta_siguiendo(usuario)
    
    return render_template('profile.html', 
                         usuario=usuario, 
                         posts=posts,
                         cantidad_seguidores=cantidad_seguidores,
                         cantidad_seguidos=cantidad_seguidos,
                         es_seguido=es_seguido)

@app.route('/usuario/<username>/seguir', methods=['POST'])
@login_required
def seguir_usuario(username):
    usuario = Usuario.query.filter_by(username=username).first_or_404()
    
    if usuario.id == current_user.id:
        return jsonify({'error': 'No puedes seguirte a ti mismo.'}), 400
    
    if current_user.esta_siguiendo(usuario):
        current_user.dejar_de_seguir(usuario)
        accion = 'unfollowed'
    else:
        current_user.seguir(usuario)
        accion = 'followed'
    
    cantidad_seguidores = Seguimiento.query.filter_by(seguido_id=usuario.id).count()
    
    return jsonify({
        'accion': accion,
        'cantidad_seguidores': cantidad_seguidores
    })

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = PerfilForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.nombre = form.nombre.data
        current_user.biografia = form.biografia.data
        
        if 'avatar' in request.files:
            archivo = request.files['avatar']
            if archivo.filename:
                avatar_filename = save_uploaded_file(archivo)
                if avatar_filename:
                    current_user.avatar = avatar_filename
        
        db.session.commit()
        flash('Perfil actualizado exitosamente.', 'success')
        return redirect(url_for('perfil', username=current_user.username))
    
    return render_template('edit_profile.html', form=form)

@app.route('/usuarios')
@login_required
def usuarios():
    query = request.args.get('q', '')
    usuarios = Usuario.query.filter(
        Usuario.username.contains(query) | 
        Usuario.nombre.contains(query)
    ).limit(20).all()
    
    return render_template('usuarios.html', usuarios=usuarios, query=query)

@app.route('/manifest.json')
def manifest():
    return app.send_file('static/manifest.json', mimetype='application/json')

@app.route('/sw.js')
def service_worker():
    return app.send_file('static/sw.js', mimetype='application/javascript')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Inicializar base de datos y carpetas al iniciar la aplicación
    init_db()
    # Usar debug solo en desarrollo, no en producción
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)


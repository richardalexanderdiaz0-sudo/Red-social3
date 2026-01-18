# Red Social Completa - Full Stack 🚀

Una red social completa desarrollada con Flask (Backend) y HTML/CSS/JavaScript (Frontend) que incluye todas las funcionalidades esenciales.

## ✨ Características Completas

### Backend (Flask + SQLite)
- ✅ **Autenticación completa**: Registro, Login, Logout con sesiones seguras
- ✅ **Gestión de usuarios**: Perfiles personalizables con avatar y biografía
- ✅ **Sistema de publicaciones**: Crear posts con texto e imágenes
- ✅ **Feed personalizado**: Ver publicaciones de usuarios seguidos
- ✅ **Sistema de seguimiento**: Seguir/dejar de seguir usuarios
- ✅ **Interacciones**: Likes y comentarios en publicaciones
- ✅ **Búsqueda de usuarios**: Buscar usuarios por nombre o username
- ✅ **API REST**: Endpoints JSON para likes y seguimiento

### Frontend (HTML/CSS/JS)
- ✅ **Diseño moderno**: Interfaz con gradientes y colores vibrantes
- ✅ **Responsive**: Funciona en móviles, tablets y desktop
- ✅ **Animaciones suaves**: Transiciones y efectos visuales
- ✅ **JavaScript interactivo**: Likes, comentarios, búsqueda en tiempo real

### PWA (Progressive Web App)
- ✅ **Instalable**: Se puede instalar como app nativa
- ✅ **Funciona offline**: Cacheo de archivos estáticos
- ✅ **Service Worker**: Manejo de caché y funcionalidad offline
- ✅ **Manifest.json**: Configuración completa de PWA

## 🚀 Inicio Rápido

### Opción 1: Script automático (Recomendado)
```bash
./start.sh
```

### Opción 2: Manual
```bash
# 1. Instalar dependencias
python3 -m pip install --user -r requirements.txt

# 2. Ejecutar la aplicación
python3 app.py
```

### 3. Abrir en el navegador
```
http://localhost:5000
```

## 📁 Estructura del Proyecto

```
ComfyUI/
├── app.py                 # ⭐ Aplicación Flask principal (Backend)
├── models.py             # ⭐ Modelos de base de datos (SQLAlchemy)
├── forms.py              # ⭐ Formularios con validación (WTForms)
├── start.sh              # Script de inicio rápido
├── requirements.txt      # Dependencias Python
│
├── templates/            # ⭐ Plantillas HTML (Frontend)
│   ├── base.html        # Template base con navegación
│   ├── index.html       # Página de inicio
│   ├── login.html       # Login
│   ├── register.html    # Registro
│   ├── feed.html        # Feed de publicaciones
│   ├── profile.html     # Perfil de usuario
│   ├── edit_profile.html# Editar perfil
│   ├── usuarios.html    # Búsqueda de usuarios
│   └── 404.html         # Página de error
│
├── static/               # ⭐ Archivos estáticos
│   ├── css/
│   │   └── style.css    # Estilos completos con colores
│   ├── js/
│   │   └── main.js      # JavaScript interactivo
│   ├── manifest.json    # ⭐ Configuración PWA
│   ├── sw.js            # ⭐ Service Worker (PWA)
│   └── uploads/         # Imágenes subidas (avatars, posts)
│       └── default_avatar.png
│
└── instance/             # Base de datos SQLite (se crea automáticamente)
    └── redsocial.db
```

## 🎯 Funcionalidades Detalladas

### 1. Autenticación
- Registro con validación de email único
- Login con sesiones persistentes
- Logout seguro
- Protección de rutas con `@login_required`

### 2. Perfiles de Usuario
- Avatar personalizable
- Nombre completo
- Biografía
- Estadísticas: posts, seguidores, siguiendo

### 3. Publicaciones
- Crear posts con texto
- Subir imágenes (PNG, JPG, JPEG, GIF)
- Ver todas las publicaciones en el feed
- Filtrado por usuarios seguidos

### 4. Interacciones
- Sistema de likes (toggle on/off)
- Comentarios en publicaciones
- Contadores en tiempo real

### 5. Seguimiento
- Seguir/dejar de seguir usuarios
- Feed personalizado con posts de seguidos
- Ver lista de seguidores y seguidos

### 6. Búsqueda
- Buscar usuarios por nombre o username
- Resultados en tiempo real

## 🎨 Tecnologías Utilizadas

### Backend
- **Flask 3.0.0**: Framework web
- **Flask-SQLAlchemy 3.1.1**: ORM para base de datos
- **Flask-Login 0.6.3**: Gestión de sesiones
- **Flask-WTF 1.2.1**: Formularios con CSRF protection
- **SQLite**: Base de datos

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con variables CSS, gradientes, animaciones
- **JavaScript (Vanilla)**: Interactividad sin frameworks
- **PWA**: Service Worker y Manifest

## 🔒 Seguridad

- Contraseñas hasheadas con Werkzeug
- Protección CSRF en formularios
- Validación de tipos de archivo
- Sanitización de nombres de archivo
- Sesiones seguras

## 📱 PWA - Instalación

La aplicación es una Progressive Web App completa:

1. **Chrome/Edge**: Verás el botón de instalación en la barra de direcciones
2. **Firefox**: Menú → Instalar sitio
3. **Safari iOS**: Compartir → Añadir a pantalla de inicio

### Funcionalidades PWA
- ✅ Instalable en dispositivos
- ✅ Funciona offline (contenido cacheado)
- ✅ Icono en la pantalla de inicio
- ✅ Experiencia nativa

## 🛠️ Comandos Útiles

```bash
# Verificar que todo funciona
python3 -c "from app import app; print('✓ OK')"

# Limpiar base de datos (si quieres empezar de nuevo)
rm instance/redsocial.db

# Ver archivos de la aplicación
ls -la templates/ static/
```

## 📝 Notas

- La base de datos se crea automáticamente en `instance/redsocial.db`
- Las imágenes se guardan en `static/uploads/`
- El servidor se ejecuta en modo debug (cambiar en producción)
- La clave secreta debe cambiarse en producción

## 🎉 ¡La aplicación está completa y funcional!

Todo está listo para usar. Simplemente ejecuta `./start.sh` o `python3 app.py` y empieza a usar tu red social.

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que todas las dependencias estén instaladas
2. Asegúrate de tener Python 3.7+
3. Revisa los logs en la consola

---

**Desarrollado con ❤️ usando Flask y tecnologías web modernas**

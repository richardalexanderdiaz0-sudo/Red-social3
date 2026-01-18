# 🚀 Guía de Despliegue - Publicar tu Red Social

Guía completa para publicar tu aplicación en diferentes plataformas.

## 📋 Requisitos Previos

1. **Cuenta en la plataforma elegida** (gratis disponible en todas)
2. **Git instalado** en tu computadora
3. **Código de la app listo** (ya lo tienes ✅)

---

## 🎯 Opción 1: Render.com (Recomendado - Gratis)

### Ventajas:
- ✅ **Gratis** con plan free tier
- ✅ **Muy fácil** de usar
- ✅ **Despliegue automático** desde GitHub
- ✅ **HTTPS incluido**
- ✅ **Base de datos SQLite** funciona bien

### Pasos:

#### 1. Subir código a GitHub
```bash
# Inicializar Git (si no lo has hecho)
git init
git add .
git commit -m "Red Social - Primera versión"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/TU_USUARIO/red-social.git
git branch -M main
git push -u origin main
```

#### 2. Crear cuenta en Render.com
1. Ve a [render.com](https://render.com)
2. Regístrate con GitHub (gratis)
3. Haz clic en "New +" → "Web Service"

#### 3. Conectar repositorio
1. Conecta tu cuenta de GitHub
2. Selecciona tu repositorio `red-social`
3. Configura:
   - **Name**: `red-social` (o el que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: **Free**

#### 4. Variables de entorno (opcional)
En "Environment Variables" agrega:
```
SECRET_KEY = tu-clave-secreta-super-segura-generada
FLASK_DEBUG = False
PORT = 10000
```

#### 5. ¡Desplegar!
- Haz clic en "Create Web Service"
- Espera 2-3 minutos
- ¡Tu app estará en `https://red-social.onrender.com`!

---

## 🎯 Opción 2: Railway.app (Gratis)

### Ventajas:
- ✅ **Muy rápido**
- ✅ **Interfaz moderna**
- ✅ **Despliegue con un clic**

### Pasos:

#### 1. Subir a GitHub (igual que Render)

#### 2. Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. "Login with GitHub"
3. "New Project" → "Deploy from GitHub repo"

#### 3. Seleccionar repositorio
- Selecciona tu repo `red-social`
- Railway detecta automáticamente que es Python

#### 4. Variables de entorno (opcional)
En "Variables" tab:
```
SECRET_KEY = tu-clave-secreta
```

#### 5. ¡Listo!
- Railway despliega automáticamente
- URL: `https://red-social-production.up.railway.app`

---

## 🎯 Opción 3: PythonAnywhere (Gratis)

### Ventajas:
- ✅ **Especializado en Python**
- ✅ **Perfecto para Flask**
- ✅ **Muy estable**

### Pasos:

#### 1. Crear cuenta
1. Ve a [pythonanywhere.com](https://www.pythonanywhere.com)
2. Crea cuenta gratuita (Beginner account)

#### 2. Subir archivos
1. En el Dashboard → "Files" tab
2. Crea carpeta `mysite/` o usa la existente
3. Sube todos los archivos de tu app:
   - `app.py`
   - `models.py`
   - `forms.py`
   - `requirements.txt`
   - Carpeta `templates/`
   - Carpeta `static/`

#### 3. Instalar dependencias
1. Abre "Consoles" → "Bash"
2. Ejecuta:
```bash
pip3.9 install --user flask flask-sqlalchemy flask-login flask-wtf wtforms werkzeug pillow gunicorn
```

#### 4. Configurar web app
1. Dashboard → "Web" tab
2. Haz clic en el link de tu web app
3. En "Source code": `/home/TU_USUARIO/mysite`
4. En "Working directory": `/home/TU_USUARIO/mysite`
5. En "WSGI configuration file": edita y cambia a:
```python
import sys
path = '/home/TU_USUARIO/mysite'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

#### 5. ¡Desplegar!
- Guarda y haz clic en el botón verde "Reload"
- URL: `https://TU_USUARIO.pythonanywhere.com`

---

## 🎯 Opción 4: Heroku (Requiere tarjeta, pero tier gratuito)

### Pasos:

#### 1. Instalar Heroku CLI
```bash
# En Linux/Mac
curl https://cli-assets.heroku.com/install.sh | sh

# O descargar desde heroku.com/cli
```

#### 2. Login
```bash
heroku login
```

#### 3. Crear app
```bash
heroku create red-social-app
```

#### 4. Configurar variables
```bash
heroku config:set SECRET_KEY=tu-clave-secreta-super-segura
```

#### 5. Desplegar
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

#### 6. ¡Listo!
```bash
heroku open
```

---

## 🔐 Configurar Variables de Entorno

### Generar SECRET_KEY segura:
```python
# Ejecuta en Python
import secrets
print(secrets.token_hex(32))
```

Copia el resultado y úsalo como `SECRET_KEY` en las variables de entorno.

---

## ✅ Checklist Antes de Desplegar

- [ ] ✅ Archivos `Procfile` creado
- [ ] ✅ `gunicorn` en `requirements.txt`
- [ ] ✅ `runtime.txt` especificado
- [ ] ✅ Código subido a GitHub
- [ ] ✅ `SECRET_KEY` generada y configurada
- [ ] ✅ `FLASK_DEBUG=False` en producción

---

## 🐛 Solución de Problemas

### Error: "Module not found"
- Verifica que todas las dependencias estén en `requirements.txt`

### Error: "No module named 'app'"
- Asegúrate de que `app.py` esté en la raíz del proyecto

### Error: "Database locked"
- SQLite puede tener problemas en algunas plataformas
- Considera usar PostgreSQL (gratis en Render/Railway)

### La app no carga
- Revisa los logs en la plataforma
- Verifica que el puerto sea configurado correctamente
- Asegúrate de que `gunicorn` esté en requirements.txt

---

## 📝 Notas Importantes

1. **SQLite en producción**: Funciona bien para apps pequeñas/medianas. Para apps grandes, considera PostgreSQL.

2. **Archivos estáticos**: Todas las plataformas sirven `/static/` automáticamente.

3. **Base de datos**: En algunas plataformas el disco es efímero. Considera usar servicios de BD separados para datos persistentes.

4. **HTTPS**: Todas las plataformas mencionadas incluyen HTTPS gratis.

---

## 🎉 ¡Ya está!

Elige la opción que prefieras. **Render.com** es la más fácil para empezar. 

¿Necesitas ayuda con algún paso específico?


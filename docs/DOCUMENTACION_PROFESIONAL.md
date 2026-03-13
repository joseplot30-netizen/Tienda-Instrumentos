# Documentación Técnica - Music Store (Proyecto Python)

> **Nota:** Esta documentación está diseñada para ser un recurso completo y profesional (estilo Microsoft) que explique la arquitectura, el despliegue, el uso y los detalles técnicos internos del proyecto.

---

## 🏷️ Keywords

Flask, MySQL, Aiven, Render, GitHub, despliegue, API REST, carrito, administrador, productos, Jinja2, CSS, JavaScript, seguridad.
### Keywords de SEO (meta keywords)

Las keywords que se incluyen en el `<meta name="keywords">` de `templates/layout.html` son:

- tienda de instrumentos
- guitarras
- bajos
- baterías
- accesorios musicales
- compra online
- carrito de compras
- música
- instrumentos eléctricos
- envío rápido
- ofertas musicales
---

## 🧩 1. Visión General del Proyecto

**Music Store** es una aplicación web de comercio electrónico orientada a la venta de instrumentos musicales (guitarras, bajos, baterías, teclados, accesorios, etc.).

La solución está desarrollada como un proyecto monolítico en **Flask (Python 3.13)** con una **base de datos MySQL** y una interfaz de usuario responsiva construida con **HTML/CSS/JavaScript (Vanilla)**.

### Objetivo

Permitir a clientes registrar cuentas, navegar el catálogo, agregar productos al carrito y enviar mensajes de contacto, mientras que los administradores pueden gestionar usuarios, productos y contenido del sitio.

### Público objetivo

- **Usuarios finales**: clientes que compran instrumentos.
- **Administradores**: gestores de productos, usuarios y contenido.

---

## ✅ 2. Características Principales

### Funcionales

- Registro e inicio de sesión de usuarios
- Roles: **usuario** y **admin**
- Catálogo de productos con categorización (guitarras, bajos, baterías, otros)
- Carrito de compras en cliente (localStorage) con contador dinámico
- Búsqueda y filtros por marca, categoría y rango de precio
- Panel administrativo para CRUD de usuarios y productos
- Gestión de contenido estático (Contacto y Nosotros)
- API REST para productos y contador de carrito

### Técnicas

- Interfaz SPA-lite (sin frameworks externos de front-end)
- Gestión de sesiones con Flask
- Templates con Jinja2
- Gestión de assets estáticos en `static/`
- Uso de `url_for()` para rutas y recursos estáticos
- Mensajes “flash” para feedback al usuario (SweetAlert2 + confetti)
- Menú responsive + sidebar para filtros

---

## 🏗️ 3. Arquitectura y Estructura de Código

### 3.1. Tech Stack

| Capa | Tecnología | Responsabilidad |
|------|------------|-----------------|
| Backend | Python 3.13 + Flask 3.1 | Enrutamiento, lógica de negocio, sessions, conexión a BD |
| Base de Datos | MySQL | Persistencia de usuarios, productos y mensajes de contacto |
| Frontend | HTML5 / CSS3 / JS | Interfaz, navegación, validación, filtros |
| Templating | Jinja2 | Renderizado dinámico de HTML |
| Despliegue | gunicorn + Procfile | Producción en contenedores / servidores |

### 3.2. Estructura de Carpetas

```
proyecto_python/
├── app.py                    # Aplicación principal de Flask
├── insertar_productos.py     # Script para importar productos (desde SQL)
├── requirements.txt          # Dependencias Python
├── Procfile                  # (Heroku / despliegues) comando de ejecución
├── docs/                     # Documentación del proyecto (ahora en Markdown)
├── static/                   # Archivos estáticos (CSS, JS, imágenes)
└── templates/                # Plantillas Jinja2 (páginas públicas y admin)
```

---

## 🧠 4. Base de Datos (MySQL)

### 4.1. Configuración de Conexión (en `app.py`)

El proyecto puede ejecutarse con **MySQL local** o con una base de datos alojada en **Aiven (MySQL Cloud)**.

#### Conexión local (desarrollo)

```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'bd_users'
}
```

#### Conexión Aiven (producción / staging)

Aiven provee un endpoint de MySQL que incluye host, puerto, usuario y contraseña.

```python
db_config = {
    'host': '<aiven-host>',
    'port': 26308,                # ejemplo, usar el puerto real del servicio Aiven
    'user': '<aiven-username>',
    'password': '<aiven-password>',
    'database': 'bd_users'
}
```

> 🔧 En producción, **no** usar credenciales en claro en el código. Utiliza variables de entorno (ej. `os.environ`) o un vault seguro.

### 4.1.1. Conectarse con MySQL Workbench

Para gestionar la base de datos Aiven desde MySQL Workbench:

1. Crear una nueva conexión.
2. Usar el **host**, **puerto**, **usuario** y **contraseña** que Aiven proporciona.
3. Si Aiven requiere SSL, habilitar la opción SSL en la conexión y añadir el certificado proporcionado.

> Nota: Aiven puede usar certificados personalizados; revisa la sección "Connection details" en el panel de Aiven.

### 4.2. Tablas Principales

#### Tabla `users`
- `id` (INT, PK, auto-increment)
- `username` (VARCHAR(255), UNIQUE)
- `email` (VARCHAR(255), UNIQUE)
- `password` (VARCHAR(255))
- `is_admin` (BOOLEAN)
- `created_at`, `updated_at` (TIMESTAMP)

> ⚠️ Actualmente la contraseña se almacena en texto plano. **Obligatorio** migrar a hashing (bcrypt/werkzeug) en producción.

#### Tabla `products`
- `id` (INT, PK)
- `name` (VARCHAR(255))
- `price` (DECIMAL(10,2))
- `stock` (INT)
- `category` (VARCHAR(100))
- `brand` (VARCHAR(100))
- `image_url` (VARCHAR(500))
- `created_at`, `updated_at` (TIMESTAMP)

#### Tabla `contacts`
- `id` (INT, PK)
- `name` (VARCHAR(255))
- `email` (VARCHAR(255))
- `message` (TEXT)
- `created_at` (TIMESTAMP)

---

## 🧩 5. Endpoints & Rutas (API y UI)

### 5.1. Rutas Públicas (UI)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página de inicio |
| GET | `/instrumentos` | Catálogo general |
| GET | `/guitarras` `/bajos` `/baterias` `/otros` | Catálogo por categoría |
| GET | `/carrito` | Vista carrito (client-side) |
| GET | `/inicio_sesion` | Formulario de login |
| POST | `/inicio_sesion` | Procesar login |
| GET | `/crear-cuenta` | Formulario de registro |
| POST | `/crear-cuenta` | Procesar registro |
| GET | `/contacto` | Formulario de contacto |
| POST | `/contacto` | Enviar contacto |
| GET | `/mas_sobre` | Página "Nosotros" |
| GET | `/logout` | Cerrar sesión |

### 5.2. Rutas de API (JSON)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/productos/<categoria>` | Devuelve productos filtrados por categoría (`todos`, `guitarras`, `bajos`, etc.) |
| GET | `/api/carrito-count` | Devuelve el número de ítems del carrito (actualmente fijo 0) |

### 5.3. Rutas Administrativas (requieren `is_admin`)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/admin/users` | Listado de usuarios |
| GET/POST | `/admin/users/create` | Crear usuario |
| GET/POST | `/admin/users/edit/<user_id>` | Editar usuario |
| POST | `/admin/users/delete/<user_id>` | Eliminar usuario |
| GET | `/admin/products` | Listado de productos |
| GET/POST | `/admin/products/create` | Crear producto |
| GET/POST | `/admin/products/edit/<product_id>` | Editar producto |
| POST | `/admin/products/delete/<product_id>` | Eliminar producto |
| GET/POST | `/admin/contacto` | Editar contenido de contactos |
| GET/POST | `/admin/nosotros` | Editar contenido "nosotros" |
| GET/POST | `/admin/init-products` | Insertar productos de ejemplo |

---

## 🔐 6. Autenticación y Autorización

### 6.1. Sesiones (Flask)

La aplicación usa `flask.session` con `app.secret_key` para almacenar:

- `session['user_id']` — Identificador del usuario.
- `session['username']` — Nombre del usuario.
- `session['is_admin']` — Booleano para identificar si el usuario es administrador.
- `session['role']` — String `"admin"` / `"user"`.

El decorador `@admin_required` protege todas las rutas administrativas.

### 6.2. Validación de credenciales

- El login compara el valor de `password` con el valor almacenado en la base de datos (texto plano).
- El registro comprueba unicidad de `username` y `email`.

> ✨ Recomendación: usar `werkzeug.security.generate_password_hash()` y `check_password_hash()`.

---

## 🖥️ 7. Frontend (Templates + Static)

### 7.1. Plantillas (Jinja2)

Ubicación: `templates/`

- `layout.html` — plantilla base con navegación y scripts globales.
- `templates/pages/` — páginas públicas.
- `templates/admin/` — páginas del panel administrativo.

**Bloques de plantilla disponibles** (en `layout.html`):
- `title` — establece `<title>` por página.
- `head` — inyecta scripts/estilos adicionales.
- `nav` — barra de navegación principal.
- `content` — contenido principal.
- `scripts` — scripts específicos al final del body.

### 7.2. CSS

Ubicación: `static/css/`

- `base/` — utilidades y estilos globales (movilidad, centrado, resets).
- `layout/` — estilos de navegación, menú lateral y layout.
- `components/` — estilos de componentes (carrito, productos, admin, contacto).
- `pages/` — estilos para páginas completas.

### 7.3. JavaScript

Ubicación: `static/js/`

- `ui.js` — control de menú hamburguesa, overlay, toggle sidebar.
- `main-productos-api.js` — carga de productos desde el endpoint `/api/productos/...`.
- `filtros.js` — aplicación de filtros y búsqueda en el catálogo.
- `carrito.js` — lógica del carrito (añadir, eliminar, actualizar cantidades).
- `sincronizar_carrito.js` — sincroniza el contador de carrito con la UI.
- `contacto.js` — validación del formulario de contacto.
- `fix_scroll.js` — ajustes de scroll y comportamiento en móviles.

---

## 🧰 8. Utilidades y Scripts

### 8.1. Script de Inserción de Productos

Archivo: `insertar_productos.py`

**Función**: Leer `productos_import.sql` y ejecutar los inserts en la base de datos.

**Uso**:
```bash
python insertar_productos.py
```

> Nota: el archivo `productos_import.sql` debe existir en el mismo directorio para que funcione.

### 8.2. Ruta de Inicialización de Productos

Ruta: `/admin/init-products`

**Uso**: Inserta productos predefinidos (lista de valores hardcodeada en `app.py`) cuando se accede mediante el botón de la página.

### 8.3. `Procfile`

Define la instrucción de arranque para plataformas como Heroku (o contenedores compatibles):

```
web: gunicorn app:app
```

---

## 🚀 9. Instalación y Ejecución (Local)

### Requisitos previos

- Python 3.13+
- MySQL 5.7+ (o servicio MySQL en la nube: Aiven)
- pip

### Pasos de configuración local

1. Clonar el repositorio:
```bash
cd proyecto_python
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar conexión a la base de datos:
   - Si usas MySQL local, crea la BD `bd_users` y ajusta las credenciales en `app.py`.
   - Si usas Aiven, usa las credenciales y el host/puerto que Aiven te proporciona.

5. Población de datos (opcional):
   - Usar `/admin/init-products` desde el navegador o
   - Ejecutar `python insertar_productos.py` si se dispone de `productos_import.sql`.

6. Ejecutar la aplicación:
```bash
python app.py
```

7. Abrir en el navegador:

- `http://localhost:3000` (por defecto)

---

## ☁️ 9.1 Despliegue en la nube (GitHub + Render)

La aplicación se despliega enlazando el repositorio de GitHub con **Render** y usando **Aiven MySQL** como base de datos.

### Flujo de despliegue

1. **Repositorio GitHub**
   - Subir todo el código a un repositorio en GitHub.
   - Asegurar que `requirements.txt` y `Procfile` estén presentes.

2. **Render**
   - Crear un nuevo servicio Web (Web Service) en Render.
   - Conectar la cuenta de GitHub y seleccionar el repositorio.
   - Configurar la rama a desplegar (por ejemplo, `main` o `master`).
   - En "Build Command" usar: `pip install -r requirements.txt`
   - En "Start Command" usar: `gunicorn app:app`

3. **Base de datos Aiven**
   - Crear un servicio MySQL en Aiven.
   - Copiar la `URI` o las credenciales (host, puerto, usuario, password).
   - En Render, configurar **Environment Variables** (Variables de Entorno) para conectarse a Aiven:
     - `DB_HOST`
     - `DB_PORT`
     - `DB_USER`
     - `DB_PASSWORD`
     - `DB_NAME` (ej. `bd_users`)

4. **Variables de entorno en Render**
   - En el dashboard del servicio, añadir las variables anteriores.
   - Actualizar `app.py` (o usar `os.environ`) para leer estas variables.

5. **Analítica (opcional)**
   - La aplicación no incluye por defecto ningún script de análisis.
   - Para monitoreo, puedes integrar Google Analytics o cualquier otra plataforma insertando el script en `templates/layout.html` (antes del cierre `</head>`).

6. **Sitemap (SEO)**
   - La aplicación expone un sitemap dinámico en `/sitemap.xml` con las rutas principales.
   - Asegúrate de que el dominio de despliegue sea accesible y que el sitemap esté indexable por motores de búsqueda.

---

---

## 🛡️ 10. Recomendaciones de Producción (Microsoft-Grade)

### Seguridad

- **Hash** y **salt** de contraseñas (bcrypt).
- Forzar HTTPS y usar cabeceras de seguridad (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`).
- Habilitar CSRF tokens (Flask-WTF o similar).
- Validar y sanitizar todas las entradas del usuario.
- Limitar intentos de login (protección contra brute force).

### Escalabilidad

- Usar contenedores (Docker) y orquestador (Kubernetes).
- Configurar `gunicorn` con workers según CPU.
- Usar cache (Redis) para sesiones y datos intensivos.

### Observabilidad

- Logging estructurado (JSON) con niveles.
- Métricas (Prometheus) y monitoreo.
- Integrar una plataforma de analítica (p.ej. Google Analytics) si se desea monitoreo de uso.
- Alertas para errores 5xx y latencia.

### Calidad de código

- Añadir tests unitarios y de integración (pytest + flask-testing).
- Usar linters (`flake8`, `black`, `ruff`).
- Validar dependencias con `pip-audit`.

---

## 📦 11. Material Adicional y Soporte

- Documentación interna: `docs/` (esta carpeta).
- Archivos de configuración: `requirements.txt`, `Procfile`.
- Recursos estáticos y diseño: `static/`.
- Templates del sitio: `templates/`.

> Para preguntas o soporte, contacta al equipo de desarrollo con un issue detallando el componente, la ruta y el comportamiento esperado vs actual.

---

### 📝 Historial de versiones (sugerido)

- **v1.0.0** - Versión inicial con funcionalidad de tienda, carrito y admin.

---

**Fin de la documentación**

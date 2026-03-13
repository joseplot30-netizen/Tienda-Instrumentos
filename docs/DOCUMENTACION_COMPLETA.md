# Documentación Completa del Proyecto

Esta guía está pensada para desarrolladores y administradores que trabajan con el proyecto **Music Store**. Incluye detalles técnicos, estructura del sistema, rutas, despliegue y recomendaciones, ampliados para cubrir los flujos reales y configuraciones modernas.

---

## 1. Descripción general del proyecto

**Music Store** es una aplicación web de comercio electrónico para vender instrumentos musicales (guitarras, bajos, baterías, teclados, accesorios).

### Objetivos del proyecto

- Proveer una tienda online funcional con catálogo y carrito.
- Permitir registro/inicio de sesión de usuarios.
- Soportar roles: usuarios normales y administradores.
- Facilitar gestión de productos/usuarios desde un panel administrativo.
- Mantener una experiencia móvil responsiva.

### Componentes principales

- **Frontend**: HTML + CSS + JavaScript (vanilla).
- **Backend**: Flask (Python 3.13) con rutas y APIs.
- **Base de datos**: MySQL (local o en Aiven).
- **Despliegue**: GitHub + Render.

---

## 2. Estructura del proyecto

```
proyecto_python/
├── app.py                   # Aplicación Flask principal
├── insertar_productos.py    # Script para poblar productos
├── requirements.txt         # Dependencias Python
├── Procfile                 # Para deploy (Render/Heroku)
├── docs/                    # Documentación del proyecto
│   ├── DOCUMENTACION_PROFESIONAL.md
│   ├── DOCUMENTACION_COMPLETA.md
│   ├── DIAGRAMA_ARQUITECTURA.md
│   └── ...
├── static/                  # Archivos estáticos (CSS, JS, img)
└── templates/               # Plantillas Jinja2
    ├── layout.html
    ├── pages/
    └── admin/
```

### Archivos clave

- **`app.py`**: Contiene las rutas, la lógica de sesión, la conexión a la BD y los endpoints de API.
- **`static/js/`**: Scripts de carrito, filtros, UI y sincronización.
- **`templates/layout.html`**: Template base con la barra de navegación, menú, mensajes y scripts globales.

---

## 3. Backend: Flask y rutas

### 3.1. Configuración de Flask

- `app = Flask(__name__)`
- `app.secret_key` asegura la integridad de la sesión.
- `db_config`: credenciales de MySQL (local o Aiven).
- `get_db_connection()`: abre una conexión a la base de datos usando mysql-connector.

### 3.2. Decoradores y seguridad

- `admin_required`: controla acceso a rutas de administración.
- `session`: almacena `user_id`, `username`, `is_admin`, `role`.

### 3.3. Rutas principales (públicas)

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Home / landing |
| `/instrumentos` | GET | Vista catálogo general |
| `/guitarras` `/bajos` `/baterias` `/otros` | GET | Catálogos por categoría |
| `/carrito` | GET | Vista del carrito (cliente) |
| `/inicio_sesion` | GET/POST | Login de usuario |
| `/crear-cuenta` | GET/POST | Registro de usuario |
| `/contacto` | GET/POST | Formulario de contacto |
| `/mas_sobre` | GET | Página "Nosotros" |
| `/logout` | GET | Cierra sesión (limpia `session`) |

### 3.4. API JSON (interno)

| Ruta | Método | Función |
|------|--------|--------|
| `/api/productos/<categoria>` | GET | Devuelve lista de productos filtrados (JSON) |
| `/api/carrito-count` | GET | Devuelve contador de carrito (actualmente siempre 0) |

### 3.5. Rutas de administración (requieren admin)

| Ruta | Método | Función |
|------|--------|--------|
| `/admin/users` | GET | Listado de usuarios |
| `/admin/users/create` | GET/POST | Crear usuario |
| `/admin/users/edit/<id>` | GET/POST | Editar usuario |
| `/admin/users/delete/<id>` | POST | Eliminar usuario |
| `/admin/products` | GET | Listado de productos |
| `/admin/products/create` | GET/POST | Crear producto |
| `/admin/products/edit/<id>` | GET/POST | Editar producto |
| `/admin/products/delete/<id>` | POST | Eliminar producto |
| `/admin/contacto` | GET/POST | Editar contenido de contacto |
| `/admin/nosotros` | GET/POST | Editar contenido "nosotros" |
| `/admin/init-products` | GET/POST | Inserta productos de ejemplo |

---

## 4. Base de datos (MySQL)

### 4.1. Conexión

El proyecto funciona con:

- MySQL local para desarrollo.
- MySQL en **Aiven** para staging/producción.

**Ejemplo de configuración Aiven (recomendada para deploy)**:

```python
import os

db_config = {
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME', 'bd_users')
}
```

### 4.2. Esquema principal

#### Tabla `users`

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INT PK AUTO_INCREMENT | Identificador único |
| username | VARCHAR(255) UNIQUE | Nombre de usuario |
| email | VARCHAR(255) UNIQUE | Email |
| password | VARCHAR(255) | Contraseña (texto plano actualmente) |
| is_admin | BOOLEAN | Flag de administrador |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Fecha de actualización |

#### Tabla `products`

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INT PK AUTO_INCREMENT | Identificador |
| name | VARCHAR(255) | Nombre producto |
| price | DECIMAL(10,2) | Precio |
| stock | INT | Cantidad disponible |
| category | VARCHAR(100) | Categoría (guitarras, bajos, etc) |
| brand | VARCHAR(100) | Marca |
| image_url | VARCHAR(500) | URL imagen |
| created_at | TIMESTAMP | Fecha creación |
| updated_at | TIMESTAMP | Fecha actualización |

#### Tabla `contacts`

| Campo | Tipo | Descripción |
|------|------|-------------|
| id | INT PK AUTO_INCREMENT | Identificador |
| name | VARCHAR(255) | Nombre del remitente |
| email | VARCHAR(255) | Email de contacto |
| message | TEXT | Mensaje |
| created_at | TIMESTAMP | Fecha de envío |

### 4.3. Insertar productos (datos de ejemplo)

- **Opción 1**: Navegar a `/admin/init-products` y ejecutar el botón.
- **Opción 2**: Ejecutar `python insertar_productos.py` (requiere `productos_import.sql`).

---

## 5. Frontend (templates + estáticos)

### 5.1. Plantillas (Jinja2)

- `templates/layout.html`: template base con navegación, mensajes y scripts globales.
- `templates/pages/`: páginas públicas (inicio, catálogo, carrito, etc.).
- `templates/admin/`: panel administrativo.

**Bloques más utilizados en las plantillas**:

- `title`, `head`, `content`, `scripts`
- `nav` para la barra superior personalizada.

### 5.2. CSS

- `static/css/base`: estilos globales y utilidades (centrado, mobile).
- `static/css/layout`: navegación, sidebar, menus.
- `static/css/components`: estilos por funcionalidad.
- `static/css/pages`: estilos por página.

### 5.3. JavaScript

- `ui.js`: comportamiento del menú y sidebar.
- `main-productos-api.js`: carga productos desde `/api/productos/...`.
- `filtros.js`: filtros dinámicos por marca, precio, categoría.
- `carrito.js`: agrega/elimina productos del carrito.
- `sincronizar_carrito.js`: mantiene el contador del carrito actualizado.
- `contacto.js`: validación simple del formulario.
- `fix_scroll.js`: fix de scroll en dispositivos móviles.

---

## 6. Despliegue (GitHub + Render + Aiven)

### 6.1. Repositorio GitHub

1. Crear repo con todo el proyecto.
2. Asegurarse de incluir:
   - `requirements.txt`
   - `Procfile` (para Render)
   - `docs/` (documentación)

### 6.2. Render

1. Crear nuevo servicio “Web Service”.
2. Conectar a GitHub y seleccionar el repositorio.
3. Configurar:
   - **Branch**: `main` / `master`.
   - **Build Command**: `pip install -r requirements.txt`.
   - **Start Command**: `gunicorn app:app`.

### 6.3. Aiven MySQL

1. Crear servicio MySQL en Aiven.
2. Copiar credenciales de conexión (host, puerto, usuario, password).
3. Crear base de datos `bd_users` en Aiven (puede hacerse desde Workbench o terminal).

### 6.4. Variables de entorno en Render

Configurar en Render:
- `DB_HOST` (host Aiven)
- `DB_PORT` (puerto MySQL)
- `DB_USER` (usuario)
- `DB_PASSWORD` (password)
- `DB_NAME` (ej. `bd_users`)

### 6.5. SSL / Seguridad

- Aiven ofrece SSL obligatorio; usar el certificado que provea Aiven en la configuración de MySQL Workbench.
- Usar `https://` en la aplicación desplegada.

---

## 7. Seguridad y buenas prácticas

### 7.1. Contraseñas

Actualmente se almacenan en texto plano. En producción **debe usarse hashing**:

```python
from werkzeug.security import generate_password_hash, check_password_hash

pwd_hash = generate_password_hash(password)
check_password_hash(pwd_hash, password)
```

### 7.2. CSRF y validaciones

- Agregar protección CSRF (Flask-WTF).
- Validar entradas en el servidor además del cliente.

### 7.3. Sesiones y tokens

- Usar `app.secret_key` robusta.
- Considerar sesiones server-side (Redis) si se escala.

---

## 8. Cómo colaborar (workflow recomendado)

1. **Fork / Branch** desde `main`.
2. Desarrollar en una rama con nombre claro (`feature/`, `fix/`).
3. Usar commits pequeños y descriptivos.
4. Crear PR con descripción, pasos de prueba y cambios.

---

## 9. Preguntas frecuentes

### ¿Dónde configuro la conexión a la base de datos?
En `app.py`, dentro de `db_config`. Se recomienda leer de variables de entorno.

### ¿Cómo cambio el puerto?
Modificar `app.run(..., port=XXXX)` al final de `app.py`.

---

**Fin de la documentación completa**

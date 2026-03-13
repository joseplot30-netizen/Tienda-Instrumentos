# Descripción General

**Music Store** es una aplicación web de comercio electrónico especializada en la venta de instrumentos musicales. Permite a usuarios navegar, buscar, comprar productos y provee un panel de administración para gestionar inventario, usuarios y contenido.

## Características Principales

- **Catálogo de Productos**: Guitarras, bajos, baterías e instrumentos varios.
- **Carrito de Compras**: Gestión en cliente con persistencia en localStorage.
- **Sistema de Usuarios**: Registro, autenticación y roles (usuario/administrador).
- **Panel Administrativo**: Gestión de productos, usuarios y configuración del sitio.
- **Búsqueda Avanzada**: Filtrado por categoría, marca, precio e ID.
- **Interfaz Responsiva**: Optimizada para dispositivos móviles y desktop.
- **Filtros de Productos**: Búsqueda por marca y rango de precio.

---

## Arquitectura

### Tech Stack

| Componente | Tecnología |
|-----------|-----------|
| **Backend** | Flask (Python 3.13) |
| **Frontend** | HTML5, CSS3, JavaScript Vanilla |
| **Base de Datos** | MySQL |
| **Templating** | Jinja2 |
| **Iconos** | Bootstrap Icons |
| **Estilos** | CSS Grid, Flexbox, Media Queries |

### Capas de Aplicación

```
┌──────────────────────────────────────┐
│    Frontend (HTML/JS/CSS)            │
│  - Interfaz de usuario responsiva    │
│  - Lógica de carrito en cliente      │
│  - Filtros de búsqueda interactivos  │
└──────────────────────┬───────────────┘
                       │
┌──────────────────────▼───────────────┐
│   API REST (Flask Routes)            │
│  - Endpoints públicos                │
│  - Endpoints protegidos (admin)      │
│  - Gestión de sesiones               │
└──────────────────────┬───────────────┘
                       │
┌──────────────────────▼───────────────┐
│     Capa de Datos (MySQL)            │
│  - Productos                         │
│  - Usuarios                          │
│  - Contactos                         │
└──────────────────────────────────────┘
```

---

## Estructura del Proyecto

```
proyecto_python/
├── app.py                          # Aplicación principal Flask
├── insertar_productos.py           # Script de inicialización
│
├── templates/
│   ├── layout.html                 # Template base
│   ├── pages/                      # Páginas públicas
│   │   ├── index.html              # Página de inicio
│   │   ├── INSTRUMENTOS.html       # Catálogo principal
│   │   ├── guitarras.html          # Categoría: guitarras
│   │   ├── bajos.html              # Categoría: bajos
│   │   ├── baterias.html           # Categoría: baterías
│   │   ├── otros.html              # Categoría: otros
│   │   ├── CARRITO_DE_COMPRAS.html # Carrito
│   │   ├── INICIO_SESION.html      # Login
│   │   ├── CREAR_CUENTA.html       # Registro
│   │   ├── CONTACTO.html           # Formulario de contacto
│   │   └── MAS_SOBRE.html          # Información de la empresa
│   │
│   └── admin/                      # Panel administrativo
│       ├── admin_users.html        # Gestión de usuarios
│       ├── admin_edit_user.html    # Editar usuario
│       ├── admin_create_user.html  # Crear usuario
│       ├── admin_products.html     # Gestión de productos
│       ├── admin_edit_product.html # Editar producto
│       ├── admin_create_product.html # Crear producto
│       ├── admin_contacto.html     # Editar info de contacto
│       └── admin_nosotros.html     # Editar info de la empresa
│
├── static/
│   ├── css/
│   │   ├── base/
│   │   │   ├── centering.css       # Utilidades de centrado
│   │   │   ├── mobile.css          # Optimizaciones móvil
│   │   │   └── zzstyle0.css        # Estilos globales
│   │   ├── components/
│   │   │   ├── style_admin.css     # Estilos panel admin
│   │   │   ├── carrito.css         # Estilos carrito
│   │   │   ├── instrumentos.css    # Estilos productos
│   │   │   └── style_contacto.css  # Estilos contacto
│   │   └── layout/
│   │       ├── nav_menu.css        # Menú navegación
│   │       ├── sidebar_menu.css    # Menú filtros
│   │       └── hamburguesa_overrides.css # Overrides responsivos
│   │
│   ├── js/
│   │   ├── ui.js                   # Lógica UI global (menú, filtros)
│   │   ├── main-productos-api.js   # API de productos
│   │   ├── filtros.js              # Filtros avanzados
│   │   ├── carrito.js              # Carrito de compras
│   │   ├── contacto.js             # Formulario contacto
│   │   ├── sincronizar_carrito.js  # Sincronización carrito
│   │   └── fix_scroll.js           # Correcciones de scroll
│   │
│   └── img/                        # Imágenes y assets
│
├── docs/
│   └── manuals/                    # Documentación dividida en secciones
│
└── README.md                       # Archivo principal
```

---

## Instalación y Configuración

### Requisitos

- Python 3.13+
- MySQL 5.7+
- pip (gestor de paquetes Python)

### Pasos de Instalación

1. Clonar o descargar el proyecto:

```bash
cd proyecto_python
```

2. Crear un ambiente virtual (recomendado):

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
   - Crear la base de datos en MySQL: `bd_users`
   - Editar `app.py` para ajustar credenciales de conexión.

5. Inicializar datos (opcional):

```bash
python insertar_productos.py
```

6. Ejecutar la aplicación:

```bash
python app.py
```

7. Acceder a la aplicación:

- `http://localhost:3000`

---

## Notas Técnicas

### Configuración Actual

- **Puerto**: 3000
- **Debug Mode**: Activado en desarrollo
- **Template Engine**: Jinja2
- **Static Files**: `/static`
- **Template Files**: `/templates`

### Variables de Sesión

```python
session['user_id']     # ID del usuario autenticado
session['username']    # Nombre de usuario
session['is_admin']    # Flag de administrador
session['role']        # 'admin' o 'user'
```

### Constantes Globales

_Si se implementan, documentarlas aquí (actualmente no hay constantes globales definidas)_

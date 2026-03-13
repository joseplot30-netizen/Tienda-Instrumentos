# Arquitectura

## 🏗️ Patrones de Arquitectura

### Patrón MVC Adaptado

Music Store implementa una arquitectura MVC ligera adaptada para Flask:

```
┌──────────────────────────────┐
│   Views (Jinja2)        │  <- Plantillas HTML
├──────────────────────────────┤
│   Routes (Flask)        │  <- Controladores
├──────────────────────────────┤
│   Database (MySQL)      │  <- Modelos de datos
└──────────────────────────────┘
```

---

## 📄 Flujo de Datos

### Solicitud HTTP

```
1. Cliente → Navegador web
2. Navegador → Servidor Flask (puerto 3000)
3. Flask → Enrutador (@app.route)
4. Enrutador → Controlador (función Flask)
5. Controlador → Base de Datos (MySQL)
6. Base de Datos → Controlador (resultados)
7. Controlador → Template Jinja2 (renderización)
8. Jinja2 → HTML final
9. HTML → Navegador
10. Navegador → Cliente (renderizado)
```

### Flujo de Carrito (Cliente)

```
1. Usuario hace clic en producto
2. JavaScript captura evento
3. Carrito se actualiza en memoria (array)
4. localStorage sincroniza datos
5. Badge de cantidad se actualiza
6. Confirmación visual en UI
```

---

## 🛠️ Componentes Principales

### 1. Capa de Aplicación (`app.py`)

**Responsabilidades:**

- Definir rutas HTTP
- Gestionar sesiones
- Renderizar templates
- Conectar a base de datos

**Funciones Clave:**

```python
@app.route(...)              # Decorador de rutas
def admin_required(f)        # Middleware de autorización
get_db_connection()          # Factory de conexiones DB
```

### 2. Capa de Vistas (`templates/`)

**Estructura:**

- `layout.html` - Template base heredado por todas las páginas
- `pages/` - Páginas públicas (catálogo, carrito, etc)
- `admin/` - Páginas administrativas (solo admins)

**Características:**

- Bloques Jinja2 para herencia
- Condicionales `{% if %}` para lógica de vista
- Loops `{% for %}` para iteración
- Filtros `|` para transformación de datos

### 3. Capa de Estilos (`static/css/`)

**Organización:**

```
css/
├── base/              # Estilos globales
│   ├── centering      # Utilidades de layout
│   ├── mobile         # Mobile-first
│   └── zzstyle0       # Estilos principales
├── components/        # Componentes específicos
│   ├── style_admin    # Panel administrativo
│   ├── carrito        # Carrito de compras
│   ├── instrumentos   # Catálogo
│   └── ...
└── layout/            # Componentes de layout
    ├── nav_menu       # Navegación
    ├── sidebar_menu   # Filtros
    └── hamburguesa    # Menú móvil
```

**Metodología:** Mobile-first con media queries

### 4. Capa de Lógica Cliente (`static/js/`)

**Módulos:**

| Archivo | Responsabilidad |
|---------|-----------------|
| `ui.js` | Menú hamburguesa, toggle de filtros |
| `main-productos-api.js` | Llamadas AJAX a productos |
| `filtros.js` | Filtrado reactivo de productos |
| `carrito.js` | Gestión del carrito |
| `sincronizar_carrito.js` | Persistencia en localStorage |
| `contacto.js` | Validación de formulario |
| `fix_scroll.js` | Correcciones de scroll |

### 5. Base de Datos (`MySQL/bd_users`)

**Tablas:**

#### Tabla `users`
Almacena información de usuarios registrados.

```
Campos: id, username, email, password, is_admin, created_at
Índices: PRIMARY KEY (id), UNIQUE (username), UNIQUE (email)
```

#### Tabla `products`
Catálogo de instrumentos disponibles.

```
Campos: id, name, price, stock, category, brand, image_url, created_at
Índices: PRIMARY KEY (id), INDEX (category), INDEX (brand)
```

#### Tabla `contacts`
Mensajes de contacto del público.

```
Campos: id, name, email, message, created_at
Índices: PRIMARY KEY (id)
```

---

## 🔐 Flujo de Autenticación

### Registro (Sign Up)

```
1. Usuario navega a /crear-cuenta
2. Completa formulario (username, email, password)
3. JavaScript valida datos cliente
4. POST a /crear-cuenta
5. Flask valida:
   - Campos no vacíos
   - Passwords coinciden
   - Username único
   - Email único
6. Si válido: INSERT en tabla users
7. Redirige a /inicio_sesion
8. Si inválido: Flash error y recarga formulario
```

### Inicio de Sesión (Login)

```
1. Usuario navega a /inicio_sesion
2. Ingresa username y password
3. POST a /inicio_sesion
4. Flask busca usuario en BD
5. Si existe y password correcto:
   - Guarda datos en session
   - Sets session['is_admin']
   - Flash bienvenida
   - Redirige a inicio
6. Si no: Flash error
```

### Protección de Rutas

```
@admin_required              # Decorador personalizado
└─> Verifica session['is_admin']
    ├─ Si no autenticado → /inicio_sesion
    └─ Si no admin → /
```

---

## 🎨 Sistema de Componentes UI

### Menú de Hamburguesa

**Archivo**: `static/js/ui.js`

**Elemento HTML**:

```html
<button class="site-nav__hamburger">☰</button>
<div class="site-nav__overlay">
  <ul class="site-nav__list">
    <!-- Items de menú -->
  </ul>
  <button class="site-nav__close">✕</button>
</div>
```

**Eventos JavaScript**:
```
click hamburger → toggle overlay
click overlay → close overlay
click X → close overlay
```

### Filtros de Productos

**Archivo**: `static/js/ui.js`, `filtros.js`

**Elementos HTML**:

```html
<aside class="sidebar closed">
  <button class="sidebar-toggle">🎚</button>
  <div class="sidebar-section">
    <!-- Filtros por precio, marca, etc -->
  </div>
  <button class="sidebar-close-btn">✕</button>
</aside>
```

**Estados**:
- `closed` - Sidebar colapsado
- `visible` - Overlay visible
- `hidden` - Botón toggle oculto

**Flujo Interactivo**:
```
click toggle → sidebar.toggle('closed')
           → toggle.toggle('hidden')
           → overlay.toggle('visible')
click close → sidebar.add('closed')
           → toggle.remove('hidden')
           → overlay.remove('visible')
click outside → cerrar automáticamente
```

---

## 📊 Panel Administrativo

### Flujo de Gestión de Productos

*Se explica en detalle en el documento principal `DOCUMENTACION_PROFESIONAL.md`.*

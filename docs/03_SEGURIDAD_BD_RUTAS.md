# Seguridad, Base de Datos y Rutas

## 🔒 Seguridad y Autenticación

### Roles de Usuario

- **Usuario Regular**: Acceso a catálogo, carrito y contacto.
- **Administrador**: Acceso completo, incluyendo panel de control.

### Sistema de Sesiones

- Uso de `session` de Flask para gestión de estado.
- Verificación de permisos mediante decorador `@admin_required`.
- Flash messages para feedback de usuario.

> ⚠️ En producción implementar:
> - Hashing de contraseñas (bcrypt, `werkzeug.security`)
> - HTTPS obligatorio
> - CSRF tokens (Flask-WTF o similar)
> - Prevención de inyección SQL (prepared statements ✅)

---

## 📊 Base de Datos

### Tablas Principales

#### `users`

```sql
id (PK)
username (VARCHAR 255, UNIQUE)
email (VARCHAR 255, UNIQUE)
password (VARCHAR 255)
is_admin (BOOLEAN)
created_at (TIMESTAMP)
```

#### `products`

```sql
id (PK)
name (VARCHAR 255)
price (DECIMAL 10,2)
stock (INT)
category (VARCHAR 100)
brand (VARCHAR 100)
image_url (VARCHAR 500)
created_at (TIMESTAMP)
```

#### `contacts` (Referencia)

```sql
id (PK)
name (VARCHAR 255)
email (VARCHAR 255)
message (TEXT)
created_at (TIMESTAMP)
```

---

## 🛣️ Rutas y Endpoints

### Rutas Públicas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página de inicio |
| GET | `/guitarras`, `/bajos`, `/baterias`, `/otros` | Categorías de productos |
| GET | `/carrito` | Carrito de compras |
| POST | `/api/productos` | Obtener lista de productos |
| GET | `/inicio_sesion` | Formulario de login |
| POST | `/inicio_sesion` | Procesar login |
| GET | `/registro` | Formulario de registro |
| POST | `/registro` | Procesar registro |
| GET | `/mas-sobre` | Página de información |
| GET | `/contacto` | Formulario de contacto |
| POST | `/contacto` | Enviar contacto |
| GET | `/logout` | Cerrar sesión |

### Rutas Administrativas (protegidas)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/admin/users` | Listar usuarios |
| GET/POST | `/admin/users/create` | Crear usuario |
| GET/POST | `/admin/users/edit/<id>` | Editar usuario |
| POST | `/admin/users/delete/<id>` | Eliminar usuario |
| GET | `/admin/products` | Listar productos |
| GET/POST | `/admin/products/create` | Crear producto |
| GET/POST | `/admin/products/edit/<id>` | Editar producto |
| POST | `/admin/products/delete/<id>` | Eliminar producto |
| GET/POST | `/admin/contacto` | Gestionar info de contacto |
| GET/POST | `/admin/nosotros` | Gestionar info de empresa |

---

## 🗂️ Notas Adicionales

- Los endpoints de administración usan `@admin_required` (admin + sesión activa).
- Algunos endpoints de API devuelven JSON (p. ej., `/api/productos/<categoria>`).
- La arquitectura prioriza la simplicidad y claridad para facilitar mantenimiento.

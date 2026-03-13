# API Endpoints (Documentación Completa)

Esta página describe todos los endpoints expuestos por la aplicación, tanto para el frontend (UI) como para APIs JSON.

## 🔐 Autenticación

### Sesión de Usuario

Las rutas protegidas necesitan que el usuario esté autenticado.

**Variables de sesión disponibles:**

```python
session['user_id']    # ID del usuario (int)
session['username']   # Nombre de usuario (str)
session['is_admin']   # Flag de administrador (bool)
session['role']       # 'admin' o 'user' (str)
```

---

## 📱 Rutas Públicas (UI)

### GET `/`
**Descripción**: Página de inicio.

**Autenticación**: No requerida.

**Respuesta**: HTML (renderiza `pages/index.html`).

---

### GET `/guitarras`, `/bajos`, `/baterias`, `/otros`
**Descripción**: Catálogo por categoría.

**Parámetros**: Ninguno.

**Autenticación**: No requerida.

**Respuesta**: HTML con productos filtrados.

---

### GET `/carrito`
**Descripción**: Vista del carrito de compras.

**Autenticación**: No requerida.

**Almacenamiento**: localStorage (cliente).

**Respuesta**: HTML interactivo.

---

### GET `/inicio_sesion`
**Descripción**: Formulario de login.

**Autenticación**: No requerida.

**Respuesta**: HTML.

---

### POST `/inicio_sesion`
**Descripción**: Procesa la autenticación de usuario.

**Parámetros (form-data)**:

- `username` (string) — requerido.
- `password` (string) — requerido.

**Flujo**:

1. Busca el usuario en la tabla `users`.
2. Compara la contraseña con el valor almacenado.
3. Si coincide, crea sesión y redirige.
4. Si falla, muestra mensaje de error.

---

### GET `/registro`
**Descripción**: Formulario de registro.

**Autenticación**: No requerida.

**Respuesta**: HTML.

---

### POST `/registro`
**Descripción**: Crea una nueva cuenta de usuario.

**Parámetros (form-data)**:

- `username` (string) — requerido, único.
- `email` (string) — requerido, único.
- `password` (string) — requerido.
- `password_confirm` (string) — requerido.

**Validaciones**:

- Todos los campos deben estar completos.
- Contraseñas deben coincidir.
- El username y el email deben ser únicos.

---

### POST `/contacto`
**Descripción**: Envía un mensaje de contacto.

**Parámetros (form-data)**:

- `name` (string) — requerido.
- `email` (string) — requerido.
- `message` (string) — requerido.

**Nota**: Actualmente no se almacena en BD; sólo se muestra un mensaje de confirmación.

---

### GET `/mas_sobre`
**Descripción**: Página "Nosotros".

**Autenticación**: No requerida.

**Respuesta**: HTML.

---

### GET `/logout`
**Descripción**: Cierra la sesión del usuario.

**Autenticación**: Requerida.

**Acción**: `session.clear()` y redirige a `/`.

---

## 🔒 Rutas Protegidas (Admin)

### GET `/admin/users`
**Descripción**: Lista todos los usuarios registrados.

**Autenticación**: Requerida (admin).

**Respuesta**: HTML con tabla de usuarios.

---

### GET/POST `/admin/users/create`
**Descripción**: Crear un nuevo usuario.

**Autenticación**: Requerida (admin).

---

### GET/POST `/admin/users/edit/<user_id>`
**Descripción**: Editar un usuario existente.

**Autenticación**: Requerida (admin).

**Parámetro**: `user_id` (int).

---

### POST `/admin/users/delete/<user_id>`
**Descripción**: Eliminar usuario.

**Autenticación**: Requerida (admin).

---

### GET `/admin/products`
**Descripción**: Lista todos los productos.

**Autenticación**: Requerida (admin).

---

### GET/POST `/admin/products/create`
**Descripción**: Crear producto.

**Autenticación**: Requerida (admin).

---

### GET/POST `/admin/products/edit/<product_id>`
**Descripción**: Editar producto existente.

**Autenticación**: Requerida (admin).

**Parámetro**: `product_id` (int).

---

### POST `/admin/products/delete/<product_id>`
**Descripción**: Eliminar producto.

**Autenticación**: Requerida (admin).

---

### GET/POST `/admin/contacto`
**Descripción**: Edita los textos y datos de contacto mostrados en la web.

**Autenticación**: Requerida (admin).

---

### GET/POST `/admin/nosotros`
**Descripción**: Edita los textos de la página "Nosotros".

**Autenticación**: Requerida (admin).

---

## 🧩 Endpoints JSON

### GET `/api/productos/<categoria>`

**Descripción**: Devuelve un arreglo de productos filtrados por categoría.

**Categorías disponibles**: `todos`, `guitarras`, `bajos`, `baterias`, `otros`.

**Ejemplo de respuesta**:

```json
[
  {
    "id": "guitarras-1",
    "titulo": "guitarra 01",
    "precio": 800000,
    "imagen": "https://...",
    "categoria": { "nombre": "yamaha", "id": "yamaha" },
    "brand": "yamaha"
  }
]
```

### GET `/api/carrito-count`

**Descripción**: Devuelve el número de ítems en el carrito.

**Respuesta actual**: siempre `0` (por diseño actual).

```json
{ "count": 0 }
```

# Base de Datos (Esquema y Consultas)

## 🗄️ Información General

- **Motor**: MySQL
- **Base de datos**: `bd_users`
- **Charset**: `utf8mb4`
- **Collation**: `utf8mb4_unicode_ci`

---

## 📊 Esquema de Tablas

### 1. Tabla `users`

**Propósito**: Almacenar datos de usuarios registrados y autenticación.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Campos clave**:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INT | Identificador único (PK) |
| `username` | VARCHAR(255) | Nombre de usuario (único) |
| `email` | VARCHAR(255) | Correo electrónico (único) |
| `password` | VARCHAR(255) | Contraseña (texto plano actualmente) |
| `is_admin` | BOOLEAN | Indicador de administrador |
| `created_at` | TIMESTAMP | Fecha de creación |
| `updated_at` | TIMESTAMP | Fecha actualización |

**Consultas frecuentes**:

```sql
-- Buscar usuario por username
SELECT * FROM users WHERE username = 'juanperez';

-- Contar usuarios totales
SELECT COUNT(*) as total FROM users;

-- Listar todos los administradores
SELECT * FROM users WHERE is_admin = 1;

-- Crear nuevo usuario
INSERT INTO users (username, email, password) 
VALUES ('nuevo_user', 'new@email.com', 'password');

-- Editar usuario
UPDATE users SET email = 'newemail@mail.com' WHERE id = 1;

-- Eliminar usuario
DELETE FROM users WHERE id = 5;
```

---

### 2. Tabla `products`

**Propósito**: Almacenar el catálogo de instrumentos.

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    category VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Campos clave**:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INT | Identificador único (PK) |
| `name` | VARCHAR(255) | Nombre del producto |
| `price` | DECIMAL(10,2) | Precio |
| `stock` | INT | Stock disponible |
| `category` | VARCHAR(100) | Categoría (guitarras/bajos/baterias/otros) |
| `brand` | VARCHAR(100) | Marca |
| `image_url` | VARCHAR(500) | URL de imagen |
| `created_at` | TIMESTAMP | Fecha de creación |
| `updated_at` | TIMESTAMP | Fecha actualización |

**Índices**:

```sql
PRIMARY KEY (id)
INDEX (category)
INDEX (brand)
```

**Consultas frecuentes**:

```sql
-- Obtener todos los productos
SELECT * FROM products;

-- Buscar por categoría
SELECT * FROM products WHERE category = 'guitarras';

-- Buscar por marca
SELECT * FROM products WHERE brand = 'yamaha';

-- Filtrar por rango de precio
SELECT * FROM products 
WHERE price BETWEEN 100000 AND 800000;

-- Obtener en stock
SELECT * FROM products WHERE stock > 0;

-- Contar por categoría
SELECT category, COUNT(*) as cantidad 
FROM products 
GROUP BY category;

-- Crear producto
INSERT INTO products (name, price, stock, category, brand, image_url)
VALUES ('guitarra 01', 800000, 10, 'guitarras', 'yamaha', 'https://...');

-- Editar stock
UPDATE products SET stock = stock - 1 WHERE id = 1;

-- Eliminar producto
DELETE FROM products WHERE id = 42;
```

---

### 3. Tabla `contacts`

**Propósito**: Guardar mensajes de contacto enviados por usuarios.

```sql
CREATE TABLE contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Campos clave**:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INT | Identificador único (PK) |
| `name` | VARCHAR(255) | Nombre del remitente |
| `email` | VARCHAR(255) | Email de contacto |
| `message` | TEXT | Mensaje |
| `created_at` | TIMESTAMP | Fecha de creación |

**Consultas**:

```sql
-- Ver todos los mensajes
SELECT * FROM contacts ORDER BY created_at DESC;

-- Ver mensajes recientes
SELECT * FROM contacts 
WHERE created_at > DATE_SUB(NOW(), INTERVAL 7 DAY);

-- Insertar mensaje
INSERT INTO contacts (name, email, message)
VALUES ('Cliente', 'cliente@email.com', 'Consulta sobre productos');
```

---

## 🔗 Relaciones y Mejoras Recomendadas

### Integridad Referencial

**Actualmente**: No se implementan claves foráneas.

**Recomendación**: En futuras versiones, agregar relaciones entre tablas. Ejemplo:

```sql
ALTER TABLE products ADD COLUMN created_by INT;
ALTER TABLE products ADD FOREIGN KEY (created_by) REFERENCES users(id);
```

---

## 📈 Estadísticas de Datos (Base de Datos)

### Distribución de Productos

**Conteo inicial (ejemplo)**:

```
guitarras   : 12 productos
bajos       : 12 productos
baterias    : 5 productos
otros       : 5 productos
───────────────────────────
Total       : 34 productos
```

**Distribución por marca**:

```
yamaha   : 12 productos
ibanez   : 12 productos
ayson    : 8 productos
jibao    : 1 producto
aire     : 2 productos
piano    : 2 productos
clasico  : 1 producto
```

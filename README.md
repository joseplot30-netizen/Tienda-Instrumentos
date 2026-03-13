# Music Store (Proyecto Python)

**Keywords:** Flask, MySQL, Aiven, Render, GitHub, despliegue, carrito, administrador, productos, Jinja2, CSS, JavaScript.

Aplicación web de comercio electrónico para la venta de instrumentos musicales.

## 📚 Documentación

La documentación completa está disponible en:

- `docs/DOCUMENTACION_PROFESIONAL.md` - Documentación técnica profesional (versión principal).
- `docs/DOCUMENTACION_COMPLETA.md` - Guía completa y detallada.
- `docs/01_DESCRIPCION_GENERAL.md` - Visión general y arquitectura.
- `docs/02_ARQUITECTURA.md` - Diseño de arquitectura y flujo de datos.
- `docs/03_SEGURIDAD_BD_RUTAS.md` - Seguridad, base de datos y rutas.
- `docs/04_API_ENDPOINTS.md` - Endpoints y API.
- `docs/05_BASE_DE_DATOS.md` - Esquema de base de datos y consultas.

## ▶️ Ejecutar localmente

1. Crear y activar un entorno virtual.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Configurar la base de datos MySQL (`bd_users`) o usar Aiven MySQL.
4. Ejecutar: `python app.py`.

Luego acceder en `http://localhost:3000`.

## ☁️ Despliegue en la nube

- **Repositorio**: GitHub.
- **Infraestructura**: Render (deploy continuo desde GitHub).
- **Base de datos**: Aiven MySQL (conexión remota desde Render y MySQL Workbench).
- **Analítica**: Google Analytics.

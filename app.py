import sentry_sdk
from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from sentry_sdk.integrations.flask import FlaskIntegration
from functools import wraps
import mysql.connector
import os
import json

# --- CONFIGURACIÓN DE SENTRY (CORREGIDA) ---
sentry_sdk.init(
    dsn="https://864c5f4eb2dffc66fd0e90f04f987352@o4511062458564608.ingest.us.sentry.io/4511062484123648",
    integrations=[FlaskIntegration()],
    # Captura datos del usuario (IP, headers)
    send_default_pii=True,
    # Monitoreo de rendimiento (100% de las transacciones)
    traces_sample_rate=1.0,
    # Profiling (100% de las sesiones de perfilado)
    profiles_sample_rate=1.0,
    # Nota: Se eliminaron 'enable_logs', 'profile_session_sample_rate' 
    # y 'profile_lifecycle' por no ser compatibles o válidos en esta versión.
)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'Tienda-Musica')

# --- CONEXIÓN A BASE DE DATOS ---
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 22510)), 
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        ssl_ca='/etc/secrets/ca.pem',
        ssl_verify_identity=False,
        use_pure=True
    )

# --- DECORADOR DE ADMINISTRADOR ---
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Debe iniciar sesión', 'warning')
            return redirect(url_for('inicio_sesion'))
        if not session.get('is_admin'):
            flash('Acceso denegado', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# --- RUTAS PRINCIPALES ---
@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/inicio_sesion', methods=['GET','POST'])
def inicio_sesion():
    if request.method == 'POST':
        user_form = request.form['username']
        password_form = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (user_form,))
            user = cursor.fetchone()
            if user and user['password'] == password_form:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = bool(user.get('is_admin', 0))
                session['role'] = 'admin' if session['is_admin'] else 'user'
                flash(f'¡Bienvenido {user["username"]}!', 'success')
                return redirect(url_for('instrumentos') if not session['is_admin'] else url_for('admin_users'))
            else:
                flash('Usuario o contraseña incorrecto', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('pages/INICIO_SESION.html')

@app.route('/crear-cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not username or not email or not password:
            flash('Todos los campos son obligatorios', 'warning')
            return render_template('pages/CREAR_CUENTA.html')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('pages/CREAR_CUENTA.html')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('El nombre de usuario ya está en uso', 'danger')
                return render_template('pages/CREAR_CUENTA.html')
            
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('El email ya está registrado', 'danger')
                return render_template('pages/CREAR_CUENTA.html')
            
            cursor.execute(
                "INSERT INTO users (username, email, password, is_admin) VALUES (%s, %s, %s, %s)",
                (username, email, password, 0)
            )
            conn.commit()
            flash('¡Cuenta creada exitosamente! Por favor inicia sesión', 'success')
            return redirect(url_for('inicio_sesion'))
            
        except Exception as e:
            flash(f'Error al crear la cuenta: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('pages/CREAR_CUENTA.html')

@app.route('/instrumentos')
def instrumentos():
    paths = ["/static/img1.jpg", "/static/img2.jpg"]
    hits = [10, 20, 30]
    return render_template('pages/INSTRUMENTOS.html', paths=paths, hits=hits)

# --- RUTAS DE CATEGORÍAS ---
@app.route('/bajos')
def bajos(): return render_template('pages/bajos.html')
@app.route('/baterias')
def baterias(): return render_template('pages/baterias.html')
@app.route('/guitarras')
def guitarras(): return render_template('pages/guitarras.html')
@app.route('/otros')
def otros(): return render_template('pages/otros.html')
@app.route('/carrito')
def carrito(): return render_template('pages/CARRITO_DE_COMPRAS.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        if name and email and message:
            flash('Mensaje enviado correctamente', 'success')
        else:
            flash('Por favor completa todos los campos', 'warning')
    return render_template('pages/CONTACTO.html')

@app.route('/mas_sobre')
def mas_sobre(): return render_template('pages/MAS_SOBRE.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    base_url = request.url_root.rstrip('/')
    urls = ['/', '/inicio_sesion', '/crear-cuenta', '/instrumentos', '/bajos', '/baterias', '/guitarras', '/otros', '/carrito', '/contacto', '/mas_sobre']
    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in urls:
        xml_parts.append(f'  <url><loc>{base_url}{path}</loc></url>')
    xml_parts.append('</urlset>')
    return Response("".join(xml_parts), mimetype='application/xml')

# --- API PRODUCTOS ---
@app.route('/api/productos/<categoria>')
def api_productos(categoria):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if categoria == 'todos':
            cursor.execute("SELECT id, name AS titulo, price AS precio, image_url AS imagen, category, brand FROM products")
        else:
            cursor.execute("SELECT id, name AS titulo, price AS precio, image_url AS imagen, category, brand FROM products WHERE category = %s", (categoria,))
        
        productos = cursor.fetchall()
        for prod in productos:
            prod['precio'] = int(prod['precio'])
            prod['categoria'] = {'nombre': prod['brand'], 'id': prod['brand']}
            prod['id'] = f"{categoria}-{prod['id']}"
        
        return Response(json.dumps(productos, default=str), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
    finally:
        cursor.close()
        conn.close()

# --- ADMIN ROUTES ---
@app.route('/admin/users')
@admin_required
def admin_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, IFNULL(is_admin,0) AS is_admin FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin/admin_users.html', users=users)

@app.route('/admin/products')
@admin_required
def admin_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price, stock, category, brand FROM products ORDER BY category, name")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin/admin_products.html', products=products)

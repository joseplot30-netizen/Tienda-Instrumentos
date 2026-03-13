from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'Tienda-Musica')

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
        
        # Validar que los campos no estén vacíos
        if not username or not email or not password:
            flash('Todos los campos son obligatorios', 'warning')
            return render_template('pages/CREAR_CUENTA.html')
        
        # Validar que las contraseñas coincidan
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('pages/CREAR_CUENTA.html')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('El nombre de usuario ya está en uso', 'danger')
                cursor.close()
                conn.close()
                return render_template('pages/CREAR_CUENTA.html')
            
            # Verificar si el email ya existe
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('El email ya está registrado', 'danger')
                cursor.close()
                conn.close()
                return render_template('pages/CREAR_CUENTA.html')
            
            # Insertar el nuevo usuario
            cursor.execute(
                "INSERT INTO users (username, email, password, is_admin) VALUES (%s, %s, %s, %s)",
                (username, email, password, 0)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('¡Cuenta creada exitosamente! Por favor inicia sesión', 'success')
            return redirect(url_for('inicio_sesion'))
            
        except Exception as e:
            flash(f'Error al crear la cuenta: {str(e)}', 'danger')
            cursor.close()
            conn.close()
            return render_template('pages/CREAR_CUENTA.html')
    
    return render_template('pages/CREAR_CUENTA.html')

@app.route('/instrumentos')
def instrumentos():
    paths = ["/static/img1.jpg", "/static/img2.jpg"]
    hits = [10, 20, 30]
    return render_template('pages/INSTRUMENTOS.html', paths=paths, hits=hits)

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
        # Guardar mensaje de contacto (sin implementar BD por ahora)
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        if name and email and message:
            flash('Mensaje enviado correctamente. Nos pondremos en contacto pronto', 'success')
        else:
            flash('Por favor completa todos los campos', 'warning')
        return render_template('pages/CONTACTO.html')
    return render_template('pages/CONTACTO.html')
@app.route('/mas_sobre')
def mas_sobre(): return render_template('pages/MAS_SOBRE.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- API Rutas para Productos ---
@app.route('/api/productos/<categoria>')
def api_productos(categoria):
    import json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if categoria == 'todos':
            cursor.execute("SELECT id, name AS titulo, price AS precio, image_url AS imagen, category, brand FROM products")
        else:
            cursor.execute("SELECT id, name AS titulo, price AS precio, image_url AS imagen, category, brand FROM products WHERE category = %s", (categoria,))
        
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convertir precio a string con formato necesario para la interfaz
        for prod in productos:
            prod['precio'] = int(prod['precio'])
            prod['categoria'] = {'nombre': prod['brand'], 'id': prod['brand']}
            prod['id'] = f"{categoria}-{prod['id']}"
        
        return json.dumps(productos, default=str), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        cursor.close()
        conn.close()
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}

@app.route('/api/carrito-count', methods=['GET'])
def api_carrito_count():
    import json
    # Esta ruta es para que los clientes obtengan el estado actualizado del carrito desde el servidor
    # Por ahora, devuelve 0 porque el carrito se maneja en cliente (localStorage)
    # En el futuro, pueden guardarlo en la BD por usuario
    return json.dumps({'count': 0}), 200, {'Content-Type': 'application/json'}

# --- Ruta para inicializar/insertar productos ---
@app.route('/admin/init-products', methods=['GET', 'POST'])
def init_products():
    import json
    
    if request.method == 'GET':
        # Mostrar un formulario o página de confirmación
        return '<h1>Inicializar Productos</h1><form method="POST"><button type="submit">Hacer Clic para Insertar Productos</button></form>'
    
    # POST - Insertar productos
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Productos de Bajos
        productos_bajos = [
            ('bajo 01', 800000, 10, 'bajos', 'yamaha', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCzY0R3q7BzjEEejlSsqv18NG88J0VxQp1iw&s'),
            ('bajo 02', 500000, 10, 'bajos', 'yamaha', 'https://yamaha.vtexassets.com/arquivos/ids/155858/TRBX305MG000-1.jpg?v=637780442784600000'),
            ('bajo 03', 100000, 10, 'bajos', 'yamaha', 'https://yamaha.vtexassets.com/arquivos/ids/158835/TRBX605FMMA0-1.jpg?v=637816616695330000'),
            ('bajo 04', 900000, 10, 'bajos', 'yamaha', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlNMFLk0qXJSZPQ1Bz4-pkx3c-CoKATc3QKQ&s'),
            ('bajo 05', 760000, 10, 'bajos', 'ibanez', 'https://www.pianosbogota.com/wp-content/uploads/2017/08/bajo-electrico-gsr200bk-A.jpg'),
            ('bajo 06', 750000, 10, 'bajos', 'ibanez', 'https://tiendadelmusico.com/23531-large_default/ibanez-gsr200-jb-bajo-electrico-4-cuerdas.jpg'),
            ('bajo 07', 790000, 10, 'bajos', 'ibanez', 'https://grandmusicsas.com/wp-content/uploads/2024/04/BAJO-ELECTRICO-IBANEZ-GSR205B-WNF.webp'),
            ('bajo 08', 240000, 10, 'bajos', 'ibanez', 'https://i.ebayimg.com/thumbs/images/g/DAUAAeSwdh9oK64X/s-l1200.jpg'),
            ('bajo 09', 20000, 10, 'bajos', 'ayson', 'https://static.wixstatic.com/media/1156f3_8925d6759ee94a9e9fb0f7c31fbff5eb~mv2.png/v1/fill/w_906,h_1600,al_c,q_90,enc_avif,quality_auto/1156f3_8925d6759ee94a9e9fb0f7c31fbff5eb~mv2.png'),
            ('bajo 10', 40000, 10, 'bajos', 'ayson', 'https://www.undermusic.com.co/wp-content/uploads/2024/05/CAFEOSCURO-2.jpg'),
            ('bajo 11', 80000, 10, 'bajos', 'ayson', 'https://i0.wp.com/undermusic.com.co/wp-content/uploads/2024/05/CAFECLARO-1.jpg?resize=480%2C480&ssl=1'),
            ('bajo 12', 100000, 10, 'bajos', 'ayson', 'https://www.undermusic.com.co/wp-content/uploads/2024/01/KIT-BAJO-3.jpg'),
        ]
        
        # Productos de Guitarras
        productos_guitarras = [
            ('guitarra 01', 800000, 10, 'guitarras', 'yamaha', 'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSN4CRsemRm_KrlytaALFg2qeyG3vRxLI6SatA6kHEDsVeSTNua0N68GwC2JVLo3jSjFK5V9-rhAtW8WF0eMTrsHpVsueqMj4TCKUEeqZlBpiutF9nTwhtcqnk'),
            ('guitarra 02', 500000, 10, 'guitarras', 'yamaha', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcS_O2XtSNDmm2GwkEBTfoOFoldqSKLN2R3upIY8WNN7bB2rmJjVxwXOmEOl46EmVfHW7Aw9J_l6ALAqM0wWWr_I705wVS2AwAeucQXdVLf0dWH1UJN-xmbpvks'),
            ('guitarra 03', 100000, 10, 'guitarras', 'yamaha', 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQmq-B2cDTmP6qZEWJ0uhDkRwpBTVzJXBE63t32IzfWcU1RbAfHzEjmmZHl0IGbL2FNraaXeBVGWzQetZOPzVxBqUTUI6y5oodC89gikFxJJSEVXFApFgkaHw'),
            ('guitarra 04', 900000, 10, 'guitarras', 'yamaha', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRZHFLK_dNgGzqPdboo_4CaD7VWh767eDzeL7_-FpJElrVYubQRS-qcTDyau67-Ffh1EosQPndc2l0V70jbR6DYxU68gVqT3othHt8Ha513TcF7RpEnrMWDKw'),
            ('guitarra 05', 760000, 10, 'guitarras', 'ibanez', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTjQBCe0t6AI6Dm41W_kmw-viiY7dCLftlCtYED-1jjJc4ZD0SHYauaWEuh3pTNwCU935viX85gEFkmzaExFJQxHLopqo7p23fT36JzcTn6T1A3TVzzid5N7_Q'),
            ('guitarra 06', 750000, 10, 'guitarras', 'ibanez', 'https://tiendadelmusico.com/23531-large_default/ibanez-gsr200-jb-guitarra-electrico-4-cuerdas.jpg'),
            ('guitarra 07', 790000, 10, 'guitarras', 'ibanez', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQtubmgDBhG-vyeNCz4xbRZHc95nt3CX7eCeWXO0pUvsasLOUPzKC9tZH8bBko9_U8IbXU-1_y9hYTW0v0JvB7ycSX6PYxigBofWKGf46juR_7naNpfnfMgNw'),
            ('guitarra 08', 240000, 10, 'guitarras', 'ibanez', 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSswT-5v_kvCGnO29Z1_o36kOhLqbbE3JH9heQGOR1FyUq-Orr6XJIjxi43EIeW6TdldTPDUbY784T6g0-XmQwHhnZubUyz3DeJ8xhk8LgO23bOuN5svhH6'),
            ('guitarra 09', 20000, 10, 'guitarras', 'ayson', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcQSR9-OaYUYWLiefC-DoCzYNeKAXO5GrT_gbBnWgWaNYTtm6qHwWFWS_1msN8lOVURWmBEgKJzKVuwlb1VN4gezu4ZYrV3n94NNNz15Obk'),
            ('guitarra 10', 40000, 10, 'guitarras', 'ayson', 'https://www.undermusic.com.co/wp-content/uploads/2024/05/CAFEOSCURO-2.jpg'),
            ('guitarra 11', 80000, 10, 'guitarras', 'ayson', 'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcS3Wmr026uc4sruc2S60ccNeH-gxZtGJ1or7mK8LuFd_QBD6aYKRroEoQ77Ycy4lrqFyCpJVhzk2wP9SuhIWaDib0iUB7HVRdzzaWHED703XT2yRK6VFKHKACQ'),
            ('guitarra 12', 100000, 10, 'guitarras', 'ayson', 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcQDcqprIVTXIJnlq6K1STg82d0TFOYvE5hWGLF4wEVKnqvZu-6vcEeHuCeM9u1vh1c0IKCh6bN4WX_RyVOM2Sv-TInfA_ny0vnB-0rkqaLbDw96u2VN9MRkI4g'),
        ]
        
        # Producto de Otros
        productos_otros = [
            ('instrumento de aire 01', 800000, 10, 'otros', 'aire', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRRmu30mI1TbE-nw4QbDv0QJTjc_Xoc9kYLVySs3kNJsgYE-c-7U2LQBZNhL9SBMHGnKrf3TcwQYJYXmxuZqAVpm9Yo6RSSzTyEJnAnz6_bjfJUY0zq9SBRL2uV'),
            ('instrumento de aire 02', 500000, 10, 'otros', 'aire', 'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSVCiWZpSWTrl0jt3yaq5owkF2pRUeudNU6_tjaDo0htXmJMUieolHFOFXqV1arC-U2fF_hp6Ooa5SXf81rmM8CCwzmfT98i5iDQoHr1ifiHVbxKxZG2p26dA'),
        ] + [
            ('piano 01', 760000, 10, 'otros', 'piano', 'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcRDBUVG-pF4BcQCaMW6jSvYKp0chBnE0Ja2InPLtgxoOlJZVLZnRI5eKkqOrQgfPIzjCPtutbYG7KAqYG9x5pdTIwTPrklLgz2moZvpIwSeLoAw_MK1pfHfJg'),
            ('piano 02', 750000, 10, 'otros', 'piano', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQ58Q3kYtKUYC4OVTVbxP6zWynPz5TNL1EJnqjzzy9dDYWOSvOxBgw21LU3aTD39SUAwwiLRjAUto36ivuLtl3ZzRQd8NSEXBbux041bmnWEViEw6JtM0olhQ'),
            ('clasico 01', 20000, 10, 'otros', 'clasico', 'https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSlyOHAL_xs_Neuw907VKFDIRnU-KjmjRN2KJEpNc8-IVDkXRWAbI11W0jxVGTaYT6Up_OgE2YSqF4ocCSJlyN2HOZ8KYjzza7K2zdc1hfRnaZLqNAMiJQa'),
        ]
        
        # Productos de Baterías
        productos_baterias = [
            ('bateria 01', 800000, 10, 'baterias', 'yamaha', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTnkR3bVgGBjzVNp0tMij4hh1Uwdko6Shb4lIn-_lzsXJqZ7RQEl6vOvKOdfVd-eVUGZLIutN6WvBrYt1oihwz-g_AJBveQPCGl9s5sCkCmi_WEtxvSLZRGRQ'),
            ('bateria 02', 500000, 10, 'baterias', 'yamaha', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRCggn-BFuJ5rAoSkdCgs8mU_xBnIixsYqQt_O3nKnjitSGyye4JPQpgHMvLw5F_qdi5oHyEiY1nVKk1qcyZHTdWe9Ro-kcXdh2d9sGFd614u75a6wXaZlx'),
            ('bateria 03', 100000, 10, 'baterias', 'yamaha', 'https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcT5zHMQt_tUm2woNcko2dW1K93Chr8qzFv3zSP4Iun4y-ifU08GC_GP1ZOk0yplMhzW7RrCNXDbvEvMDkdPr-Fy9LBmj_cSCJ-TZYRhibWDUT5mZlEzoTw2'),
            ('bateria 04', 900000, 10, 'baterias', 'yamaha', 'https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRaRxKW0aA4tJVYpalndTSNBxQNYYaafRkEHEWoc_r_fsheJdw3-1F-rTyx6qgzVcKb0iR-zFeKsEIsMIzYxh_MLwm04Uu3-rPhEGZ0uabC0P5X_UBKE4PU'),
            ('bateria 05', 760000, 10, 'baterias', 'jibao', 'https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTDIHO1_rqJcqxziN2XTLUnz75AIrAgNfifpLr_SJxOSSF--U9-VPkpSaMZdu6hl9WQQ8IcDkMKBgpvg6zU7ZPoOyBZFkj5s6qKSO4QV8OMponozq68wucc'),
        ]
        
        sql_insert = "INSERT INTO products (name, price, stock, category, brand, image_url) VALUES (%s, %s, %s, %s, %s, %s)"
        
        # Insertar todos los productos
        todos_productos = productos_bajos + productos_guitarras + productos_otros + productos_baterias
        cursor.executemany(sql_insert, todos_productos)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return json.dumps({'mensaje': f'✓ {len(todos_productos)} productos insertados correctamente'}), 200, {'Content-Type': 'application/json'}
        
    except Exception as e:
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}

# --- Admin ---
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

@app.route('/admin/users/create', methods=['GET', 'POST'])
@admin_required
def admin_create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin', 0)
        
        # Validar que los campos no estén vacíos
        if not username or not email or not password:
            flash('Todos los campos son obligatorios', 'warning')
            return render_template('admin/admin_create_user.html')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('El nombre de usuario ya está en uso', 'danger')
                cursor.close()
                conn.close()
                return render_template('admin/admin_create_user.html')
            
            # Verificar si el email ya existe
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('El email ya está registrado', 'danger')
                cursor.close()
                conn.close()
                return render_template('admin/admin_create_user.html')
            
            # Insertar el nuevo usuario
            cursor.execute(
                "INSERT INTO users (username, email, password, is_admin) VALUES (%s, %s, %s, %s)",
                (username, email, password, int(is_admin))
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Usuario creado correctamente', 'success')
            return redirect(url_for('admin_users'))
            
        except Exception as e:
            flash(f'Error al crear el usuario: {str(e)}', 'danger')
            cursor.close()
            conn.close()
            return render_template('admin/admin_create_user.html')
    
    return render_template('admin/admin_create_user.html')

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        is_admin = request.form.get('is_admin', 0)
        
        cursor.execute(
            "UPDATE users SET username = %s, email = %s, is_admin = %s WHERE id = %s",
            (username, email, int(is_admin), user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('admin_users'))
    
    cursor.execute("SELECT id, username, email, IFNULL(is_admin,0) AS is_admin FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/admin_edit_user.html', user=user)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Usuario eliminado', 'info')
    return redirect(url_for('admin_users'))

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

@app.route('/admin/products/create', methods=['GET','POST'])
@admin_required
def admin_create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category = request.form.get('category')
        brand = request.form.get('brand', '')
        image_url = request.form.get('image_url', '')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, stock, category, brand, image_url) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, price, stock, category, brand, image_url)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto creado correctamente', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/admin_create_product.html')

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description', '')
        
        cursor.execute(
            "UPDATE products SET name = %s, price = %s, stock = %s WHERE id = %s",
            (name, price, stock, product_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('admin_products'))
    
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not product:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/admin_edit_product.html', product=product)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado', 'info')
    return redirect(url_for('admin_products'))

# --- Admin: Editar información de Contacto y Nosotros ---
@app.route('/admin/contacto', methods=['GET', 'POST'])
@admin_required
def admin_contacto():
    if request.method == 'POST':
        contact_text = request.form.get('contact_text', '')
        flash('Información de contacto actualizada', 'success')
        return redirect(url_for('mas_sobre'))
    return render_template('admin/admin_contacto.html')

@app.route('/admin/nosotros', methods=['GET', 'POST'])
@admin_required
def admin_nosotros():
    if request.method == 'POST':
        about_text = request.form.get('about_text', '')
        flash('Información actualizada', 'success')
        return redirect(url_for('mas_sobre'))
    return render_template('admin/admin_nosotros.html')

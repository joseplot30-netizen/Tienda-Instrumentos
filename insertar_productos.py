import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'bd_users'
}

def insertar_productos():
    """Insertar productos desde el archivo SQL a la base de datos"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Leer el archivo SQL
        with open('productos_import.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir en statements individuales
        statements = sql_content.split(';')
        
        # Ejecutar cada statement
        for statement in statements:
            statement = statement.strip()
            if statement:  # Ignorar statements vacíos
                try:
                    cursor.execute(statement)
                    print(f"✓ Ejecutado: {statement[:50]}...")
                except Exception as e:
                    print(f"✗ Error: {e}")
                    print(f"  Statement: {statement[:50]}...")
        
        conn.commit()
        print("\n✓ Todos los productos han sido insertados correctamente")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"✗ Error de conexión a BD: {err}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    print("Iniciando inserción de productos...  \n")
    insertar_productos()

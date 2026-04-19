import hashlib
from database import conectar

def generar_hash(password):
    # Convierte la contraseña en una cadena ilegible (SHA-256)
    return hashlib.sha256(password.encode()).hexdigest()

def validar_password(password_ingresada):
    hash_ingresado = generar_hash(password_ingresada)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracion WHERE clave = 'password_sistema'")
    resultado = cursor.fetchone()
    conn.close()
    
    # Comparamos el hash guardado con el hash de lo que el usuario escribió
    if resultado and resultado[0] == hash_ingresado:
        return True
    return False

def actualizar_password(nueva_password):
    hash_nuevo = generar_hash(nueva_password)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE configuracion SET valor = ? WHERE clave = 'password_sistema'", 
                       (hash_nuevo,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
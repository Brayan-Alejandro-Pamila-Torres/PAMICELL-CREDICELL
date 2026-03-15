from database import conectar, crear_tabla

crear_tabla()


def agregar_producto():
    nombre = input("Ingrese el nombre del producto: ")
    marca = input("Marca: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, marca, precio, stock) VALUES (?, ?, ?, ?)",
        (nombre, marca, precio, stock)
    )

    conn.commit()
    conn.close()

    print("Producto agregado exitosamente.")


def ver_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    print("\nInventario:\n")

    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Marca: {p[2]} | Precio: ${p[3]:.2f} | Stock: {p[4]}")

    conn.close()


def menu():

    while True:

        print("\nMenú de Inventario:")
        print("1. Agregar producto")
        print("2. Ver productos")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_producto()

        elif opcion == "2":
            ver_productos()

        elif opcion == "3":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida.")


menu()
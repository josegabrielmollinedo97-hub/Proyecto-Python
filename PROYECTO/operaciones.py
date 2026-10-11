import csv
import os
from datetime import datetime

ARCHIVO_INVENTARIO = "inventario.csv"
ARCHIVO_VENTAS = "ventas.csv"
ARCHIVO_BITACORA = "bitacora.log"

CAMPOS_INVENTARIO = ["codigo", "nombre", "categoria", "precio", "stock"]
CAMPOS_VENTAS = [
    "fecha", "codigo", "nombre", "cantidad", "precio_unitario", "total"
]

STOCK_MINIMO = 3


def registrar_bitacora(mensaje):
    """Agrega una operación con fecha y hora al archivo de bitácora.

    Parámetros:
        mensaje (str): Descripción de la operación realizada.
    Retorna:
        None.
    """
    try:
        with open(ARCHIVO_BITACORA, "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
    except OSError as error:
        print(f"Error al escribir la bitácora: {error}")


def preparar_archivos():
    """Crea los archivos CSV con encabezados si no existen.

    Parámetros:
        Ninguno.
    Retorna:
        None.
    """
    for nombre_archivo, campos in [
        (ARCHIVO_INVENTARIO, CAMPOS_INVENTARIO),
        (ARCHIVO_VENTAS, CAMPOS_VENTAS)
    ]:
        if not os.path.exists(nombre_archivo):
            try:
                with open(
                    nombre_archivo, "w", newline="", encoding="utf-8"
                ) as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=campos)
                    escritor.writeheader()
            except OSError as error:
                print(f"No se pudo crear {nombre_archivo}: {error}")
                raise


def cargar_inventario():
    """Carga los productos guardados en el archivo CSV.

    Parámetros:
        Ninguno.
    Retorna:
        list: Lista de diccionarios con los productos del inventario.
    """
    productos = []
    try:
        with open(
            ARCHIVO_INVENTARIO, "r", newline="", encoding="utf-8"
        ) as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    producto = {
                        "codigo": fila["codigo"].strip().upper(),
                        "nombre": " ".join(fila["nombre"].split()),
                        "categoria": " ".join(
                            fila["categoria"].split()
                        ).title(),
                        "precio": float(fila["precio"]),
                        "stock": int(fila["stock"])
                    }
                    productos.append(producto)
                except (ValueError, KeyError, TypeError):
                    print("Aviso: se omitió un registro inválido.")
    except OSError as error:
        print(f"Error al cargar el inventario: {error}")
    return productos


def guardar_inventario(productos):
    """Guarda todos los productos actuales en el archivo CSV.

    Parámetros:
        productos (list): Productos que se guardarán.
    Retorna:
        bool: True si se guardó correctamente; False en caso contrario.
    """
    try:
        with open(
            ARCHIVO_INVENTARIO, "w", newline="", encoding="utf-8"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=CAMPOS_INVENTARIO
            )
            escritor.writeheader()
            for producto in productos:
                fila = producto.copy()
                fila["precio"] = f"{producto['precio']:.2f}"
                escritor.writerow(fila)
        return True
    except OSError as error:
        print(f"Error al guardar el inventario: {error}")
        registrar_bitacora(f"ERROR al guardar inventario: {error}")
        return False


def cargar_ventas():
    """Carga las ventas y las representa mediante tuplas inmutables.

    Parámetros:
        Ninguno.
    Retorna:
        list: Tuplas con fecha, código, nombre, cantidad,
              precio unitario y total.
    """
    ventas = []
    try:
        with open(
            ARCHIVO_VENTAS, "r", newline="", encoding="utf-8"
        ) as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    venta = (
                        fila["fecha"],
                        fila["codigo"],
                        fila["nombre"],
                        int(fila["cantidad"]),
                        float(fila["precio_unitario"]),
                        float(fila["total"])
                    )
                    ventas.append(venta)
                except (ValueError, KeyError, TypeError):
                    print("Aviso: se omitió una venta inválida.")
    except OSError as error:
        print(f"Error al cargar las ventas: {error}")
    return ventas


def guardar_venta(venta):
    """Añade una venta al historial CSV.

    Parámetros:
        venta (tuple): Fecha, código, nombre, cantidad,
                       precio unitario y total.
    Retorna:
        bool: True si se guardó; False si ocurrió un error.
    """
    try:
        with open(
            ARCHIVO_VENTAS, "a", newline="", encoding="utf-8"
        ) as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=CAMPOS_VENTAS
            )
            escritor.writerow({
                "fecha": venta[0],
                "codigo": venta[1],
                "nombre": venta[2],
                "cantidad": venta[3],
                "precio_unitario": f"{venta[4]:.2f}",
                "total": f"{venta[5]:.2f}"
            })
        return True
    except OSError as error:
        print(f"Error al registrar la venta: {error}")
        registrar_bitacora(f"ERROR al guardar venta: {error}")
        return False


def validar_codigo(codigo):
    """Comprueba que el código tenga tres letras y tres dígitos.

    Parámetros:
        codigo (str): Código que se desea validar.
    Retorna:
        bool: True si cumple el formato, False en caso contrario.
    """
    codigo = codigo.strip().upper()
    return (
        len(codigo) == 6
        and codigo[:3].isalpha()
        and codigo[3:].isdigit()
    )


def buscar_por_codigo(productos, codigo):
    """Busca un producto por su código exacto.

    Parámetros:
        productos (list): Inventario disponible.
        codigo (str): Código del producto.
    Retorna:
        dict o None: Producto encontrado o None.
    """
    codigo = codigo.strip().upper()
    for producto in productos:
        if producto["codigo"] == codigo:
            return producto
    return None


def agregar_producto(productos):
    """Solicita los datos y agrega un nuevo libro al inventario.

    Parámetros:
        productos (list): Inventario que se actualizará.
    Retorna:
        None.
    """
    print("\n--- AGREGAR LIBRO ---")

    codigo = input("Código (3 letras y 3 números, ej. LIB001): ")
    codigo = codigo.strip().upper()

    if not validar_codigo(codigo):
        print("Código inválido. Ejemplo válido: LIB001.")
        return

    if buscar_por_codigo(productos, codigo) is not None:
        print("Ya existe un libro con ese código.")
        return

    nombre = " ".join(input("Título del libro: ").split())
    categoria = " ".join(input("Categoría: ").split()).title()

    if not nombre or not categoria:
        print("El título y la categoría son obligatorios.")
        return

    try:
        precio = float(input("Precio del libro (Q): "))
        stock = int(input("Cantidad disponible: "))

        if precio <= 0 or stock < 0:
            print("El precio debe ser positivo y el stock no negativo.")
            return
    except ValueError:
        print("Error: ingresa un precio numérico y un stock entero.")
        return

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock
    }

    productos.append(producto)

    if guardar_inventario(productos):
        registrar_bitacora(f"Producto agregado: {codigo} - {nombre}")
        print("Libro agregado correctamente.")
        comprobar_stock(producto)
    else:
        productos.remove(producto)
        print("No se agregó el libro porque no se pudo guardar.")


def buscar_producto(productos):
    """Busca libros por código exacto o título parcial.

    Parámetros:
        productos (list): Inventario disponible.
    Retorna:
        None.
    """
    termino = " ".join(input(
        "Ingresa el código o parte del título: "
    ).split()).casefold()

    if not termino:
        print("Debes ingresar un criterio de búsqueda.")
        return

    encontrados = [
        p for p in productos
        if termino == p["codigo"].casefold()
        or termino in p["nombre"].casefold()
    ]

    if encontrados:
        mostrar_productos(encontrados)
    else:
        print("No se encontraron libros.")


def mostrar_productos(productos):
    """Muestra los productos en columnas alineadas.

    Parámetros:
        productos (list): Productos que se mostrarán.
    Retorna:
        None.
    """
    if not productos:
        print("No hay libros para mostrar.")
        return

    print("-" * 90)
    print(
        f"{'CÓDIGO':<10} {'TÍTULO':<30} {'CATEGORÍA':<18} "
        f"{'PRECIO (Q)':>12} {'STOCK':>8}"
    )
    print("-" * 90)

    for p in productos:
        print(
            f"{p['codigo']:<10} {p['nombre'][:30]:<30} "
            f"{p['categoria'][:18]:<18} "
            f"{p['precio']:>12.2f} {p['stock']:>8}"
        )
    print("-" * 90)


def ordenar_inventario(productos):
    """Permite ordenar los libros por título o precio.

    Parámetros:
        productos (list): Inventario disponible.
    Retorna:
        None.
    """
    print("\n1. Ordenar por título")
    print("2. Ordenar por precio")
    opcion = input("Selecciona el criterio: ").strip()

    if opcion == "1":
        ordenados = sorted(
            productos, key=lambda p: p["nombre"].casefold()
        )
    elif opcion == "2":
        ordenados = sorted(productos, key=lambda p: p["precio"])
    else:
        print("Opción inválida.")
        return

    mostrar_productos(ordenados)

"""-------------------------------------------------------------------------------------------------------------------------"""

def comprobar_stock(producto):
    """Avisa cuando un libro alcanza el nivel mínimo de existencias.

    Parámetros:
        producto (dict): Libro que se verificará.
    Retorna:
        None.
    """
    if producto["stock"] <= STOCK_MINIMO:
        print(
            f"¡ALERTA! Quedan {producto['stock']} ejemplares "
            f"de '{producto['nombre']}'."
        )
        registrar_bitacora(
            f"ALERTA de stock mínimo: {producto['codigo']}, "
            f"existencias={producto['stock']}"
        )


def registrar_venta(productos):
    """Registra una venta validando la existencia de libros.

    Parámetros:
        productos (list): Inventario que se actualizará.
    Retorna:
        None.
    """
    print("\n--- REGISTRAR VENTA ---")
    codigo = input("Código del libro: ").strip().upper()
    producto = buscar_por_codigo(productos, codigo)

    if producto is None:
        print("No existe un libro con ese código.")
        return

    print(f"Libro: {producto['nombre']}")
    print(f"Precio unitario: Q{producto['precio']:.2f}")
    print(f"Existencias: {producto['stock']}")

    try:
        cantidad = int(input("Cantidad que desea comprar: "))
        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            return
        if cantidad > producto["stock"]:
            print("No hay suficientes ejemplares disponibles.")
            return
    except ValueError:
        print("Error: la cantidad debe ser un número entero.")
        return

    total = round(producto["precio"] * cantidad, 2)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    venta = (
        fecha,
        producto["codigo"],
        producto["nombre"],
        cantidad,
        producto["precio"],
        total
    )

    stock_anterior = producto["stock"]
    producto["stock"] -= cantidad

    if not guardar_inventario(productos):
        producto["stock"] = stock_anterior
        print("Venta cancelada: no se pudo guardar el inventario.")
        return

    if not guardar_venta(venta):
        producto["stock"] = stock_anterior
        if not guardar_inventario(productos):
            print("¡ATENCIÓN! No se pudo restaurar el inventario.")
        print("No se pudo guardar la venta; revisa los archivos.")
        registrar_bitacora(
            f"ERROR de registro de venta para {codigo}"
        )
        return

    registrar_bitacora(
        f"Venta: {codigo}, cantidad={cantidad}, total=Q{total:.2f}"
    )

    print(f"Venta registrada. Total: Q{total:.2f}")
    comprobar_stock(producto)


def reporte_ventas_dia(ventas):
    """Muestra las ventas de la fecha actual en columnas alineadas.

    Parámetros:
        ventas (list): Lista de tuplas de ventas.
    Retorna:
        None.
    """
    hoy = datetime.now().strftime("%Y-%m-%d")
    ventas_hoy = [v for v in ventas if v[0].startswith(hoy)]

    print(f"\nREPORTE DE VENTAS DEL DÍA: {hoy}")
    print("-" * 90)
    print(
        f"{'HORA':<10} {'CÓDIGO':<10} {'TÍTULO':<28} "
        f"{'CANT.':>7} {'TOTAL (Q)':>12}"
    )
    print("-" * 90)

    total_dia = 0.0

    for venta in ventas_hoy:
        hora = venta[0][11:19]
        print(
            f"{hora:<10} {venta[1]:<10} {venta[2][:28]:<28} "
            f"{venta[3]:>7} {venta[5]:>12.2f}"
        )
        total_dia += venta[5]

    print("-" * 90)
    print(f"{'Cantidad de ventas:':<55}{len(ventas_hoy):>7}")
    print(f"{'TOTAL DEL DÍA (Q):':<55}{total_dia:>12.2f}")
    print("-" * 90)


def mostrar_categorias(productos):
    """Muestra las categorías sin duplicados usando un conjunto.

    Parámetros:
        productos (list): Inventario disponible.
    Retorna:
        None.
    """
    categorias = {p["categoria"] for p in productos}
    print("\nCategorías registradas:")
    if categorias:
        for categoria in sorted(categorias):
            print(f"- {categoria}")
    else:
        print("No hay categorías registradas.")

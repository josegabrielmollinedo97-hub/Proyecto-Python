from operaciones import (
    preparar_archivos,
    cargar_inventario,
    guardar_inventario,
    cargar_ventas,
    agregar_producto,
    buscar_producto,
    mostrar_productos,
    ordenar_inventario,
    registrar_venta,
    reporte_ventas_dia,
    mostrar_categorias,
    registrar_bitacora
)


def mostrar_menu():
    """Muestra las opciones principales del sistema.

    Parámetros:
        Ninguno.
    Retorna:
        None.
    """
    print("\n" + "=" * 45)
    print("       SISTEMA DE LIBRERÍA")
    print("=" * 45)
    print("1. Agregar un nuevo libro")
    print("2. Buscar un libro")
    print("3. Registrar una venta")
    print("4. Mostrar inventario completo")
    print("5. Reporte de ventas del día")
    print("6. Mostrar categorías")
    print("7. Salir")
    print("=" * 45)


def ejecutar_programa():
    """Inicializa los archivos y ejecuta el menú hasta salir.

    Parámetros:
        Ninguno.
    Retorna:
        None.
    """
    preparar_archivos()
    productos = cargar_inventario()
    ventas = cargar_ventas()

    print("Bienvenido al sistema de la librería.")
    print(f"Libros cargados: {len(productos)}")
    registrar_bitacora("Sistema iniciado")

    while True:
        mostrar_menu()

        try:
            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                agregar_producto(productos)

            elif opcion == "2":
                buscar_producto(productos)

            elif opcion == "3":
                registrar_venta(productos)
                # Actualizar el historial en memoria después de vender.
                ventas = cargar_ventas()

            elif opcion == "4":
                ordenar_inventario(productos)

            elif opcion == "5":
                reporte_ventas_dia(ventas)

            elif opcion == "6":
                mostrar_categorias(productos)

            elif opcion == "7":
                if guardar_inventario(productos):
                    registrar_bitacora("Sistema cerrado correctamente")
                    print("Cambios guardados. ¡Hasta pronto!")
                    break
                else:
                    print(
                        "No se pudo guardar el inventario. "
                        "Revisa el error antes de cerrar."
                    )

            else:
                print("Opción inválida. Selecciona un número del 1 al 7.")

        except (EOFError, KeyboardInterrupt):
            print("\nCierre solicitado.")
            if guardar_inventario(productos):
                registrar_bitacora("Sistema cerrado por interrupción")
                print("Inventario guardado.")
                break
            print("No se pudo guardar el inventario.")


if __name__ == "__main__":
    ejecutar_programa()

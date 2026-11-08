from inventario import Inventario
from modelos import LibroFisico, Venta
from persistencia import PersistenciaCSV
from reportes import Reportes
from excepciones import ErrorSistema

class SistemaLibreria:
    def __init__(self, carpeta="."):
        self.datos = PersistenciaCSV(carpeta)
        productos = self.datos.cargar_productos()
        self.inventario = Inventario(productos)
        self.datos.registrar_bitacora("Sistema iniciado")

    def _guardar(self):
        self.datos.guardar_productos(self.inventario.productos)

    def _pausa(self):
        input("\nPresiona Enter para continuar...")

    def agregar_producto(self):
        print("\n--- AGREGAR LIBRO ---")
        p = LibroFisico(input("Código (LIB001): "), input("Título: "),
                        input("Categoría: "), float(input("Precio Q: ")),
                        int(input("Stock: ")))
        self.inventario.agregar(p)
        self._guardar()
        self.datos.registrar_bitacora(f"Producto agregado: {p.codigo}")
        print("Libro agregado correctamente.")
        self._alerta(p)

    def _alerta(self, p):
        if self.inventario.alerta_stock(p):
            mensaje = f"ALERTA: quedan {p.stock} unidades de {p.nombre}"
            print(mensaje)
            self.datos.registrar_bitacora(mensaje)

    def buscar_producto(self):
        p = self.inventario.buscar(input("Código o parte del título: "))
        print(p.descripcion(), f"| Precio: Q{p.precio:.2f} | Stock: {p.stock}")

    def vender(self):
        codigo = input("Código del libro: ")
        cantidad = int(input("Cantidad a vender: "))
        p = self.inventario.buscar(codigo)
        venta = Venta(p, cantidad)
        p.vender(cantidad)
        try:
            self._guardar()
            self.datos.guardar_venta(venta)
        except OSError:
            p.stock += cantidad
            self._guardar()
            raise
        self.datos.registrar_bitacora(venta.descripcion())
        print(f"Venta registrada. Total: Q{venta.total:.2f}")
        self._alerta(p)

    def mostrar_inventario(self):
        productos = self.inventario.ordenar()
        if not productos:
            print("No hay libros registrados.")
        for p in productos:
            print(f"{p.codigo:<8} {p.nombre[:30]:<30} {p.categoria:<18} Q{p.precio:>8.2f} {p.stock:>5}")

    def reporte_dia(self):
        ventas = Reportes.ventas_del_dia(self.datos.cargar_ventas())
        for v in ventas:
            print(f"{v['fecha']} | {v['codigo']} | {v['nombre']} | {v['cantidad']} | Q{float(v['total']):.2f}")
        print(f"Total vendido hoy: Q{Reportes.total_ventas(ventas):.2f}")

    def mostrar_categorias(self):
        for c in self.inventario.categorias():
            print("-", c)

    def resumen(self):
        r = Reportes.resumen_inventario(self.inventario.productos)
        print(f"Tipos de libros: {r['productos']} | Unidades: {r['unidades']} | Valor del inventario: Q{r['valor']:.2f}")

    def ejecutar(self):
        while True:
            print("\\n" + "=" * 48)
            print("             SISTEMA DE LIBRERÍA")
            print("=" * 48)
            print("1. Agregar libro")
            print("2. Buscar libro")
            print("3. Registrar venta")
            print("4. Mostrar inventario ordenado")
            print("5. Reporte de ventas del día")
            print("6. Mostrar categorías")
            print("7. Resumen del inventario")
            print("8. Salir")
            opcion = input("Selecciona una opción: ").strip()
            try:
                if opcion == "1": self.agregar_producto()
                elif opcion == "2": self.buscar_producto()
                elif opcion == "3": self.vender()
                elif opcion == "4": self.mostrar_inventario()
                elif opcion == "5": self.reporte_dia()
                elif opcion == "6": self.mostrar_categorias()
                elif opcion == "7": self.resumen()
                elif opcion == "8":
                    self._guardar()
                    self.datos.registrar_bitacora("Sistema cerrado")
                    print("Datos guardados. Hasta pronto.")
                    break
                else: print("Opción inválida.")
            except (ValueError, ErrorSistema, OSError) as e:
                print(f"No se pudo completar la operación: {e}")
                self.datos.registrar_bitacora(f"ERROR: {e}")
            except (EOFError, KeyboardInterrupt):
                print("\\nCierre solicitado.")
                self._guardar()
                self.datos.registrar_bitacora("Cierre por interrupción")
                break
            self._pausa()

from excepciones import DatoInvalidoError, ProductoNoEncontradoError
from modelos import Producto

STOCK_MINIMO = 3

class Inventario:
    """Administra los productos y aplica la regla de stock mínimo."""
    def __init__(self, productos=None):
        self._productos = productos or []

    @property
    def productos(self):
        return tuple(self._productos)

    def agregar(self, producto):
        if self.buscar(producto.codigo, lanzar=False):
            raise DatoInvalidoError("Ya existe un producto con ese código.")
        self._productos.append(producto)

    def buscar(self, termino, lanzar=True):
        termino = termino.strip().casefold()
        for p in self._productos:
            if termino == p.codigo.casefold() or termino in p.nombre.casefold():
                return p
        if lanzar:
            raise ProductoNoEncontradoError("No se encontró el libro.")
        return None

    def eliminar(self, codigo):
        producto = self.buscar(codigo)
        self._productos.remove(producto)
        return producto

    def ordenar(self, criterio="nombre"):
        if criterio == "precio":
            return sorted(self._productos, key=lambda p: p.precio)
        return sorted(self._productos, key=lambda p: p.nombre.casefold())

    def categorias(self):
        return sorted({p.categoria for p in self._productos})

    def alerta_stock(self, producto):
        return producto.stock <= STOCK_MINIMO

    def registrar_venta(self, codigo, cantidad):
        producto = self.buscar(codigo)
        producto.vender(cantidad)
        from modelos import Venta
        return Venta(producto, cantidad)

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import DatoInvalidoError, StockInsuficienteError

class Registrable(ABC):
    """Clase abstracta para objetos que pueden generar una descripción."""
    @abstractmethod
    def descripcion(self):
        pass

class Producto(Registrable):
    """Representa un libro del inventario."""
    def __init__(self, codigo, nombre, categoria, precio, stock):
        self.codigo = codigo.strip().upper()
        self.nombre = " ".join(nombre.split())
        self.categoria = " ".join(categoria.split()).title()
        self.precio = float(precio)
        self.stock = int(stock)
        self._validar()

    def _validar(self):
        if len(self.codigo) != 6 or not self.codigo[:3].isalpha() or not self.codigo[3:].isdigit():
            raise DatoInvalidoError("El código debe tener 3 letras y 3 números, por ejemplo LIB001.")
        if not self.nombre or not self.categoria:
            raise DatoInvalidoError("El nombre y la categoría son obligatorios.")
        if self.precio <= 0 or self.stock < 0:
            raise DatoInvalidoError("El precio debe ser mayor que cero y el stock no puede ser negativo.")

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = valor

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = float(valor)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        self._stock = int(valor)

    def vender(self, cantidad):
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        if cantidad > self.stock:
            raise StockInsuficienteError(f"Stock insuficiente. Disponibles: {self.stock}.")
        self.stock -= cantidad

    def descripcion(self):
        return f"{self.codigo} - {self.nombre} ({self.categoria})"

    def a_diccionario(self):
        return {"codigo": self.codigo, "nombre": self.nombre, "categoria": self.categoria,
                "precio": f"{self.precio:.2f}", "stock": self.stock}

class LibroFisico(Producto):
    """Tipo de producto concreto: libro físico."""
    def descripcion(self):
        return f"Libro físico: {super().descripcion()}"

class LibroDigital(Producto):
    """Tipo de producto concreto: libro digital."""
    def descripcion(self):
        return f"Libro digital: {super().descripcion()}"

class Venta(Registrable):
    def __init__(self, producto, cantidad, fecha=None):
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.codigo = producto.codigo
        self.nombre = producto.nombre
        self.cantidad = int(cantidad)
        self.precio_unitario = producto.precio
        self.total = round(self.precio_unitario * self.cantidad, 2)

    def descripcion(self):
        return f"Venta de {self.cantidad} unidad(es) de {self.nombre}: Q{self.total:.2f}"

    def a_diccionario(self):
        return {"fecha": self.fecha, "codigo": self.codigo, "nombre": self.nombre,
                "cantidad": self.cantidad, "precio_unitario": f"{self.precio_unitario:.2f}",
                "total": f"{self.total:.2f}"}

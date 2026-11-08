import tempfile
import unittest
from pathlib import Path
from modelos import LibroFisico, LibroDigital
from inventario import Inventario
from excepciones import DatoInvalidoError, StockInsuficienteError
from persistencia import PersistenciaCSV
from reportes import Reportes

class PruebasLibreria(unittest.TestCase):
    def setUp(self):
        self.libro = LibroFisico("LIB001", "Cien años de soledad", "Novela", 85, 10)
        self.inventario = Inventario([self.libro])

    def test_agregar_y_buscar(self):
        self.inventario.agregar(LibroDigital("DIG001", "Python básico", "Educativo", 50, 4))
        self.assertEqual(self.inventario.buscar("DIG001").nombre, "Python básico")

    def test_codigo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            LibroFisico("123", "Libro", "Novela", 10, 2)

    def test_no_permite_vender_mas_stock(self):
        with self.assertRaises(StockInsuficienteError):
            self.libro.vender(11)

    def test_guardar_y_cargar_csv(self):
        with tempfile.TemporaryDirectory() as carpeta:
            datos = PersistenciaCSV(carpeta)
            datos.guardar_productos([self.libro])
            cargados = datos.cargar_productos()
            self.assertEqual(len(cargados), 1)
            self.assertEqual(cargados[0].codigo, "LIB001")

if __name__ == "__main__":
    unittest.main()

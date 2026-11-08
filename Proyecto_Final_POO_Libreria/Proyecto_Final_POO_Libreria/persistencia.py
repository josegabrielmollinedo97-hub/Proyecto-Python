import csv
from pathlib import Path
from modelos import LibroFisico, LibroDigital, Venta

class PersistenciaCSV:
    """Centraliza la lectura y escritura de los archivos CSV."""
    def __init__(self, carpeta="."):
        self.carpeta = Path(carpeta)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self.inventario = self.carpeta / "inventario.csv"
        self.ventas = self.carpeta / "ventas.csv"
        self.bitacora = self.carpeta / "bitacora.log"
        self.campos_productos = ["codigo", "nombre", "categoria", "precio", "stock"]
        self.campos_ventas = ["fecha", "codigo", "nombre", "cantidad", "precio_unitario", "total"]
        self.preparar_archivos()

    def _preparar(self, ruta, campos):
        if not ruta.exists():
            with ruta.open("w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=campos).writeheader()

    def preparar_archivos(self):
        self._preparar(self.inventario, self.campos_productos)
        self._preparar(self.ventas, self.campos_ventas)

    def cargar_productos(self):
        productos = []
        with self.inventario.open(newline="", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                try:
                    clase = LibroDigital if fila.get("tipo") == "digital" else LibroFisico
                    productos.append(clase(fila["codigo"], fila["nombre"], fila["categoria"],
                                            float(fila["precio"]), int(fila["stock"])))
                except (ValueError, KeyError, TypeError):
                    continue
        return productos

    def guardar_productos(self, productos):
        with self.inventario.open("w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos_productos)
            escritor.writeheader()
            escritor.writerows(p.a_diccionario() for p in productos)

    def guardar_venta(self, venta):
        with self.ventas.open("a", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=self.campos_ventas)
            escritor.writerow(venta.a_diccionario())

    def cargar_ventas(self):
        with self.ventas.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def registrar_bitacora(self, mensaje):
        from datetime import datetime
        with self.bitacora.open("a", encoding="utf-8") as f:
            f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {mensaje}\n")

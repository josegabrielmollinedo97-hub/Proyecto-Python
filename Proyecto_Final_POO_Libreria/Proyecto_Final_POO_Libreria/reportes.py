from datetime import datetime

class Reportes:
    @staticmethod
    def ventas_del_dia(ventas):
        hoy = datetime.now().strftime("%Y-%m-%d")
        return [v for v in ventas if v["fecha"].startswith(hoy)]

    @staticmethod
    def total_ventas(ventas):
        return sum(float(v["total"]) for v in ventas)

    @staticmethod
    def resumen_inventario(productos):
        return {"productos": len(productos),
                "unidades": sum(p.stock for p in productos),
                "valor": sum(p.precio * p.stock for p in productos)}

class ErrorSistema(Exception):
    """Error general del sistema de librería."""

class DatoInvalidoError(ErrorSistema):
    """Se usa cuando un dato ingresado no cumple las reglas."""

class ProductoNoEncontradoError(ErrorSistema):
    """Se usa cuando no existe un producto con el código indicado."""

class StockInsuficienteError(ErrorSistema):
    """Se usa cuando se intenta vender más unidades de las disponibles."""

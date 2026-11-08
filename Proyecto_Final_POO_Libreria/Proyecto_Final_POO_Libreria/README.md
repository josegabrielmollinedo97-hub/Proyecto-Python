# Proyecto Final POO: Sistema de inventario y ventas de una librería

## Descripción
Este programa administra libros, existencias y ventas de una librería. Es la versión orientada a objetos del Proyecto 1.

## Requisitos
- Python 3.10 o superior.
- No requiere instalar paquetes externos.

## Cómo ejecutar
1. Descomprimir la carpeta.
2. Abrirla en Visual Studio Code.
3. Abrir una terminal en la carpeta.
4. Ejecutar: `python main.py`

## Funciones
- Agregar y buscar libros.
- Registrar ventas y descontar existencias.
- Mostrar inventario ordenado por título.
- Consultar reporte de ventas del día.
- Mostrar categorías.
- Consultar resumen y valor del inventario.
- Guardar inventario y ventas en CSV.
- Registrar acciones y errores en `bitacora.log`.

## Regla especial conservada
Cuando el stock de un libro es menor o igual a 3 unidades, el sistema muestra una alerta y la registra en la bitácora. Esta regla proviene del Proyecto 1 (`STOCK_MINIMO = 3`).

## Programación orientada a objetos
- **Abstracción:** `Registrable` define el método abstracto `descripcion`.
- **Herencia:** `LibroFisico` y `LibroDigital` heredan de `Producto`; `Producto` y `Venta` implementan `Registrable`.
- **Encapsulamiento:** los atributos de `Producto` se almacenan como atributos privados por convención (`_precio`, `_stock`, etc.) y se acceden mediante propiedades.
- **Polimorfismo:** `LibroFisico` y `LibroDigital` implementan `descripcion` de manera distinta; ambos pueden tratarse como `Registrable`.

## Archivos
- `main.py`: punto de entrada.
- `app.py`: menú y coordinación.
- `modelos.py`: clases del dominio.
- `inventario.py`: operaciones del inventario.
- `persistencia.py`: archivos CSV y bitácora.
- `reportes.py`: reportes.
- `excepciones.py`: errores personalizados.
- `pruebas.py`: pruebas automáticas.

Los archivos `inventario.csv`, `ventas.csv` y `bitacora.log` se crean automáticamente al ejecutar el programa.

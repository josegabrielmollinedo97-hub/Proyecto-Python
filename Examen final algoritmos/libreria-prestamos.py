
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponible = True

    def mostrar_informacion(self):
        estado = "Disponible" if self.disponible else "Prestado"

        print(f"Titulo: {self.titulo}")
        print(f"Autor: {self.autor}")
        print(f"Disponibilidad: {estado}")


class Socio:
    def __init__(self, carnet, nombre):
        self.carnet = carnet
        self.nombre = nombre
        self.libros_prestados = []

    def mostrar_informacion(self):
        print(f"Carnet: {self.carnet}")
        print(f"Nombre: {self.nombre}")
        print(f"Libros prestados: {len(self.libros_prestados)}")


class Biblioteca:
    def __init__(self):
        self.libros = []
        self.socios = []

    def registrar_libro(self):
        titulo = input("Ingrese el titulo: ")
        autor = input("Ingrese el autor: ")

        # Evitar libros duplicados
        for libro in self.libros:
            if libro.titulo.lower() == titulo.lower():
                print("Este libro ya esta registrado.")
                return

        nuevo_libro = Libro(titulo, autor)
        self.libros.append(nuevo_libro)

        print("Libro registrado correctamente.")

    def registrar_socio(self):
        carnet = input("Ingrese el carnet: ")
        nombre = input("Ingrese el nombre: ")

        for socio in self.socios:
            if socio.carnet == carnet:
                print("Este carnet ya esta registrado.")
                return

        nuevo_socio = Socio(carnet, nombre)
        self.socios.append(nuevo_socio)

        print("Socio registrado correctamente.")

    def prestar_libro(self):
        carnet = input("Ingrese el carnet del socio: ")
        titulo = input("Ingrese el titulo del libro: ")

        socio = None
        libro = None

        for s in self.socios:
            if s.carnet == carnet:
                socio = s
                break

        for l in self.libros:
            if l.titulo.lower() == titulo.lower():
                libro = l
                break

        if socio is None:
            print("El socio no existe.")
            return

        if libro is None:
            print("El libro no existe.")
            return

        if not libro.disponible:
            print("El libro ya esta prestado.")
            return

        if len(socio.libros_prestados) >= 3:
            print("El socio ya tiene 3 libros prestados.")
            return

        libro.disponible = False
        socio.libros_prestados.append(libro)

        print("Prestamo realizado correctamente.")

    def devolver_libro(self):
        carnet = input("Ingrese el carnet del socio: ")
        titulo = input("Ingrese el titulo del libro: ")

        socio = None

        for s in self.socios:
            if s.carnet == carnet:
                socio = s
                break

        if socio is None:
            print("El socio no existe.")
            return

        for libro in socio.libros_prestados:
            if libro.titulo.lower() == titulo.lower():
                libro.disponible = True
                socio.libros_prestados.remove(libro)

                print("Libro devuelto correctamente.")
                return

        print("El socio no tiene prestado ese libro.")

    def mostrar_libros(self):
        if not self.libros:
            print("No hay libros registrados.")
            return

        print("\n--- INVENTARIO DE LIBROS ---")

        for libro in self.libros:
            libro.mostrar_informacion()
            print("----------------------")

    def mostrar_socios(self):
        if not self.socios:
            print("No hay socios registrados.")
            return

        print("\n--- LISTA DE SOCIOS ---")

        for socio in self.socios:
            socio.mostrar_informacion()

            for libro in socio.libros_prestados:
                print(f"  - {libro.titulo}")

            print("----------------------")


# PROGRAMA PRINCIPAL

biblioteca = Biblioteca()

while True:
    print("\n===== SISTEMA DE BIBLIOTECA =====")
    print("1. Registrar libro")
    print("2. Registrar socio")
    print("3. Prestar libro")
    print("4. Devolver libro")
    print("5. Mostrar libros")
    print("6. Mostrar socios y prestamos")
    print("7. Salir")

    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        biblioteca.registrar_libro()

    elif opcion == "2":
        biblioteca.registrar_socio()

    elif opcion == "3":
        biblioteca.prestar_libro()

    elif opcion == "4":
        biblioteca.devolver_libro()

    elif opcion == "5":
        biblioteca.mostrar_libros()

    elif opcion == "6":
        biblioteca.mostrar_socios()

    elif opcion == "7":
        print("Gracias por utilizar la biblioteca.")
        break

    else:
        print("Opcion no valida.")

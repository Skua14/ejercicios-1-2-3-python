"""
main.py

Punto de entrada de la aplicación. Inicializa la base de datos
(crea el archivo repuestos.db y la tabla si no existen) y arranca
el menú interactivo.
"""

from db import cerrar, inicializar_db
from cli.menu import ejecutar_menu


def main() -> None:
    """Inicializa la base y ejecuta el menú hasta que el usuario decida salir."""
    inicializar_db()
    try:
        ejecutar_menu()
    finally:
        cerrar()


if __name__ == "__main__":
    main()

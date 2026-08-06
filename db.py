"""
db.py

Configuración y conexión a la base de datos usando Peewee.
Centraliza el objeto `database` para que el resto de los módulos
(sobre todo models.py) lo importen desde acá.
"""

from peewee import SqliteDatabase

# Nombre del archivo de base de datos SQLite.
DB_NAME: str = "repuestos.db"

# Instancia única de la base de datos, compartida por toda la app.
database: SqliteDatabase = SqliteDatabase(DB_NAME)


def conectar() -> None:
    """Abre la conexión con la base de datos si todavía no está abierta."""
    if database.is_closed():
        database.connect()


def cerrar() -> None:
    """Cierra la conexión con la base de datos si está abierta."""
    if not database.is_closed():
        database.close()


def inicializar_db() -> None:
    """
    Conecta la base de datos y crea las tablas necesarias si no existen.

    Se importa el modelo acá adentro (en vez de al principio del archivo)
    para evitar import circular entre db.py y models.py.
    """
    from models import Repuesto

    conectar()
    database.create_tables([Repuesto], safe=True)

"""
repository.py

Capa de acceso a datos: funciones que interactúan directamente con
Peewee (queries, insert_many, updates, deletes). No contiene lógica
de negocio ni validación: eso vive en services.py y schemas.py.
"""

from datetime import datetime
from typing import Iterable, Optional

from models import Repuesto
from schemas import RepuestoCreate


def crear_repuesto(datos: RepuestoCreate) -> Repuesto:
    """Inserta un nuevo repuesto en la base y devuelve la instancia creada."""
    ahora = datetime.now()
    return Repuesto.create(
        nombre=datos.nombre,
        marca=datos.marca,
        modelo_auto=datos.modelo_auto,
        categoria=datos.categoria.value,
        precio=datos.precio,
        stock=datos.stock,
        fecha_ingreso=ahora,
        fecha_modificado=ahora,
    )


def crear_repuestos_masivo(lista_datos: list[RepuestoCreate]) -> int:
    """
    Inserta varios repuestos de una sola vez usando insert_many,
    dentro de una transacción. Devuelve la cantidad de filas insertadas.
    """
    if not lista_datos:
        return 0

    ahora = datetime.now()
    filas = [
        {
            "nombre": datos.nombre,
            "marca": datos.marca,
            "modelo_auto": datos.modelo_auto,
            "categoria": datos.categoria.value,
            "precio": datos.precio,
            "stock": datos.stock,
            "fecha_ingreso": ahora,
            "fecha_modificado": ahora,
        }
        for datos in lista_datos
    ]

    with Repuesto._meta.database.atomic():
        Repuesto.insert_many(filas).execute()

    return len(filas)


def listar_repuestos() -> list[Repuesto]:
    """Devuelve todos los repuestos ordenados por id."""
    return list(Repuesto.select().order_by(Repuesto.id))


def obtener_por_id(repuesto_id: int) -> Optional[Repuesto]:
    """Busca un repuesto por id. Devuelve None si no existe."""
    return Repuesto.get_or_none(Repuesto.id == repuesto_id)


def buscar_por_nombre_o_marca(texto: str) -> list[Repuesto]:
    """
    Busca repuestos cuyo nombre o marca contengan el texto dado,
    sin distinguir mayúsculas/minúsculas (búsqueda parcial).
    """
    patron = f"%{texto.strip().lower()}%"
    return list(
        Repuesto.select().where(
            Repuesto.nombre.ilike(patron) | Repuesto.marca.ilike(patron)
        )
    )


def actualizar_repuesto(
    repuesto: Repuesto, precio: Optional[float], stock: Optional[int]
) -> Repuesto:
    """Actualiza precio y/o stock de un repuesto existente y guarda el cambio."""
    if precio is not None:
        repuesto.precio = precio
    if stock is not None:
        repuesto.stock = stock
    repuesto.fecha_modificado = datetime.now()
    repuesto.save()
    return repuesto


def eliminar_repuesto(repuesto: Repuesto) -> None:
    """Elimina un repuesto de la base de datos."""
    repuesto.delete_instance()


def obtener_todos_para_exportar() -> Iterable[Repuesto]:
    """Alias semántico de listar_repuestos, pensado para exportación a CSV."""
    return listar_repuestos()

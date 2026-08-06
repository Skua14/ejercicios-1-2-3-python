"""
services.py

Lógica de negocio de la aplicación: valida con Pydantic, coordina
con repository.py para persistir, maneja la carga masiva desde CSV
y la exportación a CSV. Esta es la capa que usa cli/menu.py: el menú
no debería llamar directamente a repository.py ni a Peewee.
"""

import csv
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

import repository
from models import Repuesto
from schemas import RepuestoCreate, RepuestoUpdate

# Columnas esperadas tanto en el CSV de carga masiva como en el de exportación.
COLUMNAS_CSV: list[str] = [
    "id",
    "nombre",
    "marca",
    "modelo_auto",
    "categoria",
    "precio",
    "stock",
    "fecha_ingreso",
    "fecha_modificado",
]

COLUMNAS_CARGA_MASIVA: list[str] = [
    "nombre",
    "marca",
    "modelo_auto",
    "categoria",
    "precio",
    "stock",
]


@dataclass
class ErrorFilaCarga:
    """Representa una fila del CSV de carga masiva que no pasó la validación."""

    numero_fila: int
    motivo: str


@dataclass
class ResultadoCargaMasiva:
    """Resultado consolidado de una carga masiva desde CSV."""

    insertados: int = 0
    errores: list[ErrorFilaCarga] = field(default_factory=list)


def agregar_repuesto(datos_crudos: dict[str, str]) -> Repuesto:
    """
    Valida los datos crudos (por ejemplo, ingresados por el usuario en el
    menú) con RepuestoCreate y, si son válidos, los persiste.

    Puede propagar pydantic.ValidationError: quien llame decide cómo
    mostrar el error (el menú lo captura y lo muestra legible).
    """
    datos_validados = RepuestoCreate(**datos_crudos)
    return repository.crear_repuesto(datos_validados)


def listar_repuestos() -> list[Repuesto]:
    """Devuelve todos los repuestos cargados."""
    return repository.listar_repuestos()


def buscar_repuestos(texto: str) -> list[Repuesto]:
    """Busca repuestos por nombre o marca (parcial, case-insensitive)."""
    return repository.buscar_por_nombre_o_marca(texto)


def actualizar_repuesto(repuesto_id: int, datos_crudos: dict[str, str]) -> Repuesto:
    """
    Valida los datos de actualización con RepuestoUpdate y aplica los
    cambios sobre el repuesto indicado.

    Lanza ValueError si el repuesto no existe o si no se informó ningún
    campo para actualizar. Puede propagar pydantic.ValidationError si
    los datos informados no cumplen las reglas (precio > 0, stock >= 0).
    """
    repuesto = repository.obtener_por_id(repuesto_id)
    if repuesto is None:
        raise ValueError(f"No existe ningún repuesto con id {repuesto_id}.")

    datos_validados = RepuestoUpdate(**datos_crudos)
    if datos_validados.precio is None and datos_validados.stock is None:
        raise ValueError("Debe informar al menos un campo (precio o stock) para actualizar.")

    return repository.actualizar_repuesto(
        repuesto, datos_validados.precio, datos_validados.stock
    )


def eliminar_repuesto(repuesto_id: int) -> Repuesto:
    """
    Elimina el repuesto indicado. Lanza ValueError si no existe.
    Devuelve la instancia eliminada por si el menú quiere mostrar sus datos.
    """
    repuesto = repository.obtener_por_id(repuesto_id)
    if repuesto is None:
        raise ValueError(f"No existe ningún repuesto con id {repuesto_id}.")
    repository.eliminar_repuesto(repuesto)
    return repuesto


def exportar_a_csv(ruta_destino: str = "repuestos.csv") -> int:
    """
    Exporta todos los repuestos de la base a un archivo CSV con encabezados.
    Devuelve la cantidad de filas exportadas.
    """
    repuestos = repository.obtener_todos_para_exportar()

    with open(ruta_destino, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_CSV)
        escritor.writeheader()
        cantidad = 0
        for r in repuestos:
            escritor.writerow(
                {
                    "id": r.id,
                    "nombre": r.nombre,
                    "marca": r.marca,
                    "modelo_auto": r.modelo_auto,
                    "categoria": r.categoria,
                    "precio": r.precio,
                    "stock": r.stock,
                    "fecha_ingreso": r.fecha_ingreso.isoformat(),
                    "fecha_modificado": r.fecha_modificado.isoformat(),
                }
            )
            cantidad += 1

    return cantidad


def cargar_masivo_desde_csv(ruta_origen: str) -> ResultadoCargaMasiva:
    """
    Lee un CSV con columnas nombre, marca, modelo_auto, categoria,
    precio, stock; valida cada fila con RepuestoCreate y realiza una
    inserción masiva (insert_many) solo con las filas válidas.

    Las filas inválidas no frenan el proceso: se acumulan en el
    resultado junto con el motivo del error.
    """
    ruta = Path(ruta_origen)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo '{ruta_origen}'.")

    resultado = ResultadoCargaMasiva()
    filas_validas: list[RepuestoCreate] = []

    with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        columnas_faltantes = set(COLUMNAS_CARGA_MASIVA) - set(lector.fieldnames or [])
        if columnas_faltantes:
            raise ValueError(
                "El CSV no tiene las columnas requeridas. "
                f"Faltan: {', '.join(sorted(columnas_faltantes))}"
            )

        # numero_fila arranca en 2 porque la fila 1 del archivo es el encabezado.
        for numero_fila, fila in enumerate(lector, start=2):
            try:
                datos = RepuestoCreate(
                    nombre=fila.get("nombre", ""),
                    marca=fila.get("marca", ""),
                    modelo_auto=fila.get("modelo_auto", ""),
                    categoria=fila.get("categoria", ""),
                    precio=fila.get("precio", ""),
                    stock=fila.get("stock", ""),
                )
                filas_validas.append(datos)
            except ValidationError as error:
                motivo = "; ".join(
                    f"{e['loc'][0]}: {e['msg']}" for e in error.errors()
                )
                resultado.errores.append(ErrorFilaCarga(numero_fila, motivo))

    resultado.insertados = repository.crear_repuestos_masivo(filas_validas)
    return resultado

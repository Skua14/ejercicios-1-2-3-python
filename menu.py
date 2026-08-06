"""
cli/menu.py

Menú interactivo por consola. Esta es la única capa que interactúa
con el usuario (input/print). Toda la validación y persistencia se
delega a services.py; acá no se valida "a mano" nada que ya valide
Pydantic.
"""

from pydantic import ValidationError

import services
from models import Repuesto
from schemas import Categoria

SEPARADOR: str = "-" * 60


def _pedir_texto(etiqueta: str) -> str:
    """Pide un texto por consola (sin validar contenido, eso lo hace Pydantic)."""
    return input(f"{etiqueta}: ").strip()


def _pedir_categoria() -> str:
    """Muestra las categorías disponibles y pide una al usuario."""
    categorias = ", ".join(c.value for c in Categoria)
    print(f"Categorías disponibles: {categorias}")
    return input("Categoría: ").strip()


def _errores_legibles(error: ValidationError) -> str:
    """Convierte un ValidationError de Pydantic en texto legible en consola."""
    lineas = []
    for e in error.errors():
        campo = e["loc"][0] if e["loc"] else "campo"
        lineas.append(f"  - {campo}: {e['msg']}")
    return "\n".join(lineas)


def _mostrar_repuesto(r: Repuesto) -> None:
    """Imprime una fila con los datos de un repuesto en formato legible."""
    print(
        f"[{r.id}] {r.nombre} | {r.marca} | {r.modelo_auto} | {r.categoria} "
        f"| ${r.precio:.2f} | stock: {r.stock} "
        f"| ingreso: {r.fecha_ingreso:%Y-%m-%d %H:%M} "
        f"| modif: {r.fecha_modificado:%Y-%m-%d %H:%M}"
    )


def _mostrar_lista(repuestos: list[Repuesto]) -> None:
    """Imprime una lista de repuestos, o un aviso si está vacía."""
    if not repuestos:
        print("No hay repuestos para mostrar.")
        return
    for r in repuestos:
        _mostrar_repuesto(r)


def opcion_agregar() -> None:
    """Opción 2: solicita los datos de un repuesto nuevo y lo persiste."""
    print(SEPARADOR)
    print("Agregar repuesto nuevo")
    datos_crudos = {
        "nombre": _pedir_texto("Nombre"),
        "marca": _pedir_texto("Marca"),
        "modelo_auto": _pedir_texto("Modelo de auto"),
        "categoria": _pedir_categoria(),
        "precio": _pedir_texto("Precio"),
        "stock": _pedir_texto("Stock"),
    }
    try:
        repuesto = services.agregar_repuesto(datos_crudos)
    except ValidationError as error:
        print("No se pudo agregar el repuesto, revisá estos datos:")
        print(_errores_legibles(error))
        return
    print(f"Repuesto agregado correctamente con id {repuesto.id}.")


def opcion_listar() -> None:
    """Opción 3: lista todos los repuestos."""
    print(SEPARADOR)
    print("Listado de repuestos")
    _mostrar_lista(services.listar_repuestos())


def opcion_buscar() -> None:
    """Opción 4: busca repuestos por nombre o marca."""
    print(SEPARADOR)
    texto = _pedir_texto("Texto a buscar (nombre o marca)")
    if not texto:
        print("Debe ingresar un texto para buscar.")
        return
    resultados = services.buscar_repuestos(texto)
    print(f"Resultados encontrados: {len(resultados)}")
    _mostrar_lista(resultados)


def _pedir_id() -> int | None:
    """Pide un id por consola y lo convierte a entero. Devuelve None si no es válido."""
    texto_id = _pedir_texto("Id del repuesto")
    if not texto_id.isdigit():
        print("El id debe ser un número entero.")
        return None
    return int(texto_id)


def opcion_actualizar() -> None:
    """Opción 5: actualiza precio y/o stock de un repuesto existente."""
    print(SEPARADOR)
    print("Actualizar repuesto (solo precio y/o stock)")
    repuesto_id = _pedir_id()
    if repuesto_id is None:
        return

    print("Dejá vacío el campo que no querés modificar.")
    precio_texto = _pedir_texto("Nuevo precio (opcional)")
    stock_texto = _pedir_texto("Nuevo stock (opcional)")

    datos_crudos: dict[str, str] = {}
    if precio_texto:
        datos_crudos["precio"] = precio_texto
    if stock_texto:
        datos_crudos["stock"] = stock_texto

    try:
        repuesto = services.actualizar_repuesto(repuesto_id, datos_crudos)
    except ValidationError as error:
        print("No se pudo actualizar, revisá estos datos:")
        print(_errores_legibles(error))
        return
    except ValueError as error:
        print(f"No se pudo actualizar: {error}")
        return

    print("Repuesto actualizado correctamente:")
    _mostrar_repuesto(repuesto)


def opcion_eliminar() -> None:
    """Opción 6: elimina un repuesto, pidiendo confirmación antes de borrar."""
    print(SEPARADOR)
    print("Eliminar repuesto")
    repuesto_id = _pedir_id()
    if repuesto_id is None:
        return

    confirmacion = input(
        f"¿Confirmás que querés eliminar el repuesto id {repuesto_id}? (s/n): "
    ).strip().lower()
    if confirmacion != "s":
        print("Operación cancelada.")
        return

    try:
        repuesto = services.eliminar_repuesto(repuesto_id)
    except ValueError as error:
        print(f"No se pudo eliminar: {error}")
        return

    print(f"Repuesto '{repuesto.nombre}' (id {repuesto.id}) eliminado correctamente.")


def opcion_carga_masiva() -> None:
    """Opción 7: importa repuestos desde un archivo CSV."""
    print(SEPARADOR)
    print("Carga masiva desde CSV")
    ruta = _pedir_texto("Ruta del archivo CSV (ej: repuestos_seed.csv)")
    if not ruta:
        ruta = "repuestos_seed.csv"
        print(f"No se ingresó ruta, se usa por defecto: {ruta}")

    try:
        resultado = services.cargar_masivo_desde_csv(ruta)
    except (FileNotFoundError, ValueError) as error:
        print(f"No se pudo procesar la carga masiva: {error}")
        return

    print(f"Repuestos insertados correctamente: {resultado.insertados}")
    if resultado.errores:
        print(f"Filas con errores (no se insertaron): {len(resultado.errores)}")
        for err in resultado.errores:
            print(f"  - Fila {err.numero_fila}: {err.motivo}")
    else:
        print("No hubo filas con errores.")


def opcion_exportar() -> None:
    """Opción 8: exporta todos los repuestos a repuestos.csv."""
    print(SEPARADOR)
    cantidad = services.exportar_a_csv("repuestos.csv")
    print(f"Se exportaron {cantidad} repuestos a 'repuestos.csv'.")


def mostrar_menu() -> None:
    """Imprime las opciones del menú principal."""
    print(SEPARADOR)
    print("Sistema de gestión de repuestos automotrices")
    print(SEPARADOR)
    print("1. Ver este menú")
    print("2. Agregar repuesto")
    print("3. Listar repuestos")
    print("4. Buscar repuesto")
    print("5. Actualizar repuesto")
    print("6. Eliminar repuesto")
    print("7. Carga masiva desde CSV")
    print("8. Exportar a CSV")
    print("9. Salir")


ACCIONES = {
    "1": mostrar_menu,
    "2": opcion_agregar,
    "3": opcion_listar,
    "4": opcion_buscar,
    "5": opcion_actualizar,
    "6": opcion_eliminar,
    "7": opcion_carga_masiva,
    "8": opcion_exportar,
}


def ejecutar_menu() -> None:
    """Bucle principal del menú interactivo. Corre hasta que el usuario elige salir."""
    mostrar_menu()
    while True:
        opcion = input("\nElegí una opción (1-9): ").strip()

        if opcion == "9":
            print("¡Hasta luego!")
            break

        accion = ACCIONES.get(opcion)
        if accion is None:
            print("Opción inválida. Ingresá un número del 1 al 9.")
            continue

        try:
            accion()
        except Exception as error:  # protección extra: nunca romper el bucle del menú
            print(f"Ocurrió un error inesperado: {error}")

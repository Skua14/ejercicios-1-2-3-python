import json
import csv
from datetime import datetime
import os

inventario = []

archivo_json = "repuestos.json"

def generar_id():
    if not inventario:
        return 1
    return max(repuesto["id"] for repuesto in inventario) + 1


def agregar_repuesto():
    nombre = input("Nombre: ")
    marca = input("Marca: ")
    modelo = input("Modelo de auto: ")
    categoria = input("Categoría: ")

    while True:
        try:
            precio = float(input("Precio: "))
            if precio > 0:
                break
            print("El precio debe ser mayor a 0")
        except ValueError:
            print("Ingrese un número válido.")

    while True:
        try:
            stock = int(input("Stock: "))
            if stock >= 0:
                break
            print("El stock no puede ser negativo.")
        except ValueError:
            print("Ingrese un número válido.")

    fecha = datetime.now().isoformat()

    repuesto = {
        "id": generar_id(),
        "nombre": nombre,
        "marca": marca,
        "modelo_auto": modelo,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "fecha_ingreso": fecha,
        "fecha_modificado": fecha
    }

    inventario.append(repuesto)
    print("Repuesto agregado correctamente.")


def listar_repuestos():
    if not inventario:
        print("No hay repuestos cargados.")
        return

    for r in inventario:
        print("-" * 40)
        print("ID:", r["id"])
        print("Nombre:", r["nombre"])
        print("Marca:", r["marca"])
        print("Modelo:", r["modelo_auto"])
        print("Categoría:", r["categoria"])
        print("Precio:", r["precio"])
        print("Stock:", r["stock"])
        print("Fecha ingreso:", r["fecha_ingreso"])
        print("Fecha modificado:", r["fecha_modificado"])


def buscar_repuesto():
    texto = input("Buscar por nombre o marca: ").lower()

    encontrados = []

    for r in inventario:
        if texto in r["nombre"].lower() or texto in r["marca"].lower():
            encontrados.append(r)

    if not encontrados:
        print("No se encontraron resultados.")
        return

    for r in encontrados:
        print(f'ID: {r["id"]} - {r["nombre"]} - {r["marca"]}')


def actualizar_repuesto():
    try:
        id_buscar = int(input("Ingrese ID: "))
    except ValueError:
        print("ID inválido.")
        return

    for r in inventario:
        if r["id"] == id_buscar:

            while True:
                try:
                    precio = float(input("Nuevo precio: "))
                    if precio > 0:
                        break
                except ValueError:
                    pass
                print("Precio inválido.")

            while True:
                try:
                    stock = int(input("Nuevo stock: "))
                    if stock >= 0:
                        break
                except ValueError:
                    pass
                print("Stock inválido.")

            r["precio"] = precio
            r["stock"] = stock
            r["fecha_modificado"] = datetime.now().isoformat()

            print("Repuesto actualizado.")
            return

    print("Repuesto no encontrado.")


def eliminar_repuesto():
    try:
        id_buscar = int(input("Ingrese ID: "))
    except ValueError:
        print("ID inválido.")
        return

    for r in inventario:
        if r["id"] == id_buscar:
            confirmar = input("¿Eliminar? (S/N): ").upper()

            if confirmar == "S":
                inventario.remove(r)
                print("Repuesto eliminado.")
            else:
                print("Operación cancelada.")
            return

    print("Repuesto no encontrado.")


def guardar_json():
    ruta = os.path.abspath("repuestos.json")

    print("Se guardará en:")
    print(ruta)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)

    print("Datos guardados.")


def cargar_json():
    global inventario

    try:
        with open("repuestos.json", "r", encoding="utf-8") as archivo:
            inventario = json.load(archivo)
    except FileNotFoundError:
        inventario = []


def exportar_csv():
    with open("repuestos.csv", "w", newline="", encoding="utf-8") as archivo:
        campos = [
            "id",
            "nombre",
            "marca",
            "modelo_auto",
            "categoria",
            "precio",
            "stock",
            "fecha_ingreso",
            "fecha_modificado"
        ]

        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(inventario)

    print("CSV exportado correctamente.")


cargar_json()

while True:
    print("\n===== INVENTARIO =====")
    print("1. Agregar repuesto")
    print("2. Listar repuestos")
    print("3. Buscar repuesto")
    print("4. Actualizar repuesto")
    print("5. Eliminar repuesto")
    print("6. Guardar JSON")
    print("7. Exportar CSV")
    print("0. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregar_repuesto()
    elif opcion == "2":
        listar_repuestos()
    elif opcion == "3":
        buscar_repuesto()
    elif opcion == "4":
        actualizar_repuesto()
    elif opcion == "5":
        eliminar_repuesto()
    elif opcion == "6":
        guardar_json()
    elif opcion == "7":
        exportar_csv()
    elif opcion == "0":
        guardar_json()
        print("Programa finalizado.")
        break
    else:
        print("Opción inválida.")
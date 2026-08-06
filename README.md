# Sistema de gestión de repuestos automotrices

Aplicación de consola para administrar el inventario de una casa de
repuestos automotrices. Persiste los datos en SQLite mediante el ORM
**Peewee**, valida la información de entrada con **Pydantic** y permite
importar/exportar datos en formato CSV.

## Estructura del proyecto

```
repuestos/
├── main.py               # punto de entrada, arranca el menú
├── db.py                 # conexión y configuración de la base (Peewee)
├── models.py              # modelo Peewee (tabla Repuesto)
├── schemas.py              # modelos Pydantic (validación de entrada/salida)
├── repository.py           # funciones de acceso a datos (CRUD sobre Peewee)
├── services.py              # lógica de negocio (búsquedas, exportación, carga masiva)
├── cli/
│   ├── __init__.py
│   └── menu.py               # menú interactivo y manejo de entradas del usuario
├── repuestos_seed.csv         # archivo de ejemplo para probar la carga masiva
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.10 o superior (se usan type hints modernos como `int | None`)

## Instalación

1. Cloná el repositorio y entrá a la carpeta del proyecto:

   ```bash
   git clone <url-del-repositorio>
   cd repuestos
   ```

2. (Recomendado) Creá y activá un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # en Windows: venv\Scripts\activate
   ```

3. Instalá las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Cómo correr el programa

```bash
python main.py
```

Al iniciar, se crea automáticamente el archivo `repuestos.db` (SQLite) y la
tabla `repuesto` si todavía no existen. A partir de ahí, cada alta,
edición o borrado impacta directo en la base de datos.

## Uso del menú

```
1. Ver este menú
2. Agregar repuesto
3. Listar repuestos
4. Buscar repuesto
5. Actualizar repuesto
6. Eliminar repuesto
7. Carga masiva desde CSV
8. Exportar a CSV
9. Salir
```

- **Agregar repuesto**: pide nombre, marca, modelo de auto, categoría,
  precio y stock. Los datos se validan con el modelo Pydantic
  `RepuestoCreate` (precio > 0, stock >= 0, campos no vacíos) antes de
  guardarse. Si algo no es válido, se informa el motivo y no se persiste
  nada.
- **Actualizar repuesto**: se busca por `id` y solo se puede modificar
  precio y/o stock (el resto de los campos son fijos). Se valida con
  `RepuestoUpdate`. La fecha de modificación se actualiza automáticamente.
- **Eliminar repuesto**: pide el `id` y confirmación (`s`/`n`) antes de
  borrar.
- **Carga masiva desde CSV**: permite importar repuestos desde un archivo
  como `repuestos_seed.csv`. Cada fila se valida por separado con
  `RepuestoCreate`; las filas inválidas no interrumpen el proceso, se
  listan al final con el número de fila y el motivo del error. Las filas
  válidas se insertan todas juntas con `insert_many` dentro de una
  transacción.
- **Exportar a CSV**: genera `repuestos.csv` con todos los repuestos
  actuales de la base, incluyendo fila de encabezados.

## Categorías admitidas

`motor`, `frenos`, `suspension`, `electrico`, `carroceria`, `transmision`, `otro`

## Archivo de ejemplo para carga masiva

`repuestos_seed.csv` incluye filas válidas y también un par de filas
inválidas a propósito (precio vacío, stock negativo) para poder probar
que el sistema informa esos errores sin frenar la importación del resto.

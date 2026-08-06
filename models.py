"""
models.py

Definición del modelo de datos Peewee para la tabla `repuesto`.
Este módulo NO valida datos: la validación de entrada la hacen
los modelos Pydantic definidos en schemas.py. Acá solo se define
cómo se guardan los datos en la base.
"""

from datetime import datetime

from peewee import (
    Model,
    AutoField,
    CharField,
    FloatField,
    IntegerField,
    DateTimeField,
)

from db import database


class Repuesto(Model):
    """Representa un repuesto automotriz almacenado en la base de datos."""

    id = AutoField(primary_key=True)
    nombre = CharField(null=False)
    marca = CharField(null=False)
    modelo_auto = CharField(null=False)
    categoria = CharField(null=False)
    precio = FloatField(null=False)
    stock = IntegerField(null=False)
    fecha_ingreso = DateTimeField(null=False, default=datetime.now)
    fecha_modificado = DateTimeField(null=False, default=datetime.now)

    class Meta:
        database = database
        table_name = "repuesto"

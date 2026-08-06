"""
schemas.py

Modelos Pydantic usados para validar los datos que entran al sistema
(alta y actualización de repuestos) antes de persistirlos con Peewee.

Toda la validación de reglas de negocio simples (precio > 0, stock >= 0,
campos obligatorios no vacíos) vive acá. El resto de la aplicación
(menu.py, services.py) NO debe volver a validar "a mano" estos campos.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Categoria(str, Enum):
    """Categorías admitidas para un repuesto."""

    MOTOR = "motor"
    FRENOS = "frenos"
    SUSPENSION = "suspension"
    ELECTRICO = "electrico"
    CARROCERIA = "carroceria"
    TRANSMISION = "transmision"
    OTRO = "otro"


class RepuestoCreate(BaseModel):
    """
    Datos necesarios para dar de alta un repuesto.

    No incluye `id` (lo genera la base de datos) ni las fechas
    (las completa el sistema al momento de crear el registro).
    """

    nombre: str = Field(..., min_length=1, description="Nombre del repuesto")
    marca: str = Field(..., min_length=1, description="Marca del repuesto")
    modelo_auto: str = Field(..., min_length=1, description="Modelo de auto compatible")
    categoria: Categoria = Field(..., description="Categoría del repuesto")
    precio: float = Field(..., gt=0, description="Precio unitario, debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="Cantidad en stock, no puede ser negativa")

    @field_validator("nombre", "marca", "modelo_auto")
    @classmethod
    def no_vacio_tras_strip(cls, valor: str) -> str:
        """Evita que lleguen strings vacíos o solo con espacios."""
        valor_limpio = valor.strip()
        if not valor_limpio:
            raise ValueError("no puede estar vacío")
        return valor_limpio

    @field_validator("categoria", mode="before")
    @classmethod
    def normalizar_categoria(cls, valor: object) -> object:
        """Permite pasar la categoría en minúsculas/mayúsculas indistintamente."""
        if isinstance(valor, str):
            return valor.strip().lower()
        return valor


class RepuestoUpdate(BaseModel):
    """
    Datos permitidos para actualizar un repuesto ya existente.

    Según la consigna, lo único editable es precio y stock, y ambos
    son opcionales (se puede mandar solo uno de los dos).
    """

    precio: Optional[float] = Field(default=None, gt=0, description="Nuevo precio, mayor a 0")
    stock: Optional[int] = Field(default=None, ge=0, description="Nuevo stock, mayor o igual a 0")

    @field_validator("precio", "stock")
    @classmethod
    def al_menos_un_campo(cls, valor: object) -> object:
        # La validación de "al menos un campo informado" se hace aparte,
        # en services.py, porque Pydantic valida campo por campo y acá
        # no tenemos todavía el objeto completo armado.
        return valor


class RepuestoOut(BaseModel):
    """Representación de salida de un repuesto (para listar/mostrar)."""

    id: int
    nombre: str
    marca: str
    modelo_auto: str
    categoria: str
    precio: float
    stock: int
    fecha_ingreso: datetime
    fecha_modificado: datetime

    model_config = {"from_attributes": True}

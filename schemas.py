from datetime import datetime
from pydantic import BaseModel,Field

class Autorsc(BaseModel):
    nombre:str=Field(min_length=2,max_length=22)
    apellidoAutor:str=Field(min_length=2,max_length=22)
    pais:str=Field(min_length=2,max_length=30)


class Librosc(BaseModel):
    titulo:str=Field(min_length=2,max_length=40)
    autor: int
    editorial:str=Field(min_length=2,max_length=20)
    fecha_de_publicacion: datetime
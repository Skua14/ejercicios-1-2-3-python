#peewee autor libro con relacion foreingfield u backref
#crud con pydantic

from peewee import SqliteDatabase,DateField,ForeignKeyField, CharField,Field,Model
db="libreria.db"

plsql=SqliteDatabase(db,pragmas={"foreign_keys": 1})

class BaseModel(Model):
    class Meta:
        database=plsql

class Autor(BaseModel):
    nombre=CharField(max_length=22)
    apellidoAutor=CharField(max_length=22)
    pais=CharField(max_length=30)
    def __str__(self):
        return f"{self.apellidoAutor},{self.nombre}"

class Libro(BaseModel):
    titulo= CharField(max_length=40)
    autor= ForeignKeyField(Autor,backref="libros",on_delete="cascade")
    editorial=CharField(max_length=20)
    fecha_de_publicacion= DateField()

def db_init():
    with plsql:
        plsql.create_tables([Autor,Libro],safe=True)



db_init()


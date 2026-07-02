from modelos import Autor, Libro
from schemas import Autorsc,Librosc



def crear_autor(datos_autor:dict)-> Autor:
    autor_sc=Autorsc(**datos_autor)
    autor=Autor.create(**autor_sc.model_dump())
    return autor

def crear_libro(datos_libro: dict)-> Libro:
    libro_sc=Librosc(**datos_libro)
    try:
        autorp=Autor.get_by_id(libro_sc.autor)
    except:
        print("no existe el autor...") 

    schema_libro=libro_sc.model_dump(exclude={"autor"})
    libro=Libro.create(**schema_libro,autor=autorp)
    return libro

def listar_libros():
    
    for autor in Autor.select().prefetch(Libro):
        print(autor)
        for libro in autor.libros:
            print(libro.titulo)
    return
def buscarxid(id: int)-> Libro:

    libro= Libro.get_by_id(id)
    return libro

def buscar_libro_xtitulo(titulo:str)->list[Libro]:
    response=[]
    libros=Libro.select().where(Libro.titulo.contains(titulo))
    for libro in libros:
        response.append(libro)
    return response
def eliminar_autor(id: int):
    
    eliminar_autor= Autor.get_or_none(Autor.id==id)

    eliminar_autor.delete_instance()
    
    return eliminar_autor
    

listar_libros()

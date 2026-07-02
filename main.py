from crud import crear_autor,crear_libro,buscarxid,buscar_libro_xtitulo,eliminar_autor
from modelos import db_init
from datetime import date


def main():
    db_init()
    autoreli=eliminar_autor(14)
    print(autoreli)
    #nuevoautor()
    #nuevolibro()
    #crear usuario
    aut_obj={
        "nombre": "pepe", 
        "apellidoAutor":"loao",
       "pais":"Arg"}
    
    #autor=crear_autor(aut_obj)
    #print(autor)
    
    libro_obj={
        "titulo":"arda",
        "autor": 14,
        "editorial":"alras",
        "fecha_de_publicacion":date(2020, 5, 5)   }

    libro=crear_libro(libro_obj)
    print("libro:", libro)
    libros=buscar_libro_xtitulo("se")
    for libro in libros:
        print(libro.titulo)
if __name__== "__main__":

    main()
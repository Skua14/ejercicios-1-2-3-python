# Hacer una funcion que tome como argumento una lista de numeros y retorne el menor valor de la lista.


def menor(numeros: list) -> int:
    min_valor = numeros[0]

    for n in numeros:
        if n < min_valor:
            min_valor = n

    return min_valor


lista = [5, 7, 8, 9, 4]

resultado = menor(lista)

print("menor:", resultado)
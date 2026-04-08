# hacer una funcion que tome como argumento un str y retorne el caracter que mas veces aparec
# y la cantidad de veces
# "hola!!!"   --> !, 3
# 


def max_caracter(frase: str) -> tuple:
    max_letra = ""
    max_count = 0

    for letra in frase:
        count = frase.count(letra)
        if count > max_count:
            max_count = count
            max_letra = letra

    return max_letra, max_count


print(max_caracter("qwertyyyyyy"))
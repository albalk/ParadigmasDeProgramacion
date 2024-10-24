# Alba López Carruana

# Función palíndromos, que recibirá una lista de strings y nos devolverá
# una lista de True/False indicando cuales eran (o no) palíndromos. Para ello
# crearemos otra función es_palindromo que, a partir de un string, nos devuelva un
# booleano indicando si el string es palíndromo.

def es_palindromo(string: str) -> bool: # Devuelve True si es palindromo y False si no lo es
    return string == string[::-1]

def palindromos(lista: list) -> list: # Devuelve una lista de True/False indicando cuales son palíndromos y cuaales no
    return list(map(es_palindromo, lista))
    
if __name__ == "__main__":
    print(palindromos(["oso", "casa", "radar", "salas", "hola"]))
    print(palindromos(["loro", "ala", "reconocer", "salas", "caracola"]))
    print(palindromos(["rata", "anilina", "radar", "ana", "hola"]))
    print(palindromos(["caracol", "casa", "radar", "salas", "hola"]))
    print(palindromos(["oso", "casa", "tina", "salas", "hola"]))
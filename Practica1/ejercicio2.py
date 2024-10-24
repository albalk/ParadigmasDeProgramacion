# Alba López Carruana

# Función cuadrados_sumados que, a partir de un numero natural n
# devuelva la suma de los cuadrados de todos los números entre 1 y n

def cuadrados_sumados(n: int) -> int: # Devuelve la suma de los cuadrados
    return sum(map(lambda x: x**2, range(1, n+1)))

if __name__ == "__main__":
    print(cuadrados_sumados(5))
    print(cuadrados_sumados(3))
    print(cuadrados_sumados(8))
    print(cuadrados_sumados(10))
    print(cuadrados_sumados(4))
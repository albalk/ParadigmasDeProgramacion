# Alba López Carruana

# Función factorial que, tomando un numero como entrada, nos devuelva
# el factorial de ese número

def factorial(n: int) -> int: # Devuelve el factorial de un número
    return 1 if n == 0 else n * factorial(n-1)

if __name__ == "__main__":
    print(factorial(5))
    print(factorial(3))
    print(factorial(8))
    print(factorial(10))
    print(factorial(4))
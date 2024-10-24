# Alba López Carruana

# Tenemos una lista de estudiantes, donde cada estudiante tiene su
# nombre y una lista de calificaciones. Queremos filtrar a los estudiantes que tienen
# un promedio de calificaciones mayor o igual a 6 (nota mínima para aprobar).

def aprobados(estudiantes: list) -> list: # Devuelve una lista de nombres de estudiantes aprobados
                    # coge el nombre       # filtra por la media de las calificaciones >= 6
    return list(map(lambda x: x["nombre"], filter(lambda x: sum(x["calificaciones"]) / len(x["calificaciones"]) >= 6, estudiantes)))

if __name__ == "__main__":
    estudiantes1 = [
    {"nombre": "Juan", "calificaciones": [7, 6, 5]},
    {"nombre": "Ana", "calificaciones": [9, 6, 8]},
    {"nombre": "Pedro", "calificaciones": [4, 5, 3]},
    {"nombre": "Maria", "calificaciones": [10, 9, 9]},
    {"nombre": "Luis", "calificaciones": [3, 2, 5]}]
    print(aprobados(estudiantes1))

    estudiantes2 = [
    {"nombre": "Pepe", "calificaciones": [5, 6, 5]},
    {"nombre": "David", "calificaciones": [7, 6, 8]},
    {"nombre": "Laura", "calificaciones": [2, 5, 3]},
    {"nombre": "Marcos", "calificaciones": [8, 9, 9]},
    {"nombre": "Lara", "calificaciones": [1, 2, 5]}]
    print(aprobados(estudiantes2))

    estudiantes3 = [
    {"nombre": "Jaime", "calificaciones": [5, 8, 5]},
    {"nombre": "Alvaro", "calificaciones": [7, 8, 8]},
    {"nombre": "Paula", "calificaciones": [2, 7, 3]},
    {"nombre": "Mario", "calificaciones": [8, 9, 9]},
    {"nombre": "Lorena", "calificaciones": [1, 4, 5]}]
    print(aprobados(estudiantes3))

    estudiantes4 = [
    {"nombre": "Jorge", "calificaciones": [7, 8, 5]},
    {"nombre": "Anabel", "calificaciones": [9, 8, 8]},
    {"nombre": "Paco", "calificaciones": [4, 7, 3]},
    {"nombre": "Marisa", "calificaciones": [10, 9, 9]},
    {"nombre": "Leopoldo", "calificaciones": [3, 4, 5]}]
    print(aprobados(estudiantes4))

    estudiantes5 = [
    {"nombre": "Javier", "calificaciones": [9, 6, 7]},
    {"nombre": "Antonio", "calificaciones": [9, 6, 10]},
    {"nombre": "Pablo", "calificaciones": [6, 5, 5]},
    {"nombre": "Mariano", "calificaciones": [8, 9, 9]},
    {"nombre": "Lorenzo", "calificaciones": [5, 2, 7]}]
    print(aprobados(estudiantes5))
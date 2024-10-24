# Alba López Carruana

import requests
import hashlib
from passlib.hash import nthash
import json

def print_ok(mensaje):
    print(mensaje)

def print_error(mensaje):
    print(mensaje)

class GetCallback:
    def MakeGetRequest(self, url, onsuccess, onerror):   
        try:
            response = requests.get(url)
            if response.status_code == 200:
                onsuccess("Petición correcta")
                return response.text
            else: # Error de comunicación
                onerror()
        except: # Error de servidor
            onerror("Error en la petición")

# Hashear una contraseña en SHA1
def hash_password_sha1(password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    #print(sha1.hexdigest().upper())
    return sha1.hexdigest().upper()

# Hashear una contraseña en NTLM
def hash_password_ntlm(password):
    ntlm = nthash.hash(password)
    #print(ntlm.upper())
    return ntlm.upper()

def get_hash(funcion, password):
    return funcion(password)

def get_dominio(obj):
    domain = input("Introduce el dominio: ").strip()
    resultado = check_domain_breaches(obj, domain)
    print(f"Resultados para el dominio {domain}:")
    print(f"Se han filtrado {resultado} contraseñas\n")

def get_modo(obj, modo, get_hash, get_dominio):
    if modo == '1':
        hash_mode = input("Elige el formato de hash:\n\t[1] Sha1\n\t[2] Ntlm\n").strip()
        password = input("Introduce la contraseña: ").strip()
        if hash_mode == '1':
            hashed_password = get_hash(hash_password_sha1, password)
        elif hash_mode == '2':
            hashed_password = get_hash(hash_password_ntlm, password)
        else:
            print("Modo de hash no válido.")
            return
        hash_prefix = hashed_password[:5]
        resultado = check_password_pwned(obj, hash_prefix, hash_mode)
        print(f"Resultados para el prefijo {hash_prefix}:")
        print(resultado)
    elif modo == '2':
        get_dominio(obj)
    else:
        print("Modo de funcionamiento no válido.")


# Verificar si una contraseña ha sido comprometida
def check_password_pwned(obj, hash_prefix, modo):
    respuesta = obj.MakeGetRequest(f"https://api.pwnedpasswords.com/range/{hash_prefix}?mode={modo}", print_ok, print_error)
    url = f'https://api.pwnedpasswords.com/range/{hash_prefix}?mode={modo}'

    return respuesta

# Función para verificar si un dominio ha sido comprometido
# Solo funciona la petición para el dominio adobe.com
def check_domain_breaches(obj, domain):
    respuesta = json.loads(obj.MakeGetRequest(f"https://haveibeenpwned.com/api/v3/breaches?Domain={domain}", print_ok, print_error))
    num_pass_filtradas = respuesta[0]["PwnCount"] # Se extra el número de contraseñas filtradas
    return num_pass_filtradas

# Función principal
def proceso():
    obj = GetCallback()
    modo = input("Elige el modo:\n\t[1] Contraseñas\n\t[2] Dominios\n").strip()
    get_modo(obj, modo, get_hash, get_dominio)
    

if __name__ == "__main__":
    proceso()

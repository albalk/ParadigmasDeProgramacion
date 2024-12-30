from tkinter import Tk, Button, Entry, Label
from PIL import Image, ImageTk
from requests import get
import threading, json
from functools import partial

class Ventana:
    def __init__(self):
        self.window = Tk()
        self.window.title("PokeApi")

        self.mensaje = Label(text="Introduce el nombre del pokemon")
        self.mensaje.grid(row=0, column=0, padx=20, pady=20)

        self.entry = Entry()
        self.entry.grid(row=1, column=0, padx=20, pady=20)

        self.button = Button(text="Buscar Pokemon", command=self.buttonPressed)
        self.button.grid(row=2, column=0, padx=20, pady=20)

        self.nombre = Label(text="Nombre: \n")
        self.nombre.grid(row=3, column=0, padx=20, pady=20)

        self.tipo = Label(text="Tipo: \n")
        self.tipo.grid(row=4, column=0, padx=20, pady=20)

        self.altura = Label(text="Altura: \n")
        self.altura.grid(row=5, column=0, padx=20, pady=20)

        self.peso = Label(text="Peso: \n")
        self.peso.grid(row=6, column=0, padx=20, pady=20)

        self.window.mainloop()

    def buttonPressed(self):
        nombre_pokemon = self.read_entry()
        #print(nombre_pokemon)
        biuld_url(nombre_pokemon)
        make_get_request(biuld_url(nombre_pokemon), self.extract_data, self.print_error)


    def read_entry(self): # imprime el contenido escrito en el entry
        return self.entry.get()
    
    def update_info(self, data):

        self.nombre.config(text=(self.nombre.cget("text") + data.get('name')))
        self.tipo.config(text=(self.tipo.cget("text") + data.get('types')[0].get('type').get('name')))
        self.altura.config(text=(self.altura.cget("text") + str(data.get('height'))))
        self.peso.config(text=(self.peso.cget("text") + str(data.get('weight'))))

        self.generate_image(data.get('name'), data.get('sprites').get('front_default'))

    def generate_image(self, name, image_url):

        self.getImg(name, image_url)
        img = Image.open("name.jpg")
        img = img.resize((150, 150), Image.Resampling.NEAREST)
        

        self.imagen_tk = ImageTk.PhotoImage(img)
        self.imagen_label = Label(self.window, image=self.imagen_tk)
        # self.imagen_label.pack(pady=20)
        self.imagen_label.grid(row=7, column=0, padx=20, pady=20)

    def getImg(self, name, image_url):
        make_get_request(image_url, partial(self.saveImg, name), self.printError)
        

    def saveImg(title, data):
        print("imagen guardada")
        with open (f"{title}.jpg", "wb") as file:
            file.write(data)

    def extract_data(self, data):
        print('Petición correcta') 
        self.update_info(json.loads(data))

    def print_error():
        print('Error en la petición')


def make_get_request(url, onsuccess, onerror):
    response = get(url)

    if response.status_code == 200:
        onsuccess(response.content)
    else:
        onerror()

    return

def biuld_url(nombre_pokemon):  
    return f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"


if __name__ == "__main__":

    # Crear la ventana
    Ventana()


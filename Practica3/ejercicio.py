# Alba López Carruana

from tkinter import Tk, Button, Entry, Label, ttk, Listbox, END
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from rx.subject import Subject
import io, asyncio, aiohttp

img_subject = Subject()

class Ventana:
    def __init__(self):
        # Inicializa datos y configura la ventana principal
        self.img_data = []  # Almacena las imágenes descargadas
        self.window = Tk()
        self.window.title("Practica")

        # Configuración de la interfaz de usuario
        self.mensaje = Label(text="Url a procesar")
        self.mensaje.grid(row=0, column=0, padx=20, pady=20)

        self.entry = Entry()
        self.entry.grid(row=0, column=1, padx=20, pady=20)

        self.button = Button(text="     Buscar     ", command=self.button_pressed)
        self.button.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

        self.listbox = Listbox(self.window, height=10)  # Lista para mostrar los nombres de las imágenes
        self.listbox.grid(row=2, column=0, padx=20, pady=20)
        self.listbox.bind('<<ListboxSelect>>', self.mostrar_img)  # Evento para mostrar la imagen seleccionada

        self.img_label = Label(self.window)
        self.img_label.grid(row=2, column=1, padx=20, pady=20)

        self.progreso = ttk.Progressbar(self.window, orient="horizontal", length=200, mode="determinate")  # Barra de progreso
        self.progreso.grid(row=3, column=0, padx=20, pady=20, columnspan=3)

        self.contador_img = Label(text="Se encontraron 0 imágenes")
        self.contador_img.grid(row=4, column=0, padx=20, pady=20, columnspan=3)

        # Suscripción a eventos para actualizar la interfaz
        img_subject.subscribe(lambda img: self.actualizar_ventana(img))

        # Integrar asyncio con Tkinter para evitar interbloqueos
        self.window.after(100, self.tk_update)  # Actualización periódica de asyncio
        self.loop = asyncio.get_event_loop()
        self.window.mainloop()

    def tk_update(self):
        # Ejecuta tareas pendientes del bucle de asyncio y reprograma la llamada
        try:
            self.loop.run_until_complete(asyncio.sleep(0))
        except Exception as e:
            print(f"Error en bucle asyncio: {e}")
        finally:
            self.window.after(100, self.tk_update)

    def read_entry(self):
        # Lee el contenido del entry
        return self.entry.get()

    def button_pressed(self):
        # Obtiene la URL del entry
        input_url = self.read_entry()
        if not input_url:
            return
        if 'https://' not in input_url:  # Si la url no está completa
            input_url = self.build_url(input_url) # Se construye

        # Crea una corrutina para obtener imágenes
        asyncio.run_coroutine_threadsafe(self.obtener_img(input_url), self.loop)

    def build_url(self, url):
        # Añade el prefijo https
        return f"https://{url}"

    async def obtener_img(self, url):
        # Reinicia la interfaz y busca imágenes en la URL proporcionada
        self.contador_img.config(text="Se encontraron 0 imágenes")
        self.listbox.delete(0, END)
        self.img_data.clear()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"Error al obtener la página: {response.status}")
                        return
                    html = await response.text()

                    # Analiza el contenido html para obtener etiquetas <img>
                    soup = BeautifulSoup(html, 'html.parser')
                    img_tags = soup.find_all('img')
                    img_total = len(img_tags)
                    if not img_tags:
                        print("No se encontraron imágenes")
                        return

                    self.progreso['maximum'] = img_total + 1
                    # Crea tareas para descargar imágenes
                    tasks = [self.descargar_imagen(session, img) for img in img_tags]
                    await asyncio.gather(*tasks)
                    # Al terminar la barra esta al 100%
                    self.progreso['value'] = 100
        except Exception as e:
            print(e)

    async def descargar_imagen(self, session, img_tag):
        # Descarga una imagen de una etiqueta <img>
        img_url = img_tag.get('src')
        alt_name = img_tag.get('alt', 'sin_nombre')  # Obtiene el nombre (alt) de la imagen
        if not alt_name:
            alt_name = 'sin_nombre'
        if img_url:
            # Asegura que la URL sea válida
            if not img_url.startswith(('http://', 'https://')):
                img_url = self.build_url(img_url)
            try:
                async with session.get(img_url) as img_resp:
                    if img_resp.status == 200:
                        # Lee los bytes de la imagen y los almacena
                        img_bytes = await img_resp.read()
                        self.img_data.append((alt_name, img_bytes))
                        # Notifica que se ha descargado una imagen
                        img_subject.on_next((alt_name, len(self.img_data)))
            except Exception as e:
                print(f"Error descargando imagen {img_url}: {e}")

    def actualizar_ventana(self, img_info):
        # Actualiza la interfaz cuando se descarga una imagen
        alt_name, total_descargas = img_info
        self.listbox.insert(END, alt_name)  # Agrega el nombre de la imagen a la lista
        self.progreso.step(1)  # Avanza la barra de progreso
        self.contador_img.config(text=f"Se encontraron {total_descargas} imágenes")  # Actualiza el contador

    def mostrar_img(self, event):
        # Muestra la imagen seleccionada en la lista
        seleccion = self.listbox.curselection()
        if seleccion:
            name, img_bytes = self.img_data[seleccion[0]]
            img = Image.open(io.BytesIO(img_bytes))
            img = img.resize((150, 150))  # Redimensiona la imagen para la vista previa
            foto = ImageTk.PhotoImage(img)
            self.img_label.config(image=foto)
            self.img_label.image = foto

if __name__ == "__main__":
    Ventana()
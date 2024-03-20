#VisionArtificial/src/main.py
import cv2
import tkinter as tk
import sys
from PIL import Image, ImageTk
import image_processing

class VideoStreamApp:
    def __init__(self, root, default_video_url):
        self.root = root
        self.root.title("Visualización de la imagen procesada")
        self.default_video_url = default_video_url
        self.cap = None
        self.setup_ui()

    def setup_ui(self):
        self.panel = tk.Label(self.root)
        self.panel.pack(padx=10, pady=10)
        self.start_video_stream()  # Ahora este llamado será válido.

    def start_video_stream(self):
        if self.default_video_url.endswith('.jpg'):  # Si la URL es una imagen (modo de prueba)
            self.cap = cv2.imread(self.default_video_url)  # Usamos cv2.imread para cargar la imagen.
            self.show_frame(testing=True)  # Pasamos True para indicar modo de prueba.
        else:  # En caso contrario, asumimos que es una transmisión de video.
            self.cap = cv2.VideoCapture(self.default_video_url)  # Inicializamos VideoCapture con la URL.
            self.show_frame()  # Comenzamos el bucle de video normal.

    def show_frame(self, testing=False):
        if testing:
            frame = self.cap  # Aquí 'cap' es la imagen cargada, ya no necesitamos leer desde 'cap'.
            self.process_and_display_frame(frame, testing=True)
        else:
            ret, frame = self.cap.read()
            if ret:
                self.process_and_display_frame(frame)
            else:
                self.cap.release()

    def process_and_display_frame(self, frame, testing=False):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame = image_processing.process_image(frame)

        img = Image.fromarray(processed_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.panel.imgtk = imgtk  # Actualizar referencia a imgtk para evitar recolección de basura.
        self.panel.config(image=imgtk)
        if not testing:
            self.panel.after(10, self.show_frame)  # Solo reinicia el bucle si no está en modo 'testing'.

    def run(self):
        self.root.mainloop()

def manejar_menu():
    opcion = input("Seleccione una opción:\n0 - Testing\n1 - RTSP\n2 - HTTP (No disponible aún)\nOpción: ")
    if opcion == "0":
        print("Modo de calibración de reconocimiento de imagen activado.")
        return "C:/AppServ/www/VisionArtificial/tests/calibracion_deteccion_papel.jpg"  # Ruta a la imagen de prueba
    elif opcion == "1":
        return "rtsp://192.168.0.11:8080/h264.sdp"  # URL RTSP de la cámara
    elif opcion == "2":
        print("HTTP no está disponible aún.")
        return None
    else:
        print("Opción no válida.")
        sys.exit(1)


if __name__ == "__main__":
    default_video_url = "rtsp://192.168.0.11:8080/h264.sdp"
    manejar_menu()
    root = tk.Tk()
    app = VideoStreamApp(root, default_video_url)
    app.run()

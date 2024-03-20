#VisionArtificial/main_app.py
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
        self.entry = tk.Entry(self.root)
        self.entry.insert(0, self.default_video_url)
        self.entry.pack(padx=10, pady=10)

        start_button = tk.Button(self.root, text="Iniciar visualización", command=self.start_video_stream)
        start_button.pack(padx=10, pady=10)

        self.panel = tk.Label(self.root)
        self.panel.pack(padx=10, pady=10)
        self.start_video_stream()

    def start_video_stream(self):
        video_url = self.entry.get()
        self.cap = cv2.VideoCapture(video_url)
        self.show_frame()

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frame = image_processing.process_image(frame)

            img = Image.fromarray(processed_frame)
            img = ImageTk.PhotoImage(image=img)
            self.panel.img = img
            self.panel.config(image=img)
            self.panel.after(10, self.show_frame)
        else:
            self.cap.release()

    def run(self):
        self.root.mainloop()

def manejar_menu():
    opcion = input("Seleccione una opción:\n0 - Testing\n1 - RTSP\n2 - HTTP (No disponible aún)\nOpción: ")
    if opcion == "0":
        print("Seleccionaste 'Testing'.")
        # Aquí iría la lógica para el modo de calibración de reconocimiento de imagen.
    elif opcion == "1":
        print("Seleccionaste 'RTSP'.")
        # Esta es la funcionalidad actual, por lo que no necesitas cambiar nada aquí.
    elif opcion == "2":
        print("HTTP no está disponible aún.")
    else:
        print("Opción no válida.")
        sys.exit(1)


if __name__ == "__main__":
    manejar_menu()
    default_video_url = "rtsp://192.168.0.11:8080/h264.sdp"
    root = tk.Tk()
    app = VideoStreamApp(root, default_video_url)
    app.run()

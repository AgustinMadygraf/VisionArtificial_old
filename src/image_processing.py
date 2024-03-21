import cv2
import numpy as np
import sys

def rotar_imagen(frame, grados):
    """Rota la imagen un número específico de grados en sentido antihorario."""
    altura, ancho = frame.shape[:2]
    punto_central = (ancho // 2, altura // 2)
    matriz_rotacion = cv2.getRotationMatrix2D(punto_central, grados, 1.0)
    return cv2.warpAffine(frame, matriz_rotacion, (ancho, altura))

def calcular_promedio_gris(image):
    """Calcula el promedio de gris de la imagen."""
    return np.mean(image, axis=2).reshape((*image.shape[:2], 1))

def calcular_derivadas(array):
    """Calcula las derivadas del array."""
    left, mid, right = array[:-2], array[1:-1], array[2:]
    return 2 * mid - left - right

def encontrar_borde(frame):
    """Encuentra la posición del borde del papel y marca una línea amarilla."""
    grey_avg = calcular_promedio_gris(frame)
    mean = np.mean(grey_avg, axis=0).reshape(frame.shape[1])
    max_x = calcular_derivadas(mean).argmax()
    frame[:, max_x, :] = (255, 255, 0)  # Marca amarilla en la posición del borde
    return frame

def dibujar_reglas(frame, pixels_per_mm=4,altura=20):
    """Dibuja reglas métricas en la parte superior e inferior de la imagen, y una línea verde horizontal en el medio."""
    image_width = frame.shape[1]
    image_height = frame.shape[0]

    # Dibuja reglas en la parte superior e inferior de la imagen
    cv2.line(frame, (0, image_height - 30), (image_width, image_height - 30), (255, 0, 0), 2)
    cv2.line(frame, (0, 30), (image_width, 30), (255, 0, 0), 2)

    # Agrega marcas de milímetros a las reglas
    for mm in range(-10, 121, 10):
        x = (mm + 10) * pixels_per_mm
        cv2.line(frame, (x, image_height - 40), (x, image_height - 20), (0, 0, 255), 1)
        cv2.putText(frame, f"{mm} ", (x, image_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        cv2.line(frame, (x, 10), (x, 30), (0, 0, 255), 1)
        cv2.putText(frame, f"{mm} ", (x, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    # Calcula la posición media en el eje y y dibuja una línea verde horizontal
    mitad_altura = image_height // 2
    mitad_altura = mitad_altura + altura
    cv2.line(frame, (0, mitad_altura), (image_width, mitad_altura), (0, 255, 0), 2)


    return frame

def process_image(frame, grados):
    """Procesa la imagen aplicando rotación, las marcas de borde y reglas métricas."""
    if grados != 0:
        frame = rotar_imagen(frame, grados)
    frame = encontrar_borde(frame)
    frame = dibujar_reglas(frame)
    return frame

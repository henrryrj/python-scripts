import os
import shutil
import tkinter as tk
from tkinter import filedialog
import time

# Función para seleccionar la carpeta origen
def seleccionar_carpeta(titulo):
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    carpeta = filedialog.askdirectory(title=titulo)
    return carpeta

# Función para mover archivos y organizarlos en subcarpetas
def mover_archivos(carpeta_origen, carpeta_destino):
    # Definir extensiones por tipo de archivo
    extensiones = {
        'Imágenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
        'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
        'Música': ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
        'Documentos': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.odt', '.ods', '.odp', ],
        'Iso':['.iso'],
        'Comprimidos': ['.rar','.zip']
    }
    
    archivos = []
    carpetas_internas = []

    # Recorrer la carpeta de origen y buscar archivos
    for root, dirs, files in os.walk(carpeta_origen):
        # Evitar contar la carpeta origen
        if root != carpeta_origen:
            carpetas_internas.append(root)
        for file in files:
            if any(file.lower().endswith(ext) for exts in extensiones.values() for ext in exts):
                archivos.append(os.path.join(root, file))

    total_archivos = len(archivos)
    total_carpetas_internas = len(carpetas_internas)
    
    if total_archivos == 0:
        print(f"No se encontraron archivos en las {total_carpetas_internas} carpetas internas.")
        return

    simbolos = ['|', '/', '-', '\\']
    for i, archivo in enumerate(archivos):
        ruta_origen = archivo
        extension = os.path.splitext(archivo)[1].lower()
        
        # Determinar la carpeta de destino según la extensión
        carpeta_tipo = None
        for tipo, exts in extensiones.items():
            if extension in exts:
                carpeta_tipo = tipo
                break

        # Crear la subcarpeta si no existe
        carpeta_tipo_destino = os.path.join(carpeta_destino, carpeta_tipo)
        if not os.path.exists(carpeta_tipo_destino):
            os.makedirs(carpeta_tipo_destino)

        # Mover el archivo a la subcarpeta correspondiente
        ruta_destino = os.path.join(carpeta_tipo_destino, os.path.basename(archivo))
        shutil.move(ruta_origen, ruta_destino)
        
        simbolo = simbolos[i % len(simbolos)]
        porcentaje = (i + 1) / total_archivos * 100
        print(f'\rProcesando {simbolo} {porcentaje:.2f}% ({i + 1}/{total_archivos})', end='', flush=True)
        time.sleep(0.1)  # Pausa breve para mejorar la visibilidad del progreso

    print(f"\nProceso completado. Se movieron {total_archivos} archivos desde {total_carpetas_internas} carpetas internas.")

def main():
    carpeta_origen = seleccionar_carpeta("Selecciona la carpeta origen")
    carpeta_destino = seleccionar_carpeta("Selecciona la carpeta destino")
    
    # Mover archivos y organizarlos en subcarpetas en la carpeta de destino
    mover_archivos(carpeta_origen, carpeta_destino)

if __name__ == '__main__':
    main()

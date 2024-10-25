import tkinter as tk
from tkinter import filedialog, messagebox
from AFD import AFD

# Funciones de la interfaz gráfica
def cargar_archivo():
    global automata
    archivo = filedialog.askopenfilename(title="Seleccionar archivo XML", filetypes=[("XML files", "*.xml")])
    if archivo:
        try:
            automata = AFD(archivo)
            messagebox.showinfo("Archivo cargado", "El archivo XML se cargó correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

def analizar_cadena():
    if automata is None:
        messagebox.showwarning("Error", "Primero cargue un archivo XML.")
        return
    
    cadena = cadena_entry.get()
    if not cadena:
        messagebox.showwarning("Error", "Por favor, ingrese una cadena para analizar.")
        return

    resultado = automata.validar_cadena(cadena)
    resultado_label.config(text=resultado)

# Configuración de la ventana principal
automata = None
ventana = tk.Tk()
ventana.title("Simulador de Autómata Finito Determinista")

# Botón para cargar el archivo XML
cargar_button = tk.Button(ventana, text="Cargar archivo XML", command=cargar_archivo)
cargar_button.pack(pady=10)

# Campo de texto para ingresar la cadena
cadena_label = tk.Label(ventana, text="Ingrese una cadena:")
cadena_label.pack()
cadena_entry = tk.Entry(ventana, width=50)
cadena_entry.pack(pady=10)

# Botón para analizar la cadena
analizar_button = tk.Button(ventana, text="Analizar cadena", command=analizar_cadena)
analizar_button.pack(pady=10)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(ventana, text="", wraplength=400)
resultado_label.pack(pady=10)

# Ejecutar la interfaz gráfica
ventana.mainloop()

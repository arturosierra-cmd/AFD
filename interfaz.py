import tkinter as tk
from tkinter import filedialog, messagebox
from AFD import AFD  # Importa la clase AFD desde el archivo AFD.py


def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    posicion_x = int((pantalla_ancho / 2) - (ancho / 2))
    posicion_y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")

# Función para cargar archivo XML
def cargar_archivo():
    global automata
    archivo = filedialog.askopenfilename(title="Seleccionar archivo XML", filetypes=[("XML files", "*.xml")])
    if archivo:
        try:
            automata = AFD(archivo)
            messagebox.showinfo("Archivo cargado", "El archivo XML se cargó correctamente.")
            resultado_label.config(text="Archivo cargado exitosamente.")
            cadena_entry.config(state="normal")  # Habilita el ingreso de cadenas
            analizar_button.config(state="normal")  # Habilita el botón de analizar

            # Mostrar los detalles del autómata
            detalles_label.config(text=automata.mostrar_detalles())

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

# Función para analizar la cadena
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

# Función para limpiar los campos
def limpiar_campos():
    cadena_entry.delete(0, tk.END)  # Borra el contenido del campo de texto
    resultado_label.config(text="")  # Limpia el resultado

# Función para reiniciar la aplicación
def reiniciar_aplicacion():
    global automata
    automata = None
    limpiar_campos()  # Limpia los campos de entrada y resultado
    cadena_entry.config(state="disabled")  # Deshabilita el campo de cadena
    analizar_button.config(state="disabled")  # Deshabilita el botón de analizar
    resultado_label.config(text="Aplicación reiniciada. Cargue un archivo XML para continuar.")
    detalles_label.config(text="")  # Limpiar los detalles del autómata

# Interfaz gráfica con Tkinter
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Autómata Finito Determinista - GILBERTO ARTURO SIERRA 16-7372")

        # Dimensiones de la ventana
        self.ancho = 900
        self.alto = 600

        # Centrar la ventana en la pantalla
        centrar_ventana(self, self.ancho, self.alto)

        
        bg_izquierda = "#ffa500"  # Naranja
        bg_derecha = "#ffffff"    # Blanco 
        boton_color = "#007ACC"   # Azul
        boton_hover_color = "#005f9e"  
        boton_texto_color = "#ffffff" 
        limpiar_boton_color = "#007ACC"  

        # Sección izquierda
        izquierda_frame = tk.Frame(self, bg=bg_izquierda)
        izquierda_frame.place(relwidth=0.4, relheight=1)

        titulo_label = tk.Label(izquierda_frame, text="-Autómata Finito Determinista-", bg=bg_izquierda, fg='white', font=("Helvetica", 18, "bold"))
        titulo_label.pack(pady=40)

        descripcion_label = tk.Label(izquierda_frame, text="Instrucciones: Seleccione un archivo en formato XML para analizar cadenas con su Autómata Finito Determinista.",
                                     bg=bg_izquierda, fg='white', font=("Helvetica", 14), wraplength=250, justify="left")
        descripcion_label.pack(padx=20, pady=10)

        #Cargar archivo, ingresar cadena y botones
        derecha_frame = tk.Frame(self, bg=bg_derecha)
        derecha_frame.place(relwidth=0.6, relheight=1, relx=0.4)

        # Botón para cargar archivo XML
        cargar_button = tk.Button(derecha_frame, text="Cargar archivo XML", command=cargar_archivo, font=("Helvetica", 12), bg=boton_color, fg=boton_texto_color, bd=0, relief="flat")
        cargar_button.pack(pady=20)

        # Campo para ingresar la cadena
        cadena_label = tk.Label(derecha_frame, text="Ingrese una cadena:", bg=bg_derecha, font=("Helvetica", 12))
        cadena_label.pack()

        global cadena_entry
        cadena_entry = tk.Entry(derecha_frame, width=40, font=("Helvetica", 12), bd=2, relief="solid", state="disabled")
        cadena_entry.pack(pady=10)

        # Botón para analizar la cadena (verde con texto negro)
        global analizar_button
        analizar_button = tk.Button(derecha_frame, text="Analizar", command=analizar_cadena, font=("Helvetica", 14), bg=boton_color, fg=boton_texto_color, bd=0, relief="flat", state="disabled")
        analizar_button.pack(pady=10)

        # Botón para limpiar los campos
        limpiar_button = tk.Button(derecha_frame, text="Limpiar", command=limpiar_campos, font=("Helvetica", 12), bg=limpiar_boton_color, fg=boton_texto_color, bd=0, relief="flat")
        limpiar_button.pack(pady=10)

        # Botón para reiniciar la aplicación
        reiniciar_button = tk.Button(derecha_frame, text="Reiniciar y cargar otro XML", command=reiniciar_aplicacion, font=("Helvetica", 12), bg=limpiar_boton_color, fg=boton_texto_color, bd=0, relief="flat")
        reiniciar_button.pack(pady=10)

        # Etiqueta para mostrar el resultado del análisis
        global resultado_label
        resultado_label = tk.Label(derecha_frame, text="", bg=bg_derecha, font=("Helvetica", 12))
        resultado_label.pack(pady=20)

        # Etiqueta para mostrar los detalles del autómata
        global detalles_label
        detalles_label = tk.Label(derecha_frame, text="", bg=bg_derecha, font=("Helvetica", 10), justify="left")
        detalles_label.pack(pady=10)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()

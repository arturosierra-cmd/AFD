import tkinter as tk
from tkinter import filedialog, messagebox
from AFD import AFD

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    x_ventana = ventana.winfo_screenwidth() // 2 - ancho // 2
    y_ventana = ventana.winfo_screenheight() // 2 - alto // 2
    ventana.geometry(f"{ancho}x{alto}+{x_ventana}+{y_ventana}")

# Clase principal de la interfaz
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AFD - GILBERTO ARTURO SIERRA RAX 16-7372")
        self.ancho = 900
        self.alto = 450
        centrar_ventana(self, self.ancho, self.alto)

        self.automata = None  # Variable para almacenar el autómata cargado

        # Colores 
        bg_izquierda = "#FF9900"
        bg_derecha = "#FFFFFF"
        boton_color = "#007ACC"
        boton_hover_color = "#005C99"
        boton_texto_color = "#FFFFFF"
        entry_bg_color = "#F0F0F0"
        limpiar_boton_color = "#007ACC" 
        reiniciar_boton_color = "#007ACC" 

        # Sección izquierda
        izquierda_frame = tk.Frame(self, bg=bg_izquierda)
        izquierda_frame.grid(row=0, column=0, sticky="nsew")

        derecha_frame = tk.Frame(self, bg=bg_derecha)
        derecha_frame.grid(row=0, column=1, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        titulo_label = tk.Label(izquierda_frame, text="-Autómata Finito Determinista-", bg=bg_izquierda, fg='white', font=("Helvetica", 18, "bold"), justify="left")
        titulo_label.pack(pady=40, padx=20)

        descripcion_label = tk.Label(izquierda_frame, text="Instrucciones: Cargue un archivo en formato XML para analizar cadenas con su Autómata Finito Determinista.",
                                     bg=bg_izquierda, fg='white', font=("Helvetica", 14), wraplength=300, justify="left")
        descripcion_label.pack(padx=20, pady=10)

        #descripcion_label = tk.Label(izquierda_frame, text="Elaborado por: Gilberto Arturo Sierra Rax 16-7372.",
         #                            bg=bg_izquierda, fg='white', font=("Helvetica", 12), wraplength=300, justify="left")
       # descripcion_label.pack(padx=20, pady=10)

        # Botón para cargar el archivo XML
        self.cargar_button = tk.Button(derecha_frame, text="Cargar archivo XML", command=self.cargar_archivo, font=("Helvetica", 12), bg=boton_color, fg=boton_texto_color, bd=0, relief="flat")
        self.cargar_button.pack(pady=(50, 5))

        # Campo para ingresar la cadena
        token_label = tk.Label(derecha_frame, text="Ingrese una cadena:", bg=bg_derecha, font=("Helvetica", 12))
        token_label.pack(pady=(20, 5))

        self.cadena_entry = tk.Entry(derecha_frame, width=40, font=("Helvetica", 14), bg=entry_bg_color, bd=1, relief="flat")
        self.cadena_entry.pack(pady=10)

        # Botón para analizar la cadena
        self.analizar_button = tk.Button(derecha_frame, text="Analizar", command=self.analizar_cadena, font=("Helvetica", 14), bg=boton_color, fg=boton_texto_color, bd=0, relief="flat")
        self.analizar_button.pack(pady=20)

        # Botón para limpiar el campo y resultado
        self.limpiar_button = tk.Button(derecha_frame, text="Limpiar", command=self.limpiar_campos, font=("Helvetica", 12), bg=limpiar_boton_color, fg=boton_texto_color, bd=0, relief="flat")
        self.limpiar_button.pack(pady=10)

        # Botón para reiniciar la aplicación
        self.reiniciar_button = tk.Button(derecha_frame, text="Reiniciar y cargar otro XML", command=self.reiniciar_aplicacion, font=("Helvetica", 12), bg=reiniciar_boton_color, fg=boton_texto_color, bd=0, relief="flat")
        self.reiniciar_button.pack(pady=10)

        self.resultado_label = tk.Label(derecha_frame, text="", bg=bg_derecha, font=("Helvetica", 12), wraplength=300)
        self.resultado_label.pack(pady=20)

        # Hover effect en los botones
        self._hover_effect(self.cargar_button, boton_color, boton_hover_color)
        self._hover_effect(self.analizar_button, boton_color, boton_hover_color)
        self._hover_effect(self.limpiar_button, limpiar_boton_color, "#007ACC")  
        self._hover_effect(self.reiniciar_button, reiniciar_boton_color, "#007ACC")  

    # Función para cargar archivo XML
    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(title="Seleccionar archivo XML", filetypes=[("XML files", "*.xml")])
        if archivo:
            try:
                self.automata = AFD(archivo)
                messagebox.showinfo("Archivo cargado", "El archivo XML se cargó correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    # Función para analizar la cadena
    def analizar_cadena(self):
        if self.automata is None:
            messagebox.showwarning("Error", "Primero cargue un archivo XML.")
            return
        
        cadena = self.cadena_entry.get()
        if not cadena:
            messagebox.showwarning("Error", "Por favor, ingrese una cadena para analizar.")
            return

        resultado = self.automata.validar_cadena(cadena)
        self.resultado_label.config(text=resultado)

    # Función para limpiar los campos (mantiene el XML cargado)
    def limpiar_campos(self):
        self.cadena_entry.delete(0, tk.END)  # Borra el campo de texto
        self.resultado_label.config(text="")  # Limpia el resultado

    # Función para reiniciar la aplicación (cargar un nuevo XML)
    def reiniciar_aplicacion(self):
        self.automata = None  # Elimina el autómata cargado
        self.limpiar_campos()  # Limpia los campos de entrada y resultado
        messagebox.showinfo("Reiniciar", "Por favor, cargue un nuevo archivo XML.")

    # Hover effect en los botones
    def _hover_effect(self, widget, original_color, hover_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=original_color))

# Ejecutar la interfaz gráfica
if __name__ == "__main__":
    app = App()
    app.mainloop()

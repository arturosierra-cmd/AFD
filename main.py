from AFD import AFD

def main():
    print("### Autómata Finito Determinista ###")
    filename = 'automata.xml'  # Cambié para que busque el archivo automata.xml

    try:
        automata = AFD(filename)
    except Exception as e:
        print(f"Error al inicializar el AFD: {e}")
        return

    cadena_entrada = input("Ingrese una cadena de caracteres para validar: ")
    automata.validar_cadena(cadena_entrada)

if __name__ == "__main__":
    main()

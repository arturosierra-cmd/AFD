def main():
    print("### Autómata Finito Determinista ###")
    filename = input("Ingrese el nombre del archivo XML con la definición del autómata: ")

    try:
        automata = AFD(filename)
    except Exception as e:
        print(f"Error al inicializar el AFD: {e}")
        return
    
    cadena_entrada = input("Ingrese una cadena de caracteres para validar: ")
    automata.validar_cadena(cadena_entrada)

if __name__ == "__main__":
    main()
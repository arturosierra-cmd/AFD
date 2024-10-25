from AFD import AFD

def main():
    print("### Autómata Finito Determinista ###")
    filename = 'automata.xml'
    
    try:
        automaton = AFD(filename)
    except Exception as e:
        print(f"Error initializing AFD: {e}")
        return
    
    input_string = input("Ingrese una cadena de caracteres para validar: ")
    automaton.validate_string(input_string)

if __name__ == "__main__":
    main()

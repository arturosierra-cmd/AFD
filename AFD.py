import xml.etree.ElementTree as ET

class AutomatonError(Exception):
    """Clase para manejar errores personalizados del autómata."""
    pass

class AFD:
    def __init__(self, filename):
        """Inicializa el AFD con los elementos principales."""
        self.states = set()
        self.alphabet = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}
        self._load_automaton(filename)

    def _load_automaton(self, filename):
        """Carga el autómata desde un archivo XML."""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            # Cargar alfabeto
            for symbol in root.find('ALFABETO'):
                self._validate_symbol(symbol.text)
                self.alphabet.add(symbol.text)

            # Cargar estados
            for state in root.find('ESTADO'):
                self.states.add(self._validate_state(state.text))

            # Cargar estado inicial
            self.initial_state = self._validate_state(root.find('INICIAL').text)

            # Cargar estados finales
            for final in root.find('FINAL'):
                self.final_states.add(self._validate_state(final.text))

            # Cargar transiciones
            for transition in root.find('TRANSICIONES'):
                self._load_transition(transition.text)

        except ET.ParseError:
            raise AutomatonError("Error parsing the XML file")
        except Exception as e:
            raise AutomatonError(f"Error loading automaton: {str(e)}")

    def _validate_symbol(self, symbol):
        """Valida los símbolos del alfabeto."""
        if not symbol.isalnum():
            raise AutomatonError(f"Invalid symbol in alphabet: {symbol}")
        return symbol

    def _validate_state(self, state):
        """Valida que los estados sean números enteros."""
        if not state.isdigit():
            raise AutomatonError(f"Invalid state: {state}")
        return int(state)

    def _load_transition(self, transition_str):
        """Carga una transición desde una cadena."""
        n, a, m = transition_str.split(',')
        n, m = self._validate_state(n), self._validate_state(m)
        a = self._validate_symbol(a)

        if (n, a) in self.transitions:
            raise AutomatonError(f"Multiple transitions detected for state {n} with symbol {a}")
        self.transitions[(n, a)] = m

    def validate_string(self, input_string):
        """Valida si una cadena es aceptada por el autómata."""
        current_state = self.initial_state
        trace = [current_state]

        for symbol in input_string:
            if symbol not in self.alphabet:
                print(f"Error: symbol '{symbol}' not in alphabet")
                return False
            if (current_state, symbol) not in self.transitions:
                print(f"Error: no transition for symbol '{symbol}' from state {current_state}")
                return False
            current_state = self.transitions[(current_state, symbol)]
            trace.append(current_state)

        if current_state in self.final_states:
            print(f"String accepted. Trace: {trace}")
            return True
        else:
            print(f"String rejected. Trace: {trace}")
            return False

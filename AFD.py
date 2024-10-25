import xml.etree.ElementTree as ET

class ErrorAutomata(Exception):
    """Clase para manejar errores del autómata."""
    pass

class AFD:
    def __init__(self, filename):
        """Inicializa el AFD con los elementos del archivo XML."""
        self.states = set()
        self.alphabet = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}
        self.valid_symbols = set('abcdefghijklmnopqrstuvwxyz0123456789')
        self._cargar_automata_xml(filename)

    def _cargar_automata_xml(self, filename):
        """Carga el autómata desde un archivo XML."""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            # Cargar alfabeto
            for symbol in root.find('ALFABETO'):
                self._validar_simbolo(symbol.text)
                self.alphabet.add(symbol.text)

            # Cargar estados
            for state in root.find('ESTADO'):
                self.states.add(self._validar_estado(state.text))

            # Cargar estado inicial
            self.initial_state = self._validar_estado(root.find('INICIAL').text)

            # Cargar estados finales
            for final in root.find('FINAL'):
                self.final_states.add(self._validar_estado(final.text))

            # Cargar transiciones
            for transition in root.find('TRANSICIONES'):
                self._cargar_transicion(transition.text)

        except ET.ParseError:
            raise ErrorAutomata("Error al procesar el archivo XML")
        except Exception as e:
            raise ErrorAutomata(f"Error cargando el autómata: {str(e)}")

    def _validar_simbolo(self, symbol):
        """Valida que el símbolo pertenezca al alfabeto [a-z0-9]."""
        if symbol not in self.valid_symbols:
            raise ErrorAutomata(f"Símbolo inválido en el alfabeto: {symbol}")
        return symbol

    def _validar_estado(self, state):
        """Valida que los estados sean números enteros."""
        if not state.isdigit():
            raise ErrorAutomata(f"Estado inválido: {state}")
        return int(state)

    def _cargar_transicion(self, transition_str):
        """Carga una transición desde una línea."""
        n, a, m = transition_str.split(',')
        n, m = self._validar_estado(n), self._validar_estado(m)
        a = self._validar_simbolo(a)

        # Verificar si ya existe una transición con el mismo símbolo desde el estado n
        if (n, a) in self.transitions:
            raise ErrorAutomata(f"Transición duplicada para el estado {n} con el símbolo {a}")
        self.transitions[(n, a)] = m
        self.states.update([n, m])

    def validar_cadena(self, cadena_entrada):
        """Valida si una cadena es aceptada por el autómata."""
        estado_actual = self.initial_state
        trazabilidad = [estado_actual]

        for simbolo in cadena_entrada:
            if simbolo not in self.alphabet:
                return f"Error: el símbolo '{simbolo}' no está en el alfabeto"
            if (estado_actual, simbolo) not in self.transitions:
                return f"Error: no existe transición para el símbolo '{simbolo}' desde el estado {estado_actual}"
            estado_actual = self.transitions[(estado_actual, simbolo)]
            trazabilidad.append(estado_actual)

        if estado_actual in self.final_states:
            return f"Cadena aceptada. Trazabilidad: {trazabilidad}"
        else:
            return f"Cadena rechazada. Trazabilidad: {trazabilidad}"

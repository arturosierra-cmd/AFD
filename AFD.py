import xml.etree.ElementTree as ET  

# Clase para representar el autómata finito determinista
class AFD:
    def __init__(self, filename):
        self.states = set()
        self.alphabet = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}
        self._cargar_automata(filename)

    def _cargar_automata(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()

        # Cargar alfabeto (Σ)
        for symbol in root.find('ALFABETO'):
            self.alphabet.add(symbol.text)

        # Cargar estados (Q)
        for state in root.find('ESTADO'):
            self.states.add(state.text)

        # Cargar estado inicial (q₀)
        self.initial_state = root.find('INICIAL').text

        # Cargar estados finales (F)
        for final_state in root.find('FINAL'):
            self.final_states.add(final_state.text)

        # Cargar transiciones (δ)
        for transition in root.find('TRANSICIONES'):
            src, symbol, dst = transition.text.split(',')
            if (src, symbol) not in self.transitions:
                self.transitions[(src, symbol)] = dst
            else:
                raise ValueError(f"Transición duplicada para el estado {src} con el símbolo {symbol}")

    # Método para validar la cadena
    def validar_cadena(self, cadena):
        estado_actual = self.initial_state
        trazabilidad = [estado_actual]

        for simbolo in cadena:
            if simbolo not in self.alphabet:
                return f"Error: símbolo '{simbolo}' no pertenece al alfabeto."

            clave = (estado_actual, simbolo)
            if clave in self.transitions:
                estado_actual = self.transitions[clave]
                trazabilidad.append(estado_actual)
            else:
                return f"Error: no existe transición para el símbolo '{simbolo}' desde el estado {estado_actual}"

        if estado_actual in self.final_states:
            return f"Cadena aceptada.\nTrazabilidad: {trazabilidad}"
        else:
            return f"Cadena no aceptada.\nTrazabilidad: {trazabilidad}"

    # Método para mostrar los detalles del autómata
    def mostrar_detalles(self):
        detalles = f"""
        Q (Conjunto de estados): {self.states}
        Σ (Alfabeto): {self.alphabet}
        δ (Transiciones): {self.transitions}
        q₀ (Estado inicial): {self.initial_state}
        F (Estados finales): {self.final_states}
        """
        return detalles

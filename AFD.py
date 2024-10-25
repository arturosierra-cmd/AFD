class ErrorAutomata(Exception):
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
        self.valid_symbols = set('abcdefghijklmnopqrstuvwxyz0123456789')
        self._cargar_automata(filename)

    def _cargar_automata(self, filename):
        """Carga el autómata desde un archivo de texto plano."""
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith('ESTADO_INICIAL'):
                        # Estado inicial está definido como: ESTADO_INICIAL=n
                        self.initial_state = self._validar_estado(line.split('=')[1])
                    elif line.startswith('ESTADOS_FINALES'):
                        # Estados finales: ESTADOS_FINALES=1,2
                        finales = line.split('=')[1].split(',')
                        self.final_states.update(self._validar_estado(f) for f in finales)
                    elif ',' in line:
                        # Transiciones codificadas como: n,a,m
                        self._cargar_transicion(line)
                    else:
                        raise ErrorAutomata(f"Línea inválida en el archivo del autómata: {line}")

        except Exception as e:
            raise ErrorAutomata(f"Error cargando el autómata: {str(e)}")

    def _validar_simbolo(self, symbol):
        """Valida que el símbolo pertenezca al alfabeto válido [a-z0-9]."""
        if symbol not in self.valid_symbols:
            raise ErrorAutomata(f"Símbolo inválido en el alfabeto: {symbol}")
        return symbol

    def _validar_estado(self, state):
        """Valida que los estados sean números enteros."""
        if not state.isdigit():
            raise ErrorAutomata(f"Estado inválido: {state}")
        return int(state)

    def _cargar_transicion(self, transicion_str):
        """Carga una transición desde una línea de texto."""
        n, a, m = transicion_str.split(',')
        n, m = self._validar_estado(n), self._validar_estado(m)
        a = self._validar_simbolo(a)

        # Verificar si ya existe una transición con el mismo símbolo desde el estado n
        if (n, a) in self.transitions:
            raise ErrorAutomata(f"Transiciones múltiples detectadas para el estado {n} con el símbolo {a}")
        self.transitions[(n, a)] = m
        self.states.update([n, m])
        self.alphabet.add(a)

    def validar_cadena(self, cadena_entrada):
        """Valida si una cadena es aceptada por el autómata."""
        estado_actual = self.initial_state
        trazabilidad = [estado_actual]

        for simbolo in cadena_entrada:
            if simbolo not in self.alphabet:
                print(f"Error: el símbolo '{simbolo}' no está en el alfabeto")
                return False
            if (estado_actual, simbolo) not in self.transitions:
                print(f"Error: no existe transición para el símbolo '{simbolo}' desde el estado {estado_actual}")
                return False
            estado_actual = self.transitions[(estado_actual, simbolo)]
            trazabilidad.append(estado_actual)

        if estado_actual in self.final_states:
            print(f"Cadena aceptada. Trazabilidad: {trazabilidad}")
            return True
        else:
            print(f"Cadena rechazada. Trazabilidad: {trazabilidad}")
            return False

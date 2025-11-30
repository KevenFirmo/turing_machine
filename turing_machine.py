class TuringMachine:
    def __init__(self, states, alphabet, tape_alphabet, transitions, start_state, accept_state, reject_state, blank_symbol='B'):
        # Componentes formais da MT
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = set(tape_alphabet)  # Usamos um Set para validação rápida
        self.transitions = transitions  # Dicionário da Função de Transição: (q, X) -> (q', Y, D)
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

        # Variáveis de Simulação (serão redefinidas em initialize_tape)
        self.tape = {}
        self.head_position = 0
        self.current_state = self.start_state
        self.is_running = False

    # ------------------------------------
    # Fita e Inicialização
    # ------------------------------------

    def _validate_input_tape(self, input_string):
        """Verifica se a fita de entrada contém apenas símbolos do Alfabeto da Fita (Γ)."""
        # Note que a string de entrada não deve conter o blank_symbol, apenas o alfabeto de entrada
        for symbol in input_string:
            if symbol not in self.tape_alphabet or symbol == self.blank_symbol:
                raise ValueError(
                    f"Símbolo inválido '{symbol}' encontrado na fita. "
                    f"O alfabeto de fita (Γ) aceita apenas: {self.tape_alphabet} (exceto o branco)."
                )

    def initialize_tape(self, input_string):
        """Inicializa a fita com a string de entrada."""
        # A fita é um dicionário que armazena apenas símbolos não-brancos
        self.tape = {i: symbol for i, symbol in enumerate(input_string)}
        self.head_position = 0
        self.current_state = self.start_state
        self.is_running = True
        print(f"--- Fita inicializada: {self.get_tape_string()} (Estado inicial: {self.start_state}) ---")

    def get_tape_symbol(self):
        """Lê o símbolo na posição atual da cabeça."""
        # Se a posição não está no dicionário (fora da entrada original), é o símbolo branco
        return self.tape.get(self.head_position, self.blank_symbol)

    def write_tape_symbol(self, symbol):
        """Escreve um símbolo na posição atual da cabeça."""
        # Se o símbolo a ser escrito é o símbolo branco, ele é omitido do dicionário (limpa o espaço)
        if symbol == self.blank_symbol:
            if self.head_position in self.tape:
                del self.tape[self.head_position]
        else:
            self.tape[self.head_position] = symbol

    def move_head(self, direction):
        """Move a cabeça de leitura/escrita."""
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        # 'P' ou qualquer outra coisa: permanece na posição

    def get_tape_string(self):
        """Retorna uma representação legível da fita."""
        # Otimizado para fita infinita baseada em dicionário
        
        # Encontra as extremidades da fita onde há símbolos não-brancos
        keys = self.tape.keys()
        min_pos = min(keys) if keys else 0
        max_pos = max(keys) if keys else -1

        # Expande a visualização para garantir que o 'B' ao redor da cabeça seja visto
        start = min(min_pos, self.head_position) - 3
        end = max(max_pos, self.head_position) + 3

        display_string = []
        for i in range(start, end + 1):
            symbol = self.tape.get(i, self.blank_symbol)
            if i == self.head_position:
                # Indica a posição da cabeça com colchetes e negrito
                display_string.append(f"**[{symbol}]**")
            else:
                display_string.append(symbol)

        return "".join(display_string)

    # ------------------------------------
    # Simulação Principal
    # ------------------------------------

    def run_step(self):
        """Função de Transição: Executa um único passo da Máquina de Turing."""
        if not self.is_running:
            return False

        # 1. Leitura do Símbolo
        read_symbol = self.get_tape_symbol()
        transition_key = (self.current_state, read_symbol)

        # 2. Execução da Transição
        if transition_key in self.transitions:
            next_state, write_symbol, direction = self.transitions[transition_key]

            # 🛑 REGISTRO DO PASSO ANTES DA EXECUÇÃO
            # O estado impresso é o estado ATUAL da MT antes da mudança
            print(f"Passo: {self.current_state}, {read_symbol} -> {next_state}, {write_symbol}, {direction}")
            
            # 3. Escrita do Símbolo
            self.write_tape_symbol(write_symbol)

            # 4. Movimento da Cabeça
            self.move_head(direction)

            # 5. Mudança de Estado
            self.current_state = next_state
            
            # 6. Verificação de Parada
            if self.current_state in {self.accept_state, self.reject_state}:
                self.is_running = False
                return False  # Indica que a MT parou

            return True  # Indica que a MT continua
        else:
            # Não há transição definida: MT "morre" (Rejeita)
            print(f"❌ Erro: Transição não definida para {transition_key}. Rejeitando.")
            self.current_state = self.reject_state
            self.is_running = False
            return False

    def run(self, input_string):
        """Simulação Completa: Executa a MT até atingir o estado de aceitação ou rejeição."""
        
        # Validação do alfabeto antes de iniciar (para evitar erros de inicialização)
        try:
            self._validate_input_tape(input_string)
        except ValueError as e:
            print(f"❌ REJEITADO (Erro de Alfabeto): {e}")
            return False

        self.initialize_tape(input_string)

        step_count = 0
        while self.is_running:
            if not self.run_step():
                break
            step_count += 1
            
            # 💡 Proteção contra loops infinitos (limite de passos)
            if step_count > 500:
                print("\n⚠️ Limite de 500 passos atingido. Parada de emergência (Loop Infinito?).")
                self.current_state = self.reject_state
                break

        print("\n--- Simulação Concluída ---")
        if self.current_state == self.accept_state:
            print(f"✅ Aceito! (Estado final: {self.accept_state})")
        elif self.current_state == self.reject_state:
            print(f"❌ Rejeitado! (Estado final: {self.reject_state})")
        else:
            print(f"🛑 Parada Inesperada. Estado final: {self.current_state}")
            
        print(f"Fita final: {self.get_tape_string()}")
        return self.current_state == self.accept_state
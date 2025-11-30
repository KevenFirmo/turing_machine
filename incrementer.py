# machines/generic_incrementer.py

def create_incrementer_config(user_alphabet):
  
    
    # Validação básica
    if len(user_alphabet) < 2:
        raise ValueError("O alfabeto precisa de pelo menos 2 símbolos para um sistema posicional.")

    symbols = list(user_alphabet)
    first_sym = symbols[0]   # Ex: '0'
    second_sym = symbols[1]  # Ex: '1' (usado para criar novos dígitos, como 9 -> 10)
    last_sym = symbols[-1]   # Ex: '9' (o que causa o 'vai um')
    
    transitions = {}

    # --- FASE 1: Ir para o final da fita (direita) ---
    # Para qualquer símbolo conhecido, move para a direita
    for char in symbols:
        transitions[('q_start', char)] = ('q_move_right', char, 'R')
        transitions[('q_move_right', char)] = ('q_move_right', char, 'R')

    # Se a fita estiver vazia ou chegar ao fim
    # Caso especial: Entrada vazia vira "1" (ou segundo simbolo)
    transitions[('q_start', 'B')] = ('q_accept', second_sym, 'P') 
    # Chegou no fim da string, começa a voltar para incrementar
    transitions[('q_move_right', 'B')] = ('q_increment', 'B', 'L') 

    # --- FASE 2: Incrementar (Lógica do "Vai Um") ---
    for i, char in enumerate(symbols):
        if char == last_sym:
            # CASO DE OVERFLOW (Ex: 9 -> 0 e vai para esquerda)
            # Regra: Se ler o último, escreve o primeiro e move Left (continue no estado q_increment)
            transitions[('q_increment', char)] = ('q_increment', first_sym, 'L')
        else:
            # CASO NORMAL (Ex: 3 -> 4)
            # Regra: Se ler X, escreve X+1 e Para (Aceita)
            next_char = symbols[i + 1]
            transitions[('q_increment', char)] = ('q_accept', next_char, 'P')

    # CASO DE EXPANSÃO (Ex: 99 -> 100)
    # Se estamos carregando um "vai um" e batemos no branco à esquerda
    transitions[('q_increment', 'B')] = ('q_accept', second_sym, 'P')

    # Configuração final
    return {
        'states': {'q_start', 'q_move_right', 'q_increment', 'q_accept', 'q_reject'},
        'alphabet': set(symbols),
        'tape_alphabet': set(symbols) | {'B'},
        'transitions': transitions,
        'start_state': 'q_start',
        'accept_state': 'q_accept',
        'reject_state': 'q_reject',
        'blank_symbol': 'B'
    }
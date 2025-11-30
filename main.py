import sys
# AJUSTE 1: Imports simplificados (assumindo que tudo está na mesma pasta)
from turing_machine import TuringMachine
from incrementer import create_incrementer_config

def load_config_and_tapes(filepath):
    tapes = []
    alphabet_line = None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                content = line.strip()
                # Ignora linhas vazias e comentários
                if not content or content.startswith('#'):
                    continue
                
                if alphabet_line is None:
                    # A primeira linha não-vazia é o Alfabeto
                    # .replace(" ", "") garante que "0 1" vire "01" se o usuário usar espaços
                    alphabet_line = content.replace(" ", "") 
                else:
                    tapes.append(content)
                    
    except FileNotFoundError:
        print(f"❌ Erro: Crie o arquivo '{filepath}' na mesma pasta do script.")
        sys.exit(1)
        
    if alphabet_line is None:
        print(f"❌ Erro: O arquivo '{filepath}' está vazio.")
        sys.exit(1)

    return alphabet_line, tapes

def main():
    filename = "fitas.txt"
    
    # 1. Carregar Alfabeto e Fitas
    print(f"--- Carregando '{filename}' ---")
    user_alphabet, tape_inputs = load_config_and_tapes(filename)

    print(f"🔤 Alfabeto Dinâmico: {user_alphabet}")
    print(f"📼 Fitas para processar: {len(tape_inputs)}")
    
    # 2. Gerar a Configuração baseada no Alfabeto lido
    try:
        config = create_incrementer_config(user_alphabet)
        # Instancia a MT
        mt = TuringMachine(**config)
    except ValueError as e:
        print(f"\n❌ Erro na configuração: {e}")
        return

    # 3. Executar processamento
    for i, tape_input in enumerate(tape_inputs):
        print(f"\n=============================================")
        print(f"▶️  TESTE {i+1}: Entrada '{tape_input}'")
        
        # A função run já faz a validação e reset da fita interna
        success = mt.run(tape_input)
        
        # O estado interno da MT persiste, então resetamos o estado lógico para garantir
        mt.current_state = mt.start_state
        mt.is_running = False

if __name__ == "__main__":
    main()
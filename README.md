Documentação Técnica: Simulador de Máquina de Turing Universal
1. Visão Geral do Projeto
Este projeto consiste na implementação de um Simulador de Máquina de Turing Determinística (MT) em Python. O objetivo principal é demonstrar a capacidade de processamento de algoritmos baseados em autômatos finitos com memória em fita infinita.
Como caso de uso principal, o sistema implementa um Incrementador Universal (Sucessor). Diferente de implementações estáticas, este software é capaz de ler um alfabeto arbitrário definido pelo usuário (Binário, Decimal, Hexadecimal, Base-36, etc.) e aplicar a lógica de soma aritmética (n+1) adaptada dinamicamente a esse alfabeto.
2. Estrutura do Projeto
O código foi modularizado para separar o motor de execução da lógica de configuração.
2.1 Arquivos e Responsabilidades
turing_machine.py (O Motor): Contém a classe TuringMachine. É o núcleo genérico que não possui conhecimento sobre "números" ou "soma". Ele apenas executa transições baseadas em estados, leitura e escrita.
incrementer.py (A Lógica): Responsável por gerar a tabela de transições (δ) dinamicamente. Ele analisa o alfabeto fornecido e cria as regras de estado para navegar até o fim da fita e realizar o "vai-um" (carry) na volta.
main.py (O Controlador): Gerencia a entrada/saída (I/O). Lê o arquivo de configuração, valida os dados, instancia a máquina e exibe os resultados passo a passo.
fitas.txt (A Entrada): Arquivo de texto onde a primeira linha define o alfabeto e as linhas subsequentes contêm as entradas a serem processadas.
3. Definição Formal e Implementação
A implementação segue rigorosamente a definição matemática de uma Máquina de Turing M=(Q,Σ,Γ,δ,q0​,qaceita​,qrejeita​).
Componente Teórico
Representação no Código (Python)
Detalhes de Implementação
Fita (Γ)
self.tape = {}
Implementada como um Dicionário (Hash Map). Isso permite uma fita virtualmente infinita (índices negativos e positivos) sem alocação prévia de memória.
Estados (Q)
self.states
Conjunto de strings (ex: 'q_move_right', 'q_increment').
Alfabeto (Σ)
self.alphabet
Lista de caracteres lida da 1ª linha de fitas.txt.
Transição (δ)
self.transitions
Dicionário onde a chave é (estado_atual, simbolo_lido) e o valor é (novo_estado, simbolo_escrito, direção).
Cabeça
self.head_position
Inteiro assinado que aponta para o índice atual da fita.

4. Lógica do Algoritmo "Incrementador Universal"
O algoritmo gerado em incrementer.py opera em três fases lógicas para calcular o sucessor de um número em qualquer base:
Fase 1: Posicionamento (q_move_right)
A máquina inicia no começo da fita.
Move-se continuamente para a Direita (R), copiando os símbolos lidos, até encontrar um símbolo Branco (B).
Ao encontrar o Branco, recua uma posição para a Esquerda (L) e muda para o estado q_increment.
Fase 2: Incremento e Transporte (q_increment)
A máquina processa o número do dígito menos significativo para o mais significativo (direita para esquerda):
Sem Overflow: Se o símbolo lido não é o último do alfabeto (ex: ler '3' em decimal), a máquina escreve o sucessor imediato ('4'), muda para o estado q_accept e para.
Com Overflow (Vai-um): Se o símbolo lido é o último do alfabeto (ex: '9' em decimal ou 'F' em hexa):
Substitui o símbolo pelo primeiro do alfabeto ('0').
Move para a Esquerda (L).
Permanece no estado q_increment para processar o próximo dígito.
Fase 3: Expansão (q_increment em Branco)
Se o transporte (carry) chegar ao início da fita e encontrar um Branco (ex: somar 1 a '99'):
Escreve o segundo símbolo do alfabeto (geralmente '1').
Muda para q_accept.
Resultado: A fita cresce (ex: '100').
5. Instruções de Uso
Certifique-se de que o Python 3 está instalado.
Crie um arquivo fitas.txt na mesma pasta do código.
Formate o arquivo da seguinte maneira:
Linha 1: O alfabeto ordenado (ex: 01 para binário ou 0123456789ABC para bases maiores).
Linhas 2+: As sequências que você deseja processar.
Execute o comando:
Bash
python main.py


Exemplo de fitas.txt (Base 36)
Plaintext
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
19
1Z
ZZ

6. Resultados de Validação e Testes
O sistema foi submetido a testes de estresse utilizando um sistema de Base 36 (0-9, A-Z). Abaixo estão os resultados obtidos, comprovando a robustez da lógica de transição e gerenciamento de fita.
Entrada
Saída Gerada
Análise Lógica
Resultado
0
1
Incremento simples unitário.
✅ Sucesso
19
1A
Transição numérica para literal (9 -> A) sem carry.
✅ Sucesso
1Z
20
Overflow no último símbolo (Z -> 0) gerando carry para o anterior (1 -> 2).
✅ Sucesso
ZZ
100
Duplo overflow (Z -> 0, Z -> 0) resultando em expansão da fita (novo dígito 1).
✅ Sucesso
PYTHON
PYTHOO
Incremento alfabético posicional (N -> O).
✅ Sucesso

7. Conclusão
O projeto atende a todos os requisitos funcionais estabelecidos. A utilização de um dicionário Python para simular a fita mostrou-se eficiente, permitindo operações em fitas longas (como no teste de stress ZZZZZZ -> 1000000) sem degradação de performance. A abstração da lógica de transição permite que este mesmo código seja reutilizado para simular qualquer computação algorítmica, bastando alterar o gerador de configurações.


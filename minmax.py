import math

# Contadores de nós visitados
nos_visitados_minimax = 0
nos_visitados_alpha_beta = 0

# Função para verificar se há um vencedor
def check_winner(board):
    lines = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]

    if ['x', 'x', 'x'] in lines:
        return 1  # Vitória de 'x'
    elif ['o', 'o', 'o'] in lines:
        return -1  # Vitória de 'o'
    elif all(cell != '_' for row in board for cell in row):
        return 0  # Empate
    return None  # Jogo não acabou

# Função Minimax sem poda
def minimax(board, depth, is_maximizing):
    global nos_visitados_minimax
    nos_visitados_minimax += 1  # Incrementa o contador de nós visitados

    score = check_winner(board)

    if score is not None:
        return score

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'x'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = '_'
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'o'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = '_'
                    best_score = min(score, best_score)
        return best_score

# Função Minimax com poda alfa-beta
def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing):
    global nos_visitados_alpha_beta
    nos_visitados_alpha_beta += 1  # Incrementa o contador de nós visitados

    score = check_winner(board)

    if score is not None:
        return score

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'x'
                    score = minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                    board[i][j] = '_'
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'o'
                    score = minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                    board[i][j] = '_'
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score

# Função para encontrar a melhor jogada sem poda
def find_best_move(board):
    best_score = -math.inf
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'x'
                move_score = minimax(board, 0, False)
                board[i][j] = '_'

                if move_score > best_score:
                    best_score = move_score
                    best_move = (i, j)

    return best_move

# Função para encontrar a melhor jogada com poda alfa-beta
def find_best_move_alpha_beta(board):
    best_score = -math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'x'
                move_score = minimax_alpha_beta(board, 0, alpha, beta, False)
                board[i][j] = '_'

                if move_score > best_score:
                    best_score = move_score
                    best_move = (i, j)

    return best_move

# Testando as configurações iniciais fornecidas na imagem
configs = [
    [['x', 'o', 'x'], ['o', 'x', 'o'], ['_', '_', '_']],  # Configuração i
    [['x', 'o', 'x'], ['o', 'o', 'x'], ['_', '_', '_']],  # Configuração ii
    [['o', '_', 'x'], ['_', 'x', '_'], ['o', '_', '_']]   # Configuração iii
]

print("Minimax sem Poda:")
for idx, config in enumerate(configs):
    best_move = find_best_move(config)
    print(f"Melhor jogada para a configuração {idx + 1}: {best_move}")

print("\nMinimax com Poda Alfa-Beta:")
for idx, config in enumerate(configs):
    best_move = find_best_move_alpha_beta(config)
    print(f"Melhor jogada para a configuração {idx + 1}: {best_move}")

# Agora, vamos calcular o número de nós visitados a partir do tabuleiro vazio

# Inicializando o tabuleiro vazio
empty_board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

# Resetando os contadores e executando os algoritmos para o tabuleiro vazio
nos_visitados_minimax = 0
nos_visitados_alpha_beta = 0

find_best_move(empty_board)
nos_visitados_sem_poda = nos_visitados_minimax

find_best_move_alpha_beta(empty_board)
nos_visitados_com_poda = nos_visitados_alpha_beta

# Exibindo a tabela de comparação
print("\nComparação do número de nós visitados (a partir do tabuleiro vazio):")
print(f"{'Algoritmo':<30}{'Nós Visitados'}")
print(f"{'Minimax sem poda':<30}{nos_visitados_sem_poda}")
print(f"{'Minimax com poda alfa-beta':<30}{nos_visitados_com_poda}")
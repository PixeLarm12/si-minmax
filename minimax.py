import pandas as pd
from IPython.display import display
import math

# visited nodes counter
visitedNodesMinimax = 0
visitedNodesAlphabeta = 0

# to check if winner exists
def checkWinner(board):
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
        return 1  # X wins
    elif ['o', 'o', 'o'] in lines:
        return -1  # O wins
    elif all(cell != '_' for row in board for cell in row):
        return 0  # Draw
    return None

# withouth pruning
def minimax(board, depth, isMaximizing):
    global visitedNodesMinimax
    visitedNodesMinimax += 1

    score = checkWinner(board)

    if score is not None:
        return score

    if isMaximizing:
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'x'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = '_'
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'o'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = '_'
                    bestScore = min(score, bestScore)
        return bestScore

# alpha beta
def minimaxAlphaBeta(board, depth, alpha, beta, isMaximizing):
    global visitedNodesAlphabeta
    visitedNodesAlphabeta += 1

    score = checkWinner(board)

    if score is not None:
        return score

    if isMaximizing:
        bestScore = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'x'
                    score = minimaxAlphaBeta(board, depth + 1, alpha, beta, False)
                    board[i][j] = '_'
                    bestScore = max(score, bestScore)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'o'
                    score = minimaxAlphaBeta(board, depth + 1, alpha, beta, True)
                    board[i][j] = '_'
                    bestScore = min(score, bestScore)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore

# find best move without pruning
def findBestMove(board):
    bestScore = -math.inf
    bestMove = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'x'
                moveScore = minimax(board, 0, False)
                board[i][j] = '_'

                if moveScore > bestScore:
                    bestScore = moveScore
                    bestMove = (i, j)

    return bestMove

# find best move with pruning (alpha beta)
def findBestMoveAlphaBeta(board):
    bestScore = -math.inf
    bestMove = None
    alpha = -math.inf
    beta = math.inf

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'x'
                moveScore = minimaxAlphaBeta(board, 0, alpha, beta, False)
                board[i][j] = '_'

                if moveScore > bestScore:
                    bestScore = moveScore
                    bestMove = (i, j)

    return bestMove

# check given examples
configs = [
    [['x', 'o', 'x'], ['o', 'x', 'o'], ['_', '_', '_']], 
    [['x', 'o', 'x'], ['o', 'o', 'x'], ['_', '_', '_']], 
    [['o', '_', 'x'], ['_', 'x', '_'], ['o', '_', '_']]  
]

print("Minimax sem Poda:")
for idx, config in enumerate(configs):
    bestMove = findBestMove(config)
    print(f"Melhor jogada para a configuração {idx + 1}: {bestMove}")

print("\nMinimax com Poda Alfa-Beta:")
for idx, config in enumerate(configs):
    bestMove = findBestMoveAlphaBeta(config)
    print(f"Melhor jogada para a configuração {idx + 1}: {bestMove}")

emptyBoard = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

print("\n")

visitedNodesMinimax = 0
visitedNodesAlphabeta = 0

findBestMove(emptyBoard)
visitedNodesWithouthPruning = visitedNodesMinimax

findBestMoveAlphaBeta(emptyBoard)
visitedNodesWithPruning = visitedNodesAlphabeta

def plotComparisonNodes(minimax_nodes, alphabeta_nodes):
    data = {
        "Versão": ["Minimax sem poda", "Minimax com poda Alfa-Beta"],
        "Nós Visitados": [minimax_nodes, alphabeta_nodes]
    }

    # style table
    df = pd.DataFrame(data)
    df.set_index("Versão", inplace=True)

    styled_df = df.style \
        .background_gradient(cmap="Greys", low=0, high=1) \
        .set_table_styles({
            'Versão': [{'selector': 'td:hover', 'props': 'background-color: #f5f5f5;'}],
            '': [{'selector': 'th', 'props': 'background-color: #d3d3d3d3; border: 1px solid black;'}],
            'td': [{'selector': 'td', 'props': 'border: 1px solid black;'}]
        }) \
        .set_caption("Comparação dos Nós Visitados")
    display(styled_df)

plotComparisonNodes(visitedNodesWithouthPruning, visitedNodesWithPruning)

import copy
from sudokuGenerator import *


Board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

solvedBoard = copy.deepcopy(Board)

def solve(board):
    # condition de fin :- arriver à la fin du tableau - la fonction findEmpty return NONE
    find = findEmpty(board)
    if find is None:  # if find != False
        return True
    else:
        row, col = find
    # boucle pour
    for number in range(1, 10):
        if validCheck(board, number, (row, col)):
            board[row][col] = number
            # TODO : besoin de l'afficher sur l'interface graphique

            if solve(board):
                return True

            board[row][col] = 0
            # TODO : supprimer le numéro dans l'interface graphique
    return False


def mainSolver(level):
    sudokuGenerate(Board, level)
    solvedBoard = copy.deepcopy(Board)
    solve(solvedBoard)
    return solvedBoard
   
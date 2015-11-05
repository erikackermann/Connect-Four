## simple file to test minimax

from minimax import *
import connect4

def printState(board):
    for i in range(5, -1, -1):
        print("\t"),
        for j in range(7):
            print("| " + str(board[i][j])),
        print("|")
    print("\t  _   _   _   _   _   _   _ ")
    print("\t  1   2   3   4   5   6   7 ")

b = [[' ', 'x', 'o', 'x', 'o', ' ', 'x'], [' ', 'x', 'o', 'o', ' ', ' ', ' '], [' ', ' ', 'o', 'o', ' ', ' ', ' '], [' ', ' ', 'x', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]

printState(b)
m = Minimax(b)

print("Finding best move for x...")

print(m.bestMove(5, b, 'x'))


# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Connect 4 Module
# February 27, 2012

import random
import os
import time
from minimax import Minimax

class Game(object):
    """ Game object that holds state of Connect 4 board and game values
    """
    
    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = u"Connecter Quatre\u2122" # U+2122 is "tm" this is a joke
    colors = ["x", "o"]
    
    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None
        
        # do cross-platform clear screen
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        print(u"Welcome to {0}!".format(self.game_name))
        print("Should Player 1 be a Human or a Computer?")
        while self.players[0] == None:
            choice = str(raw_input("Type 'H' or 'C': "))
            if choice == "Human" or choice.lower() == "h":
                name = str(raw_input("What is Player 1's name? "))
                self.players[0] = Player(name, self.colors[0])
            elif choice == "Computer" or choice.lower() == "c":
                name = str(raw_input("What is Player 1's name? "))
                diff = int(raw_input("Enter difficulty for this AI (1 - 4) "))
                self.players[0] = AIPlayer(name, self.colors[0], diff+1)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[0].name, self.colors[0]))
        
        print("Should Player 2 be a Human or a Computer?")
        while self.players[1] == None:
            choice = str(raw_input("Type 'H' or 'C': "))
            if choice == "Human" or choice.lower() == "h":
                name = str(raw_input("What is Player 2's name? "))
                self.players[1] = Player(name, self.colors[1])
            elif choice == "Computer" or choice.lower() == "c":
                name = str(raw_input("What is Player 2's name? "))
                diff = int(raw_input("Enter difficulty for this AI (1 - 4) "))
                self.players[1] = AIPlayer(name, self.colors[1], diff+1)
            else:
                print("Invalid choice, please try again")
        print("{0} will be {1}".format(self.players[1].name, self.colors[1]))
		
	# x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]
		
        self.board = []
        for i in xrange(6):
            self.board.append([])
            for j in xrange(7):
                self.board[i].append(' ')
    
    def newGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.finished = False
        self.winner = None
        
        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]
		
        self.board = []
        for i in xrange(6):
            self.board.append([])
            for j in xrange(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
		    self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        # there are only 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > 42:
            self.finished = True
            # this would be a stalemate :(
            return
        
        # move is the column that player want's to play
        move = player.move(self.board)

        for i in xrange(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFours()
                self.printState()
                return

        # if we get here, then the column is full
        print("Invalid move (column is full)")
        return
	
    def checkForFours(self):
        # for each piece in the board...
        for i in xrange(6):
            for j in xrange(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        print(slope)
                        self.finished = True
                        return
	    
    def verticalCheck(self, row, col):
        #print("checking vert")
        fourInARow = False
        consecutiveCount = 0
    
        for i in xrange(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
    
        return fourInARow
    
    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
        
        for j in xrange(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fourInARow
    
    def diagonalCheck(self, row, col):
        fourInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
			
        if consecutiveCount >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is decremented

        if consecutiveCount >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fourInARow = True
        if count == 2:
            slope = 'both'
        return fourInARow, slope
    
    def findFours(self):
        """ Finds start i,j of four-in-a-row
            Calls highlightFours
        """
    
        for i in xrange(6):
            for j in xrange(7):
                if self.board[i][j] != ' ':
                    # check if a vertical four-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.highlightFour(i, j, 'vertical')
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.highlightFour(i, j, 'horizontal')
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    # also, get the slope of the four if there is one
                    diag_fours, slope = self.diagonalCheck(i, j)
                    if diag_fours:
                        self.highlightFour(i, j, 'diagonal', slope)
    
    def highlightFour(self, row, col, direction, slope=None):
        """ This function enunciates four-in-a-rows by capitalizing
            the character for those pieces on the board
        """
        
        if direction == 'vertical':
            for i in xrange(4):
                self.board[row+i][col] = self.board[row+i][col].upper()
        
        elif direction == 'horizontal':
            for i in xrange(4):
                self.board[row][col+i] = self.board[row][col+i].upper()
        
        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in xrange(4):
                    self.board[row+i][col+i] = self.board[row+i][col+i].upper()
        
            elif slope == 'negative' or slope == 'both':
                for i in xrange(4):
                    self.board[row-i][col+i] = self.board[row-i][col+i].upper()
        
        else:
            print("Error - Cannot enunciate four-of-a-kind")
	
    def printState(self):
        # cross-platform clear screen
        os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
        print(u"{0}!".format(self.game_name))
        print("Round: " + str(self.round))

        for i in xrange(5, -1, -1):
            print("\t"),
            for j in xrange(7):
                print("| " + str(self.board[i][j])),
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")
                
class Player(object):
    """ Player object.  This class is for human players.
    """
    
    type = None # possible types are "Human" and "AI"
    name = None
    color = None
    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color
    
    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(raw_input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


class AIPlayer(Player):
    """ AIPlayer object that extends Player
        The AI algorithm is minimax, the difficulty parameter is the depth to which 
        the search tree is expanded.
    """
    
    difficulty = None
    def __init__(self, name, color, difficulty=5):
        self.type = "AI"
        self.name = name
        self.color = color
        self.difficulty = difficulty
        
    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        
        # sleeping for about 1 second makes it looks like he's thinking
        #time.sleep(random.randrange(8, 17, 1)/10.0)
        #return random.randint(0, 6)
        
        m = Minimax(state)
        best_move, value = m.bestMove(self.difficulty, state, self.color)
        return best_move





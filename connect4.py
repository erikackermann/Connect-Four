# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Connect 4 Module
# February 27, 2012

class Game(object):
    """ Game object that holds state of Connect 4 board and game values
    """
    
    board = None
    round = None
    finished = None
    winner = None
    turn = None
    
    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = ' '
		
		# Red always goes first (arbitrary choice on my part)
        self.turn = 'R'
		
        self.board = []
        for i in xrange(6):
            self.board.append([])
            for j in xrange(7):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == 'R':
            self.turn = 'Y'
        else:
		    self.turn = 'R'

        # increment the round
        self.round += 1

    def move(self, player, column):
        if player != self.turn:
	        print("It's not your turn")
	        return
		
        # there are only 42 legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > 42:
            self.finished = True
            # this would be a stalemate :(

        for i in xrange(6):
            if self.board[i][column] == ' ':
                self.board[i][column] = player
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
					if self.diagonalCheck(i, j):
						self.finished = True
						return
	    
    def verticalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
		
        for i in xrange(row, 6):
            if self.board[i][col] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
		
		if consecutiveCount >= 4:
			fourInARow = True
			self.winner = self.board[row][col]
		
		return fourInARow
    
    def horizontalCheck(self, row, col):
        fourInARow = False
        consecutiveCount = 0
        
        for j in xrange(col, 7):
            if self.board[row][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 4:
            fourInARow = True
            self.winner = self.board[row][col]

        return fourInARow
    
    def diagonalCheck(self, row, col):
        fourInARow = False

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, 6):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
			
        if consecutiveCount >= 4:
            fourInARow = True
            self.winner = self.board[row][col]
            return fourInARow

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= 4:
            fourInARow = True
            self.winner = self.board[row][col]
            return fourInARow

        return fourInARow
	
    def printState(self):
        print("Round: " + str(self.round))

        for i in xrange(5, -1, -1):
            for j in xrange(7):
                print("|" + str(self.board[i][j])),
            print("|")
        print(" - - - - - - - ")

        if self.finished:
            print("Game Over!")
            if self.winner != ' ':
                print(str(self.winner) + " is the winner")
            else:
                print("Game was a draw")
                
#class Player(object):
#    """ Player object
#    """
#    def __init__(self):
        
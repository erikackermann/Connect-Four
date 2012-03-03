# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Connect 4 Module
# February 27, 2012

class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """
    
    board = None
    def __init__(self, board, my_color):
        # copy the board to self.board
        self.board = [x[:] for x in board]
        self.my_color = my_color
        if self.my_color == 'R':
            self.opp_color = 'B'
        else:
            self.opp_color = 'R'
        
    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and the player whose
            turn it is is whomever called this search
        """
        
        # enumerate all legal moves
        legal_moves = []
        for i in xrange(7):
            # if column i is a legal move...
            if isLegalMove(i, state):
                # make a copy of the state
                temp = [x[:] for x in state]
                # make the move in column i for curr_player
                temp = makeMove(temp, i, curr_player)
                legal_moves.append(temp)
        
        # if node is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves == 0):
            # return the heuristic value of node
            return value(state)
        
        alpha = -9999
        for child in legal_moves:
            alpha = max(alpha, -search(child, depth-1))
        return alpha
        
    
    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        for i in xrange(6):
            if self.board[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True
        
        # if we get here, the column is full
        return False
    
    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
        """        
        for i in xrange(6):
            if state[i][column] == ' ':
                state[i][column] = color
                return

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*9999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*9999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == 'R':
            o_color = 'B'
        else:
            o_color = 'R'
        
        my_fours = checkForStreak(state, color, 4)
        my_threes = checkForStreak(state, color, 3)
        my_twos = checkForStreak(state, color, 2)
        opp_fours = checkForStreak(state, o_color, 4)
        opp_threes = checkForStreak(state, o_color, 3)
        opp_twos = checkForStreak(state, o_color, 2)
        
            
    def checkForStreak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in xrange(6):
            for j in xrange(7):
                if state[i][j] != color:
                    # check if a vertical streak starts at (i, j)
                    count += verticalStreak(i, j, state, streak)
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += horizontalStreak(i, j, state, streak)
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += diagonalCheck(i, j, state, streak)
        # return the sum of streaks of length 'streak'
        return count
            
    def verticalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for i in xrange(row, 6):
            if state[i][col] == state[row][col]:
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount == streak:
            return 1
        else:
            return 0
    
    def horizontalStreak(self, row, col, state, streak):
        consecutiveCount = 0
        for j in xrange(col, 7):
            if state[row][j] == state[row][col]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount == streak:
            return 1
        else:
            return 0
    
    def diagonalCheck(self, row, col, state, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount == streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in xrange(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount == streak:
            total += 1

        return total
        
# [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
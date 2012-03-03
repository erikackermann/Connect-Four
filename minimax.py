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
    colors = ["x", "o"]
    
    def __init__(self, board, my_color):
        # copy the board to self.board
        self.board = [x[:] for x in board]
        self.my_color = my_color
        if self.my_color == self.colors[0]:
            self.opp_color = self.colors[1]
        else:
            self.opp_color = self.colors[0]
            
    def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]
        
        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in xrange(7):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.search(depth-1, temp, opp_player)
        
        best_alpha = -999999
        best_move = None
        print("legal_moves", legal_moves)
        for move, alpha in legal_moves.items():
            if alpha > best_alpha:
                best_alpha = alpha
                best_move = move
        
        return best_move, best_alpha
        
    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and the player whose
            turn it is is whomever called this search
            
            Returns and the alpha value
        """
        
        # enumerate all legal moves
        legal_moves = []
        for i in xrange(7):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)
        
        # if node is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0:
            # return the heuristic value of node
            return self.value(state, curr_player)
        
        # determine opponent's color
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        alpha = -9999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        
        for i in xrange(6):
            if state[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True
        
        # if we get here, the column is full
        return False
    
    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """
        
        temp = [x[:] for x in state]
        for i in xrange(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]
        
        my_fours = self.checkForStreak(state, color, 4)
        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)
        opp_fours = self.checkForStreak(state, o_color, 4)
        opp_threes = self.checkForStreak(state, o_color, 3)
        opp_twos = self.checkForStreak(state, o_color, 2)
        
        return my_fours*99999 + my_threes*100 + my_twos*10 -\
            opp_fours*9999 - opp_threes*100 - opp_twos*10
        
            
    def checkForStreak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in xrange(6):
            for j in xrange(7):
                if state[i][j] != color:
                    # check if a vertical streak starts at (i, j)
                    count += self.verticalStreak(i, j, state, streak)
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, state, streak)
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonalCheck(i, j, state, streak)
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
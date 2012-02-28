# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Play connect four
# February 27, 2012

from connect4 import *
import random

def main():
    """ Play a game!
    """
    
    g = Game()
    g.printState()
    
    while not g.finished:
        current_player = g.turn
        if current_player == 'R':
            column = int(raw_input("Enter a column (1 - 7):")) - 1
        else:
            column = random.randint(0, 6)
        g.move(current_player, column)
        
if __name__ == "__main__": # Default "main method" idiom.
    main()

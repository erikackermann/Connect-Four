# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Play connect four
# February 27, 2012

from connect4 import *

def main():
    """ Play a game!
    """
    
    g = Game()
    g.printState()
    
    while not g.finished:
        g.nextMove()
        
if __name__ == "__main__": # Default "main method" idiom.
    main()

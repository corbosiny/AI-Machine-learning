import threading
from connect4 import Connect4Game
from connect4PlayerRandom import Connect4PlayerRandom
from tkinter import *


class Connect4GameViewer(threading.Thread):

    def __init__(self, game):
        self.game = game
        super(Connect4GameViewer, self).__init__()

    def run(self):
        self.initDisplay()

        while True:
            self.updateGame()
            self.root.update_idletasks()
            self.root.update()


    def initDisplay(self):
        self.root = Tk()
        self.textBox = Text(self.root, height=  self.game.board.boardHeight + 4,width= 5 * self.game.board.boardLength)
        self.textBox.pack()
    
    def updateGame(self):
        self.textBox.config(state= NORMAL)
        self.textBox.delete(1.0, END)
        self.textBox.insert(CURRENT, str(self.game))
        self.textBox.config(state= DISABLED)            #prevents viewer from writing in the textbox


    def close(self):
        self.root.destroy()
        self.root.quit()

        






if __name__ == "__main__":
    newGame = Connect4Game()
    viewer = Connect4GameViewer(newGame)
    viewer.start()
    player1 = Connect4PlayerRandom()
    player2 = Connect4PlayerRandom()
    while True:
        newGame.addPlayer(player1)
        newGame.addPlayer(player2)

        while newGame.gameIsNotOver():
            pass

        newGame.prepareForNewGame()


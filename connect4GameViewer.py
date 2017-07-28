import threading
from tkinter import *


class Connect4GameViewer(threading.Thread):

    def __init__(self, gameMaster):
        self.windows = []
        self.textBoxes = []
        self.gameMaster = gameMaster
        super(Connect4GameViewer, self).__init__()

    def run(self):
        self.root = Tk()
        self.windows = [Toplevel(self.root) for game in range(len(self.gameMaster.games))]
        self.textBoxes = [Text(self.windows[x], height= 10,width= 30) for x in range(len(self.windows))]
        for textBox in self.textBoxes:
            textBox.pack()
        mainloop()
    
    def updateGames(self):
        for x, textBox in enumerate(self.textBoxes):
            textBox.delete(1.0, END)
            textBox.insert(CURRENT, str(self.gameMaster.games[x]))

    def close(self):
        self.root.destroy()
        self.root.quit()
        
if __name__ == "__main__":
    viewer = Connect4GameViewer(games)
    viewer.start()



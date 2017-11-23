from serialMonitor import SerialMonitor
from tkinter import *
import threading

class SerialMonitorViewer(threading.thread):

    def __init__(self, comPort, baudRate = 9600):
        self.serialMonitorHandler = SerialMonitor(comPort, baudRate)
        super(SerialMonitorViewer, self).__init__()
        
    def run(self):
        self.initSerialDisplay()

        while True:
            self.updateSerialMonitorDisplay()
        
    def initSerialDisplay(self):
        self.displayFrame = Tk()
        self.textBox = Text(self.displayFrame, height= 100, width= 100)
        self.textBox.pack()

        self.userInputBar = Entry(self.displayFrame)
        self.userInputBar.pack()
        self.userInputButton(self.displayFrame, command= writeUserInputToComPort)
        self.userInputButton.pack()
        
    def updateSerialMonitorDisplay(self):
        self.textBox.config(state= NORMAL)
        if self.serialMonitorHandler
            newData = self.serialMonitorHandler.getLineFromComPort()
            self.textBox.insert(CURRENT, newData)
        self.textBox.config(state= DISABLED)

    def writeUserInputToComPort():
        messageToSend = self.userInputBar.get()
        self.userInputBar.delete(0, END)
        self.serialMonitorHandler.sendStringToComPort(messageToSend)


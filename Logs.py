from Card import Card
from Player import Player

class Logs:
    def __init__(self):
        self.cardsPlayed = []
        self.logs = []
        self.turnCounter = 0

    def newTurn(self, player):
        self.logs.append(Turn(self.turnCounter, player))
        self.turnCounter += 1

    def addAction(self, text):
        self.logs[-1].addAction(text)

    def getTurnCounter(self):
        return self.turnCounter

    def printTurn(self):
        print(self.logs[-1])

    def showTurnsAfterPreviousMoveMadeByCurrentPlayer(self, currentPlayer):
        i = -2
        imax = -self.logs.__len__() - 1
        log = self.logs[i]
        while i >= imax and not log.getPlayer() == currentPlayer:
            i -= 1
        i += 1
        for x in self.logs[i:-1]:
            print(x)

    def showAll(self):
        for x in self.logs[:-1]:
            print(x)


class Turn:
    def __init__(self, number, player):
        self.number = number            # może zbędne
        self.player = player
        self.text = 'Ruch ' + str(number)
        if not player == None:
            self.text += ' - ' + player.getName()

    def __str__(self):
        return self.text

    def addAction(self, text):
        self.text += '\n\t' + text

    def getPlayer(self):
        return self.player

    def getNumber(self):
        return self.number
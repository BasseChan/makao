from Card import Card

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.toPass = 0

    def giveCards(self, cards):
        self.cards += cards

    def giveSingleCard(self, card):
        self.cards.append(card)

    def getCards(self):
        return self.cards

    def getWithGivenValue(self, value):
        cards = []
        for card in self.cards:
            if card.getValue() == value:
                cards.append(card)
        return cards

    def separateValidAndInvalid(self, validCards):
        valid = []
        invalid = []
        for card in self.cards:
            if card.isValid(validCards):
                valid.append(card)
            else:
                invalid.append(card)
        return valid, invalid

    def removeSingleCard(self, card):
        a = []
        if card in self.cards:
            i = self.cards.index(card)
            self.cards = self.cards[:i] + self.cards[(i + 1):]

    def removeCards(self, cards):
        for card in self.cards:
            self.removeSingleCard(card)

    def getToPass(self):
        return toPass

    def passTurn(self):
        self.toPass -= 1

    def setToPass(self, toPass):
        self.toPass = toPass

    def getName(self):
        return self.name

    def showCards(self):
        i = 1
        imax = self.cards.__len__()
        for x in self.cards:
            if i % 10 == 0 or i == imax:
                print(x)
            else:
                print(x, end=', ')
            i += 1

    def getCardsNumber(self):
        return self.cards.__len__()

    def showCardsNumber(self):
        a = self.cards.__len__()
        if a == 1:
            print('%s - 1 karta' % self.name, end='\t')
        elif a % 10 > 1 and a % 10 < 5:
            print('%s - %s karty' % (self.name, a), end='\t')
        else:
            print('%s - %s kart' % (self.name, a), end='\t')
        if self.toPass > 0:
            if self.toPass == 1:
                print('(czeka 1 turę)')
            elif self.toPass % 10 > 1 and self.toPass % 10 < 5:
                print('(czeka %s tury)' % self.toPass)
            else:
                print('(czeka %s tur)' % self.toPass)
        else:
            print()

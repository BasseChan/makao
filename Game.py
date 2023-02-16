from Card import Card
import random
from Logs import Logs
from Player import Player
from time import sleep

# to do:
# upewnić się że wszędzie można dać damę w wariancie
# Wszędzie można dać jokera


class Game:
    def __init__(self, players, startCardsNubers, numberOfDecks, firstToWin, queenRule, whySoSirious):
        #players - array of infos about players (name, number of starting cards ...)

        self.colors = ['kier', 'karo', 'trefl', 'pik']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'walet', 'dama', 'król', 'as']
        self.standardCards = ['5', '6', '7', '8', '9', '10']
        if not queenRule:
            self.standardCards.append('dama')

        # self.cards = [('2', give2), ('3', give3), ('4', stop), ('5', None), ('6', None), ('7', None), ('8', None),
        #               ('9', None), ('10', None), ('walet', chooseValue), ('dama', None), ('as', chooseColor)]

        self.numberOfDecks = numberOfDecks

        self.firstToWin = firstToWin

        self.queenRule = queenRule
        self.whySoSirious = whySoSirious

        self.queue, self.players = self.createPlayers(players, startCardsNubers)

        self.cards = self.getCards()

        self.validCards = []

        self.startGame()

    def startGame(self):
        self.deck = self.getDeck() * self.numberOfDecks
        random.shuffle(self.deck)
        self.logs = Logs()
        self.pile = []
        self.placeStartCard()
        self.addStartCards()
        self.winners = []
        self.surrenders = []

        self.info = 'Zagraj kartę'

        self.toGet = 0
        self.toPass = 0
        self.toRefresh = 0

        random.shuffle(self.queue)

        # a = self.doNothing
        # a()

        self.infoForPlayer()

    def getCards(self):
        #druga wartość w parze z efektem mówi czy efekt jest wykorzystywany wielokrotnie przy zagraniu kilku kart na raz
        cards = {('król', 'kier'): ((self.give5, True), [('król', 'kier'), ('król', 'pik'), ('2', 'kier'), ('3', 'kier')]),
                 ('król', 'pik'): ((self.give5rev, True), [('król', 'kier'), ('król', 'pik'), ('2', 'pik'), ('3', 'pik')]),
                 ('król', 'trefl'): ((self.lazyKingTrefl, True), ['król', 'trefl']),
                 ('król', 'karo'): ((self.lazyKingKaro, True), ['król', 'karo'])}
        for color in self.colors:
            for card in self.standardCards:
                cards[(card, color)] = ((self.doNothing, True), [color, card])
            cards[('4', color)] = ((self.stop, True), ['4'])
            cards[('walet', color)] = ((self.chooseValue, False), ['walet'])
            cards[('as', color)] = ((self.chooseColor, False), ['as'])
            if self.queenRule:
                cards[('dama', color)] = ((self.queenOnEverythingAndViceVersa(), false), self.colors)
        for color in ['kier', 'pik']:
            cards[('2', color)] = ((self.give2, True), ['2', ('3', color), ('król', color)])
            cards[('3', color)] = ((self.give3, True), ['3', ('2', color), ('król', color)])
        for color in ['trefl', 'karo']:
            cards[('2', color)] = ((self.give2, True), ['2', ('3', color)])
            cards[('3', color)] = ((self.give3, True), ['3', ('2', color)])
        cards[('joker', '')] = ((self.wannaSeeAMagicTrick, True), [])
        if self.queenRule:
            for card in cards:
                cards[card][1].append('dama')
        if self.whySoSirious:
            for card in cards:
                cards[card][1].append('joker')
        return cards

    def getDeck(self):
        deck = []
        for color in self.colors:
            for value in self.values:
                deck.append(Card(color, value))
        if self.whySoSirious:
            for _ in range(3):
                deck.append(Card('', 'jocker'))
        return deck

    def createPlayers(self, players, startCardsNubers):
        newPlayers = []
        dict = {}
        for i in range(players.__len__()):
            player = Player(players[i])
            dict[player] = startCardsNubers[i]
            newPlayers.append(player)
        return newPlayers, dict

    def addStartCards(self):
        for player in self.queue:
            self.giveCards(self.players[player], player)
            # player.giveCards( self.players[player])

    def nextPlayer(self):
        input()
        sleep(0.01)
        self.queue = self.queue[1:] + self.queue[:1]
        if self.toRefresh == 1:
            self.updateValidCards()
            self.info = 'Zagraj kartę'
        if self.toRefresh > 0:
            self.toRefresh -= 1
        if self.queue[-1].getCardsNumber() == 0:
            self.winners.append(self.queue[-1])
            self.queue = self.queue[:-1]
            self.logs.addAction('Gracz położył ostatnią kartę')
        if self.queue.__len__() > self.firstToWin:
            self.infoForPlayer()

    # def getNewDeck(self):
    #     deck = []
    #     for _ in range(self.numberOfDecks):
    #         deck.append(Card('kier', 'król', give5, [('król', 'kier'), ('król', 'pik'), ('2', 'kier'), ('3', 'kier')]))
    #         deck.append(Card('pik', 'król', give5rev, [('król', 'kier'), ('król', 'pik'), ('2', 'pik'), ('3', 'pik')]))
    #         deck.append(Card('trefl', 'król', None, ['król', 'trefl']))
    #         deck.append(Card('karo', 'król', None, ['król', 'karo']))
    #         for color in self.colors:
    #             for card in ['5', '6', '7', '8', '9', '10', 'dama']:
    #                 deck.append(Card(color, card, None, [color, card]))
    #             deck.append(Card(color, '4', self.stop, ['4']))
    #             deck.append(Card(color, 'walet', self.chooseValue, ['walet']))
    #             deck.append(Card(color, 'as', self.chooseValue, ['as']))
    #         for color in ['kier', 'pik']:
    #             deck.append(Card(color, '2', self.give2, ['2', ('3', color), ('król', color)]))
    #             deck.append(Card(color, '3', self.give3, ['3', ('2', color), ('król', color)]))
    #         for color in ['trefl', 'karo']:
    #             deck.append(Card(color, '2', self.give2, ['2', ('3', color)]))
    #             deck.append(Card(color, '3', self.give3, ['3', ('2', color)]))
    #     random.shuffle(deck)
    #     return deck

    def pileToDeck(self):
        self.deck = self.pile[:-1]
        self.pile = self.pile[-1:]
        random.shuffle(self.deck)

    def giveCards(self, n, player):
        len = self.deck.__len__()
        if n > len:
            player.giveCards(self.deck)
            self.pileToDeck()
            player.giveCards(self.deck[:n-len])
            self.deck = self.deck[n-len:]
        else:
            player.giveCards(self.deck[:n])
            self.deck = self.deck[n:]

    def updateValidCards(self):
        if self.pile[-1].getValue() == 'joker':
            self.validCards = self.previousJoker
        else:
            self.validCards = [self.pile[-1].getValue(), self.pile[-1].getColor()]
        if self.queenRule:
            self.validCards.append('dama')

    def placeStartCard(self):
        i = 0
        self.pile.append(self.deck[0])
        self.deck = self.deck[1:]
        toLogs = 'Startowe wyłożenie kart: ' + str(self.pile[0])
        while not self.pile[-1].isValid(self.standardCards + [('król', 'karo'), ('król', 'trefl')]):
            self.pile.append(self.deck[0])
            self.deck = self.deck[1:]
            toLogs += ', ' + str(self.pile[-1])
        self.updateValidCards()
        self.logs.newTurn(None)
        self.logs.addAction(toLogs)

    # def addPlayers(self, players):
    #     for x in players:
    #         player = Player(x[0])
    #         self.giveCards(x[1], player)
    #         self.players.append(player)

    def doNothing(self):
        if self.toRefresh < 1:
            self.info = 'Zagraj kartę'
        # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    def lazyKingTrefl(self):
        if self.toGet > 0:
            self.validCards = [('2', 'trefl'), ('3', 'trefl'), ('król', 'kier'), ('król', 'pik')]
            if self.queenRule:
                self.validCards.append('dama')
        else:
            self.info = 'Zagraj kartę'

    def lazyKingKaro(self):
        if self.toGet > 0:
            self.validCards = [('2', 'karo'), ('3', 'karo'), ('król', 'kier'), ('król', 'pik')]
            if self.queenRule:
                self.validCards.append('dama')
        else:
            self.info = 'Zagraj kartę'

    def give2(self):
        self.toGet += 2
        self.info = 'Liczba kart do dobrania: ' + str(self.toGet)

    def give3(self):
        self.toGet += 3
        self.info = 'Liczba kart do dobrania: ' + str(self.toGet)

    def give5(self):
        self.toGet += 5
        self.info = 'Liczba kart do dobrania: ' + str(self.toGet)

    def give5rev(self):
        self.toGet += 5
        a = self.queue[1:]
        a.reverse()
        self.queue = self.queue[:1] + a
        self.info = 'Liczba kart do dobrania: ' + str(self.toGet)

    def stop(self):
        self.toPass += 1
        # print(str(self.toPass))
        self.info = 'Liczba tur do przeczekania: ' + str(self.toPass)
        # print(self.info)

    def chooseValue(self):
        a = input('Podaj żądaną wartość (' + ', '.join(self.standardCards) + ')\n')
        sleep(0.01)
        while a not in self.standardCards:
            a = input('Podana wartość jest niedostępna. Podaj wartość ze zbioru (' + ', '.join(self.standardCards) + ')\n')
            sleep(0.01)
        self.validCards = ['walet', a]
        if self.queenRule:
            self.validCards.append('dama')
        self.toRefresh = self.queue.__len__() + 1
        self.info = self.queue[0].getName() + ' żąda kart wartości ' + a
        self.logs.addAction('Gracz zażądał kart wartości %s' % a)


    def chooseColor(self):
        a = input('Podaj żądany kolor (' + ', '.join(self.colors) + ')\n')
        sleep(0.01)
        while a not in self.colors:
            a = input('Podano niewłaściwy kolor. Podaj kolor ze zbioru (' + ', '.join(self.colors) + ')\n')
            sleep(0.01)
        self.validCards = ['as', a]
        if self.queenRule:
            self.validCards.append('dama')
        self.info = str(self.queue[0]) + ' zmienia kolor na ' + a
        self.logs.addAction('Gracz zażądał kart koloru %s' % a)

    def queenOnEverythingAndViceVersa(self):
        self.toPass = 0
        self.toGet = 0
        self.toRefresh = 0
        self.info = "Połóż dowolną kartę"

    # def checkIfIn(self, a, list):
    #     for b in list:
    #         if b[0] + ' ' + b[1] == a:
    #             return True
    #     return False

    def wannaSeeAMagicTrick(self):
        print('Wybierz kartę jaką ma udawać joker')
        valid = []
        valid2 = []
        i = 1
        for color in self.colors:
            for value in self.values:
                if value in self.validCards or color in self.validCards or (value, color) in self.validCards or (color, value) in self.validCards:
                    valid.append((value, color))
                    valid.append(value + ' ' + color)
                    print(i + ' - ' + value + ' ' + color, end='\t')
                    if i % 5 == 0:
                        print()
                    i += 1
        if not i % 5 == 1:
            print()

        numbers = []
        for j in range(1, i + 1):
            numbers.append(str(j))

        a = input()
        sleep(0.01)
        if a in numbers or a in valid2:
            if a in numbers:
                i = numbers.index(a)
            if a in valid2:
                i = valid2.index(a)
            card = valid[i]
            (effect, toPlay), validAfter = self.cards[card]
            self.previousJoker = [card[0], card[1]]

            if toPlay:
                effect()
            self.placeExtraCard(self.queue[0].getCards(), card[0], card)            # Czy wystarczy???

        else:
            print("Podano nieprawidłową wartość")
            self.wannaSeeAMagicTrick()


    # def firstSaves(self):
    #     card = self.deck[0]
    #     self.deck = self.deck[1:]
    #     if self.toGet > 0:
    #         print("Pierwsza karta: " + card)
    #     else:
    #         print("Dobrana karta: " + card)
    #         # czy przy dobieraniu pierwszej jest ona odejmowana z puli?
    #     if card.isValid(self.validCards):
    #         a = input('Czy chcesz ją zagrać (1 - tak, 2 - nie)\n')
    #         sleep(0.01)
    #         if a == 1:
    #             self.placeCards()
    #
    #         # wybór kart dodatkowych
    #         # dołożenie kart i realizacja ich funkcji
    #         else:
    #             self.queue[0].giveCards([card])
    #             if self.toGet > 0:
    #                 self.giveCards(self.toGet-1, self.queue[0])
    #                 self.updateValidCards()
    #                 self.toGet = 0



    def placeExtraCard(self, cards, value, previous, toLogs, numberOfCardsPlayed):       #przerobić żeby nie powtażać wartości

        allowed = self.queue[0].getWithGivenValue(value)
        if allowed:
            print("Czy chcesz zagrać dodatkowe karty tej wartości?\n0 - pass")

            allowed2 = []
            for i in range(1, allowed.__len__() + 1):
                allowed2.append(str(i))

            self.listThem(allowed, 5)
            a = input()
            sleep(0.01)
            if a in allowed or a in allowed2:
                if a in allowed:
                    i = allowed.index(a)
                else:
                    i = allowed2.index(a)
                card = allowed[i]
                effect, toPlay = self.cards[(card.getValue(), card.getColor())][0]
                self.queue[0].removeSingleCard(card)
                self.pile.append(card)
                if toPlay:
                    effect()
                if card.getValue() == 'joker':
                    self.placeExtraCard(allowed[:i] + allowed[(i + 1):], value, (card.getValue(), card.getColor()),
                                        '%s, joker (%s %s)' % (toLogs, self.previousJoker[0], self.previousJoker[1]), numberOfCardsPlayed + 1)
                else:
                    self.placeExtraCard(allowed[:i] + allowed[(i + 1):], value, (card.getValue(), card.getColor()),
                                        '%s, %s' % (toLogs, card), numberOfCardsPlayed + 1)
            elif a in ['0', '']:
                # wydzielić do funkcji
                card = self.pile[-1]
                (effect, toPlay), valid = self.cards[previous]
                if self.toRefresh <= 1:
                    self.validCards = valid
                isItChanged = self.toRefresh
                if not toPlay:
                    effect()
                if self.toRefresh > 1 and isItChanged == self.toRefresh:
                    self.validCards = [card.getValue(), 'joker']
                    if self.queenRule:
                        self.validCards.append('queen')
                self.logs.addAction('Gracz zagrał %s kart: %s' % (numberOfCardsPlayed, toLogs))
                if numberOfCardsPlayed > 1:
                    print('Zagrano karty')
                else:
                    print('Zagrano kartę')
                self.nextPlayer()
                #
            else:
                print("Podano nieprawidłową wartość")
                self.placeExtraCard(allowed, value, previous)
        else:
            #
            card = self.pile[-1]
            (effect, toPlay), valid = self.cards[previous]
            if self.toRefresh <= 1:
                self.validCards = valid
            isItChanged = self.toRefresh
            if not toPlay:
                effect()
            if self.toRefresh > 1 and isItChanged == self.toRefresh:
                self.validCards = [card.getValue(), 'joker']
                if self.queenRule:
                    self.validCards.append('queen')
            if numberOfCardsPlayed == 1:
                self.logs.addAction('Gracz zagrał 1 kartę: %s' % toLogs)
            elif numberOfCardsPlayed < 5:
                self.logs.addAction('Gracz zagrał %s karty: %s' % (numberOfCardsPlayed, toLogs))
            else:
                self.logs.addAction('Gracz zagrał %s kart: %s' % (numberOfCardsPlayed, toLogs))
            if numberOfCardsPlayed > 1:
                print('Zagrano karty')
            else:
                print('Zagrano kartę')
            self.nextPlayer()
            #

    def firstSaves(self):
        card = self.deck[0]
        self.deck = self.deck[1:]
        if self.toGet > 0:
            print('\nPierwsza karta: ' + str(card))
        else:
            print('\nDobrana karta: ' + str(card))
            # czy przy dobieraniu pierwszej jest ona odejmowana z puli?
        if card.isValid(self.validCards):
            a = input('Czy chcesz ją zagrać (1 - tak, 2 - nie)\n')
            sleep(0.01)
            if a == '1':
                self.pile.append(card)
                # sprawdzić czy (card.getValue(), card.getColor()) może zastąpić card (z jokerem chyba już nie)
                effect, toPlay = self.cards[(card.getValue(), card.getColor())][0]
                if toPlay:
                    effect()
                self.logs.addAction('Gracz dobrał kartę i ją zagrał')
                self.placeExtraCard(self.queue[0].getCards(), card.getValue(), (card.getValue(), card.getColor()), card, 1)
            else:
                # wydzielić
                self.queue[0].giveSingleCard(card)
                if self.toGet > 0:
                    self.giveCards(self.toGet-1, self.queue[0])
                    self.updateValidCards()
                    self.toGet = 0
                    self.info = 'Zagraj kartę'
                    if self.toGet < 5:
                        self.logs.addAction('Gracz dobrał %s karty' % self.toGet)
                    else:
                        self.logs.addAction('Gracz dobrał %s kart' % self.toGet)
                else:
                    self.logs.addAction('Gracz dobrał kartę')
                self.nextPlayer()
                #
        else:
            self.queue[0].giveSingleCard(card)
            if self.toGet > 0:
                self.giveCards(self.toGet - 1, self.queue[0])
                self.updateValidCards()
                self.info = 'Zagraj kartę'
                if self.toGet < 5:
                    self.logs.addAction('Gracz dobrał %s karty' % self.toGet)
                    print('Dobierasz %s karty' % self.toGet)
                else:
                    self.logs.addAction('Gracz dobrał %s kart' % self.toGet)
                    print('Dobierasz %s kart' % self.toGet)
            else:
                self.logs.addAction('Gracz dobrał kartę')
            self.toGet = 0
            self.nextPlayer()

    def placeCard(self):
        # print(self.validCards)
        print(self.info)
        valid, invalid = self.queue[0].separateValidAndInvalid(self.validCards)
        if valid:
            if self.toPass > 0:
                print('0 - czekaj')
            else:
                print('0 - dobierz')
            self.listThem(valid, 5)
            if invalid:
                print('Niedostępne karty: ', end='')
                self.listThemWithoutIndexes(invalid)
            a = input()
            sleep(0.01)

            numbers = []
            for i in range(1, valid.__len__()+1):
                numbers.append(str(i))              #brzydkie

            if a == '0' or a == '':
                #
                if self.toPass > 0:
                    self.queue[0].setToPass(self.toPass - 1)
                    self.toPass = 0
                    self.info = 'Zagraj kartę'
                    if self.toPass == 1:
                        self.logs.addAction('Gracz czeka 1 kolejkę')
                    elif self.toPass > 1 and self.toPass < 5:
                        self.logs.addAction('Gracz czeka %s koleji' % self.toPass)
                    else:
                        self.logs.addAction('Gracz czeka %s kolejek' % self.toPass)
                    self.nextPlayer()
                else:
                    self.firstSaves()
                #
            elif a in numbers or a in valid:
                if a in numbers:
                    i = numbers.index(a)
                else:
                    i = valid.index(a)
                card = valid[i]
                self.queue[0].removeSingleCard(card)
                self.pile.append(card)
                (effect, toPlay), validAfter = self.cards[(card.getValue(), card.getColor())]
                if toPlay:
                    effect()
                self.placeExtraCard(self.queue[0].getCards(), card.getValue(), (card.getValue(), card.getColor()), card, 1)
            elif a in unvalid:
                print("Nie można zagrać tej karty")
                self.placeCard(cards)
            else:
                print("Podano nieprawidłową wartość")
                self.placeCard(cards)
        else:
            print("Brak dostępnych kard")
            print('Niedostępne karty: ', end='')
            self.listThemWithoutIndexes(invalid)
            # wydzielić
            if self.toPass > 0:
                self.queue[0].setToPass(self.toPass)
                self.toPass = 0
                self.info = 'Zagraj kartę'
                if self.toPass == 1:
                    self.logs.addAction('Gracz czeka 1 kolejkę')
                elif self.toPass > 1 and self.toPass < 5:
                    self.logs.addAction('Gracz czeka %s kolejki' % self.toPass)
                else:
                    self.logs.addAction('Gracz czeka %s kolejek' % self.toPass)
                self.nextPlayer()
            else:
                self.firstSaves()
            #

    def playerTurn(self):
        player = self.queue[0]
        if player.getToPass() > 0:
            player.passTurn()
        else:
            self.placeCard()
        self.nextPlayer()

    def listThem(self, cards, inLine):
        i = 1
        for card in cards:
            if i % inLine == 0:
                print(str(i) + ' - ' + str(card))
            else:
                print(str(i) + ' - ' + str(card), end='\t')
            i += 1
        if not i % inLine == 1:
            print()

    def listThemWithoutIndexes(self, cards):
        if cards:
            # print(', '.join(cards))             #???
            print(str(cards[0]), end='')
            for card in cards[1:]:
                print(', ' + str(card), end='')
        print()

    def infoForPlayer(self):
        # wypisz graczy z jedną kartą
        print('\n'*50)
        self.logs.newTurn(self.queue[0])
        self.logs.printTurn()
        input()
        sleep(0.01)
        print('Poprzednie tury:')
        self.logs.showTurnsAfterPreviousMoveMadeByCurrentPlayer(self.queue[0])
        print('\nTwoja talia:')
        self.queue[0].showCards()
        if self.pile[-1].getValue() == 'joker':
            print('\nKarta na szczycie: joker(%s %s)' % (self.previousJoker[0], self.previousJoker[1]))
        else:
            print('\nKarta na szczycie: ' + str(self.pile[-1]))
        print(self.info)
        self.menu()




    def menu(self):
        print('\nWybierz akcję:\n1 - kontynuuj\n2 - wyświetl swoją talię\n3 - wyświetl liczbę kart przeciwników\n'
              '4 - wyświetl stos kart\n5 - wyświetl ostatnie logi\n6 - wyświetl wszystkie logi\n7 - poddaj się')
        a = input()
        sleep(0.01)
        if a == '2':
            print('Twoja talia:')
            self.queue[0].showCards()
            self.menu()
        elif a == '3':
            for x in self.queue[1:]:
                x.showCardsNumber()
            self.menu()
        elif a == '4':
            print('Stos kart:')
            for x in self.pile:
                print(str(x))
            self.menu()
        elif a == '5':
            print('Poprzednie tury:')
            self.logs.showTurnsAfterPreviousMoveMadeByCurrentPlayer(self.queue[0])
            self.menu()
        elif a == '6':
            self.logs.showAll()
            self.menu()
        elif a == '7':
            self.surrenders.append(self.queue[0])
            self.logs.addAction('Gracz poddał się')
            if self.toPass > 0:
                self.toPass = 0
                self.info = 'Stopowanie unieważnione, zagraj kartę'
            if self.toGet > 0:
                self.toGet = 0
                self.info = 'Dobieranie unieważnione, zagraj kartę'
            self.queue = self.queue[-1:] + self.queue[1:]
            self.nextPlayer()
        else:
            self.placeCard()



Game(['gracz 1', 'gracz 2', 'gracz 3'], [5,5,5], 1, 2, False, False)

    # def placeCard(self):
    #     print(self.info)
    #     print('0 - dobierz')
    #     valid, unvalid = self.queue[0].separateValidAndUnvalid(self.validCards)
    #     self.listThem(valid, 5)
    #     print('Niedostępne karty: ', end='')
    #     self.listThemWithoutIndexes(unvalid)
    #     a = input()
    #     sleep(0.01)
    #
    #     numbers = []
    #     for i in range(1, valid.__len__()+1):
    #         numbers.append(str(i))              #brzydkie
    #
    #     if a == '0' or a == '':
    #         #dobierz
    #         pass
    #     elif a in numbers:
    #         i = numbers.index(a)
    #         card = valid[i]
    #         self.queue[0].removeSingleCard(card)
    #         self.pile.append(card)
    #         #sprawdź czy można więcej i tam zagraj efekt itd
    #     elif a in valid:
    #         i = valid.index(a)
    #         card = valid[i]
    #         self.queue[0].removeSingleCard(card)
    #         self.pile.append(card)
    #         # sprawdź czy można więcej i tam zagraj efekt itd
    #     elif a in unvalid:
    #         print("Nie można zagrać tej karty")
    #         self.placeCards(cards)
    #     else:
    #         print("Podano nieprawidłową wartość")
    #         self.placeCards(cards)

    # def placeSingleCard(self, card):
    #     self.queue[0].removeSingleCard(card)
    #     self.pile.append(card)
    #     effect, self.validCards = self.cards[(card.getValue(), card.getColor())]
    #     effect()
    #
    # def placeSameValue(self, cards, value, played):
    #     print("Czy chcesz zagrać dodatkowe karty tej wartości?\n 0 - pass")
    #     allowed = self.queue[0].getWithGivenValue(value)
    #     allowed2 = []
    #     for i in range(1, allowed.__len__()+1):
    #         allowed2.append(str(i))
    #
    #     self.listThem(allowed, 5)
    #     a = input()
    #     sleep(0.01)
    #     if a in allowed2:
    #         i = allowed2.index(a)
    #         card = allowed[i-1]
    #         j = cards.index(card)
    #         self.placeSameValue(cards[:j] + cards[(j+1):], value, played.append(card))
    #     elif a in allowed:
    #         i = cards.index(a)
    #         self.placeSameValue(cards[:i] + cards[(i + 1):], value, played.append(cards[i]))
    #     elif a in ['0', '']:
    #         # self.queue[0].removeCards(played)
    #         pass
    #     else:
    #         print("Podano nieprawidłową wartość")
    #         self.placeSameValue(cards, value, played)
    #
    # def placeCards(self, cards):
    #     self.pile += cards
    #     card = cards[-1]
    #     effect, self.validCards = self.cards[(card.getValue(), card.getColor())]





#     def afterPass(self):
#         if self.toGet > 0:
#
#
#     def placeCard(self):
#         pass
#
#
#
# def give2():
#     pass
#
# def give3():
#     pass
#
# def give5():
#     pass
#
# def give5rev():
#     pass
#
# def chooseColor():
#     pass
#
# def chooseValue():
#     pass
#
# def stop():
#     pass
#





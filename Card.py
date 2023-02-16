

class Card:
    # def __init__(self, color, value, effect, validAfter):
    #     self.color = color
    #     self.value = value
    #     self.effect = effect
    #     self.validAfter = validAfter
    #
    # def isNormal(self):
    #     if self.effect is None:
    #         return true
    #     else:
    #         return false

    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return self.value + ' ' + self.color

    def getColor(self):
        return self.color

    def getValue(self):
        return self.value

    def isValid(self, list):
        validity = False
        for x in list:
            validity = validity or self.isValid2(x)
        return validity

    def isValid2(self, a):
        return self.color == a or self.value == a or (self.color, self.value) == a or (self.value, self.color) == a

    # def isValid2(self, a):
    #     return self.color == a or self.value == a
    #
    # def isValid2(self, a, b):
    #     return self.color == a and self.value == b or self.color == b and self.value == a

    def __eq__(self, other):
        return self.value + ' ' + self.color == other or self.color + ' ' + self.value == other

class Joker (Card):

    def __init__(self):
        self.value = 'joker'
        self.color = ''

    def __str__(self):
        return 'joker'

    def __eq__(self, other):
        return isinstance(other, str)
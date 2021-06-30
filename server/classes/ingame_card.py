from copy import copy

class IngameCard():
    def __init__ (self, name, attack, defence):
        self.name = name
        self.attack = attack
        self.defence = defence

    @staticmethod
    def generate(name, attack, defence):
        return IngameCard(copy(name), copy(attack), copy(defence))

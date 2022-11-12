from random import randint


class Chest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inside = ('hp', 'gm')[randint(0, 1)]

    def colide(self, other):
        return self.x == other.x and self.y == other.y

    def attack(self, other):
        if self.inside == 'hp':
            other.health = int(other.health * 2)
        elif self.inside == 'gm':
            other.damage = int(other.damage * 1.5)
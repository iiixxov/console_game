class GameObject:
    def __init__(self, **kwargs: {'pos': (int, int), 'health': int, 'damage': int}):
        self.x, self.y = kwargs['pos']
        self.health = kwargs['health']
        self.damage = kwargs['damage']

    def move(self, key):
        keys = {'w': lambda x, y: (x, y - 1),
                's': lambda x, y: (x, y + 1),
                'a': lambda x, y: (x - 1, y),
                'd': lambda x, y: (x + 1, y)}
        if key not in keys:
            return False
        self.x, self.y = keys[key](self.x, self.y)
        return True

    def healing(self, key):
        if key == 'healing':
            self.health = int(self.health * 1.5)
            return True

    def colide(self, other):
        return self.x == other.x and self.y == other.y

    def is_a_live(self):
        return self.health > 0

    def attack(self, other):
        other.health -= self.damage

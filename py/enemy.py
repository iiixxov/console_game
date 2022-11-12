from py.game_object import GameObject


class Enemy(GameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

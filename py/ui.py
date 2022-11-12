class UI:
    def __init__(self, game_object):
        self.object = game_object
        self.hp = self.object.health
        self.damage = self.object.damage
        self.size = len(max(str(self.hp), str(self.damage), key=len))

    def show(self, other=None):
        if other is None:
            otherUI = None
        else:
            otherUI = UI(other)
        ui = list()
        self.hp = self.object.health
        self.damage = self.object.damage
        self.size = len(max(str(self.hp), str(self.damage), key=len)) + 3

        if otherUI is None:
            ui.append(': HP '+'  '*(self.size-len(str(self.hp))-3)+str(self.hp)+' :')
            ui.append(': DM '+'  '*(self.size-len(str(self.damage))-3)+str(self.damage)+' :')

        else:
            otherUI.hp = otherUI.object.health
            otherUI.damage = otherUI.object.damage
            otherUI.size = len(max(str(otherUI.hp), str(otherUI.damage), key=len)) + 3
            ui.append(': HP '+'  '*(self.size-len(str(self.hp))-3)+str(self.hp)+' : HP '+'  '*(otherUI.size-len(str(otherUI.hp))-3)+str(otherUI.hp)+' :')
            ui.append(': DM '+'  '*(self.size-len(str(self.damage))-3)+str(self.damage)+' : DM '+'  '*(otherUI.size-len(str(otherUI.damage))-3)+str(otherUI.damage)+' :')
        return ui

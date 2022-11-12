import os
from random import randint
from time import sleep

import pygame

from py.chest import Chest
from py.enemy import Enemy
from py.player import Player
from py.ui import UI


class Game:
    def free_ceil(self):
        free = False
        while not free:
            pos = [randint(1, self.field_size[0] - 1), randint(1, self.field_size[1] - 1)]
            for enemy in self.enemies:
                if enemy.x == pos[0] and enemy.y == pos[1]:
                    free = False
                    break
                else:
                    free = True
        return pos

    def __init__(self, field_size, enemies_count):
        self.player = Player(pos=(0, 0), health=20, damage=5)
        self.field_size = field_size
        self.player_ui = UI(self.player)
        self.enemies = [Chest(5, 5)]
        for _ in range(enemies_count - 1):
            self.enemy_spawn()

    def show_field(self):
        field = list()

        for i in range(self.field_size[0]):
            stri = ''
            for j in range(self.field_size[1]):
                ceil = '  '
                if self.player.x == j and self.player.y == i:
                    ceil = 'P'
                for enemy in self.enemies:
                    if j == enemy.x and i == enemy.y:
                        if type(enemy) == Enemy:
                            if self.player.x == j and self.player.y == i:
                                ceil = '#'
                            else:
                                ceil = 'E'
                        elif type(enemy) == Chest:
                            ceil = 'C'
                stri += ceil+' '
            field.append(stri)
        return field

    def enemy_spawn(self, pos='random'):
        if pos == 'random':
            pos = self.free_ceil()
            hp = randint(int(0.4 * self.player.health), int(0.8 * self.player.health))
            dmg = randint(int(0.4 * self.player.damage), int(0.8 * self.player.damage))
            self.enemies.append(Enemy(pos=pos, health=hp, damage=dmg))

    def chest_spawn(self, pos='random'):
        if pos == 'random':
            pos = self.free_ceil()
            self.enemies.append(Chest(pos[0], pos[1]))

    def update(self, arg):
        result = ''
        self.player.move(arg)
        if self.player.healing(arg):
            self.enemy_spawn()
        colide_with = None
        for enemy in self.enemies:
            if enemy.colide(self.player):
                colide_with = enemy
                enemy.attack(self.player)
                if type(enemy) == Chest:
                    self.enemies.remove(enemy)
                    colide_with = None
                    continue
                if arg == 'attack':
                    self.player.attack(enemy)
                if not self.player.is_a_live():
                    return False
                if not enemy.is_a_live():
                    self.player.health += int(enemy.damage * 1.5)
                    self.player.damage += int(enemy.damage * 0.4)
                    self.enemies.remove(enemy)
                    self.enemy_spawn()
                    if randint(0, 4) == 0:
                        self.chest_spawn()
                    colide_with = None
        return (self.player_ui.show(colide_with), self.show_field())

    def run(self):
        def write(screen, text, pos, size=36):
            f1 = pygame.font.Font(None, size)
            text = f1.render(text, 1, (255, 255, 255))
            screen.blit(text, pos)

        pygame.init()
        size = [800, 600]
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        update = False
        bind_keys = {
            pygame.K_w: 'w',
            pygame.K_a: 'a',
            pygame.K_s: 's',
            pygame.K_d: 'd',
            pygame.K_h: 'healing',
            pygame.K_SPACE: 'attack',
        }

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP and event.key in bind_keys:
                    update = True
            if update:
                screen.fill((0, 0, 0))
                ui, field = self.update(bind_keys[event.key])
                for y, s in enumerate(ui):
                    write(screen, s, (10, y*30+10))
                for y, s in enumerate(field):
                    write(screen, s, (100, y*30+100))
                pygame.time.wait(30)
                pygame.display.update()
                update = False
        pygame.quit()

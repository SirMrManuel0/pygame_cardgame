from sympy.codegen.ast import continue_
from sympy.codegen.fnodes import dimension
from torch.distributed.elastic.multiprocessing.redirects import get_libc

import game
from game.gui.objects import BaseObject
from pylix.algebra import Vector
from game.gui import globals
import pygame
import math
import random

def grn(start, end):
    return random.randint(start, end)

def random_unit_circle(a1, a2):
    a = grn(a1, a2)
    return Vector([math.cos(math.radians(a)), math.sin(math.radians(a))])

class Ghost(BaseObject):
    def __init__(self):
        super().__init__()
        self._speed = 600
        self._position = Vector(dimension=2)
        self._velocity = Vector([200, 200])
        self._img = pygame.image.load(game.get_path_resource("ghosts", "ghost-4"))
        self._scale = 0.2

        original_width, original_height = self._img.get_size()
        self._img = pygame.transform.scale(self._img, (original_width * self._scale, original_height * self._scale))

        self._delay = 1
        self._animation = False
        self.get_random_position_velocity()

    def draw(self, screen):
        surface = pygame.Surface(self._img.get_size(), pygame.SRCALPHA)
        self._img = self._img.convert_alpha()
        self._img.set_alpha(128)
        surface.blit(self._img, self._position.get_data())
        screen.blit(self._img, self._position.get_data())


    def left_the_screen(self):
        if self._position[0] > globals.SIZE[0]:
            return True
        if self._position[1] > globals.SIZE[1]:
            return True
        if self._position[0] < -1 * self._img.get_size()[0]:
            return True
        if self._position[1] < -1 * self._img.get_size()[1]:
            return True

        return False

    def get_random_position_velocity(self):
        self._side = grn(0, 3)

        #left
        if self._side == 0:
            self._position = Vector([-1 * self._img.get_size()[0], grn(0, int(globals.SIZE[1] - self._img.get_size()[1]))])
            self._velocity = random_unit_circle(120, 240) * grn(self._speed, self._speed + 50) * -1
        #right
        elif self._side == 1:
            self._position = Vector([globals.SIZE[0], grn(0, int(globals.SIZE[1] - self._img.get_size()[1]))])
            self._velocity = random_unit_circle(300, 420) * grn(self._speed, self._speed + 50) * -1
            #top
        elif self._side == 2:
            self._position = Vector([grn(0, int(globals.SIZE[0] - self._img.get_size()[0])), -1 * self._img.get_size()[1]])
            self._velocity = random_unit_circle(210, 330) * grn(self._speed, self._speed + 50) * -1
            #bottom
        elif self._side == 3:
            self._position = Vector([grn(0, int(globals.SIZE[0] - self._img.get_size()[0])), globals.SIZE[1]])
            self._velocity = random_unit_circle(30, 150) * grn(self._speed, self._speed + 50) * -1


    def update_animation(self, dt):
        if self._delay > 0:
            self._delay = self._delay - dt
            return

        self._position = self._position + (dt * self._velocity)

        if self.left_the_screen() and self._animation:
            self._delay = grn(5, 20)

            self._img = pygame.image.load(game.get_path_resource("ghosts", "ghost-" + str(grn(1, 12))))

            original_width, original_height = self._img.get_size()
            self._img = pygame.transform.scale(self._img, (original_width * self._scale, original_height * self._scale))

            self.get_random_position_velocity()
            self._animation = False

        if not self.left_the_screen():
            self._animation = True

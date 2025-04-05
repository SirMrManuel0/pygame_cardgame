from pylix.algebra import Vector, Matrix
from game.gui import globals
from game.gui.objects import BaseObject
import pygame
import random
import math


def grn(start, end):
    return random.randint(start, end)

# anlges in degree
def random_unit_circle(a1, a2):
    a = grn(a1, a2)
    return Vector([math.cos(math.radians(a)), math.sin(math.radians(a))])

class Particle():
    def __init__(self, position, velocity, radius,delay, color):
        self._position = position
        self._velocity = velocity
        self._color = Vector([0, 200, 200])
        self._forces = [Vector([0, 400])]
        self._radius = radius
        self._delay = delay
        self._color = color

    def update(self, dt):
        if self._delay > 0:
            self._delay -= dt
            return

        for force in self._forces:
            self._velocity = self._velocity + (dt * force)

        self._position = self._position + (dt * self._velocity)

    def draw(self, screen):
        if self._delay > 0:
            return

        pygame.draw.circle(screen,
                           self._color,
                           self._position.get_data(),
                           self._radius)

class Fireworks(BaseObject):
    def __init__(self, size, base_position, angle_from_to):
        super().__init__()
        self._particles = []
        self._size = size
        self._base_position = base_position
        self._angle_from_to = angle_from_to
        print(self._angle_from_to[0], self._angle_from_to[1])
        self._color_palette = [(206, 32, 41), (255, 252, 175), (255, 225, 124), (255, 102, 75), (144, 56, 67)]

        for i in range(self._size):
            randomDir = random_unit_circle(int(self._angle_from_to[0]), int(self._angle_from_to[1]))
            randomVel = grn(-750, -550)
            randomDelay = grn(1, 100) / 50
            randomColor = grn(0, len(self._color_palette) - 1)

            self._particles.append(Particle(
                self._base_position,
                randomVel * randomDir,
                3 + 2 * ((-550 - randomVel) / 200),
                randomDelay,
                self._color_palette[randomColor]
            ))


    def draw(self, screen):
        for particle in self._particles:
            particle.draw(screen)

    def update_animation(self, dt):
        for particle in self._particles:
            particle.update(dt)




import pygame

from game.logic import CaboLogic

pygame.init()
canvas = pygame.display.set_mode((1920, 1080))

# TITLE OF CANVAS
pygame.display.set_caption("My Board")
exit = False

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()

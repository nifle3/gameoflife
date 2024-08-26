from typing import Final

import pygame

SCREEN_WIDTH: Final[int] = 1280
SCREEN_HEIGHT: Final[int] = 720

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT,))
clock = pygame.time.Clock()
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False            

    screen.fill('purple')

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
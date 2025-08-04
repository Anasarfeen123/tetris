import pygame, sys
import grid as gd
import blocks as bk

pygame.init()
screen = pygame.display.set_mode((1980//2, 1980//2))
pygame.display.set_caption('TETRIS')
(width, height) = pygame.display.get_window_size()
print("Debug: ",width, height)
clock = pygame.time.Clock()
Running = True
grid = gd.Grid((25, 10), screen)
block = bk.blocks(grid)
speed = 2
fast_speed = 10
down_held = False

while Running:
    screen.fill((0, 0, 40))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                block.move((-1, 0))
            elif event.key == pygame.K_RIGHT:
                block.move((1, 0))
            elif event.key == pygame.K_DOWN:
                down_held = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                down_held = False

    current_speed = speed + fast_speed if down_held else speed
    block.update(current_speed)

    block.draw_shape()
    grid.draw_grid()
    pygame.display.flip()

    if block.end():
        block = bk.blocks(grid)

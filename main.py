import pygame, sys, time
import grid as gd
import blocks as bk
pygame.init()
pygame.mixer.init()
BG = pygame.mixer.Sound(file="bg.mp3")
FG = pygame.mixer.Sound(file="fg.mp3")
FG2 = pygame.mixer.Sound(file="fg2.mp3")
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1025
RUNNING = True
RESTART = False
CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TETRIS')

GRID = gd.Grid((25, 10), SCREEN)
BLOCK = bk.blocks(GRID, pygame.time)
SPEED = 2
FAST_SPEED = 10
DOWN_HELD = False
HORIZONTAL_MOVE_DELAY = 120
PAUSED = False
GHOST = True
DEBUG_MODE = False
last_horizontal_move_time = 0

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)

font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 16)

raw_array = BG.get_raw()
raw_array = raw_array[:-700000]
cut_sound = pygame.mixer.Sound(buffer=raw_array)
cut_sound.set_volume(0.3)

raw_array = FG.get_raw()
cut_sound_2 = pygame.mixer.Sound(buffer=raw_array)
cut_sound.play(-1)

raw_array = FG2.get_raw()
cut_sound_3 = pygame.mixer.Sound(buffer=raw_array)
while RUNNING:
    horizontal_move_occurred = False
    
    Score = font.render(f'Score: {GRID.score}', True, green)
    textRect = Score.get_rect()
    textRect.topleft = (10, 10)
    
    Next = font.render(f'Next: {BLOCK.next_shape_name}', True, BLOCK.next_color)
    textRect2 = Next.get_rect()
    textRect2.topright = ((SCREEN_WIDTH)-10, 10)
    
    Instruct = font2.render(f'SPACE: Pause/Play  V: SMASH DOWN ', True, red)
    Instruct2 = font2.render(f'Left/Right Arrows: Controls Esc/q: Exit UP Arrow: Rotate', True, red)
    textRect4 = Instruct.get_rect()
    textRect5 = Instruct2.get_rect()
    textRect4.bottomright = ((SCREEN_WIDTH)-10, SCREEN_HEIGHT-50)
    textRect5.bottomright = ((SCREEN_WIDTH)-10, SCREEN_HEIGHT-20)
    
    if PAUSED:
        Pause = font.render(f'PAUSED', True, red)
    else:
        Pause = font.render('', True, red)
    textRect3 = Pause.get_rect()
    textRect3.center = ((SCREEN_WIDTH)//2, (SCREEN_HEIGHT)-10)
    
    SCREEN.fill((0, 0, 40))
    CLOCK.tick(60)
    current_time = pygame.time.get_ticks()
    
    if DEBUG_MODE:
        BLOCK.test()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                DOWN_HELD = True
            if event.key == pygame.K_v:
                BLOCK.smash_down()
            elif event.key == pygame.K_ESCAPE:
                RUNNING = False
            elif event.key == pygame.K_UP:
                if DEBUG_MODE: print("DEBUG: Rotation initialised")
                BLOCK.rotate()
            elif event.key == pygame.K_q:
                RUNNING = False
            elif event.key == pygame.K_r:
                RESTART = True
            elif event.key == pygame.K_x:
                DEBUG_MODE = not DEBUG_MODE
            elif event.key == pygame.K_e:
                GHOST = not GHOST
            elif event.key == pygame.K_SPACE:
                PAUSED = not PAUSED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                DOWN_HELD = False
            
    keys = pygame.key.get_pressed()
    if current_time - last_horizontal_move_time > HORIZONTAL_MOVE_DELAY:
        if keys[pygame.K_LEFT]:
            BLOCK.move((-1, 0))
            last_horizontal_move_time = current_time
            horizontal_move_occurred = True
        elif keys[pygame.K_RIGHT]:
            BLOCK.move((1, 0))
            last_horizontal_move_time = current_time
            horizontal_move_occurred = True
    
    if GHOST:
        ghost_coords = BLOCK.get_ghost_position()
        GRID.draw_ghost_cells(ghost_coords, BLOCK.color)    

    current_speed = SPEED + FAST_SPEED if DOWN_HELD else SPEED
    if not PAUSED:
        BLOCK.update(current_speed)
        GRID.draw_locked()
        BLOCK.draw_shape()
        GRID.draw_grid()
        SCREEN.blit(Score, textRect)
        SCREEN.blit(Next, textRect2)
        SCREEN.blit(Instruct, textRect4)
        SCREEN.blit(Instruct2, textRect5)
        pygame.display.flip()
        BLOCK.end()
    else:
        GRID.draw_locked()
        BLOCK.draw_shape()
        GRID.draw_grid()
        SCREEN.blit(Score, textRect)
        SCREEN.blit(Next, textRect2)
        SCREEN.blit(Pause, textRect3)
        SCREEN.blit(Instruct, textRect4)
        SCREEN.blit(Instruct2, textRect5)
        pygame.display.flip()
    
    if BLOCK.locked or RESTART:
        sound_play = GRID.clear_line(DEBUG_MODE)
        if sound_play:
            cut_sound_3.play()
        else:
            cut_sound_2.play()
    
        if BLOCK.locked:
            # Save the old block's "next piece" info
            shape_for_new_block = BLOCK.next_shape_name
            color_for_new_block = BLOCK.next_color

            # Create the new block with the correct shape and color from the start
            BLOCK = bk.blocks(GRID, pygame.time, shape_name=shape_for_new_block, color=color_for_new_block)

        if RESTART:
            GRID.locked_cells = {}
            GRID.score = 0
            BLOCK = bk.blocks(GRID, pygame.time) 
            RESTART = False
    if BLOCK.game_over:
        PAUSED = True
        GRID.score = 0
        RESTART = True

# Music by 
# <a href="https://pixabay.com/users/djartmusic-46653586/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=301278">
# Krzysztof Szymanski</a> 
# from <a href="https://pixabay.com/music//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=301278">Pixabay</a>
# Sound Effect by 
# <a href="https://pixabay.com/users/floraphonic-38928062/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=229503">
# floraphonic</a> 
# from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=229503">Pixabay</a>
# <a href="https://pixabay.com/users/floraphonic-38928062/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=224394">
# floraphonic</a> 
# from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=224394">Pixabay</a>
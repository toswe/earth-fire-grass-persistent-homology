# Generated with chat GPT4
# Link to conversation:
# https://chat.openai.com/share/aaf73e8c-60b2-47c9-8102-f1299bfd00a2

import pygame
import utils

SCREEN_SIZE = (500, 600)
N = 25
matrix = [[0 for j in range(N)] for i in range(N)]

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

GREEN_SQUARE_CHANGE_FREQ = 1000
BLACK_SQUARE_CHANGE_FREQ = 500

green_square_last_change_time = pygame.time.get_ticks()
black_square_last_change_time = pygame.time.get_ticks()

font = pygame.font.Font(None, 30)
text_color = (255, 255, 255)

active_color = 1  # start with red

timer_running = True
timer_last_toggled_time = pygame.time.get_ticks()

def handle_key_press(key):
    global active_color, timer_running, timer_last_toggled_time
    if key == pygame.K_r:
        active_color = 1
    elif key == pygame.K_g:
        active_color = 2
    elif key == pygame.K_b:
        active_color = 3
    elif key == pygame.K_SPACE:
        if timer_running:
            timer_running = False
        else:
            timer_running = True
        timer_last_toggled_time = pygame.time.get_ticks()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row = pos[1] // utils.CELL_SIZE
            col = pos[0] // utils.CELL_SIZE
            matrix[row][col] = active_color
        elif event.type == pygame.KEYDOWN:
            handle_key_press(event.key)

    current_time = pygame.time.get_ticks()
    if timer_running:
        if current_time - green_square_last_change_time >= GREEN_SQUARE_CHANGE_FREQ:
            for i in range(N):
                for j in range(N):
                    if matrix[i][j] == 2:
                        matrix[i][j] = 0
            green_square_last_change_time = current_time
        if current_time - black_square_last_change_time >= BLACK_SQUARE_CHANGE_FREQ:
            for i in range(N):
                for j in range(N):
                    if matrix[i][j] == 1:
                        matrix[i][j] = 0
            black_square_last_change_time = current_time

    utils.draw_matrix(screen, matrix)

    tick_surface = font.render("Tick: " + str(current_time), True, text_color)
    screen.blit(tick_surface, (10, 10))

    if timer_running:
        status_surface = font.render("Timer: Running", True, text_color)
    else:
        status_surface = font.render("Timer: Stopped", True, text_color)
    screen.blit(status_surface, (10, 40))

    desc_surface = font.render("Press 'r' for red, 'g' for green, 'b' for blue, and spacebar to start/stop timer", True, text_color)
    screen.blit(desc_surface, (10, 70))

    pygame.display.flip()

pygame.quit()

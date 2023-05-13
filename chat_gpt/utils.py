import pygame

# Define some colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_matrix(screen, matrix, cell_size):
    """Draws the matrix on the screen."""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            color = BLACK
            if matrix[i][j] == 1:
                color = RED
            elif matrix[i][j] == 2:
                color = GREEN
            pygame.draw.rect(screen, color, [j * cell_size, i * cell_size, cell_size, cell_size])
import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CELL_SIZE = 20

def draw_matrix(screen, matrix):
    """Draws the matrix on the screen."""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            color = BLACK
            if matrix[i][j] == 1:
                color = RED
            elif matrix[i][j] == 2:
                color = GREEN
            pygame.draw.rect(screen, color, [j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE])

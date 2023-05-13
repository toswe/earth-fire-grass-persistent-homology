import pygame

def handle_key_press():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        return "RED"
    elif keys[pygame.K_g]:
        return "GREEN"
    elif keys[pygame.K_b]:
        return "BLUE"
    elif keys[pygame.K_SPACE]:
        return "PAUSE"
    return None

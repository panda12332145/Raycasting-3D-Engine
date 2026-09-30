import math
import os
import pygame
from .renderer import WIDTH, HEIGHT, FPS, cast_rays, draw_2d_minimap
from .world import is_wall, TILE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTURE_PATH = os.path.join(ROOT, "data", "texture.png")
PLAYER_SPEED = 3
PLAYER_ROTATION = 0.07


def handle_movement(keys, px, py, angle):
    dx, dy = 0, 0
    if keys[pygame.K_w]:
        dx += PLAYER_SPEED * math.cos(angle)
        dy += PLAYER_SPEED * math.sin(angle)
    if keys[pygame.K_s]:
        dx -= PLAYER_SPEED * math.cos(angle)
        dy -= PLAYER_SPEED * math.sin(angle)
    if keys[pygame.K_a]:
        angle -= PLAYER_ROTATION
    if keys[pygame.K_d]:
        angle += PLAYER_ROTATION
    new_x = px + dx if not is_wall(px + dx, py) else px
    new_y = py + dy if not is_wall(px, py + dy) else py
    return new_x, new_y, angle


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Raycasting 3D Engine")
    clock = pygame.time.Clock()

    try:
        texture = pygame.image.load(TEXTURE_PATH)
        texture = pygame.transform.scale(texture, (TILE, TILE))
    except Exception:
        texture = pygame.Surface((TILE, TILE))
        texture.fill((180, 80, 50))

    player_x, player_y, player_angle = 150.0, 150.0, 0.0

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        keys = pygame.key.get_pressed()
        player_x, player_y, player_angle = handle_movement(keys, player_x, player_y, player_angle)
        cast_rays(screen, player_x, player_y, player_angle, texture)
        draw_2d_minimap(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

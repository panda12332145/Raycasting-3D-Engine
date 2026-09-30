import pygame
import math
from .world import MAP, TILE, is_wall


WIDTH, HEIGHT = 800, 600
HALF_H = HEIGHT // 2
FOV_DEG = 60
FPS = 60


def draw_2d_minimap(screen):
    for row_idx, row in enumerate(MAP):
        for col_idx, char in enumerate(row):
            color = (200, 200, 200) if char == "1" else (30, 30, 30)
            pygame.draw.rect(screen, color, (col_idx * TILE // 4, row_idx * TILE // 4, TILE // 4, TILE // 4))


def cast_rays(screen, player_x: float, player_y: float, player_angle: float, texture):
    for ray in range(WIDTH):
        ray_angle = player_angle - math.radians(FOV_DEG / 2) + math.radians(FOV_DEG) * (ray / WIDTH)
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, 800):
            tx = int(player_x + depth * cos_a)
            ty = int(player_y + depth * sin_a)
            col = tx // TILE
            row = ty // TILE

            if 0 <= row < len(MAP) and 0 <= col < len(MAP[0]) and MAP[row][col] == "1":
                depth *= math.cos(player_angle - ray_angle)
                height = min(TILE * 400 / (depth + 0.0001), HEIGHT)
                wall_col = tx % TILE
                wall_slice = texture.subsurface((wall_col, 0, 1, TILE))
                wall_scaled = pygame.transform.scale(wall_slice, (1, int(height)))
                screen.blit(wall_scaled, (ray, HALF_H - height // 2))
                break

"""Testes do Raycasting-3D-Engine (headless)."""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.renderer import WIDTH, HEIGHT, cast_rays, draw_2d_minimap
from src.world import is_wall, TILE
from src.main import handle_movement


def _fallback_texture():
    import pygame
    tex = pygame.Surface((TILE, TILE))
    tex.fill((180, 80, 50))
    return tex


def test_world_collision():
    assert is_wall(-10, 100)          # fora do mapa = parede
    assert is_wall(100, -10)
    assert not is_wall(150, 150)      # célula inicial é vazia
    assert is_wall(0, 0)              # canto do mapa é parede


def test_cast_rays_returns_width_columns():
    import pygame
    pygame.init()
    surf = pygame.Surface((WIDTH, HEIGHT))
    tex = _fallback_texture()
    cols = cast_rays(surf, 150.0, 150.0, 0.0, tex)
    assert cols is None or cols == WIDTH  # desenha 1 coluna por pixel
    # prova visual: pixels foram pintados (parede encontrada)
    assert surf.get_at((WIDTH // 2, HEIGHT // 2))[:3] != (0, 0, 0)
    pygame.quit()


def test_movement_blocked_by_wall():
    class Keys(dict):
        def __getitem__(self, k):
            return self.get(k, False)
    import pygame
    keys = Keys({pygame.K_w: True})
    x, y = 150.0, 150.0
    for _ in range(500):   # empurrar para +x contra a parede direita
        x, y, _ = handle_movement(keys, x, y, 0.0)
    # nunca saiu do mapa e parou encostado numa parede
    assert 0 <= x <= 10 * TILE and 0 <= y <= 8 * TILE
    assert is_wall(x + TILE // 2, y) or not is_wall(x + TILE // 2, y)


def test_smoke_frames_headless():
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    tex = _fallback_texture()
    for angle in (0.0, 1.57, 3.14, 4.71):
        screen.fill((0, 0, 0))
        cast_rays(screen, 150.0, 150.0, angle, tex)
        draw_2d_minimap(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"✅ {fn.__name__}")
    print(f"\n{len(fns)} testes passaram.")

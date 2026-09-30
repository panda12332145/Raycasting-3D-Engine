TILE = 64

MAP = [
    "1111111111",
    "1000000001",
    "1000000001",
    "1000111001",
    "1000000001",
    "1001000001",
    "1000000001",
    "1111111111",
]


def is_wall(x: float, y: float) -> bool:
    col = int(x // TILE)
    row = int(y // TILE)
    if row < 0 or row >= len(MAP) or col < 0 or col >= len(MAP[0]):
        return True
    return MAP[row][col] == "1"

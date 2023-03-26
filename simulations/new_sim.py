import pygame
from e2 import main

pygame.init()

def grid_to_window_coordinates(path, rows, columns, window_width=900, window_height=900):
    cell_width = window_width / float(columns)
    cell_height = window_height / float(rows)
    rect_size = min(cell_width, cell_height)

    window_coordinates = []
    for point in path:
        x = point.x * cell_width + (cell_width - rect_size) / 2
        y = point.y * cell_height + (cell_height - rect_size) / 2
        window_coordinates.append((x, y))

    return window_coordinates

# ASCII grid
grid = [
    "@_#_____",
    "___#____",
    "_#______",
    "___##___",
    "_____#__",
    "_#_#__#_",
    "___#____",
    "__#__G__",
]

# Window dimensions and grid size
width, height = 900, 900
grid_size = 8
rows = 8
columns = 8

# Calculate cell size
cell_width = width // grid_size
cell_height = height // grid_size

# Initialize Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ASCII to Pygame")

# Rectangle and circle sizes
rect_size = min(cell_width, cell_height)
circle_radius = rect_size // 4

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for row in range(grid_size):
        for col in range(grid_size):
            char = grid[row][col]
            x, y = col * cell_width, row * cell_height

            if char == "#":
                pygame.draw.rect(screen, (0, 0, 0), (x + (cell_width - rect_size) // 2, y + (cell_height - rect_size) // 2, rect_size, rect_size))

    # Draw path
    path = main(grid)
    print(path)
    full_path = grid_to_window_coordinates(path, rows, columns)
    pygame.draw.lines(screen, (0, 0, 255), False, full_path, 3)

    for row in range(grid_size):
        for col in range(grid_size):
            char = grid[row][col]
            x, y = col * cell_width, row * cell_height

            if char == "@":
                pygame.draw.circle(screen, (255, 0, 0), (x + cell_width // 2, y + cell_height // 2), circle_radius)
            elif char == "G":
                pygame.draw.circle(screen, (0, 255, 0), (x + cell_width // 2, y + cell_height // 2), circle_radius)

    pygame.display.flip()

pygame.quit()

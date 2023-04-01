import pygame
from e3 import main
import sys
import logging

pygame.init()

#def path_points_to_window_coordinates(obstacles, path_points, rows, columns, window_width=900, window_height=900):
    #cell_width = window_width / columns
    #cell_height = window_height / rows
    
    #def grid_to_window(point):
        #x = point.x * cell_width + cell_width // 2
        #y = point.y * cell_height + cell_height // 2
        #return (x, y)
    
    #window_coordinates = []
    #for path_point in path_points:
        #found = False
        #for obstacle in obstacles:
            #for i, obstacle_point in enumerate(obstacle):
                #if path_point.x == obstacle_point[0] and path_point.y == obstacle_point[1]:
                    #found = True
                    #window_coordinates.append(obstacle[i % 4])
                    #break
            #if found:
                #break
        
        #if not found:
            #window_coordinates.append(grid_to_window(path_point))

    #return window_coordinates

def path_points_to_window_coordinates(path_points, rows, columns, window_width, window_height):
    cell_width = window_width / columns
    cell_height = window_height / rows

    def grid_to_window(point):
        x = point.x * cell_width + cell_width // 2
        y = point.y * cell_height + cell_height // 2
        return (x, y)

    window_coordinates = []
    for path_point in path_points:
        window_coordinates.append(grid_to_window(path_point))

    return window_coordinates

def select_obstacle_points(path_points, obstacles, grid):
    print(path_points)
    selected_points = []

    def find_obstacle_point(row, col, position):
        for obstacle in obstacles:
            obstacle_tl, obstacle_tr, obstacle_bl, obstacle_br = obstacle
            obstacle_col = int(obstacle_tl[0] // cell_width)
            obstacle_row = int(obstacle_tl[1] // cell_height)

            if obstacle_col == col and obstacle_row == row:
                if position == 'tl':
                    return obstacle_tl
                elif position == 'tr':
                    return obstacle_tr
                elif position == 'bl':
                    return obstacle_bl
                elif position == 'br':
                    return obstacle_br

        return None

    for point in path_points:
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == "#" and row >= 0 and col >= 0:
                    if point.x == row and point.y == col + 1:
                        selected_points.append(find_obstacle_point(row, col, 'tr'))
                    elif point.x == row+1 and point.y == col:
                        selected_points.append(find_obstacle_point(row, col, 'bl'))
                    elif point.x == row+1 and point.y == col+1:
                        selected_points.append(find_obstacle_point(row, col, 'br'))
                    elif point.x == row and point.y == col:
                        selected_points.append(find_obstacle_point(row, col, 'tl'))
    print(selected_points)
    return selected_points


# ASCII grid

grid_ = [
    "__@_###########",
    "_#__________##_",
    "___#___________",
    "##____#########",
    "__#__##_____###",
    "#__#__________#",
    "_____##_____G##",
    "__##____#____##",
    "###############",
]

grid_2 = [
    "#@_________##_",
    "#__#_##____#__",
    "#_##__#______#",
    "#__##________#",
    "#_##__#__#__G#",
    "##############",
]

grid = [
    "@__##_#_______",
    "#__#___#______",
    "_#____#______#",
    "_##______##___",
    "#____________#",
    "##_###_#_____#",
    "#_#_____#___G#",
    "##############",
]

# Window dimensions and grid size
#res = pygame.display.Info()
#screen_width = res.current_w
#screen_height = res.current_h
#width, height = 5000, 1200
#width, height = int(screen_width * 0.8), int(screen_height*0.8)

grid_size = len(grid)
rows = len(grid)
columns = len(grid[0])
#print(rows)
#print(columns)
# Calculate cell size
cell_width = 50
cell_height = 50

width = columns * cell_width
height = rows * cell_height

# Initialize Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ASCII to Pygame")

# Rectangle and circle sizes
rect_size = min(cell_width, cell_height)
circle_radius = rect_size // 4

# Path coordinates
agent_location = None
goal_location = None

font_size = 20
font = pygame.font.Font(None, font_size)
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    obstacles = []
    for row in range(grid_size):
        for col in range(columns):
            char = grid[row][col]
            #print(str(row) + "," + str(col))
            x, y = col * cell_width, row * cell_height

            if char == "#":
                temp = []
                pygame.draw.rect(screen, (0, 0, 0), (x + (cell_width - rect_size) // 2, y + (cell_height - rect_size) // 2, rect_size, rect_size))
                #obstacles.append(pygame.Rect(x + (cell_width - rect_size) // 2, y + (cell_height - rect_size) // 2, rect_size, rect_size))
                rect_x = x + (cell_width - rect_size) // 2
                rect_y = y + (cell_height - rect_size) // 2

                # Calculate the coordinates of the four points
                point1 = (rect_x, rect_y)
                point2 = (rect_x + rect_size, rect_y)
                point3 = (rect_x, rect_y + rect_size)
                point4 = (rect_x + rect_size, rect_y + rect_size)

                temp.append(point1)
                temp.append(point2)
                temp.append(point3)
                temp.append(point4)
                obstacles.append(temp)
                # Draw small circles at the calculated coordinates
            elif char == "@":
                pygame.draw.circle(screen, (255, 0, 0), (x + cell_width // 2, y + cell_height // 2), circle_radius)
                agent_location = (x + cell_width // 2, y + cell_height // 2)
            elif char == "G":
                pygame.draw.circle(screen, (0, 255, 0), (x + cell_width // 2, y + cell_height // 2), circle_radius)
                goal_location = (x + cell_width // 2, y + cell_height // 2)
    #print(agent_location)
    #print(goal_location)
    #sys.exit(1)
    # Draw path
    # Automate path with A* in solver function
    if agent_location and goal_location:
        #full_path = [agent_location] + path_screen_coords + [goal_location]
        path, dynamic_obstacles = main(grid)
        print(path)
        full_path = [agent_location] + select_obstacle_points(path[1:len(path)-1], obstacles, grid) + [goal_location]
        print(full_path)
        print(obstacles)
        print(dynamic_obstacles)
        pygame.draw.lines(screen, (0, 0, 255), False, full_path, 3)
        dynamic_color = (255, 0, 255)
        for ob in dynamic_obstacles:
          row, col = ob["location"]
          x, y = col * cell_width, row * cell_height
          pygame.draw.rect(screen, dynamic_color, (x + (cell_width - rect_size) // 2, y + (cell_height - rect_size) // 2, rect_size, rect_size))
          emergence_text = font.render(str(ob["emergence"]), True, (0, 0, 0))
          text_width, text_height = emergence_text.get_size()
          text_x = x + (cell_width - text_width) // 2
          text_y = y + (cell_height - text_height) // 2
          screen.blit(emergence_text, (text_x, text_y))
    
    pygame.display.flip()

pygame.quit()

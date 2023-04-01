import sys
import pyvisgraph as vg
import argparse
from collections import defaultdict
import heapq as heap
import operator as op
import shapely.geometry as geometry
import random
import math

def findLocation(state, target):
  return [ [x, y] for x, row in enumerate(state) for y, i in enumerate(row) if target in i ]

def connect_points(points):
  edges = []

  for i in range(len(points)):
    for j in range(i + 1, len(points)):
      edges.append((points[i], points[j]))

  return edges

def is_interior(p):
  if p != int(p):
    return True

def random_obstacles(row, column, environment, start, goal, blocked):
  dynamic_obstacles = []
  #num_obstacles = random.randint(3, 5)
  num_obstacles = 2 
  for i in range(num_obstacles):
    obstacle_placed = False
    while not obstacle_placed:
      # generate obstacle location
      cur_obstacle = [random.randint(0, row-1), random.randint(0, column-1)]
      print(cur_obstacle)
      if cur_obstacle == start[0] or cur_obstacle == goal[0]:
        continue
      if cur_obstacle in blocked:
        continue
      if cur_obstacle[1] > len(environment[cur_obstacle[0]]):
        continue
      for existing in dynamic_obstacles:
        if cur_obstacle == existing:
          break
      else:
        # valid dynamic obstacles
        dynamic_obstacles.append(cur_obstacle)
        obstacle_placed = True
  return dynamic_obstacles

def check_collision(edge, obstacles):
  print(edge)
  line = geometry.LineString([(edge[0].x, edge[0].y), (edge[1].x, edge[1].y)])
  for ob in obstacles:
    p = geometry.Polygon([[ob[0], ob[1]], [ob[0], ob[1]+1], [ob[0]+1, ob[1]+1], [ob[0]+1, ob[1]]])
    inter = line.intersection(p)
    print(inter)
    inter_points = list(inter.coords)
    print(inter_points)
    if len(inter_points) > 2:
      return True
    elif len(inter_points) == 2:
      if ( is_interior(inter_points[0][0]) or is_interior(inter_points[0][1]) or is_interior(inter_points[1][0]) or is_interior(inter_points[1][1]) ) or ( [inter_points[0][0], inter_points[0][1]] in obstacles or [inter_points[1][0], inter_points[1][1]] in obstacles ) or ( inter_points[0][0] != inter_points[1][0] and inter_points[0][1] != inter_points[1][1] ):
        return True
  return False

def heuristic(node, goal):
  return abs(node.x - goal.x) + abs(node.y - goal.y)

def build_dict(seq, key):
  return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def get_neighbors(current, graph, dynamic_list):
  neighbors = []
  for edge in graph:
    if edge['blocked']:
      continue
    if edge['edge'][0] == current:
      neighbor = edge['edge'][1]
      blocked_dynamic = False
      for ob in dynamic_list:
        if check_collision((current, neighbor), [ob]):
          blocked_dynamic = True
          break
      if not blocked_dynamic:
        cost = abs(current.x - neighbor.x) + abs(current.y - neighbor.y)
        neighbors.append((neighbor, cost))
  return neighbors

# not finding dynamic obstacle on one edge of path
#def validate_path(path, graph, dynamic_obstacles):
  #valid_path = [path[0]]
  #print("Validate Path")
  #print(path)
  #i = 0
  #while i < len(path)-1:
    #print(i)
    #print(valid_path)
    #current_pos = valid_path[-1]
    #next_pos = path[i+1]
    #print("Current")
    #print(current_pos)
    #print("Next")
    #print(next_pos)
    #collision = False
    #for obstacle in dynamic_obstacles:
      #print("Obstacle")
      #print(obstacle)
      #print("CURRENT PATH")
      #print(valid_path)
      #if check_collision((current_pos, next_pos), [d for d in dynamic_obstacles]):
        #print("COLLISION- PATH MUST CHANGE")
        #print(current_pos)
        #print(next_pos)
        #find_blocked = build_dict(graph, key="edge")
        #edge_blocked = find_blocked.get((current_pos, next_pos))
        #if edge_blocked is not False:
          #graph[edge_blocked['index']]['blocked'] = True
        
        #new_path = astar(current_pos, path[-1], graph)
        # check for no valid path as no solution case
        #if new_path is not None:
          #collision_index = i + 1
          #while collision_index < len(path) - 1 and check_collision((current_pos, path[collision_index + 1]), [obstacle]):
            #collision_index += 1
          #valid_path = valid_path[:-1] + new_path[new_path.index(current_pos) : new_path.index(path[collision_index]) + 1]
          #i = collision_index - 1
	
          #collision = True
        #if collision:
          #break
        #if new_path is None:
          #print("Environment unsolvable")
          #print(dynamic_obstacles)
          #sys.exit(1)
    #if not collision:
      #valid_path.append(next_pos)
      #i += 1
  #return valid_path

def validate_path(path, graph, dynamic_obstacles):
    valid_path = [path[0]]
    i = 0
    while i < len(path) - 1:
        current_pos = valid_path[-1]
        next_pos = path[i + 1]
        collision = False
        for obstacle in dynamic_obstacles:
            if check_collision((current_pos, next_pos), [d for d in dynamic_obstacles]):
                collision = True
                #print("DYNAMIC COLLISION!")
                for edge in graph:
                  if (edge['edge'][0] == current_pos and edge['edge'][1] == next_pos) or (edge['edge'][0] == next_pos and edge['edge'][1] == current_pos):
                    edge['blocked'] = True
                break
        
        if collision:
            new_path = astar(current_pos, path[-1], graph)
            if new_path is not None:
                valid_new_path = validate_path(new_path, graph, dynamic_obstacles)
                valid_path.extend(valid_new_path[1:])
                break
            else:
                print("Environment unsolvable")
                print(dynamic_obstacles)
                sys.exit(1)
        else:
            valid_path.append(next_pos)
            i += 1
    return valid_path

# math.sqrt is expensive
def euclidean_distance(p1, p2):
  return math.sqrt((p1.x-p2.x) ** 2 + (p1.y - p2.y) ** 2)

def astar(start, goal, graph):
  print("A* Start")
  print(start)
  print(goal)

  open_list = []
  heap.heappush(open_list, (0, start))

  costs = {start: 0}

  parents = {start: None}

  while open_list:
    current = heap.heappop(open_list)[1]

    # returns path when goal is reached
    if current == goal:
      path = [current]
      while parents[current] is not None:
        current = parents[current]
        path.append(current)
      print("Full Path")
      print(path[::-1])
      return path[::-1]
      # find neighbors of current point
    neighbors = []
    for edge in graph:
      if edge['blocked'] == True:
        continue
      if edge['edge'][0] == current:
        neighbors.append(edge['edge'][1])
    for neighbor in neighbors:
      cost = costs[current] + (abs(current.x - neighbor.x) + abs(current.y - neighbor.y))
      if neighbor not in costs or cost < costs[neighbor]:
        costs[neighbor] = cost
        parents[neighbor] = current
        heap.heappush(open_list, (cost + heuristic(neighbor, goal), neighbor))
  print("never got to goal")

def astar_old(start, goal, graph, dynamic_list):
  #print(start)
  #print(goal)

  open_list = []
  heap.heappush(open_list, (0, start))

  costs = {start: 0}

  parents = {start: None}

  while open_list:
    current = heap.heappop(open_list)[1]

    # returns path when goal is reached
    if current == goal:
      path = [current]
      while parents[current] is not None:
        current = parents[current]
        path.append(current)
      print("Full Path")
      print(path[::-1])
      return
    # find neighbors of current point
    neighbors = []
    for edge in graph:
      if edge['blocked'] == True:
        continue
      if edge['edge'][0] == current:
        neighbors.append(edge['edge'][1])
    # check obstacle list for dynamic obstacles
    # expand for smaller g(n)
    # check if an edge exists as a function of g(n)
    for neighbor in neighbors:
      collision = False
      cost = costs[current] + (abs(current.x - neighbor.x) + abs(current.y - neighbor.y))
      for i in range(0, len(dynamic_list)):
        if cost >= dynamic_list[i]['emergence'] and check_collision((current, neighbor), [d.get('location') for d in dynamic_list]):
          print("Collision with Dynamic Obstacle")
          print(current)
          print(neighbor)
          print()
          # change edges with dynamic collision to blocked-find way to look up blocked property of edge in graph list
          find_blocked = build_dict(graph, key="edge")
          edge_blocked = find_blocked.get((current, neighbor))
          print(edge_blocked)
          graph[edge_blocked['index']]['blocked'] = True
          for i in range(0, len(graph)):
            print(graph[i])
          collision = True
          break
      if collision:
        continue
      # distance can equate to time- g(n)
      # True False on blocked spaces can relate to g(n)
      if neighbor not in costs or cost < costs[neighbor]:
        costs[neighbor] = cost
        parents[neighbor] = current
        heap.heappush(open_list, (cost + heuristic(neighbor, goal), neighbor))
      print()
  print("never got to goal")

def full_path(start, goal, graph):
  return astar(start, goal, graph)

def main(env):
  #read in environment
  lines = env
  #for line in sys.stdin:
    #stripped = line.strip()
    #if not stripped: break
    #lines.append(stripped)
  
  #print("---ENVIRONMENT INFO---")
  rows = len(lines)
  print(rows)
  calc_columns = list()
  for i in range(0, len(lines)):
    calc_columns.append(len(lines[i]))

  columns = max(calc_columns)
  print(columns)
  agent = findLocation(lines, "@")
  #find obstacles
  blocked = findLocation(lines, "#")
  goal = findLocation(lines, "G")
  
  print(agent)
  print(blocked)
  print(goal)
  obstacles = list()
  for i in range(0, len(blocked)):
    p = [vg.Point(blocked[i][0], blocked[i][1]), vg.Point(blocked[i][0]+1, blocked[i][1]), vg.Point(blocked[i][0], blocked[i][1]+1), vg.Point(blocked[i][0]+1, blocked[i][1]+1)]
    obstacles.append(p)

  for i in range(0, len(obstacles)):
    for j in range(0, len(obstacles[i])):
      print(obstacles[i][j])

  print("-----------------------------------------------")

  print("---GRAPH INFO---")
  #define dynamic obstacles
  #random #? random locations?
  dynamic_obstacles = [ [1, 6], [2, 3], [4, 5] ]
  #dynamic_obstacles = random_obstacles(rows, columns, lines, agent, goal, blocked)
  print(dynamic_obstacles)
  graph_vertices = list()
  # build meaningful corners for visibility graph
  for i in range(0, len(obstacles)):
    for j in range(0, len(obstacles[i])):
      cur_point = obstacles[i][j]
      
      count = 0
      if [cur_point.x, cur_point.y] in blocked:
        count+=1
      if [cur_point.x + 1, cur_point.y] in blocked:
        count+=1
      if [cur_point.x, cur_point.y + 1] in blocked:
        count+=1
      if [cur_point.x + 1, cur_point.y + 1] in blocked:
        count+=1

      if count <= 1:
        if cur_point not in graph_vertices:
          graph_vertices.append(cur_point)
  final_graph = list()
  for i in range(0, len(graph_vertices)):
    cur_vert = graph_vertices[i]
    count = 0
    for j in range(0, len(obstacles)):
      for k in range(0, len(obstacles[j])):
        if cur_vert == obstacles[j][k]:
          count+=1
    if count == 1:
      if cur_vert.x == rows:
        check_list = [int(cur_vert.x-1), int(cur_vert.y)]
        if check_list not in blocked and vg.Point(cur_vert.x - 1, cur_vert.y) in graph_vertices:
          final_graph.append(cur_vert)
      elif cur_vert.y == columns:
        if [int(cur_vert.x), int(cur_vert.y - 1)] not in blocked and vg.Point(cur_vert.x, cur_vert.y - 1) in graph_vertices:
          final_graph.append(cur_vert)
      else:
        final_graph.append(cur_vert)

  final_graph.insert(0, vg.Point(agent[0][0], agent[0][1]))
  final_graph.append(vg.Point(goal[0][0], goal[0][1]))
  print(final_graph)
  for i in range(0, len(final_graph)):
    print(final_graph[i])
  # connect edges of graph
  edges = connect_points(final_graph)
  #for i in range(0, len(edges)):
    #if [edges[i][0].x, edges[i][0].y] in agent and [edges[i][1].x, edges[i][1].y] in goal:
      #del edges[i]
      #break

  for i in range(0, len(edges)):
    print(edges[i])

  #sys.exit(1)
  print("-----------------------------------------------")
  print("---COLLISION DETECTION---")
  #check and filter out edges with collisions
  final_edges = list()
  for i in range(0, len(edges)):
    cur_check = check_collision(edges[i], blocked)
    print(cur_check)
    print("--------------------------------------")
    if cur_check == False:
      if edges[i] not in final_edges:
        # could add distance value (equivalent to time) -- "this is the current time does the edge exist"
	# current time + time to get to obstacle (may be valid when departing but edge does not exist when reaching destination)
	# calculate distance here since needed for timing
        # use information of when obstacle appears
        # "blocked" not currently updated
        final_edges.append({"edge": edges[i], "blocked": False, "distance": abs(edges[i][0].x-edges[i][1].x) + abs(edges[i][0].y-edges[i][1].y)})
  
  for i in range(len(final_edges)):
    print(final_edges[i])

  print("-----------------------------------------------")
  print("---A*---")
  first_path = astar(final_graph[0], final_graph[len(final_graph)-1], final_edges)
  print(blocked)
  final_path = validate_path(first_path, final_edges, dynamic_obstacles)
  print("Dynamic Obstacles")
  print(dynamic_obstacles)
  print("Original Path")
  print(first_path)
  print("Validated Path")
  print(final_path)
  #print(dynamic_obstacles)
  return first_path, dynamic_obstacles, final_path
if __name__ == "__main__":
  main(env)

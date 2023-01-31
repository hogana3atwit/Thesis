import sys
import pyvisgraph as vg
import argparse
from collections import defaultdict
import heapq as heap
import operator as op
import shapely.geometry as geometry

# define dynamic obstacle (1) - start with putting it somewhere close to the goal at a hardcoded position 
# have to find a way to represent time- "after x time interval, the dynamic obstacle appears"
# distance and time notion in edge list (before calling A*)

def findLocation(state, target):
  return [ [x, y] for x, row in enumerate(state) for y, i in enumerate(row) if target in i ]

def connect_points(points):
  edges = []

  for i in range(len(points)):
    for j in range(i + 1, len(points)):
      edges.append((points[i], points[j]))

  return edges

def check_collision(edge, obstacles):
  print(edge)
  line = geometry.LineString([(edge[0].x, edge[0].y), (edge[1].x, edge[1].y)])
  for ob in obstacles:
    p = geometry.Polygon([[ob[0], ob[1]], [ob[0], ob[1]+1], [ob[0]+1, ob[1]+1], [ob[0]+1, ob[1]]])
    inter = line.intersection(p)
    print(inter)
    inter_points = list(inter.coords)
    print(inter_points)
    if len(inter_points) >= 2:
      return True
  return False

def heuristic(node, goal):
  return abs(node.x - goal.x) + abs(node.y - goal.y)

def astar(start, goal, graph, dynamic_list):
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
        print(path[::-1])
        return
    # find neighbors of current point
    neighbors = []
    for edge in graph:
      if edge['edge'][0] == current:
        neighbors.append(edge['edge'][1])
    # check obstacle list for dynamic obstacles
    # expand for smaller g(n)
    # check if an edge exists as a function of g(n)
    for neighbor in neighbors:
      cost = costs[current] + (abs(current.x - neighbor.x) + abs(current.y - neighbor.y))
      if cost >= dynamic_list[0]['emergence'] and check_collision((current, neighbor), [d.get('location') for d in dynamic_list]):
        print("Collision with Dynamic Obstacle")
        print(current)
        print(neighbor)
        continue
      # distance can equate to time- g(n)
      # True False on blocked spaces can relate to g(n)
      if neighbor not in costs or cost < costs[neighbor]:
        costs[neighbor] = cost
        parents[neighbor] = current
        heap.heappush(open_list, (cost + heuristic(neighbor, goal), neighbor))
  print("never got to goal")

def main():
  #read in environment
  lines = []
  for line in sys.stdin:
    stripped = line.strip()
    if not stripped: break
    lines.append(stripped)

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

  #define dynamic obstacle(s) : 1 for env 3
  dynamic_obstacles = list()
  dynamic_obstacles.append({"location": [goal[0][0]-1, goal[0][1]-2], "emergence": 3})
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
  for i in range(0, len(edges)):
    print(edges[i])
  
  print(blocked)
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
        final_edges.append({"edge": edges[i], "blocked": False, "distance": abs(edges[i][0].x-edges[i][1].x) + abs(edges[i][0].y-edges[i][1].y)})
  
  for i in range(len(final_edges)):
    print(final_edges[i])

  # run A* for static worlds
  astar(final_graph[0], final_graph[len(final_graph)-1], final_edges, dynamic_obstacles)

if __name__ == "__main__":
  main()

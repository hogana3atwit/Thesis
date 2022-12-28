import sys
import pyvisgraph as vg
import argparse
from collections import defaultdict
import heapq as heap
import operator as op

def findLocation(state, target):
  return [ [x, y] for x, row in enumerate(state) for y, i in enumerate(row) if target in i ]

def connect_points(points):
  edges = []

  for i in range(len(points)):
    for j in range(i + 1, len(points)):
      edges.append((points[i], points[j]))

  return edges

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

  #print(obstacles)
  print("-----------------------------------------------")

  graph_vertices = list()
  # build meaningful corners for visibility graph
  for i in range(0, len(obstacles)):
    for j in range(0, len(obstacles[i])):
      cur_point = obstacles[i][j]
      #if cur_point.x == rows or cur_point.y == columns:
        #if cur_point not in graph_vertices:
          #graph_vertices.append(cur_point)
        #continue
      #if cur_point.x + 1 == rows or cur_point.y + 1 == columns or cur_-1 == 0 or j-1 == 0:
        #graph_vertices.append(cur_point)
        #continue
      
      count = 0
      if [cur_point.x, cur_point.y] in blocked:
        count+=1
      if [cur_point.x + 1, cur_point.y] in blocked:
        count+=1
      #if [cur_point.x - 1, cur_point.y] in blocked:
        #count+=1
      if [cur_point.x, cur_point.y + 1] in blocked:
        count+=1
      #if [cur_point.x, cur_point.y - 1] in blocked:
        #count+=1
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
        #print(cur_vert)
        #print([int(cur_vert.x-1),int(cur_vert.y)])
        check_list = [int(cur_vert.x-1), int(cur_vert.y)]
        if check_list not in blocked and vg.Point(cur_vert.x - 1, cur_vert.y) in graph_vertices:
          #print("yes")
          final_graph.append(cur_vert)
      elif cur_vert.y == columns:
        if [int(cur_vert.x), int(cur_vert.y - 1)] not in blocked and vg.Point(cur_vert.x, cur_vert.y - 1) in graph_vertices:
          final_graph.append(cur_vert)
      else:
        final_graph.append(cur_vert)

  # check any additional walls
  #for i in range(0, rows):
    #if vg.Point(i, columns) not in graph_vertices:
      #graph_vertices.append(vg.Point(i, columns))

  #for i in range(0, columns):
    #if vg.Point(rows, i) not in graph_vertices:
      #graph_vertices.append(vg.Point(rows, i))

  print(final_graph)
  for i in range(0, len(final_graph)):
    print(final_graph[i])

  # connect edges of graph
  edges = connect_points(final_graph)
  print(edges)

if __name__ == "__main__":
  main()

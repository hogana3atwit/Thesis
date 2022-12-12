import sys
import pyvisgraph as vg
import argparse
from collections import defaultdict
import heapq as heap

def findLocation(state, target):
  return [ [x, y] for x, row in enumerate(state) for y, i in enumerate(row) if target in i ]

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

  graph_vertices = list()
  # build meaningful corners for visibility graph
  for i in range(0, len(obstacles)):
    for j in range(0, len(obstacles[i])):
      cur_point = obstacles[i][j]
      if cur_point.x == rows or cur_point.y == columns:
        if cur_point not in graph_vertices:
          graph_vertices.append(cur_point)
        continue
      #if cur_point.x + 1 == rows or cur_point.y + 1 == columns or cur_-1 == 0 or j-1 == 0:
        #graph_vertices.append(cur_point)
        #continue
      
      count = 0
      if [cur_point.x, cur_point.y] in blocked:
        count+=1
      if [cur_point.x + 1, cur_point.y] in blocked:
        count+=1
      if [cur_point.x - 1, cur_point.y] in blocked:
        count+=1
      if [cur_point.x, cur_point.y + 1] in blocked:
        count+=1
      if [cur_point.x, cur_point.y - 1] in blocked:
        count+=1
      if [cur_point.x + 1, cur_point.y + 1] in blocked:
        count+=1

      if count <= 1:
        if cur_point not in graph_vertices:
          graph_vertices.append(cur_point)

  # check any additional walls
  for i in range(0, rows):
    if vg.Point(i, columns) not in graph_vertices:
      graph_vertices.append(vg.Point(i, columns))

  for i in range(0, columns):
    if vg.Point(rows, i) not in graph_vertices:
      graph_vertices.append(vg.Point(rows, i))

  for i in range(0, len(graph_vertices)):
    print(graph_vertices[i])
      
if __name__ == "__main__":
  main()

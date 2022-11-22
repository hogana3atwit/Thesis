import sys
import pyvisgraph as vg
import argparse

#helper function to find the [x, y] location of the agent in the grid at any given time
def agentLocation(state):
  return [ [x, y] for x, row in enumerate(state) for y, i in enumerate(row) if "@" in i ]

#helper function to produce a list of all of the [x, y] locations of blocked spaces in the grid state
def blockedSpaces(state):
  return [ [x, y] for x, row in enumerate(state) for y, i in enumerate(row) if "#" in i ]

def findGoal(state):
  return [ [x, y] for x, row in enumerate(state) for y, i in enumerate(row) if "G" in i ]

def validSpace(state, row, column):
  return not (row < 0 or row >= len(state) or column < 0 or column >= len(state[0]))

def move(state, row, column, direction):
  if direction == "L":
    if state[row][column-1] == "G":
      state[row][column-1] = "@G"
      state[row][column] = "_"
    else:
      state[row][column-1] = "@"
      state[row][column] = "_"
  if direction == "R":
    if state[row][column+1] == "G":
      state[row][column+1] = "@G"
      state[row][column] = "_"
    else:
      state[row][column+1] = "@"
      state[row][column] = "_"
  if direction == "U":
    if state[row-1][column] == "G":
      state[row-1][column] = "@G"
      state[row][column] = "_"
    else:
      state[row-1][column] = "@"
      state[row][column] = "_"
  if direction == "D":
    if state[row+1][column] == "G":
      state[row+1][column] = "@G"
      state[row][column] = "_"
    else:
      state[row+1][column] = "@"
      state[row][column] = "_"
  return state

def expand(state, path, parent, blocked, agentRow, agentColumn):
  children = []

  #checks the 5 actions for any valid states and adds valid actions to the children list
  if validSpace(state, agentRow, agentColumn-1) and [agentRow, agentColumn-1] not in blocked and parent["action"] != "R":
      children.append( {"state": move(list(map(list, state)), agentRow, agentColumn, "L"), "time": parent["time"]+1, "goal": False, "agentRow": agentRow, "agentColumn": agentColumn-1, "action": "L", "path": path + "\nL", "parent": parent,} )

  if validSpace(state, agentRow, agentColumn+1) and [agentRow, agentColumn+1] not in blocked and parent["action"] != "L":
      children.append( {"state": move(list(map(list, state)), agentRow, agentColumn, "R"), "time": parent["time"]+1, "goal": False, "agentRow": agentRow, "agentColumn": agentColumn+1, "action": "R", "path": path + "\nR", "parent": parent,} )

  if validSpace(state, agentRow-1, agentColumn) and [agentRow-1, agentColumn] not in blocked and parent["action"] != "D":
      children.append( {"state": move(list(map(list, state)), agentRow, agentColumn, "U"), "time": parent["time"]+1, "goal": False, "agentRow": agentRow-1, "agentColumn": agentColumn, "action": "U", "path": path + "\nU", "parent": parent,} )

  if validSpace(state, agentRow+1, agentColumn) and [agentRow+1, agentColumn] not in blocked and parent["action"] != "U":
      children.append( {"state": move(list(map(list, state)), agentRow, agentColumn, "D"), "time": parent["time"]+1, "goal": False, "agentRow": agentRow+1, "agentColumn": agentColumn, "action": "D", "path": path + "\nD", "parent": parent,} )

  return children

def pathCost(node):
  return len(node["path"])

def main():
  #read in environment 
  lines = []
  for line in sys.stdin:
    stripped = line.strip()
    if not stripped: break
    lines.append(stripped)

  agent = agentLocation(lines)
  #find obstacles (blocked spaces)
  blocked = blockedSpaces(lines)
  goal = findGoal(lines)

  obstacles = list()
  for i in range(0, len(blocked)):
    p = [vg.Point(blocked[i][0], blocked[i][1]), vg.Point(blocked[i][0]+1, blocked[i][1]), vg.Point(blocked[i][0], blocked[i][1]+1), vg.Point(blocked[i][0]+1, blocked[i][1]+1)]
    obstacles.append(p)

  open_list = [{"state": lines, "time": 1, "goal": False, "agentRow": agent[0][0], "agentColumn": agent[0][1], "action": "none", "path": "", "parent": None}]

  closed_list = {}
  nodes_gen = 0
  nodes_exp = 0

  # A*
  if len(open_list) == 0:
    print("Error: Empty World")

  while True:
    if len(open_list) == 0:
      print("Empty World")
      print(cur_node["path"][1:])
      break

    cur_node = open_list.pop(0)

    if cur_node["agentRow"] + cur_node["agentColumn"] in closed_list.keys():
      continue

    if cur_node["state"][cur_node["agentRow"]][cur_node["agentColumn"]] == "@G":
      print(cur_node["path"][1:])
      break
    else:
      children = expand(cur_node["state"], cur_node["path"], cur_node, blocked, cur_node["agentRow"], cur_node["agentColumn"])
      nodes_gen += len(children)
      children.sort(key=pathCost, reverse=True)

    for node in children:
      open_list = [node] + open_list
    closed_list[cur_node["agentRow"] + cur_node["agentColumn"]] = len(cur_node["path"])

  print("%d nodes generated" % (nodes_gen))
  print("%d nodes expanded" % (len(closed_list)))

  #for i in range(0, len(polys)):
    #print(polys[i])

  g = vg.VisGraph()
  #polys2 = [[vg.Point(0.0,1.0), vg.Point(3.0,1.0), vg.Point(1.5,4.0)], [vg.Point(4.0,4.0), vg.Point(7.0,4.0), vg.Point(5.5,8.0)]]
  #print(polys2)
  g.build(obstacles)
  print(g)
  shortest = g.shortest_path(vg.Point(agent[0][0], agent[0][1]), vg.Point(goal[0][0], goal[0][1]))
  print(shortest)

  g.save('graph.pk1')


if __name__ == "__main__":
  main()

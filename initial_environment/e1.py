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

def main():
  #read in environment 
  lines = []
  for line in sys.stdin:
    stripped = line.strip()
    if not stripped: break
    lines.append(stripped)

  agent = agentLocation(lines)
  #find obstacles (blocked spaces)
  obstacles = blockedSpaces(lines)
  goal = findGoal(lines)

  polys = list()
  for i in range(0, len(obstacles)):
    p = [vg.Point(obstacles[i][0], obstacles[i][1]), vg.Point(obstacles[i][0]+1, obstacles[i][1]), vg.Point(obstacles[i][0], obstacles[i][1]+1), vg.Point(obstacles[i][0]+1, obstacles[i][1]+1)]
    polys.append(p)

  for i in range(0, len(polys)):
    print(polys[i])

  g = vg.VisGraph()
  #polys2 = [[vg.Point(0.0,1.0), vg.Point(3.0,1.0), vg.Point(1.5,4.0)], [vg.Point(4.0,4.0), vg.Point(7.0,4.0), vg.Point(5.5,8.0)]]
  #print(polys2)
  g.build(polys)
  print(g)
  shortest = g.shortest_path(vg.Point(agent[0][0], agent[0][1]), vg.Point(goal[0][0], goal[0][1]))
  print(shortest)

  g.save('graph.pk1')


if __name__ == "__main__":
  main()

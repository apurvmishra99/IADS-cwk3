import math
import graph

g = graph.Graph(-1, "cities50")
# g.swapHeuristic()
# g.TwoOptHeuristic()
g.Greedy()
print(g.tourValue())
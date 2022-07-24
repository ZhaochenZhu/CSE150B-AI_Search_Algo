from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [(0,self.grid.start)]
            self.explored = []
        elif self.type == "astar":
            self.frontier = [(self.calculateDistance(self.grid.start,self.grid.goal), self.grid.start)]
            self.explored = []

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    #DFS: BUGGY, fix it first
    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()

        #if current in self.explored:
         #  return
        self.explored.append(current)

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if (n not in self.explored ) and (not n in self.frontier):
                        self.previous[n] = current
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True

    #Implement BFS here (Don't forget to implement initialization at line 23)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop(0)

        # if current in self.explored:
        #  return
        self.explored.append(current)

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if (n not in self.explored) and (not n in self.frontier):
                        self.previous[n] = current
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True

    #Implement UCS here (Don't forget to implement initialization at line 23)
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        self.frontier.sort(reverse=False)
        (currentCost,current) = self.frontier.pop(0)

        # if current in self.explored:
        #  return
        self.explored.append(current)

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if (n not in self.explored) and (not self.isInFrontier(n)):
                        self.previous[n] = current
                        self.frontier.append((self.grid.nodes[n].cost()+currentCost,n))
                        self.grid.nodes[n].color_frontier = True
                    elif (self.isInFrontier(n)):
                        if(self.withHigherCost(n,self.grid.nodes[n].cost()+currentCost)):
                            self.replaceNode(n,self.grid.nodes[n].cost()+currentCost)
                            self.previous[n] = current

    #Implement Astar here (Don't forget to implement initialization at line 23)
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        self.frontier.sort(reverse=False)
        (currentCost, current) = self.frontier.pop(0)

        # if current in self.explored:
        #  return
        self.explored.append(current)

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    newCost = self.grid.nodes[n].cost() + currentCost+ self.calculateDistance(n,self.grid.goal)-self.calculateDistance(current,self.grid.goal)
                    if (n not in self.explored) and (not self.isInFrontier(n)):
                        self.previous[n] = current
                        self.frontier.append((newCost,n))
                        self.grid.nodes[n].color_frontier = True
                    elif self.isInFrontier(n):
                        if (self.withHigherCost(n, newCost)):
                            self.replaceNode(n, newCost)
                            self.previous[n] = current


    def isInFrontier(self,node):
        for x in self.frontier:
            if x[1] == node:
                return True
        return False

    def withHigherCost(self,node,cost):
        for x in self.frontier:
            if x[1] == node and x[0]>cost:
                return True
        return False

    def replaceNode(self,node,cost):
        for x in self.frontier:
            if x[1] == node:
                self.frontier.remove(x)
                self.frontier.append((cost,node))
                #x[0] = cost
                return

    def calculateDistance(self,node,goal):
        return abs(node[0]-goal[0])+abs(node[1]-goal[1])
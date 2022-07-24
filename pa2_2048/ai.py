from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if(self.children):
            return False
        else:
            return True

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        if depth == 0:
            return

        self.simulator.set_state(*node.state)
        if node.player_type == MAX_PLAYER:
            curState = copy.deepcopy(self.simulator.current_state())
            for move in MOVES:
                if self.simulator.move(move):
                    node.children.append((move,Node(self.simulator.current_state(),CHANCE_PLAYER)))
                self.simulator.set_state(*curState)
            for tree_child in node.children:
                self.build_tree(tree_child[1],depth-1)
            #return

        if node.player_type == CHANCE_PLAYER:
            tiles = self.simulator.get_open_tiles()
            curState = copy.deepcopy(self.simulator.current_state())
            copyState = copy.deepcopy(curState)
            for spot in tiles:
                #self.simulator.current_state()[0][spot[0]][spot[1]] = 2
                #node.children.append((None,Node(self.simulator.current_state(),MAX_PLAYER)))
                #self.simulator.set_state(*curState)
                copyState[0][spot[0]][spot[1]] = 2
                node.children.append((None,Node(copyState,MAX_PLAYER)))
                copyState = copy.deepcopy(curState)
            for tree_child in node.children:
                self.build_tree(tree_child[1],depth-1)




    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):

        if(node.is_terminal()):
            return -1, node.state[1]
        elif(node.player_type == MAX_PLAYER):
            direction = 0
            value = float('-inf')
            for child in node.children:
                move, exp_max = self.expectimax(child[1])
                if(exp_max>=value):
                    value = exp_max
                    direction = child[0]
            return direction,value

        elif(node.player_type == CHANCE_PLAYER):
            value = 0
            for child in node.children:
                move, exp_max = self.expectimax(child[1])
                value = value + (float)(exp_max/(len(node.children)))
            return -1,value

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction


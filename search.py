#Breadth First Search on 15 Puzzle
#Sarit Adhikari
#Spring 2024

import queue
import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        if len(tiles) != 16:
            raise ValueError("Not a 4x4 grid.")
        self.tiles = tiles


    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        newTiles = self.tiles[:]
        emptySpot = newTiles.index('0')
        
        if action == 'U' and emptySpot - 4 >= 0:
            origSpot = newTiles[emptySpot - 4]
            newTiles[emptySpot - 4] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        elif action == 'D' and emptySpot + 4 < 16:
            origSpot = newTiles[emptySpot + 4]
            newTiles[emptySpot + 4] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        elif action == 'L' and emptySpot % 4 > 0: 
            origSpot = newTiles[emptySpot - 1]
            newTiles[emptySpot - 1] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        elif action == 'R' and emptySpot % 4 < 3 :
            origSpot = newTiles[emptySpot + 1]
            newTiles[emptySpot + 1] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        
        return Board(newTiles)


            



# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action 

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))



class Search:




    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        actions = ['U', 'D', 'L', 'R']
        children = []
        for action in actions:
            children.append(Node(parent_node.state.execute_action(action), parent_node, action) )
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while node.parent:
            path.insert(0, node.action)
            node = node.parent 
        return path 


    # This function runs breadth first search from the given root node and returns path, number of nodes expanded and total time taken
    def run_bfs(self, root_node):
        startTime = time.time()
        mem = 0 
        frontier = queue.Queue()
        frontier.put(root_node) 
        explored = set()
        explored.add(root_node)

        while frontier:
            mem = max(mem, sum(map(sys.getsizeof,[frontier, explored])))
            curr = frontier.get()
            

            if self.goal_test(curr.state.tiles):
                path = self.find_path(curr)
                return path, len(explored), time.time() - startTime, mem

            for child in self.get_children(curr):
                if child not in explored:
                    explored.add(child)
                    frontier.put(child)

        print("frontier is empty. Solution not found.")
        return False



    def goal_test(self, cur_tiles):
        return cur_tiles == [str(i) for i in range(1,16)] + ['0']

    def solve(self, input):

        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.run_bfs(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

# Testing the algorithm locally
if __name__ == '__main__':
    agent = Search()
    #agent.solve("1 2 3 4 5 6 7 8 9 10 11 0 13 14 15 12")
    agent.solve("2 8 1 0 4 6 3 7 5 9 10 12 13 14 11 15")


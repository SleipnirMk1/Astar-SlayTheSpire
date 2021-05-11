# Nama  : Ilyasa Salafi Putra Jamal
# NIM   : 13519023
# Source code for paper assignment 'Determining Lowest Risk Paths in the game Slay The Spire using A* Algorithm'

# Directed Graph Representation
class Graph:
    def __init__(self):
        self.graph_dict = {}
    # Add link from A and B with certain distance
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
    # Get neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
    # Return list of nodes
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

# Node class for the graph
class Node:
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # g(n)
        self.h = 0 # h(n)
        self.f = 0 # f(n)
    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name
    # Sort nodes from smallest
    def __lt__(self, other):
            return self.f < other.f

# A* search
def Astar(graph, heuristics, start_node, goal_node):
    # Variables for expand and visited nodes, start and goal
    expand = []
    visited = []
    start = Node(start_node, None)
    goal = Node(goal_node, None)

    # Add the start node
    expand.append(start)
    # Loop until no expandable node
    while len(expand) > 0:
        # Sort and pop lowest value node from expand into visited
        expand.sort()
        currNode = expand.pop(0)
        visited.append(currNode)
        
        # If goal is already reached
        if currNode == goal:
            # Get path from goal to start with sum of risk g(n)
            path = {}
            while currNode != start:
                path[currNode.name] = currNode.g
                currNode = currNode.parent
            path[start.name] = start.g
            # Return path from start to goal
            return dict(reversed(list(path.items())))

        # Check each neighbor
        neighbors = graph.get(currNode.name)   
        for key, value in neighbors.items():
            # Create the neighbor node
            neighbor = Node(key, currNode)
            # If already visited, skip current loop
            if(neighbor in visited):
                continue
            # A* evaluation function, f(n) = g(n) + h(n)
            neighbor.g = currNode.g + graph.get(currNode.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # If neighbor is in expand list and has lower f(n)
            if(expandable(expand, neighbor) == True):
                expand.append(neighbor) # Add neighbor to expand list

    # No path found
    return None

# If neighbor is in expand list and has lower f(n)
def expandable(expand, neighbor_node):
    for node in expand:
        if (neighbor_node == node and neighbor_node.f > node.f):
            return False
    return True

# Read custom txt file
def readFile(filename):
    # Open file and declare variables
    f = open(filename, 'r')
    encounterRisk = {}
    edges = {}
    heuristics = {}

    # Read number of floor for heuristics
    dataType = 'Floors'
    f.readline()    # Skip first line
    floors = f.readline().rstrip()  # remove newline
    currFloor = int(floors)     # for heuristics

    # Read the rest of the data
    for line in f:
        # Check what data is being read
        line = line.rstrip()
        if (line == 'Encounters'):  # Encounter tag
            dataType = line
            continue
        elif (line == 'Links'): # Links tag
            dataType = line
            continue

        # Split to read data per space/tab
        line = line.split()
        # if the data type is Encounters
        if (dataType == 'Encounters'):
            # Get all encounters and their risks
            for word in line:
                word = word.split('-')
                # Assess risk
                if (word[1] == 'B' or word[1] == 'ST') :
                    word[1] = 0 # Boss or dummy: unavoidable
                elif (word[1] == 'T' or word[1] == 'R' or word[1] == 'M') :
                    word[1] = 1 # Rest, Treasure, or Merchant: low risk
                elif (word[1] == 'N') :
                    word[1] = 2 # Enemy: medium risk
                elif (word[1] == 'E' or word[1] == 'U') :
                    word[1] = 3 # Elite or Unknown: high risk
                else :  # word[1] == EX,
                    word[1] = 4 # Buffed Elite: very high risk
                # Add to dictionary of risk and heuristics
                encounterRisk[word[0]] = word[1]
                heuristics[word[0]] = currFloor
            # Reduce heuristic each floor
            currFloor -= 1

        # If the data type is Links
        elif (dataType == 'Links'):
            # Get linked encounters
            for word in line:
                word = word.split(',')
                # Get array of linked nodes
                temp = []
                for i in range(1,len(word)):
                    temp.append(word[i])
                # Pair node with array of its linked nodes
                edges[word[0]] = temp
    
    return encounterRisk, edges, heuristics, floors

# Link the encounters
def buildGraph(encounterRisk, edges):
    graph = Graph()
    # For each node
    for node in edges:
        # For each nodes linked to previous node
        for target in edges[node]:
            graph.connect(node, target, encounterRisk[target])
    return graph

# main function
def main():
    # Input file path
    fileName = input('Enter custom txt file path:\n')
    #fileName = 'C:\Tugas\Stima\Makalah\TestMap1.txt' # DEBUG
    # Read file
    encounterRisk, edges, heuristics, floors = readFile(fileName)
    # Build graph
    graph = buildGraph(encounterRisk, edges)

    start = ''
    while True:
        # Input starting node
        start = input('Search lowest risk path from where? (Enter \'0\' if from the beginning)\n')
        if (start == 'exit'): break
        # Run the search algorithm
        path = Astar(graph, heuristics, start, floors)
        # Print results
        if path != None :
            print('Path with the lowest risk:\n', path)
            print('Total risk value taken:', list(path.values())[-1] )
        else :
            print('No possible path')
        # Exit
        print('Enter \'exit\' when you are done')

    print('Exiting...')
    
# main
if __name__ == "__main__":
    try :
        main()
    except :
        input('Something went wrong, enter to exit\n')
# Burak Kocausta

from collections import defaultdict
from collections import deque
import random

# dynamic graph implementation which makes topological sorting
class DynamicGraph:
    def __init__(self):
        # create empty adj list as <v, list>
        self.adjList = defaultdict(list)

    def addVertex(self, vertex):
        self.adjList[vertex]

    # add edge between v1 and v2
    def addEdge(self, v1, v2):
        self.adjList[v1].append(v2)
        self.adjList[v2]

    def printAdjList(self):
        for k,v in self.adjList.items():
            print(k,"-->",v)

    # function for dfs based topological sorting
    def DFSTopologicalSort(self):
        visitedVertices = set()

        # ordering holds the topological sorted data
        ordering = deque()
        
        # function definition which makes dfs, and inserts to queue
        def dfsTop(curVertex):
            visitedVertices.add(curVertex)
            edges = self.adjList[curVertex]
            for dest in edges:
                # if it is not visited go deep
                if dest not in visitedVertices:
                    dfsTop(dest)

            # insert at head to the dequeue
            ordering.appendleft(curVertex)

        # iterate through keys
        for vertex in self.adjList.keys():
            # call not visited elements
            if vertex not in visitedVertices:
                dfsTop(vertex)

        # print the result        
        print("dfs based topological order:", end=" ")
        for i in ordering:
            if i is ordering[-1]:
                print(i)
            else:
                print(i, "->", end = " ")

    # non-dfs based topological sort algorithm
    def nonDFSTopSort(self):
        visitedVertices = set()
        stack = deque() # stack of the vertices which have no incoming edges.
        incomingEdges = defaultdict() # hashmap of <Vertex, number of incoming edge>

        # sub procedures

        # initialize the number of incoming edges for every element to 0
        def init():
            for vertex in self.adjList:
                incomingEdges[vertex] = 0
                edges = self.adjList[vertex]
                for dest in edges:
                    incomingEdges[dest] = 0

        # count the incoming edges for every element
        def countIncomingEdges():
            for vertex in self.adjList:
                edges = self.adjList[vertex]
                for dest in edges:
                    incomingEdges[dest] += 1

        # add the vertices which have no incoming edges to the top of the stack
        def addNoIncomings():
            for vertex in incomingEdges:
                if incomingEdges[vertex] == 0:
                    stack.append(vertex)

        # consumes the stack, and removes the vertexes, that are visited.
        def nonDFSTop():
            ordering = "non-dfs based topological order: "
            # loop till stack is not empty
            while len(stack) != 0:
                curVertex = stack.pop()
                ordering += curVertex + " -> "
                visitedVertices.add(curVertex)

                edges = self.adjList[curVertex]
                # insert other elements which does not have incoming edges to the stack and decrease the incoming edges after adding
                for dest in edges:
                    incomingEdges[dest] -= 1
                    if incomingEdges[dest] == 0:
                        stack.append(dest)
            print(ordering[:-3])

        # call every sub procedure.
        init()
        countIncomingEdges()
        addNoIncomings()
        nonDFSTop()

print("\nQuestion 1 test-------\n")
# test for question 1
g = DynamicGraph()
g.addEdge("CSE102", "CSE241")
g.addEdge("CSE241", "CSE222")
g.addEdge("CSE222", "CSE321")
g.addEdge("CSE321", "CSE422")
g.addEdge("CSE211", "CSE321")

g.printAdjList()
g.DFSTopologicalSort()
g.nonDFSTopSort() 
        

def logExp(a, n):

    # if it is 0, directly return.
    if (a == 0):
        return 0

    # a^0 = 0, base case
    elif (n == 0):
        return 1

    # a^(2*(n/2)) = a^n, this eliminates half of the computation with n/2
    elif (n % 2 == 0):
        return logExp(a*a, n // 2) # "//" means floor operation

    # a^n = a * a ^ (2 * (n-1) / 2), this also eliminates half of the computation with (n-1) / 2 
    else:
        return a * logExp((a*a), (n-1) // 2) # "//" means floor operation

#test question 2

print("\nQuestion 2 test-------\n")
print("2^5 = ", logExp(2,5))
print("3^6 = ", logExp(3,6))
print("-5^3 = ", logExp(-5,3))
print("10^4 = ", logExp(10,4))
print("2^0 = ", logExp(2,0))


# a sudoku game class
class Sudoku9x9:
    def __init__(self, board=None):
        if board is None:
            # generate a solvable board if none is provided
            self.board = self.generateBoard()
        else:
            self.board = board
    
    # generate a random board
    def generateBoard(self):
        board = [[0 for i in range(9)] for j in range(9)]
        
        self.board = board
        self.solver()

        emptyCellList = [(i, j) for i in range(9) for j in range(9)]
        
        # randomly choose the number of empty cells
        n = random.randint(35, 50)
        
        # randomly choose empty cells
        emptyCellList = random.sample(emptyCellList, n)
        for i, j in emptyCellList:
            self.board[i][j] = 0

        return self.board

    
    # checks if move is valid or not
    def isValid(self, row, col, num):
        
        # first check

        # check all rows
        if num in self.board[row]:
            return False
        
        # check all columns
        if num in [self.board[i][col] for i in range(9)]:
            return False
        
        # second check

        # check if number is present in the 3x3 box
        boxCol = col // 3
        boxRow = row // 3
        if num in [self.board[i][j] for i in range(boxRow * 3, boxRow * 3 + 3)
                                     for j in range(boxCol * 3, boxCol * 3 + 3)]:
                    return False
        
        # if all conditions checked, it is valid
        return True

    # a brute force solving algorithm for sudoku 9x9, which uses backtracing 
    def solver(self):
        emptyCell = self.findEmpty()
        
        if not emptyCell:
            return True
        
        row, col = emptyCell # get the empty coordinations

        # do this for numbers between 1-9(included)
        for num in range(1, 10):
            
            # check if move is valid
            if self.isValid(row, col, num):
                self.board[row][col] = num
                
                # check if it is solved
                if self.solver():
                    return True
                
                # take back the last move, and continue
                self.board[row][col] = 0
        
        return False

    # finds the empty cell
    def findEmpty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None
    
    # print board pretty
    def printBoard(self):
        for i in range(9):
            for j in range(9):
                if j % 3 == 0:
                    print("|", end=" ")
                print(self.board[i][j], end=" ")
            print("|")
            if i % 3 == 2:
                print("-" * 25)


print("\nQuestion 3 test-------\n")

board =         [[9, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 3, 6, 0, 0, 0, 0, 0], 
                 [0, 6, 0, 0, 9, 0, 2, 0, 0], 
                 [0, 5, 0, 0, 0, 2, 0, 0, 0], 
                 [0, 0, 0, 0, 4, 5, 7, 0, 0], 
                 [0, 0, 0, 1, 0, 0, 0, 3, 0], 
                 [0, 0, 1, 0, 0, 0, 0, 6, 8], 
                 [0, 0, 8, 5, 0, 0, 0, 1, 0], 
                 [0, 9, 0, 0, 0, 0, 4, 0, 0]]

sudoku = Sudoku9x9(board)
sudoku.printBoard()
print("******************************************")
sudoku.solver()
sudoku.printBoard()
print()


while True:
    # show menu to user
    print("\nTest Menu: ")
    print("1. Input edges")
    print("2. Input exponent and base")
    print("3. Generate Sudoku Board and solve")
    print("Enter 'q' to quit")

    userInput = input("Enter your selection: ")


    if userInput == "1":
        g1 = DynamicGraph()

        while True:
            x = input("(q for quit)edge source = ")
            
            if x == "q":
                break
            
            y = input("(q for quit)edge destination = ")

            if y == "q":
                break

            g1.addEdge(x, y)

        print("Adjacency List Representation of graph: ")
        g1.printAdjList()
        print("Topological Sort Results: \n")
        g1.DFSTopologicalSort()
        g1.nonDFSTopSort()

    elif userInput == "2":
        base = int(input("Enter base: "))
        exp = int(input("Enter exponent: "))
        result = logExp(base, exp)
        print(result)

    elif userInput == "3":
        sudoku = Sudoku9x9()
        sudoku.generateBoard()
        print("\nGenerated board: \n")
        sudoku.printBoard()
        sudoku.solver()
        print("\nSudoku Solution: \n")
        sudoku.printBoard()
        print()
    elif userInput == "q":
        break

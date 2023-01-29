import random

# question 1
# route game class
class RouteGame:
    def __init__(self, num_row, num_col, map2d = None):
        # generate random 2d map
        def generate_2dmap():
            return [[random.randint(1, 99) for i in range(num_col)] for i in range(num_row)]

        if map2d is None:
            self.map2d = generate_2dmap()
        else:
            self.map2d = map2d

    # print 2d map in 2d grid format nicely
    def print_map(self):
        print(f'{"":2}', end="")
        for i in range(1, len(self.map2d[0]) + 1):
            print(f'{"":3}{"B"}{i}', end="")
        print()

        ctr = 1
        for row in self.map2d:
            print(f'{"":1}{"A"}{ctr}', end="")
            ctr += 1
            for col in row:
                print(f'{""}{"| "}{col:2}', end=" ")
            print()
        print()


    # find max point route
    def find_max_point_route(self):
        # hash map <sum, route>
        sum_route = dict(list())

        # save all routes in sum_route dictionary
        def save_all_routes(arr2d, row, col, sum, route):    
            if (row == len(arr2d)-1 and col == len(arr2d[0])-1):
                route.append((row, col))
                sum_route[sum + arr2d[row][col]] = route
            # go right in 2d map
            if col+1 < len(arr2d[0]):
                # copy route list to temp list to prevent route list from being changed
                temp = route.copy()
                temp.append((row, col))     
                save_all_routes(arr2d, row, col+1, sum+arr2d[row][col], temp)
            # go down in 2d map
            if row+1 < len(arr2d):
                # copy route list to temp list to prevent route list from being changed
                temp = route.copy()
                temp.append((row, col))
                save_all_routes(arr2d, row+1, col, sum+arr2d[row][col], temp)

        # find max point route
        save_all_routes(self.map2d, 0, 0, 0, list())
        keys = sum_route.keys()
        sum = max(keys)
        route = sum_route[sum]
        points = list()

        # print route     
        print("Route: ", end="")
        for row, col in route:
            print(f'{"A"}{row+1}{"B"}{col+1}', end="")
            if row == len(self.map2d)-1 and col == len(self.map2d[0])-1:
                print()
            else:
                print(" -> ", end="")
            # add points to points list
            points.append(self.map2d[row][col])

        # print points and sum
        print("Points: ", end="")
        for point in points:
            if point == points[-1]:
                print(f'{point}', end="")
            else:
                print(f'{point}{" + "}', end="")
        print(" =", sum)        

# test RouteGame class
print("Test Question 1: ")
routeGame = RouteGame(4, 3, [[25, 30, 25], [45, 15, 11], [1, 88, 15], [9, 4, 23]])
print("2D Map: ")
routeGame.print_map()
routeGame.find_max_point_route()
print()
# routeGame2 = RouteGame(5, 5)
# routeGame2.print_map()
# routeGame2.find_max_point_route()

# question 2
# lomuto partition algorithm
def lomuto_partition(arr, left, right):
    # select rightmost element as pivot
    pivot = arr[right]
    i = left - 1
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            #swap
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
    #swap
    temp2 = arr[i+1]
    arr[i+1] = arr[right]
    arr[right] = temp2

    return i+1

# finds median of unsorted array using lomuto partition algorithm with decrease and conquer
# if number of elements in array is even, returns the smaller of the two medians
def find_median(arr, left, right):
    # base case
    if left == right:
        return arr[left]
    else:
        # find pivot index
        pivot_index = lomuto_partition(arr, left, right)

        # if pivot index is the median, return it
        if pivot_index == (len(arr) - 1)//2:
            return arr[pivot_index]
        
        # find right subarray's median
        elif pivot_index < len(arr)//2:
            return find_median(arr, pivot_index+1, right)

        # find left subarray's median
        else:
            return find_median(arr, left, pivot_index-1)
            

# test find_median function 
print("Test Question 2: ")
print("Unsorted Array: ", end="")
arr = [3, 1, 7, 5, 2, 4, 6, 8, 12]
print(arr)
print("Median: ", end="")
print(find_median(arr, 0, len(arr)-1))
print()

# question 3a

# circular linked list implementation with insert and print functions, elements represented as people
class PeopleCLL:

    # inner class Node 
    class Person:
        def __init__(self, data):
            self.data = data
            self.next = None
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, data):
        new_node = self.Person(data)
        # insert at head
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.next = new_node
        # insert at tail
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.tail.next = self.head
    
    # print circular linked list in Pdata->Pdata->Pdata->Pdata->Pdata format
    def print_list(self):
        temp = self.head
        while temp.next != self.head:
            print(f'{"P"}{temp.data}', end="->")
            temp = temp.next
        print(f'{"P"}{temp.data}')


# implement josephus problem using circular linked list
def josephus_problem(n):
    circle = PeopleCLL()

    # insert people into circular linked list
    for i in range(1, n+1):
        circle.insert(i)
    
    # print people
    print("people: ", end="")
    circle.print_list()
    print()

    # start at first person
    temp = circle.head
    # iterate until next person is the same person
    while temp.next != temp:
        # print eliminated person
        print(f'{"P"}{temp.data}', "eliminates", f'{"P"}{temp.next.data}')
        temp.next = temp.next.next
        temp = temp.next
    # print winner
    print(f'{"P"}{temp.data}', "is the winner")

# test question 3a
print("Test Question 3a: ")
josephus_problem(7)
print()

# question 3b
# implementation of josephus problem recursively using decrease and conquer
# algorithm decreases the problem into two subproblems, result is determined by if n is even or odd
# more explanation is in the report
def josephus_problem_dc(n):
    # base case
    if n == 1:
        return 1
    else:
        # if n is even
        if n % 2 == 0:
            return 2*josephus_problem_dc(n//2) - 1

        # if n is odd
        else:
            return 2*josephus_problem_dc(n//2) + 1

# test question 3b
print("Test Question 3b: ")
print("input: n = 7")
print(f'{"P"}{josephus_problem_dc(7)}', "is the winner")
print()

# test menu for questions 1-3b
def test_menu():
    print("Test Menu: ")
    print("1. Test Question 1")
    print("2. Test Question 2")
    print("3. Test Question 3a")
    print("4. Test Question 3b")
    print("5. Exit")
    print()
    choice = int(input("input(1-5): "))
    print()
    if choice == 1:
        print("Question 1: ")
        print()
        # get number of rows and columns
        row = int(input("Enter number of rows: "))
        col = int(input("Enter number of columns: "))
        print()

        # create route game object
        routeGame = RouteGame(row, col)
        print("2D Map: ")
        routeGame.print_map()
        routeGame.find_max_point_route()
        print()
        test_menu()
    elif choice == 2:
        print("Question 2: ")
        print()
        # get array size
        size = int(input("Enter size of array: "))
        print()
        # generate random array
        arr = list()
        for i in range(size):
            arr.append(random.randint(1, 100))
        print("Generated Unsorted Array: ", end="")
        print(arr)
        print("Median: ", end="")
        print(find_median(arr, 0, len(arr)-1))
        print()
        test_menu()
    elif choice == 3:
        print("Question 3a: ")
        print()
        # get number of people
        n = int(input("Enter number of people: "))
        print()
        josephus_problem(n)
        print()
        test_menu()
    elif choice == 4:
        print("Question 3b: ")
        print()
        # get number of people
        n = int(input("Enter number of people: "))
        print()
        print(f'{"P"}{josephus_problem_dc(n)}', "is the winner")
        print()
        test_menu()
    elif choice == 5:
        print("Terminated")
        print()
    else:
        print("Invalid choice")
        print()
        test_menu()

test_menu()
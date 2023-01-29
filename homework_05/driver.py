import random

# finds the longest common substring in a list of strings
# substring is beginning of all strings in the list
# returns the common substring
def find_LC_substring(string_list) :
    
    def find_LC_substring_helper(start, end):
        if start == end:
            return string_list[start]
        else:
            mid = (start + end) // 2
            left = find_LC_substring_helper(start, mid)
            right = find_LC_substring_helper(mid+1, end)
            return find_common_substring(left, right)

    # search for the longest common substring in str1 and str2
    def find_common_substring(str1, str2):
        substr = ""
        min_len = min(len(str1), len(str2))
        for i in range(min_len):
            if str1[i] == str2[i]:
                substr += str1[i]
            else:
                break
        return substr
    
    return find_LC_substring_helper(0, len(string_list)-1)


# test question 1
print()
print("Test for question 1:")
strlist1 = ["programmable", "programming", "programmer", "programmatic", "programmability"]
print("input: ", strlist1)
print("output: ", find_LC_substring(strlist1))
print()

strlist2 = ["compute", "compatible", "computer", "compare", "compactness"]
print("input: ", strlist2)
print("output: ", find_LC_substring(strlist2))
print()

# returns the maximum profit that can be made by buying and selling the stock on different days
def maximize_profit(prices):

    # returns min, max, buy, sell indices
    def maximize_profit_helper(start, end):
        # base case
        if start == end:
            return start, start, start, start
        else:
            mid = (start + end) // 2
            min_left, max_left, buy_left, sell_left = maximize_profit_helper(start, mid)
            min_right, max_right, buy_right, sell_right = maximize_profit_helper(mid+1, end)
            return merge_result(min_left, max_left, buy_left, sell_left, min_right, max_right, buy_right, sell_right)

    # merge the results of the left and right subarrays
    def merge_result(min_left, max_left, buy_left, sell_left, min_right, max_right, buy_right, sell_right):
        
        # flag for min and max to indicate which subarray it came from
        flag_min = ""
        flag_max = ""

        # find min
        if prices[min_left] < prices[min_right]:
            min_price = min_left
            flag_min = "left"
        else:
            min_price = min_right
            flag_min = "right"

        # find max
        if prices[max_left] > prices[max_right]:
            max_price = max_left
            flag_max = "left"
        else:
            max_price = max_right
            flag_max = "right"

        # if min and max came from left subarray
        if flag_max == "left" and flag_min == "left":

            # check if min and max are the same index, if so, buy and sell are left subarray's max and min
            if min_left != buy_left:
                buy = min_left
                sell = max_right
            
            # if they are not the same index, buy and sell are left subarray
            else:
                buy = buy_left
                sell = sell_left
        
        # if min and max came from right subarray
        elif flag_max == "right" and flag_min == "right":

            # check if min and max are the same index, if so, min is left subarray's min and max is right subarray's max
            if min_right != buy_right:
                buy = min_left
                sell = max_right

            # if they are not the same index, buy and sell are right subarray's buy and sell
            else:
                buy = buy_right
                sell = sell_right

        # if min came from right, max came from left
        elif flag_max == "left" and flag_min == "right":
            profit1 = prices[sell_left] - prices[buy_left]
            profit2 = prices[sell_right] - prices[buy_right]
            profit3 = prices[sell_right] - prices[buy_left]
            profit4 = prices[max_right] - prices[min_left]

            # if profit1 is the largest, buy and sell are left subarray
            if profit1 >= profit2 and profit1 >= profit3 and profit1 >= profit4:
                buy = buy_left
                sell = sell_left
            
            # if profit2 is the largest, buy and sell are right subarray
            elif profit2 >= profit1 and profit2 >= profit3 and profit2 >= profit4:
                buy = buy_right
                sell = sell_right

            # if profit4 is the largest, buy is left subarray's min and sell is right subarray's max
            elif profit4 >= profit1 and profit4 >= profit2 and profit4 >= profit3:
                buy = min_left
                sell = max_right

            # if profit3 is the largest, buy is left subarray and sell is right subarray    
            else:
                buy = buy_left
                sell = sell_right
        # if min came from left, max came from right, then buy is left subarray and sell is right subarray
        else:
            buy = min_left
            sell = max_right

        # for debugging
        # print()
        # print("min_left: ", prices[min_left], "max_left: ", prices[max_left], "buy_left: ", prices[buy_left], "sell_left: ", prices[sell_left])
        # print("min_right: ", prices[min_right], "max_right: ", prices[max_right], "buy_right: ", prices[buy_right], "sell_right: ", prices[sell_right])
        # print("min: ", prices[min_price], "max: ", prices[max_price], "buy: ", prices[buy], "sell: ", prices[sell])
        # print()

        return min_price, max_price, buy, sell

    min_price, max_price, buy, sell = maximize_profit_helper(0, len(prices)-1)
    #print the result
    print("buy on", f'day{buy}', "at price ", prices[buy])
    print("sell on", f'day{sell}', "at price ", prices[sell])
    print("profit: ", prices[sell] - prices[buy])


# test question 2a
print()
print("Test for question 2a:")
prices1 = [10, 11, 10, 9, 8, 7, 9, 11]
print("input: ", prices1)
print("output: ")
maximize_profit(prices1)

print()
prices2 = [100, 110, 80, 90, 110, 70, 80, 80, 90]
print("input: ", prices2)
print("output: ")
maximize_profit(prices2)
print()

# prices3 = [8, 7, 1, 2]
# print("input: ", prices3)
# print("output: ")
# maximize_profit(prices3)

# prices4 = [74, 18, 34, 68]
# print("input: ", prices4)
# print("output: ")
# maximize_profit(prices4)

# prices5 = [85, 32, 36, 4]
# print("input: ", prices5)
# print("output: ")
# maximize_profit(prices5)

# quadratic time solution
def maximize_profit_qd(prices):

    buy = 0
    sell = 0

    for i in range(len(prices)):

        # if new minimum is found, update buy and sell
        if prices[i] < prices[buy]:
            old_buy = buy
            buy = i
            old_sell = sell

            # find the new sell
            for j in range(i, len(prices)):
                if prices[j] > prices[sell] and j > buy:
                    sell = j
                    break
            # if buy is on the right of sell, then don't change
            if buy > sell:
                sell = old_sell
                buy = old_buy

    #print the result
    print("buy on", f'day{buy}', "at price ", prices[buy])
    print("sell on", f'day{sell}', "at price ", prices[sell])
    print("profit: ", prices[sell] - prices[buy])

# dynamic programming solution
def maximize_profit_dp(prices):
    profit = 0
    buy = 0
    sell = 0
    min_val = prices[0]
    
    # temp is the index of the min_val price, it is needed because old value of buy index can be needed
    temp = 0

    for i in range(1, len(prices)):

        # if the current price is less than the min_val, update min_val and temp
        if prices[i] < min_val:
            temp = i
            min_val = prices[i]

        # if the current price is greater than the min_val, update profit, buy, and sell
        if prices[i] - min_val > profit:
            profit = prices[i] - min_val
            buy = temp
            sell = i
    
    print("buy on", f'day{buy}', "at price ", prices[buy])
    print("sell on", f'day{sell}', "at price ", prices[sell])
    print("profit: ", profit)

# test question 2b
print()
print("test for question 2b(dynamic programming):")
prices1 = [10, 11, 10, 9, 8, 7, 9, 11]
print("input: ", prices1)
print("output: ")
maximize_profit_dp(prices1)
print()

prices2 = [100, 110, 80, 90, 110, 70, 80, 80, 90]
print("input: ", prices2)
print("output: ")
maximize_profit_dp(prices2)
print()

print()
print("test for question 2b(quadratic approach):")
prices1 = [10, 11, 10, 9, 8, 7, 9, 11]
print("input: ", prices1)
print("output: ")
maximize_profit_qd(prices1)
print()

prices2 = [100, 110, 80, 90, 110, 70, 80, 80, 90]
print("input: ", prices2)
print("output: ")
maximize_profit_qd(prices2)


# prices3 = [8, 7, 1, 2]
# print("input: ", prices3)
# print("output: ")
# maximize_profit_dp(prices3)

# prices4 = [74, 18, 34, 68]
# print("input: ", prices4)
# print("output: ")
# maximize_profit_dp(prices4)


# finds the longest increasing sub array using dynamic programming
def find_longest_incsub(array):
    
    # table to store the length of the longest increasing sub array
    table = [0 for i in range(len(array))]
    table[0] = 1

    ctr = 1
    for i in range(1, len(array)):
        
        # if current is greater then update the table
        if array[i] > array[i-1]:
            table[ctr] = 1
            ctr += 1
        else:
            ctr = 1
    
    # print("table: ", table)

    # reversely traverse the table
    for i in range(len(table)-1, -1, -1):
        if table[i] == 1:
            return i+1
    return 0

# test question 3
print()
print("Test for question 3:")
array1 = [1, 4, 5, 2, 4, 3, 6, 7, 1, 2, 3, 4, 7]
print("input: ", array1)
print("output: ", find_longest_incsub(array1))
print()

array2 = [1, 2, 3, 4, 1, 2, 3, 5, 2, 3, 4]
print("input: ", array2)
print("output: ", find_longest_incsub(array2))
print()

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

    # find the shortest path from top left to bottom right using dynamic programming
    def find_max_point_route_dp(self):

        # create nxm dynamic table
        table = [[0 for i in range(len(self.map2d[0]))] for i in range(len(self.map2d))]

        table[0][0] = self.map2d[0][0]
        # fill the table
        for i in range(0, len(self.map2d)):
            for j in range(0, len(self.map2d[0])):
                
                # skip the first element
                if i == 0 and j == 0:
                    continue
                
                # if current element is on the first row, add the left element
                elif i == 0:
                    table[i][j] = table[i][j-1] + self.map2d[i][j]

                # if current element is on the first column, add the top element
                elif j == 0:
                    table[i][j] = table[i-1][j] + self.map2d[i][j]

                # otherwise, add the max of the top and left element
                else:
                    table[i][j] = max(table[i-1][j], table[i][j-1]) + self.map2d[i][j]

    
        print("dynamic table: ")
        for row in table:
            for col in row:
                print(f'{col:3}', end=" ")
            print()
        print()

        print("max point is: ", table[len(self.map2d)-1][len(self.map2d[0])-1])

    # find the shortest path from top left to bottom right using greedy algorithm
    # in each step, always choose the path with the most points
    def find_max_point_route_greedy(self):
        def greedy(row, col, sum):

            row_max = len(self.map2d) - 1
            col_max = len(self.map2d[0]) - 1

            # base case
            if row == row_max and col == col_max:
                return sum + self.map2d[row][col]
            
            else:
                # if current element is on the last row, go right
                if row == row_max:
                    return greedy(row, col + 1, sum + self.map2d[row][col])

                # if current element is on the last column, go down
                elif col == col_max:
                    return greedy(row + 1, col, sum + self.map2d[row][col])

                else:
                    # always choose the path with the most points
                    if self.map2d[row+1][col] > self.map2d[row][col+1]:
                        return greedy(row + 1, col, sum + self.map2d[row][col])
                    else:
                        return greedy(row, col + 1, sum + self.map2d[row][col])

        print("max point is: ", greedy(0, 0, 0))
        
# test question 4a
print()
print("Test Question 4a(dynamic): ")
routeGame = RouteGame(4, 3, [[25, 30, 25], [45, 15, 11], [1, 88, 15], [9, 4, 23]])
print("2D Map: ")
routeGame.print_map()
routeGame.find_max_point_route_dp()
print()
# routeGame2 = RouteGame(5, 5)
# routeGame2.print_map()
# routeGame2.find_max_point_route()

# test question 4b
print()
print("Test Question 4b(greedy): ")
routeGame = RouteGame(4, 3, [[25, 30, 25], [45, 15, 11], [1, 88, 15], [9, 4, 23]])
print("2D Map: ")
routeGame.print_map()
routeGame.find_max_point_route_greedy()
print()


# test menu for questions 1-4b
def test_menu():
    print("Test Menu: ")
    print("1. Test Question 1")
    print("2. Test Question 2a")
    print("3. Test Question 2b")
    print("4. Test Question 3")
    print("5. Test Question 4a")
    print("6. Test Question 4b")
    print("7. Exit")
    print()
    choice = int(input("input(1-7): "))
    print()

    # test for find_LC_substring function
    if choice == 1:
        print("Question 1: ")
        num_str = int(input("number of strings: "))
        str_list = []
        for i in range(num_str):
            str_list.append(input(f"string {i+1}: "))
        print()
        print("output: ", find_LC_substring(str_list))
        print()
        test_menu()
    
    # test for maximize_profit function
    elif choice == 2:
        print("Question 2a: ")
        size = int(input("size of array: "))
        array = [random.randint(1, 99) for i in range(size)]
        print("input: ", array)
        print("output: ")
        maximize_profit(array)
        print()
        test_menu()

    elif choice == 3:
        print("Question 2b: ")
        size = int(input("size of array: "))
        array = [random.randint(1, 99) for i in range(size)]
        print("input: ", array)
        maximize_profit_qd(array)
        print()
        test_menu()

    # test for find_longest_incsub function
    elif choice == 4:
        print("Question 3: ")
        size = int(input("size of array: "))
        array = [random.randint(1, 99) for i in range(size)]
        print("input: ", array)
        print("output: ", find_longest_incsub(array))
        print()
        test_menu()

    

    # test for find_max_point_route_dp function
    elif choice == 5:
        print("Question 4a: ")
        print()
        # get number of rows and columns
        row = int(input("Enter number of rows: "))
        col = int(input("Enter number of columns: "))
        print()

        # create route game object
        routeGame = RouteGame(row, col)
        print("2D Map: ")
        routeGame.print_map()
        routeGame.find_max_point_route_dp()
        print()
        test_menu()

    # test for find_max_point_route_greedy function
    elif choice == 6:
        print("Question 4b: ")
        print()
        # get number of rows and columns
        row = int(input("Enter number of rows: "))
        col = int(input("Enter number of columns: "))
        print()

        # create route game object
        routeGame = RouteGame(row, col)
        print("2D Map: ")
        routeGame.print_map()
        routeGame.find_max_point_route_greedy()
        print()
        test_menu()

    # exit
    else:
        print("Terminated. Bye!")
        return

test_menu()
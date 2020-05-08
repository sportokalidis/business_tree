import pandas as pd

class Node(object):

    prod_A = 100          # Total number of type-A produced per week
    prod_B = 80           # Total number of type-A produced per week

    cost_A = 225*prod_A   # Total cost of type-A production per week
    cost_B = 310*prod_B   # Total cost of type-B production per week

    penalty = 500         # Penalty to change product line from type-A to type-B or type-B to type-A
    interest_rate = 0.195 # annual interest rate to store products

    cost_arr = []         # Double Array: Cost of all valid possible directrories
    dir_arr = []          # All valid possible directories

    num_of_weeks = 8      # The num of weeks that I want to predict the minimum cost


    def __init__(self, data, store, cost, week, directory):

        self.left = None          # Node Obj:   The left child of node
        self.right = None         # Node Obj:   The right child of node
        self.data = data          # Character:  The type of product 'A' or 'B'
        self.store = store        # Int Arr[2]: The num of products in storage -> store[0]: type-A and store[1]: type:B
        self.cost = cost          # Double:     The total cost of production + penalties
        self.week = week          # Integer:    The week that take place the node,   week = 0(root), 1, 2, ..., num_of_weeks
        self.valid = True         # Boolean:    Validation of decision, valid == True if company requirements are met,  False if not
        self.dir = directory      # String:     The path of production line, (A->A->B...)

        # When insert a child, set True or False the valid attribute
        self.valid_checking()


    # insert a left and a right child in every node at the end line, only if the decision is valid
    def insert(self):
        if self.data == 'A' and self.valid:
            if self.left is None:
                directory = self.dir + ' -> A'
                self.left = Node('A', [self.store[0]+Node.prod_A, self.store[1]], self.cost + Node.cost_A, self.week+1, directory)
            else:
                self.left.insert()

            if self.right is None:
                directory = self.dir + ' -> B'
                self.right = Node('B', [self.store[0], self.store[1]+Node.prod_B], self.cost + Node.cost_B+Node.penalty, self.week+1, directory)
            else:
                self.right.insert()

        if self.data == 'B' and self.valid:
            if self.left is None:
                directory = self.dir + ' -> A'
                self.left = Node('A', [self.store[0]+Node.prod_A, self.store[1]], self.cost + Node.cost_A+Node.penalty, self.week+1, directory)
            else:
                self.left.insert()

            if self.right is None:
                directory = self.dir + ' -> B'
                self.right = Node('B', [self.store[0], self.store[1]+Node.prod_B], self.cost + Node.cost_B, self.week+1, directory)
            else:
                self.right.insert()


    # When insert a child, call 'valid_checking' function to set True or False the valid attribute
    def valid_checking(self):
        if self.week != 0:
            # Take data from data.csv file
            data = pd.read_csv("data.csv")

            # Update the num of products in storage
            cur_A = self.store[0] - data['A'][self.week-1]
            cur_B = self.store[1] - data['B'][self.week-1]
            self.store = [cur_A, cur_B]

            # Update the cost
            self.cost = self.cost + cur_A * Node.interest_rate*Node.cost_A/52 + cur_B * Node.interest_rate*Node.cost_B/52

            # check the requirement of company, to have 80% of next week order in storage
            if(cur_A < 0.8*data['A'][self.week] or cur_B <  0.8*data['B'][self.week]):
                self.valid = False


    # print the nodes of tree and main results
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()

        ''' print only valid and <num_of_weeks> nodes  '''
        if self.valid and self.week == Node.num_of_weeks:
            # print(f"1. cost: {self.cost:7}", f"2. store: {self.store}", f"3. valid: {self.valid}", f"  4. week: {self.week}", f"5. dir: {self.dir}", sep="\t")
            print('1. cost: {}    2. store: {}    3. valid: {}    4. week: {}    5. dir: {}'.format(self.cost, self.store, self.valid, self.week, self.dir))
            Node.cost_arr.append(self.cost)
            Node.dir_arr.append(self.dir)

        # '''print the week <num_of_weeks> nodes'''
        # if self.week == num_of_weeks:
        #     print(f"1. cost: {self.cost:7}", f"2. store: {self.store}", f"3. valid: {self.valid}", f"  4. week: {self.week}", f"5. dir: {self.dir}", sep="\t")
        #     Node.cost_arr.append(self.cost)
        #     Node.dir_arr.append(self.dir)

        # '''print all nodes '''
        # print(f"1. cost: {self.cost:7}", f"2. store: {self.store}", f"3. valid: {self.valid}", f"  4. week: {self.week}", f"5. dir: {self.dir}", sep="\t")
        # Node.cost_arr.append(self.cost)
        # Node.dir_arr.append(self.dir)

        if self.right:
            self.right.PrintTree()


# Inint values -> values of root
data = 'A'
store = [125, 143]
cost = 0
week = 0
directory = 'A'

# Create the root
root = Node(data, store, cost, week, directory)

# Add nodes
for i in range(Node.num_of_weeks):
    root.insert()

# print the results
root.PrintTree()



# Find the minimun
minimum = Node.cost_arr[0];
for i in Node.cost_arr:
    if(minimum > i):
        minimum = i

# Find how many times we have the minimum cost
# And which directories have the minimum cost
count=0
min_dir = []
for i in range(len(Node.cost_arr)):
        if(Node.cost_arr[i] == minimum):
            count = count + 1
            min_dir.append(Node.dir_arr[i])


print("\n\n\n")
print(len(Node.cost_arr), len(Node.dir_arr))

print(minimum, count)
for i in min_dir:
    print(i)

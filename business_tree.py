import pandas as pd

class Node(object):

    prod_A = 100
    prod_B = 80

    cost_A = 225*prod_A
    cost_B = 310*prod_B

    penalty = 500

    cost_arr = []
    dir_arr = []

    num_of_weeks = 8

    def __init__(self, data, store, cost, week, directory):

        self.left = None
        self.right = None
        self.data = data
        self.store = store
        self.cost = cost
        self.week = week
        self.valid = True
        self.dir = directory
        self.valid_checking()

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


    def valid_checking(self):
        if self.week != 0:
            data = pd.read_csv("data.csv")
            cur_A = self.store[0] - data['A'][self.week-1]
            cur_B = self.store[1] - data['B'][self.week-1]
            self.store = [cur_A, cur_B]

            if(cur_A < 0.8*data['A'][self.week] or cur_B <  0.8*data['B'][self.week]):
                self.valid = False


    def PrintTree(self):
        if self.left:
            self.left.PrintTree()

        ''' print only valid node at the end '''
        if self.valid and self.week == Node.num_of_weeks:
            print(f"1. cost: {self.cost:7}", f"2. store: {self.store}", f"3. valid: {self.valid}", f"  4. week: {self.week}", f"5. dir: {self.dir}", sep="\t")
            Node.cost_arr.append(self.cost)
            Node.dir_arr.append(self.dir)

        # '''print the week 7 nodes'''
        # if self.week == 8:
        #     print(f"1. cost: {self.cost:7}", f"2. store: {self.store}", f"3. valid: {self.valid}", f"  4. week: {self.week}", f"5. dir: {self.dir}", sep="\t")
        #     Node.cost_arr.append(self.cost)
        #     Node.dir_arr.append(self.dir)

        # '''print all nodes '''
        # print(f"1. cost: {self.cost:7}", f"2. store: {self.store}", f"3. valid: {self.valid}", f"  4. week: {self.week}", f"5. dir: {self.dir}", sep="\t")
        # Node.cost_arr.append(self.cost)
        # Node.dir_arr.append(self.dir)

        if self.right:
            self.right.PrintTree()


data = 'A'
store = [125, 143]
cost = 0
week = 0
directory = 'A'


root = Node(data, store, cost, week, directory)

for i in range(Node.num_of_weeks):
    root.insert()

root.PrintTree()

count=0

minimum = Node.cost_arr[0];
# Find the minimun
for i in Node.cost_arr:
    if(minimum > i):
        minimum = i

# Find how many times we have the minimum cost
# And which directories have the minimum cost
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



#
# data = pd.read_csv("data.csv")
#
# cur_A = data['A']
# print(cur_A[3])
#

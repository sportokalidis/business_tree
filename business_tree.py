import pandas as pd

class Node(object):

    prod_A = 100
    prod_B = 80

    cost_A = 225*prod_A
    cost_B = 310*prod_B

    penalty = 500

    cost_arr = []

    count = 0

    def __init__(self, data, store, cost, week):

        self.left = None
        self.right = None
        self.data = data
        self.store = store
        self.cost = cost
        self.week = week
        self.valid = True
        self.valid_checking()

    def insert(self):
        if self.data == 'A' and self.valid:
            if self.left is None:
                self.left = Node('A', [self.store[0]+Node.prod_A, self.store[1]], self.cost + Node.cost_A, self.week+1)
            else:
                self.left.insert()

            if self.right is None:
                self.right = Node('B', [self.store[0], self.store[1]+Node.prod_B], self.cost + Node.cost_B+Node.penalty, self.week+1)
            else:
                self.right.insert()

        if self.data == 'B' and self.valid:
            if self.left is None:
                self.left = Node('A', [self.store[0]+Node.prod_A, self.store[1]], self.cost + Node.cost_A+Node.penalty, self.week+1)
            else:
                self.left.insert()

            if self.right is None:
                self.right = Node('B', [self.store[0], self.store[1]+Node.prod_B], self.cost + Node.cost_B, self.week+1)
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
            # print("A -> ", end = " ")
            self.left.PrintTree()

        if self.valid and self.week == 7:
            Node.count = Node.count + 1
            print(Node.count,". " "-> ", self.data, "\t 1. cost: ", self.cost, "\t 2. store", self.store, "\t 3. valid", self.valid, "\t 3. week", self.week)
            Node.cost_arr.append(self.cost)

        # if self.right == None :
        #     print("-> ", self.data, "\t 1. cost: ", self.cost, "\t 2. store", self.store, "\t 3. valid", self.valid, "\t 3. week", self.week)

        # print("-> ", self.data, "\t 1. cost: ", self.cost, "\t 2. store", self.store, "\t 3. valid", self.valid, "\t 3. week", self.week)

        if self.right:
            # print("B -> ",  end = " ")
            self.right.PrintTree()


data = 'A'
store = [125, 143]
cost = 0
week = 0

root = Node(data, store, cost, week)

root.insert()
root.insert()
root.insert()
root.insert()
root.insert()
root.insert()
root.insert()

root.PrintTree()

count=0
minimum = Node.cost_arr[0];
for i in Node.cost_arr:
    if(minimum > i):
        minimum = i
    if(i == 165400):
        count = count + 1

print(minimum, count)




#
# data = pd.read_csv("data.csv")
#
# cur_A = data['A']
# print(cur_A[3])
#

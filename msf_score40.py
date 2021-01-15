import sys
import random
import math

DEBUG = False  # False when you submit to kattis

# function which queries the next set of neighbors from kattis
if DEBUG:
    N = 21000000  # the number of nodes
    eps = 0.1  # desired accuracy
    maxWeight = 3  # largest weight in our graph
    # we will simulate a graph that is just one large cycle
    # you could add some other types of graphs for debugging/testing your program

    def getNeighbors(node):
        leftNeighbor = (node-1) % N
        rightNeighbor = (node+1) % N
        weight = 1
        return [(leftNeighbor, weight), (rightNeighbor, weight)]
else:
    N = int(sys.stdin.readline())  # read number of nodes from the input
    eps = float(sys.stdin.readline()) - 1  # we read the desired approximation
    # read the largest weight of the graph
    maxWeight = int(sys.stdin.readline())

    def getNeighbors(node):
        # ask kattis for the next node
        print(node)
        sys.stdout.flush()
        # read the answer we get from kattis
        line = sys.stdin.readline().split()
        # the answer has the form 'numNeighbors neighbor1 weight1 neighbor2 weight2 ...'
        # we want to have a list of the form:
        #[ (neighbor1, weight1), (neighbor2, weight2) , ...]
        return [(int(line[i]), int(line[i+1])) for i in range(1, len(line), 2)]

if N == 0 or N == 1:
    print('end ' + str(0))
    sys.stdout.flush()
    sys.exit()


def approx_msf_weight(s, cHat):
    # range 1 to W - 1
    for i in range(1, maxWeight):
        cHat += approx_connected_comps(s, i)
    number_of_trees = approx_connected_comps(s, maxWeight)
    return N - (maxWeight*number_of_trees) + cHat


def approx_connected_comps(s, currWeight):
    if currWeight >= maxWeight / 2:
        s = math.floor(maxWeight**2/eps**2)
    if currWeight >= maxWeight / 1.5:
        s = math.floor(maxWeight/eps**2)
    b = 0
    for i in range(0, s):
        x = calculate_x()
        u = random.randint(0, N-1)
        b += BFS(u, x, currWeight)
    return (N/s) * b


def calculate_x():
    x = math.floor(1.0/random.random())
    if x > 10.0:
        x = 10.0
    return x


def BFS(n, x, currWeight):
    queue = []
    visited = []

    queue.append(n)
    visited.append(n)
    iterations = 0

    while queue and iterations < x:
        currNode = queue.pop(0)
        neighbors = getNeighbors(currNode)
        iterations += 1

        for neighbor in neighbors:
            if (neighbor[1] <= currWeight) and (neighbor[0] not in visited):
                queue.append(neighbor[0])
                visited.append(neighbor[0])
            else:
                continue

    if not queue:
        return 1
    else:
        return 0


def main():
    s = math.floor(maxWeight/eps**2)
    cHat = 0
    weight_of_spanning_forest = approx_msf_weight(s, cHat)

    # print the answer
    print('end ' + str(weight_of_spanning_forest))
    sys.stdout.flush()


if __name__ == "__main__":
    main()

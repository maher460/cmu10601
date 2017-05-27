#import itertools
import jsonpickle


# Creating all possible graphs


def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    result = []
    for i in range(1 << x):
        result.append([ss for mask, ss in zip(masks, s) if i & mask])

    return result


def cyclic(g):
    """Return True if the directed graph g has a cycle.
    g must be represented as a dictionary mapping vertices to
    iterables of neighbouring vertices. For example:

    >>> cyclic({1: (2,), 2: (3,), 3: (1,)})
    True
    >>> cyclic({1: (2,), 2: (3,), 3: (4,)})
    False

    """
    path = set()
    visited = set()

    def visit(vertex):
        if vertex in visited:
            return False
        visited.add(vertex)
        path.add(vertex)
        #for neighbour in g[vertex]:
        for i in range(len(g[vertex])):
            if(g[vertex][i] == 1):
                neighbour = i
                if neighbour in path or visit(neighbour):
                    return True
        path.remove(vertex)
        return False

    return any(visit(v) for v in range(len(g)))


complete_graph = []

for i in range(5):
    for j in range(5):
        if(i != j):
            complete_graph.append([i,j])

# print(complete_graph)

all_graphs = powerset(complete_graph)

#print(all_graphs)
print("Size of complete graph: ", len(complete_graph))
print("Number of all possible graphs: ", len(all_graphs))

#all_graphs = [[[0,1], [1,2], [2,0]],[[0,1],[1,2]]]

all_graphs_dict = []
for g in all_graphs:

    temp_graph_dict = []
    for i in range(5):
        temp_graph_dict.append([0] * 5)

    for e in g:
        temp_graph_dict[e[0]][e[1]] = 1

    all_graphs_dict.append(temp_graph_dict)

print("Number of all possible graphs changed to dict type: ",len(all_graphs_dict))

all_dags = []
for g in all_graphs_dict:
    if(cyclic(g) == False):
        all_dags.append(g)

print("Number of all possible DAGs: ", len(all_dags))
# print(all_dags[0])
# print(all_dags[1])
# print(all_dags[-1])

print("Writing all_dags to file...")
traindata_processed_file = open("processed_stuff/all_dags", "w")
traindata_processed_file.write(jsonpickle.encode(all_dags))
traindata_processed_file.close()
print("Done writing all_dags to file")
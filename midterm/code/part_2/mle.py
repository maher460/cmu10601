import itertools

DEBUG = False

SMOOTH_E = 0.1

# Segregating out instances that take a particular value
# attributearray is an N x 1 array.
def segregate_set(attributearray, value):
    outlist = set()
    for i in range(0, len(attributearray)):
        if(attributearray[i] == value):
            outlist.add(i)
    return outlist

def select_labels(labels, ids):
    result = []
    for i in ids:
        result.append(labels[i])
    return result

def unique_labels(labels):
    unique_labels = []
    for e in labels:
        if (e not in unique_labels):
            unique_labels.append(e)
    return unique_labels

def transpose(matrix):
    if(len(matrix) < 1):
        return matrix
    else:
        new_matrix = []
        for k in range(len(matrix[0])):
            new_matrix.append([])
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                new_matrix[j].append(matrix[i][j])

            if DEBUG:
                if(i % 1000 == 0):
                    print("transposing " + str(i) + " ....")
        return new_matrix

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    result = []
    for i in range(1 << x):
        result.append([ss for mask, ss in zip(masks, s) if i & mask])

    return result

def calc_prob_all_values(child_parents_tuple, traindata_t):

    #print(child_parents_tuple)
    child = child_parents_tuple[0]
    parents = list(child_parents_tuple)[1:]

    parents_set = set(range(len(traindata_t[0])))
    for p in parents:
        set_p = segregate_set(traindata_t[p[0]], p[1])
        parents_set = parents_set.intersection(set_p)

    prob = 0.0

    if(len(parents_set) > 0):
        set_c = segregate_set(traindata_t[child[0]], child[1])
        set_c_given_parents = set_c.intersection(parents_set)
        prob = ((1.0 * len(set_c_given_parents)) + SMOOTH_E) / ((len(parents_set) * 1.0) + SMOOTH_E)
    else:
        prob = 1.0 / len(unique_labels(traindata_t[child[0]]))
    return prob


def all_pos(child, parents, traindata_t):
    # c_values = unique_labels(traindata_t[child])
    # p_values = {}
    # for p in parents:
    #   p_values[p] = unique_labels(traindata_t[p])

    # for c_val in c_values:
    #   calc_child = [child, c_val]
    #   calc_parents = {}
    #   for p in parents:
    #       calc_parents[p] = 
    child_parents_keys = []
    child_parents_values = []

    child_parents_keys.append(child)
    child_parents_values.append(unique_labels(traindata_t[child]))

    for p in parents:
        child_parents_keys.append(p)
        child_parents_values.append(unique_labels(traindata_t[p]))

    all_comb_values = list(itertools.product(*child_parents_values))

    for idx, item in enumerate(all_comb_values):
        temp = []
        for i in range(len(child_parents_keys)):
            temp.append((child_parents_keys[i],item[i]))
        #item[-1] = item[-1][:-1]
        all_comb_values[idx] = tuple(temp)
        # if(idx % 1 == 0):
        #   print("Done reading " + str(idx) + " traindata")

    result = {}

    for t in all_comb_values:
        result[t] = calc_prob_all_values(t, traindata_t)

    if DEBUG:
        parents_keys = child_parents_keys[1:]
        parents_values = child_parents_values[1:]
        all_combs_parents = list(itertools.product(*parents_values))
        for idx, item in enumerate(all_combs_parents):
            temp = []
            for i in range(len(parents_keys)):
                temp.append((parents_keys[i],item[i]))
            #item[-1] = item[-1][:-1]
            all_combs_parents[idx] = tuple(temp)
            # if(idx % 1 == 0):
            #   print("Done reading " + str(idx) + " traindata")

        for e in all_combs_parents:
            total_prob = 0.0
            for c_val in unique_labels(traindata_t[child]):
                temp_list = [(child, c_val)]
                temp_list.extend(list(e))
                temp_tuple = tuple(temp_list)
                total_prob = total_prob + result[temp_tuple]
            print total_prob

    return result

def all_comb_probs(nodes, traindata):
    traindata_t = transpose(traindata)
    result = {}
    for n in nodes:
        rest_nodes = list(nodes)
        rest_nodes.remove(n)
        all_combs_parents = powerset(rest_nodes)
        for e in all_combs_parents:
            temp_result = all_pos(n, e, traindata_t)
            result.update(temp_result)

    return result











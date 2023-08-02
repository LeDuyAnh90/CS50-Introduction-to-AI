# from generate import *

# structure = 'data/structure0.txt'
# words = 'data/words0.txt'

# crossword = Crossword(structure, words)
# creator = CrosswordCreator(crossword)

# creator.enforce_node_consistency()
# creator.ac3()

# var = list(crossword.variables)[0]
# print(var)
# values = [word for word in creator.domains[var]]
# print(values)
# neighbors = creator.crossword.neighbors(var)
# print(neighbors)
# costs = []
# for val in values:
#     cost = 0
#     for neighbor in neighbors:
#         overlap = creator.crossword.overlaps[var,neighbor]
#         for val2 in creator.domains[neighbor]:
#             if val[overlap[0]] != val2[overlap[1]]:
#                 cost += 1
#     costs.append(cost)
# keydict = dict(zip(values,costs))
# print(keydict)
# values.sort(key = keydict.get)
# print(values)

l = ['A','B','C']

d1 = {'A':1,'B':1,'C':3}
d2 = {'A':3,'B':1,'C':2}

key = lambda x: (d1[x],d2[x])
l.sort(key=key)
print(l)
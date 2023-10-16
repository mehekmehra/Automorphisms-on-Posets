from sympy.combinatorics.named_groups import SymmetricGroup
from sympy.combinatorics.perm_groups import PermutationGroup
import numpy as np

# automorphisms and automorphism checker provide information about automorphisms of posets.
# Ensure that you follow the conventions for inputs and that your input is in fact a poset.
# I am planning to update this with a poset checker and possibly a converter to make inputs simpler.

def automorphisms(myArr):
    """ automorphisms takes in an array representation of a matrix (less than matrix, similar to adjacency)
        and returns the number of automorphisms and the mappings (as permutations)

        parameters: myArr: an array representation of a matrix where less than/equal to relations
                            are represented by 1s by rows and non adjacent/ greater than relations
                            are 0s. (see the examples and the reference picture)
                            
        output: automorphism counter: returns the number of automorphisms
                permutations: prints the mappings as permutations
                                (eg 0 -> 1, 1 -> 0, 0 -> 0 would be [1, 0, 2])
    """
    
    posetArr = np.array(myArr)
    possibleMaps = permutationGroup(myArr)
    autCount = 0
    elements = elementList(myArr)

    for permutation in possibleMaps:
        possiblePoset = np.array(myArr)
        # swap cols
        possiblePoset[:] = possiblePoset[:, permutation]
        # swap rows
        possiblePoset[elements] = possiblePoset[permutation]

        if (possiblePoset == posetArr).all():
            autCount += 1
            print(permutation)

    return autCount

def automorphismChecker(myArr, autPermutation):
    """ automorphismChecker takes in an array representation of a matrix (less than matrix, similar to adjacency)
        and a permutation, and returns a boolean

        parameters: myArr: an array representation of a matrix where less than/equal to relations
                            are represented by 1s by rows and non adjacent/ greater than relations
                            are 0s. (see the examples and the reference picture)
        
                    autPermutation: a list representation of the permutation
                                    (eg 0 -> 1, 1 -> 0, 0 -> 0 would be [1, 0, 2])
                            
        output: boolean: True if autPermutation is an automorphism on myArr. 
                         False if it is not. 
    """
    posetArr = np.array(myArr)
    elements = elementList(myArr)
    possiblePoset = np.array(myArr)

    possiblePoset[:] = possiblePoset[:, autPermutation]
    possiblePoset[elements] = possiblePoset[autPermutation]

    if (possiblePoset == posetArr).all():
        return True
    else:
        return False

def permutationGroup(myArr):
    """ permutationGroup outputs the permutation group for all of the nodes in a given poset matrix
        primarily a helper function

        parameters: myArr: an array representation of a matrix where less than/equal to relations
                            are represented by 1s by rows and non adjacent/ greater than relations
                            are 0s. (see the examples and the reference picture)

        output: permutations: a list of the permutaions in the permutation group
    """
    generators = SymmetricGroup(len(myArr))
    permutations = list(generators.generate_schreier_sims(af=True))
    return permutations


def elementList(myArr):
    """ elementList outputs a list of the nodes in myArr
        primarily a helper function

        parameters: myArr: an array representation of a matrix where less than/equal to relations
                            are represented by 1s by rows and non adjacent/ greater than relations
                            are 0s. (see the examples and the reference picture)

        output: a list of nodes. 
    """
    elementsList = []
    start = 0
    for x in range(len(myArr)):
        elementsList += [start]
        start += 1
    return elementsList



##############
## examples ##
##############

# test 1
# test = [[1, 1, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]]
# print(automorphisms(test))

# test 2: chain
# test = [[1, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]]
# print(automorphisms(test))

# test 3: separate
# test = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# print(automorphisms(test))

# test 4:
# test = [[1, 1, 1, 1, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]]
# print(automorphisms(test))

# test 5:
# test = [[1, 1, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1]]
# print(automorphisms(test))

# test 6:
# test = [[1, 1, 1, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]]
# print(automorphisms(test))
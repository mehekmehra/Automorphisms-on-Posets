from sympy.combinatorics.named_groups import SymmetricGroup
from sympy.combinatorics.perm_groups import PermutationGroup
import numpy as np

##################
## AUTOMORPHISM ##
##################

def automorphism():
    """ automorphism runs an interface to make it easier for the user to input posets and permutations.
    It has the option to find all of the automorphisms for a given poset or check if a mapping is an automorphism.
    """
    print('Hello! This finds and checks for automorphisms on posets!')
    print()
    instructions = input('Do you want instructions? Enter y for yes : ')
    if instructions == 'y' or instructions == 'Y':
        print()
        print('Enter the strictly less than relations as two element pairs separated') 
        print('by lines with the lower element on the left.')
        print('Ensure that you label your nodes with integers starting at 0. Start by entering the number of relations')
        print()
        print('For example, the input for a chain of 3 nodes where 0 < 1 < 2 would be :')
        print('Number of Relations : 2')
        print('Enter a relation : 0 1')
        print('Enter a relation : 1 2')
        print()

    relationsList = []
    n = int(input("Number of Relations : "))
    print()
    for i in range(0, n):
        ele = list(map(int,input("Enter a relation : ").strip().split()))[:2]
        relationsList.append(ele)
    print()
    numNodes = int(input('How many nodes are in your poset? '))
    
    myArr = leqMatrix(numNodes, relationsList)

    print()
    print('Do you want to find all of the automorphisms for your poset')
    print('or check if a permutation is an automorphism?')
    choice = input('Enter in a for all automorphisms or b to check : ')
    print()
    if choice == 'a' or choice == 'A':
        fancyAutomorphisms(myArr)
    elif choice == 'b' or choice == 'B':
        instructions = input('Do you want instructions? Enter y for yes : ')
        if instructions == 'y' or 'Y':
            print()
            print('Enter the mappings as two element pairs separated by lines.')
            print('Ensure that you follow the same node labeling as you did while entering the poset.')
            print('You do need to include mappings for elements that do not change.')
            print()
            print('For example, the mapping 0 -> 0, 1 -> 2, 2 -> 3, 3 -> 1 would be entered as :')
            print('Number of Mappings : 3')
            print('Enter a mapping : 1 2')
            print('Enter a mapping : 2 3')
            print('Enter a mapping : 3 1')
            print()
            print('For a mapping where you have something along the lines of a <-> b. You must enter it as :')
            print('Number of Mappings : 2')
            print('Enter a mapping : a b')
            print('Enter a mapping : b a')
            print()
            print('Make sure that you only enter integers')
        mappingList = []
        numMap = int(input("Number of Mappings : "))
        print()
        for i in range(0, numMap):
            mapping = list(map(int,input("Enter a mapping : ").strip().split()))[:2]
            mappingList.append(mapping)
        print()
        perm = listToPerm(mappingList, numNodes)
        # print(perm)
        automorphismChecker(myArr, perm)
    else:
        print('Invalid input :(')


##########################
## AUTOMORPHISM CHECKER ##
##########################

def automorphismChecker(myArr, autPermutation):
    """ automorphismChecker takes in an array representation of a matrix (less than matrix, similar to adjacency) and a permutation, and returns a boolean

        parameters: myArr: an array representation of a matrix where less than/equal to relations
                            are represented by 1s by rows and non adjacent/ greater than relations
                            are 0s. (see the examples and the reference picture)
        
                    autPermutation: a list representation of the permutation
                                    (eg 0 -> 1, 1 -> 0, 0 -> 0 would be [1, 0, 2])
                            
        output: boolean: True if autPermutation is an automorphism on myArr.
                         False if it is not.
    """
    if autPermutation == 0:
        print('Invalid input :(')
        return False
    posetArr = np.array(myArr)
    elements = elementList(myArr)
    possiblePoset = np.array(myArr)

    possiblePoset[:] = possiblePoset[:, autPermutation]
    possiblePoset[elements] = possiblePoset[autPermutation]


    if (possiblePoset == posetArr).all():
        print('Your input is an automorphism on the given poset')
        return True
    else:
        print('Your input is not an automorphism on the given poset')
        return False


#########################
## AUTOMORPHISM FINDER ##
#########################

def fancyAutomorphisms(myArr):
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
    autsArr = []

    for permutation in possibleMaps:
        possiblePoset = np.array(myArr)
        # swap cols
        possiblePoset[:] = possiblePoset[:, permutation]
        # swap rows
        possiblePoset[elements] = possiblePoset[permutation]

        if (possiblePoset == posetArr).all():
            autCount += 1
            autsArr += [permutation]
    print('The automorphisms on this poset are :  \n')

    for i in range(len(autsArr)):
        print('f' + str(i) + ': \n')
        for j in range(len(autsArr[i])):
            print(str(j) + ' -> ' + str(autsArr[i][j]))
        print('\n')

    print('This poset has ' + str(autCount) + ' automorphisms')
    return autsArr, autCount


#############
## HELPERS ##
#############

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


def defaultMatrix(numNodes):
    """ defaultMatrix makes an n x n identity matrix where n is equal to numNodes

        parameters: numNodes: an integer that corresponds to the number of nodes in the poset

        output: a nested array where each sub array is a row in the matrix.
    """
    resArr = []
    for i in range(numNodes):
        subArr = []
        for j in range(numNodes):
            if i == j:
                subArr += [1]
            else:
                subArr += [0]
        resArr += [subArr]
    return resArr


def toRelationsDictionary(relationsList):
    """ toRelationsDictionary makes a dictionary out of an array of 2-element arrays

        parameters: relationsList: an array of 2-element arrays where the elements or the sub arrays are nodes

        output: a dictionary where the keys are the first values in the 2 element arrays and the values
                are the second values in the sub arrays.
    """
    dictionary = {}
    for i in relationsList:  
        dictionary.setdefault(i[0],[]).append(i[1])
    return dictionary


def leqMatrix(numNodes, relationsList):
    """ leqMatrix makes an array representation of a matrix where less than/equal to relations
        are represented by 1s by rows and non adjacent/ greater than relations are 0s. 
        
        parameters: numNodes: an integer corresponding to the number of nodes in the poset
                    relationsList: an array of 2-element arrays where the elements or the sub arrays are nodes. 
                                   the 2-element arrays represent less than relations, so for example, 
                                   [1, 2] corresponds to 1 < 2. 
        
        output: a nested array where each sub array is a row in the matrix.
    """
    relationsDict = toRelationsDictionary(relationsList)
    resMatrix = defaultMatrix(numNodes)
    for i in range(numNodes):
        if i in relationsDict:
            for x in relationsDict[i]:
                resMatrix[i][x] = 1
    return resMatrix
        

def listToPerm (mappings, numNodes):
    """ listToPerm creates a permutation representation from a list of mappings

        parameters: mappings: an array of 2-element arrays where the 2-element arrays correspond to mappings. 
                              For example, [1, 2] corresponds to 1 -> 2
                    numNodes: an integer corresponding to the number of nodes in the poset
        
        output: an array representation of the permutation. For example, for the mapping 1 -> 2, 2 -> 1 on the nodes
                0, 1, 2, the output would be [0, 2, 1]. 
                if there is an invalid input such that the mapping does not result in a permutation, 
                listToPerm returns 0
    """
    mappingDict = toRelationsDictionary(mappings)
    perm = []
    for i in range(numNodes):
        if i in mappingDict:
            perm += mappingDict[i]
        else:
            perm += [i]
    if len(set(perm)) != numNodes:
        return 0
    else:
        return perm

########################
##    examples for    ##
## fancyAutomorphisms ##
########################

# test 1
# test = [[1, 1, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]]
# print(fancyAutomorphisms(test))

# test 2: chain
# test = [[1, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]]
# print(fancyAutomorphisms(test))

# test 3: separate
# test = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# print(fancyAutomorphisms(test))

# test 4:
# test = [[1, 1, 1, 1, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]]
# print(fancyAutomorphisms(test))

# test 5:
# test = [[1, 1, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1]]
# print(fancyAutomorphisms(test))

# test 6:
# test = [[1, 1, 1, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]]
# print(fancyAutomorphisms(test))
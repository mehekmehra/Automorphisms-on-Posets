from itertools import permutations, product
from sympy.combinatorics.named_groups import SymmetricGroup
from collections import defaultdict
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

    # takes in the relations list
    relationsList = []
    n = int(input("Number of Relations : "))
    print()
    for i in range(0, n):
        ele = list(map(int,input("Enter a relation : ").strip().split()))[:2]
        relationsList.append(ele)
    print()

    # takes in the number of nodes
    numNodes = int(input('How many nodes are in your poset? '))

    # check if poset is valid
    if posetChecker(relationsList, numNodes) == False:
        print('Unfortunately that is not a valid poset. Please try again with a different set of relations')
        return

    # generates the covers matrix that are used later
    myArr = leqMatrix(numNodes, relationsList)

    print()
    print('Do you want to find all of the automorphisms for your poset')
    print('or check if a permutation is an automorphism?')
    choice = input('Enter in a for all automorphisms or b to check : ')
    print()
    if choice == 'a' or choice == 'A':
        print()
        print('Do you want to use the (mostly) faster algorithm or the slower algorithm?')
        print('The faster one is recommended for larger posets but requires more information')
        fastChoice = input('Enter F for faster : ')

        if fastChoice == 'f' or fastChoice == 'F':
            print()
            print('Enter the nodes at each height.')

            instructions  = input('Do you want instructions? Enter y for yes : ')
            if instructions == 'y' or 'Y':
                print()
                print('Enter the number of heights in your poset. Then, enter the number of nodes at each of these heights.')
                print('If all of the nodes are dijoint, then enter them as being at the same height.')
                print('However, if there is a node disjoint from the rest of the poset (more than just single disjoint nodes,')
                print('then the disjoint node would have its own height.')
                print('For example, the poset defined as 0 < 1, 0 < 2, 1 < 3, 2 < 3 and a single disjoint node 4 would be entered as')
                print('Number of Heights: 4')
                print('Nodes at a Height: 0')
                print('Nodes at a Height: 1 2')
                print('Nodes at a Height: 3')
                print('Nodes at a Height: 4')

            # takes in the height list for the faster algorithm
            print()
            heightList = []
            numHeight = int(input("Number of Heights : "))
            print()
            for i in range(0, numHeight):
                heightStr = input('Nodes at a Height : ')
                nodesAtHeight = [int(x) for x in heightStr.split()]
                heightList += [nodesAtHeight]
            print(heightList)
            print()

            # runs the faster automorphism finder
            fancy = input('Enter F for fancy printing : ')
            if fancy == 'F' or fancy == 'f':
                faster(relationsList, heightList, numNodes, True)
            else:
                faster(relationsList, heightList, numNodes, False)
        
        else:
            # runs the slower automorphism finder
            print()
            fancy = input('Enter F for fancy printing : ')
            if fancy == 'F' or fancy == 'f':
                fancyAutomorphisms(myArr, True)
            else:
                fancyAutomorphisms(myArr, False)



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
        
        # takes in the mapping for the automorphism that the user wants to check
        mappingList = []
        numMap = int(input("Number of Mappings : "))
        print()
        for i in range(0, numMap):
            mapping = list(map(int,input("Enter a mapping : ").strip().split()))[:2]
            mappingList.append(mapping)
        print()
        perm = listToPerm(mappingList, numNodes)

        # runs the automorphism checker
        automorphismChecker(myArr, perm)
    else:
        # if the user doesn't input an appropriate choice
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

def fancyAutomorphisms(myArr, fancy):
    """ automorphisms takes in an array representation of a matrix (less than matrix, similar to adjacency)
        and returns the number of automorphisms and the mappings (as permutations)

        parameters: myArr: an array representation of a matrix where less than/equal to relations
                            are represented by 1s by rows and non adjacent/ greater than relations
                            are 0s. (see the examples and the reference picture)
                    fancy: boolean: true if the user wants fancy printing (printing out the automorphisms)
                            
        output: autCount: returns the number of automorphisms
                autsArray: prints the mappings as permutations
                                (eg 0 -> 1, 1 -> 0, 0 -> 0 would be [1, 0, 2])
    """
    
    posetArr = np.array(myArr)
    possibleMaps = permutationGroup(myArr)
    autCount = 0
    elements = elementList(len(myArr))
    autsArr = []
    file = open('ouput.txt', 'w+')

    for permutation in possibleMaps:
        possiblePoset = np.array(myArr)
        # swap cols
        possiblePoset[:] = possiblePoset[:, permutation]
        # swap rows
        possiblePoset[elements] = possiblePoset[permutation]

        if (possiblePoset == posetArr).all():
            autCount += 1
            autsArr += [permutation]
            if fancy == False:
                print(permutation)


    if fancy == True:
        print('The automorphisms on this poset are :  \n')
        file.write('The automorphisms on this poset are :  \n')
        
        for i in range(len(autsArr)):
            print('f' + str(i) + ': \n')
            for j in range(len(autsArr[i])):
                print(str(j) + ' -> ' + str(autsArr[i][j]))
                file.write(str(j) + ' -> ' + str(autsArr[i][j]) + '\n')
            print('\n')
            file.write('\n')

    print('This poset has ' + str(autCount) + ' automorphisms')
    file.write('This poset has ' + str(autCount) + ' automorphisms')
    file.close()
    return autsArr, autCount


###################
## Faster Finder ##
###################


def faster(relationsList, heightList, numNodes, fancy):
    """ faster finds all of the automorphisms on an inputed poset.
    parameters: heightList: list of lists. each sublist represents the nodes with the same height. even if a node is the only one of
                that height include it. So a chain would be [[0], [1], [2]] and disjoint would be [[0, 1, 2]]

                relationsList: a list of strictly less that relations. Lower element first. So a chain with 0 < 1 < 2 would be
                [[0, 1], [1, 2]]

                numNodes: the number of nodes

                fancy: boolean: true if the user wants fancy printing (printing out the automorphisms)

    output: autCount: an integer corresponding to the number of automorphisms
            autsArray: an array of all of the automorphisms as permutations
    """
    myArr = leqMatrix(numNodes, relationsList)
    posetArr = np.array(myArr)
    possibleMaps = fasterPerm(heightList)
    autCount = 0
    elements = elementList(numNodes)
    autsArr = []
    file = open('ouput.txt', 'w+')

    for permDict in possibleMaps:
        permutation = []
        sortKeys = sorted(permDict.keys())
        for key in sortKeys:
            permutation += [permDict[key]]
        

        possiblePoset = np.array(myArr)
            # swap cols
        possiblePoset[:] = possiblePoset[:, permutation]
            # swap rows
        possiblePoset[elements] = possiblePoset[permutation]

        if (possiblePoset == posetArr).all():
            autCount += 1
            autsArr += [permutation]
            
    if fancy is True:
        print('The automorphisms on this poset are :  \n')
        file.write('The automorphisms on this poset are :  \n')

        for i in range(len(autsArr)):
            print('f' + str(i) + ': \n')
            file.write('f' + str(i) + ': \n')
            for j in range(len(autsArr[i])):
                print(str(j) + ' -> ' + str(autsArr[i][j]))
                file.write(str(j) + ' -> ' + str(autsArr[i][j]) + '\n')
            print('\n')
            file.write('\n')

    print('This poset has ' + str(autCount) + ' automorphisms')
    file.write('This poset has ' + str(autCount) + ' automorphisms')
    file.close()

    return  autCount, autsArr


###################
## Poset Checker ##
###################

def posetChecker(relationsList, numNodes):
    """ posetChecker checks to see if an inputted relations list acutally corresponds to a poset
        parameters: relationsList: a list of strictly less that relations. Lower element first. So a chain with 0 < 1 < 2 would be
                    [[0, 1], [1, 2]]

                    numNodes: the number of nodes
        
        output: boolean: true if the input is a poset
    """
    poset = Poset(numNodes)
    for edges in relationsList:
        poset.addEdge(edges)
    if poset.isCyclic():
        return False

    elif coversAreValid(relationsList):
        return True
    else:
        return False


#############
## Helpers ##
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

def fasterPerm(heightList):
    """ fasterPerm finds all of the permutations of the nodes in a given poset but restricts it to possible posets based on preserving height

        parameters: heightList: list of lists. each sublist represents the nodes with the same height. even if a node is the only one of
                that height include it. So a chain would be [[0], [1], [2]] and disjoint would be [[0, 1, 2]]

        output: permutations: a list of dictionary representations of the possible permutations
    """
    lol = []
    for x in heightList:
        dictsList = []
        unPerm = sorted(x)
        perms = list(permutations(unPerm))
        # print(perms)
        
        for perm in perms:
            dictionary = {}
            for i in range(len(x)):
                dictionary[unPerm[i]] = perm[i]
                # print(dictionary)
            dictsList += [dictionary]
        lol += [dictsList]
    test = list(product(*lol))
    res = []
    for x in test:
        combinedDict = {}
        for dict in x:
            combinedDict.update(dict)
        res += [combinedDict]
    print(len(res))
    print('')
    return res


def elementList(numNodes):
    """ elementList outputs a list of the nodes in myArr
        primarily a helper function

        parameters: myArr: an array representation of a matrix where less than/equal to relations
                            are represented by 1s by rows and non adjacent/ greater than relations
                            are 0s. (see the examples and the reference picture)

        output: a list of nodes. 
    """
    elementsList = []
    start = 0
    for x in range(numNodes):
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

##########################
## Poset Checker Helper ##
##########################

## adapts code from https://www.geeksforgeeks.org/detect-cycle-in-a-graph/ for the isCyclic
class Poset():
    def __init__(self, numNodes):
        """ constructor: creates a poset object

            parameters: numNodes: an integer corresponding to the number of nodes in the poset
        """
        self.poset = defaultdict(list)
        self.N = numNodes
  
    def addEdge(self, edgePair):
        """ addEdge adds an edge to the poset object

            parameters: edgePairs: a 2-element list of two nodes with the lower node being the first entry
        """
        lower = edgePair[0]
        greater = edgePair[1]

        self.poset[lower].append(greater)
  
    def isCyclicRecursion(self, node, visited, recStack):
        visited[node] = True
        recStack[node] = True

        for neighbour in self.poset[node]:
            if visited[neighbour] == False:
                if self.isCyclicRecursion(neighbour, visited, recStack) == True:
                    return True
            elif recStack[neighbour] == True:
                return True
  
        recStack[node] = False
        return False
  
    def isCyclic(self):
        visited = [False] * (self.N + 1)
        recStack = [False] * (self.N + 1)
        for node in range(self.N):
            if visited[node] == False:
                if self.isCyclicRecursion(node,visited,recStack) == True:
                    return True
        return False

def commonElement(list1, list2):
    """ commonElement returns true if list1 and list2 share at least one common element

        parameters: list1, list2: lists that will be compared

        output: boolean
    """
    res = False
    for x in list1:
        for y in list2:
            if x == y:
                res = True
                return res        
    return res


def coversAreValid(relationsList):
    """ coversAreValid returns a boolean corresponding to whether or not the provided covers are covers or if there are paths in which they are not covers
       
        parameters: relationsList: an array of 2-element arrays where the elements or the sub arrays are nodes

        output: boolean: true if covers are valid, false if covers are not valid
    """
    relationsDict = toRelationsDictionary(relationsList)
    for relation in relationsList:
        lower = relation[0]   
        greater = relation[1]
        if lower in relationsDict and greater in relationsDict:
            if commonElement(relationsDict[lower], relationsDict[greater]):
                return False
    return True



# Z4
# relationsList = [[0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [7, 8], [9, 10], [10, 11], [0, 5], [3, 8], [6, 11], [9, 2]]
# heightList = [[0, 3, 6, 9], [1, 4, 7, 10], [2, 5, 8, 11]]
# numNodes = 12
# print(faster(relationsList, heightList, numNodes))


# relationsList = [[0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [7, 8], [0, 5], [3, 8], [6, 2], [9, 10], [10, 11], [12, 13], [13, 14], [15, 16], [16, 17], [18, 19], [19, 20], [21, 22], [22, 23], [9, 14], [12, 17], [15, 20], [18, 23], [21, 11]]
# heightList = [[0, 3, 6], [1, 4, 7], [2, 5, 8], [9, 12, 15, 18, 21], [10, 13, 16, 19, 22], [11, 14, 17, 20, 23]]
# numNodes = 24
# print(faster(relationsList, heightList, numNodes))

### p = 5
# 2 on each
# relationsList = [[0, 1], [0, 3], [2, 3], [2, 5], [4, 5], [4, 7], [6, 7], [6, 9], [8, 1], [8, 9]]
# heightList = [[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]]
# numNodes = 10
# print(faster(relationsList, heightList, numNodes))

#### has 10 auts

# 3 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [2, 3], [2, 5], [2, 7], [4, 5], [4, 7], [4, 9], [6, 1], [6, 7], [6, 9], [8, 1], [8, 3], [8, 9]]
# heightList = [[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]]
# numNodes = 10
# print(faster(relationsList, heightList, numNodes))
#### has 10 auts



# 4 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [0, 7], [2, 3], [2, 5], [2, 7], [2, 9], [4, 1], [4, 5], [4, 7], [4, 9], [6, 1], [6, 3], [6, 7], [6, 9], [8, 1], [8, 3], [8, 5], [8, 9]]
# heightList = [[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]]
# numNodes = 10
# print(faster(relationsList, heightList, numNodes))
#### has 120 auts



# 5 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [0, 7], [0, 9], [2, 1], [2, 3], [2, 5], [2, 7], [2, 9], [4, 1], [4, 3], [4, 5], [4, 7], [4, 9], [6, 1], [6, 3], [6, 5], [6, 7], [6, 9], [8, 1], [8, 3], [8, 5], [8, 7], [8, 9]]
# heightList = [[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]]
# numNodes = 10
# print(faster(relationsList, heightList, numNodes))
#### has 14400


#### p = 7
# 7 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [0, 7], [0, 9], [0, 11], [0, 13], [2, 1], [2, 3], [2, 5], [2, 7], [2, 9], [2, 11], [2, 13], [4, 1], [4, 3], [4, 5], [4, 7], [4, 9], [4, 11], [4, 13], [6, 1], [6, 3], [6, 5], [6, 7], [6, 9], [6, 11], [6, 13], [8, 1], [8, 3], [8, 5], [8, 7], [8, 9], [8, 11], [8, 13], [10, 1], [10, 3], [10, 5], [10, 7], [10, 9], [10, 11], [10, 13], [12, 1], [12, 3], [12, 5], [12, 7], [12, 9], [12, 11], [12, 13]]
# heightList = [[0, 2, 4, 6, 8, 10, 12], [1, 3, 5, 7, 9, 11, 13]]
# numNodes = 14
# print(faster(relationsList, heightList, numNodes))

### 25401600 automorphisms


# 6 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [0, 7], [0, 9], [0, 11], [2, 3], [2, 5], [2, 7], [2, 9], [2, 11], [2, 13], [4, 1], [4, 5], [4, 7], [4, 9], [4, 11], [4, 13], [6, 1], [6, 3], [6, 7], [6, 9], [6, 11], [6, 13], [8, 1], [8, 3], [8, 5], [8, 9], [8, 11], [8, 13], [10, 1], [10, 3], [10, 5], [10, 7], [10, 11], [10, 13], [12, 1], [12, 3], [12, 5], [12, 7], [12, 9],  [12, 13]]
# heightList = [[0, 2, 4, 6, 8, 10, 12], [1, 3, 5, 7, 9, 11, 13]]
# numNodes = 14
# print(faster(relationsList, heightList, numNodes))

## 5040

# 5 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [0, 7], [0, 9], [2, 3], [2, 5], [2, 7], [2, 9], [2, 11], [4, 5], [4, 7], [4, 9], [4, 11], [4, 13], [6, 1], [6, 7], [6, 9], [6, 11], [6, 13], [8, 1], [8, 3], [8, 9], [8, 11], [8, 13], [10, 1], [10, 3], [10, 5], [10, 11], [10, 13], [12, 1], [12, 3], [12, 5], [12, 7], [12, 13]]
# heightList = [[0, 2, 4, 6, 8, 10, 12], [1, 3, 5, 7, 9, 11, 13]]
# numNodes = 14
# print(faster(relationsList, heightList, numNodes))

## 14

# 4 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [0, 7], [2, 3], [2, 5], [2, 7], [2, 9], [4, 5], [4, 7], [4, 9], [4, 11], [6, 7], [6, 9], [6, 11], [6, 13], [8, 1], [8, 9], [8, 11], [8, 13], [10, 1], [10, 3], [10, 11], [10, 13], [12, 1], [12, 3], [12, 5],  [12, 13]]
# heightList = [[0, 2, 4, 6, 8, 10, 12], [1, 3, 5, 7, 9, 11, 13]]
# numNodes = 14
# print(faster(relationsList, heightList, numNodes))

## 14

# 3 on each
# relationsList = [[0, 1], [0, 3], [0, 5], [2, 3], [2, 5], [2, 7], [4, 5], [4, 7], [4, 9], [6, 7], [6, 9], [6, 11], [8, 9], [8, 11], [8, 13], [10, 1], [10, 11], [10, 13], [12, 1], [12, 3],  [12, 13]]
# heightList = [[0, 2, 4, 6, 8, 10, 12], [1, 3, 5, 7, 9, 11, 13]]
# numNodes = 14
# print(faster(relationsList, heightList, numNodes))

## 14

# 2 on each
# relationsList = [[0, 1], [0, 3], [2, 3], [2, 5], [4, 5], [4, 7], [6, 7], [6, 9], [8, 9], [8, 11], [10, 11], [10, 13], [12, 1], [12, 13]]
# heightList = [[0, 2, 4, 6, 8, 10, 12], [1, 3, 5, 7, 9, 11, 13]]
# numNodes = 14
# print(faster(relationsList, heightList, numNodes))

## 14
#!/usr/bin/python

# Program that parses LISP-esque intermediate code for the 3rd COMP3109 assignment.
# Why reinvent the wheel?

from pyparsing import OneOrMore, nestedExpr


#Declare node class here
#as per tutorial wk 11, it will require 'in' sets and 'out' sets for 
#variable analysis. It would also probably need a read variable list and a
#write variable list.
#Obvioulsy its going to need a list of children. No parent as it is a directed list.

class blockNode:
    def __init__(self,blockNumber):
        self.inSet = []
        self.outSet = []
        #children is a STRING list of block names.
        #A dictionary will be required to match names with block reference
        #This makes tree construction simpler, as it solves the problem of
        #trying to refernce a child node that has not been constructed yet.
        self.children = []
        self.readReg = []
        self.writeReg = []
        self.name = blockNumber
        self.visited = False

class functionTree:
    def __init__(self,name,arguments,headBlock):
        self.name = name
        self.args = arguments
        self.headBlock = headBlock
        self.visitedBlocks = []

all_the_text = open('tests/simple.in').read()      # all text from a text file
data = OneOrMore(nestedExpr()).parseString(all_the_text)
data = data[0];                                    # Remove redundant first list layer
print 'Data is length: '
print len(data)

#this is a list of functionTrees
functionList = []

for i in range(0,len(data)):
    #print 'Function: ' + repr(i) + repr(data[i])
    #This is the function layer
    #data[i][0] is the function name
    #data[i][1] is the args
    #data[i][2-len] is the blocks

    #This will involve the creation of a new tree for each function, so that
    #each function can be analyzed.
    #Do we cut out entire functions if they are unreachable?
    #It might be best if we do the analysis function by function,
    #but begin the search at main, and flag functions that are used.
    #Then add these functions to the work list. If a function has already
    #been analyzed, skip it. This requires the use of a 'searched' list
    print 'Function name is: ' 
    print data[i][0]
    print 'Arguments are: ' 
    print data[i][1]

    #This is a dictionary of block labels with matching blockNode references
    functionBlocks = {}

    for j in range(2,len(data[i])):
        #This is the block level loop
        #It will require the construction of a new block node.
        print 'Blocks number is: '
        print data[i][j][0]
        print 'Instructions list: '

        currentNode = blockNode(data[i][j][0])
        #add reference to dictionary
        functionBlocks[data[i][j][0]] = currentNode


        for k in range(1,len(data[i][j])):
            #Scan for register reads, writes and branches here
            #Register read/writes will be useful for dead code detection
            #Branch detection will be needed for unreachable code analysis
            if(data[i][j][k][0] == 'br'):
                currentNode.children.append(data[i][j][k][2])
                currentNode.children.append(data[i][j][k][3])

            if(data[i][j][k][0] == 'call'):
                #this is where the nex function would be added to the work queue
                print data[i][j][k][2]
                print 'Called'

            print data[i][j][k]

    functionList.append(functionTree(data[i][0],data[i][1],functionBlocks['0']))
    # It might be preferable to go around and fix the children references at this
    # point in code.
    for blkName, blkRef in functionBlocks.iteritems():
        #read in child list
        stringList = blkRef.children
        #blank out child list
        blkRef.children = []
        #create new child list of references
        for child in stringList:
            blkRef.children.append(functionBlocks[child])


##TREE CONSTRUCTION FINISHED

#START TASK 2 BFS HERE



def bfsTree(block,functionTree):
    block.visited = True
    #add block REFERENCE to the function visited list.
    if block not in functionTree.visitedBlocks:
        functionTree.visitedBlocks.append(block)
    for child in block.children:
        bfsTree(child,functionTree)



for func in functionList:
    #This should not be a for loop, instead the traverser should start at 'main'
    #and add any functions that are called to a work list. I (Alex) am starting this
    #way because I'm tackling the block node traversal problem first.
    bfsTree(func.headBlock,func)
    print 'Function Name: '
    print func.name
    print 'Visited Blocks: '
    for blk in func.visitedBlocks:
        print blk.name


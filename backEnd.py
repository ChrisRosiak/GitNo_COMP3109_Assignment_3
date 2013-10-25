#!/usr/bin/python

# Program that parses LISP-esque intermediate code for the 3rd COMP3109 assignment.
# Why reinvent the wheel?

from pyparsing import OneOrMore, nestedExpr
import sys

# sys.argv is a list of the command line arguments used to execute this Python script.
# sys.argv[0] is the Python script name.
# sys.argv[1] is the first argument, i.e. file name of the input intermediate code.

#Declare node class here
#as per tutorial wk 11, it will require 'in' sets and 'out' sets for 
#variable analysis. It would also probably need a read variable list and a
#write variable list.
#Obvioulsy its going to need a list of children. No parent as it is a directed list.

class blockNode:
    def __init__(self,blockNumber):
        self.inSet = set()
        self.outSet = set()
        self.useSet = set()
        self.defSet = set()
        self.regToVar = {}
        #children starts as a string list of node References. It is then fixed to actual references, otherwise it attempts to link a node that has not been created yet.
        self.children = set()
        self.readReg = []
        self.writeReg = []
        self.instrs = [] #list of instructions for block
        self.name = blockNumber
        self.visited = False
        self.parent = set()
    # This method is inserted for testing purposes.
    def __repr__(self):
        return repr((self.name))

class functionTree:
    def __init__(self,name,arguments,headBlock):
        self.name = name
        self.args = arguments
        self.headBlock = headBlock
        self.visitedBlocks = []

#inputFile = "tests/task3/example.in"
all_the_text = open(sys.argv[1]).read()      # all text from a text file
#all_the_text = open(inputFile).read()      # all text from a text file
data = OneOrMore(nestedExpr()).parseString(all_the_text)
data = data[0];                                    # Remove redundant first list layer
#print 'Data is length: '
#print len(data)

#this is a list of functionTrees
functionList = []
variableDict = {}

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
    #print 'Function name is: ' 
    #print data[i][0]
    #print 'Arguments are: ' 
    #print data[i][1]

    #This is a dictionary of block labels with matching blockNode references
    functionBlocks = {}

    for j in range(2,len(data[i])):
        #This is the block level loop
        #It will require the construction of a new block node.
        #print 'Blocks number is: '
        #print data[i][j][0]
        #print 'Instructions list: '

        currentNode = blockNode(data[i][j][0])
        #add reference to dictionary
        functionBlocks[data[i][j][0]] = currentNode


        for k in range(1,len(data[i][j])):
            #Scan for register reads, writes and branches here
            #Register read/writes will be useful for dead code detection
            #Branch detection will be needed for unreachable code analysis

            #But first, add the instruction to the node instruction list
            currentNode.instrs.append(data[i][j][k])
            if(data[i][j][k][0] == 'br'):
                currentNode.children.add(data[i][j][k][2])
                currentNode.children.add(data[i][j][k][3])

                #If non-called functions are to be culled, this is where functions should be marked as called, and therefore the functions are reachable.
            #if(data[i][j][k][0] == 'call'):
                #print data[i][j][k][2]
                #print 'Called'
            #print data[i][j][k]

    functionList.append(functionTree(data[i][0],data[i][1],functionBlocks['0']))
    #This is where the string references to blocks are fixed to be actual node references using the functionBlocks dictionary.
    for blkName, blkRef in functionBlocks.iteritems():
        #read in child list
        stringList = blkRef.children
        #blank out child list
        blkRef.children = []
        #create new child list of references
        for child in stringList:
            blkRef.children.append(functionBlocks[child])
            functionBlocks[child].parent.add(blkRef)

##TREE CONSTRUCTION FINISHED

##START TASK 2 DFS HERE
def dfsTree(block,functionTree):
    block.visited = True
    #add block to the function visited list.
    if block not in functionTree.visitedBlocks:
        functionTree.visitedBlocks.append(block)
    for child in block.children:
        dfsTree(child,functionTree)

for func in functionList:
    dfsTree(func.headBlock,func)

#END TASK 2
##############################################################
# BEGIN TASK 4


# KEY TERMS 
# varToRegDict[n] - a mapping of registers to variables avaliable for node (n).


#function for joining the variables that are avaliable to a basic block
def unionVariableDicts(blockNode):
    newVarToReg = {}
    newRegToVar = {}
    for parent in blockNode.parent:
        for reg in parent.regToVar:
            if reg in newRegToVar and parent.regToVar[reg] != newRegToVar[reg]:
                newRegToVar[reg] = None #there are two possible values for a variable hence dont know s
            else:
                newRegToVar[reg] = parent.regToVar[reg]
    return newRegToVar


#Traverse through a blocks children until the register containing the value is changed or the value in the variable is changed
def replaceRegister(basicBlock,replaceValue,toReplace,variable):
    for instruction in basicBlock.instrs:
        #checking if an instruction changes the value in the replace register
        if instruction[0] in ['add', 'sub', 'mul', 'div', 'eq', 'gt', 'lt', 'call'] and instruction[1] == replaceValue:
            if instruction[0] == 'ld' and instruction[1] == toReplace: pass
            if instruction[0] == 'st' and instruction[1] == variable: return
            if instruction[0] in ['add', 'sub', 'mul', 'div', 'eq', 'gt', 'lt']:
                if instruction[2] == toReplace: instruction[2] = replaceValue
                if instruction[3] == toReplace: instruction[3] = replaeValue
            return

        #checking if an instruction changes the value of the search variable
        if instruction[0] == "st" and instruction[1] == variable:
            return

        #if an instruction hasnt changed the register or variable we are replacing check if an instruction needs to be
        #rewritten in place in order for the dead code elimination which follows to remove the now dead code
        if not(instruction[0] == "ret"):
            if instruction[0] in ['lc','ld'] and instruction[2] == toReplace:
                instruction[2] = replaceValue
            if instruction[0] in ['add', 'sub', 'mul', 'div', 'eq', 'gt', 'lt']:
                if instruction[2] == toReplace: instruction[2] = replaceValue
                if instruction[3] == toReplace: instruction[3] = replaceValue
            if instruction[0] == 'call':
                for i in range(3,len(instruction)):
                    if  instruction[i] == toReplace:
                        instruction[i] = replaceValue

    #recurse on each of the blocks children for the change to propergate until the value gets changed
    for succesor in basicBlock.children:
        replaceRegister(succesor,replaceValue,replace,variable)
    return


# traverse through the CFG and if a variable is already defined in memory replace the following references to that register to be the register
# that already holds the value. By changing the instructions in place it allows the dead code removal to later remove he value in further processing
for CFG in functionList:
   CFG = CFG.visitedBlocks
   CFG = sorted(CFG, key=lambda node: node.name, reverse=False)
   for basicBlock in CFG:
      basicBlock.regToVar = unionVariableDicts(basicBlock)  #need to union its reg var dict with all its succesors to know what variables are in registers
      for i in range(0, len(basicBlock.instrs)):
            if basicBlock.instrs[i][0] in ['ld']:
                if basicBlock.instrs[i][2] in basicBlock.regToVar.values(): #if the variable is already in a reg
                    key = [key for key,value in basicBlock.regToVar.items() if value == basicBlock.instrs[i][2]][0] #get the variable in the register
                    replace = basicBlock.instrs[i][1]
                    replaceRegister(basicBlock,key,replace,basicBlock.regToVar[key]) #replaces the instructions in place
                else: basicBlock.regToVar[basicBlock.instrs[i][1]] = basicBlock.instrs[i][2]
                
            if basicBlock.instrs[i][0] in ['add', 'sub', 'mul', 'div', 'eq', 'gt', 'lt', 'call']: ##if the reg value gets changed make the dict
                if basicBlock.instrs[i][1] in basicBlock.regToVar:
                    basicBlock.regToVar[basicBlock.instrs[i][1]] = None



##############################################################
# BEGIN TASK 3 


# KEY TERMS 
# use[n] - set of registers that are used at node n.
#        - A variable/register is used when its value is (1) returned from the current function (ret),
#           (2) stored to a variable (st), (3) is used as a condition for a branch (br), or (4) used by an instruction
#           whose result is used.
# def[n] - set of registers that are defined at node n.
#        - An assignment of a value to a register.


# Function declaration for one of the data-flow equations in the iterator.
def unionSuccessors(blockNode):
   """Function that creates a list of all the in sets from the successors of the given blockNode."""
   newOutSet = set()
   for child in blockNode.children:
      # Add the child inSet to the newSet, as well as the successors of the given blockNode.
      newOutSet.union(child.inSet)
      newOutSet.union(unionSuccessors(child))
   return newOutSet

# Determine use[n] and def[n] for all nodes in functionList.
for CFG in functionList:
   CFG = CFG.visitedBlocks
   CFG = sorted(CFG, key=lambda node: node.name, reverse=False)
   for basicBlock in CFG:
      # This loop is used to determine what registers are used as per condition (4).
      for i in range(0, len(basicBlock.instrs)):
         for futureInstr in basicBlock.instrs[i+1:]:
            if basicBlock.instrs[i][0] in ['add', 'sub', 'mul', 'div', 'eq', 'gt', 'lt', 'call']:
               # Check if any future instructions use the result of the instruction basicBlock.instrs[i].
               if futureInstr[0] in ['add', 'sub', 'mul', 'div', 'eq', 'gt', 'lt', 'st', 'call']:
                  if basicBlock.instrs[i][1] in futureInstr[2:]:
                     basicBlock.useSet.update(set(basicBlock.instrs[i][2:]))
                     break
               elif futureInstr[0] in ['br', 'ret']:
                  if basicBlock.instrs[i][1] in futureInstr[1]:
                     basicBlock.useSet.update(set(basicBlock.instrs[i][2:]))
                     break
      # This loop determines def[n] and use[n] for conditions (1), (2), and (3).
      for instruction in basicBlock.instrs:
         # Does the instruction assign a value to a register.
         if instruction[0] in ['lc', 'ld', 'add', 'sub', 'mul', 'div', 'eq', 'gt', 'lt', 'call']:
            # If so, add the register name to the def set of the basic block node.
            basicBlock.defSet.add(instruction[1])
         # Does the value of a register get used.
         elif instruction[0] in ['ret', 'br']:
            basicBlock.useSet.add(instruction[1])
         elif instruction[0] == 'st':
            basicBlock.useSet.add(instruction[2])


# Create dictionary variables to store the in and out set of the basic blocks.
# The key will be node (basic block) and the value will be the inSet or outSet of the node.
in_prime = {}
out_prime = {}

## ANALYSIS PHASE 

# Pseudocode of the iterator algorithm.
### Comments on actual Python code are prefixed with three '#' symbols.

### Analyse each CFG from the functionList variable.
for CFG in functionList:
   CFG = CFG.visitedBlocks
   CFG = sorted(CFG, key=lambda node: node.name, reverse=True)
   # for each node n in CFG                 # Initialise solutions
   # in[n] = None ; out[n] = None           ##
   for node in CFG:
      node.inSet = []
      node.outSet = []
   # repeat
   while True:
      # for each node n in CFG in reverse topsort order
      for node in CFG:
         # in'[n] = in[n]                                        # Save current results
         # out'[n] = out[n]                                      ##
         in_prime[node] = node.inSet
         out_prime[node] = node.outSet
         # out[n] = Union in[s] (where s is an element from the set of all successors of the node n)    # Solve data-flow equations
         node.outSet = unionSuccessors(node)
         # in[n] = use[n] Union (out[n] - def[n])                                                       ##
         node.inSet = node.useSet.union(node.outSet - node.defSet)
      # until in'[n] = in[n] and out'[n] = out[n] for all n               ## Test for convergence
      for node in CFG:
         if node.inSet != in_prime[node] or node.outSet != out_prime[node]:
            break
      else:
         break

## TRANSFORMATION PHASE

# For the transformation phase, a union of the in and out sets must be made for each basic block. For each
# instruction that uses a register name not contained in the union of out and in set, must be removed.

for CFG in functionList:
   CFG = CFG.visitedBlocks
   CFG = sorted(CFG, key=lambda node: node.name, reverse=False)
   for node in CFG:
      keepRegSet = node.inSet.union(node.outSet)
      for i in range(0, len(node.instrs)):
         if node.instrs[i][0] in ['lc', 'ld', 'call']:
            if node.instrs[i][1] not in keepRegSet:
               node.instrs[i] = None
         elif node.instrs[i][0] in ['add', 'sub', 'mul', 'div', 'eq', 'lt', 'gt']:
            if set(node.instrs[i][1:]).difference(keepRegSet):
               node.instrs[i] = None
      # Remove all instances of None in the instruction member list.
      for i in range(0, node.instrs.count(None)):
         node.instrs.remove(None)

# Sort the visitedBlocks list in ascending order.
for CFG in functionList:
   CFG.visitedBlocks = sorted(CFG.visitedBlocks, key=lambda node: node.name, reverse=False)


# END TASK 3
#############################################################
#BEGIN FILE OUTPUT

#print 'OUTPUT - remove all print statements above this line (and this one)'
print '(',                                               #open file
for func in functionList:
    #If not first function, fix indentation
    if func != functionList[0]:
        print ' ',
    print '(' + func.name + ' (' + ' '.join(func.args) + ')' #open function
    for blk in func.visitedBlocks:
        print '    (' + str(blk.name),                       #open block
        for inst in blk.instrs:
            print '\t' + '(' + ' '.join(inst) + ')',
            #If not last element in list, print newline
            if inst != blk.instrs[-1]:
                print
        print ')',                                        #close block
        #Do not print newline at last element
        if blk != func.visitedBlocks[-1]:
            print
    print ')',                                           #close function
    if func != functionList[-1]:
        print
print ')'                                                #close file

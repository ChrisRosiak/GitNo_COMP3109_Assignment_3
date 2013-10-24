#!/usr/bin/python

## Python module for task 3 of the COMP3109 Assignment 3.
## This module performs dead code elimintation.
## Author: Christopher Rosiak
## Date: 2013-10-17


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
      newOutSet.union(child.inSet)
      newOutSet.union(unionSuccessors(child))
   newOutSet = set(newOutSet)
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
               # Check is any future instructions use the result of the instruction basicBlock.instrs[i].
               if basicBlock.instrs[i][1] in futureInstr[2:]:
                  basicBlock.useSet.add(basicBlock.instrs[i][2:])
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



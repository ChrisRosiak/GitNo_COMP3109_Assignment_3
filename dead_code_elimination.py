#!/usr/bin/python

## Python module for task 3 of the COMP3109 Assignment 3.
## This module performs dead code elimintation.
## Author: Christopher Rosiak
## Date: 2013-10-17


# KEY TERMS 
# use[n] - set of variables that are used at node n.
# def[n] - set of variables that are defined at node n.

# Function declaration for the iterator.
def unionSuccessors(blockNode):
   """Function that creates a list of all the in sets from the successors of the given blockNode."""
   newOutSet = []
   for child in blockNode.children:
      newOutSet.extend(child.inSet)
      newOutSet.extend(unionSuccessors(child))
   newOutSet = list(set(newOutSet))
   return newOutSet

def newInSet(blockNode, useSet, defSet):
   """Function that returns the new in set for the given blockNode."""
   inSet = set(useSet).union(set(blockNode.outSet) - set(defSet))
   return list(inSet)

# TODO - Determine use[n] for all nodes in functionList.

# TODO - Determine def[n] for all nodes in functionList.

# Create dictionary variables to store the in and out set of the basic blocks.
# The key will be node (basic block) and the value will be the inSet or outSet of the node.
in_prime = {}
out_prime = {}
# TODO - Finish the iterator algorithm.

# Pseudocode of the iterator algorithm.
### Comments on actual Python code are prefixed with three '#' symbols.

### Analyse each CFG from the functionList variable.
for CFG in functionList:
   #for each node n in CFG                 # Initialise solutions
   #   in[n] = None ; out[n] = None        ##
   for node in CFG:
      node.inSet = []
      node.outSet = []
   #repeat
   while True:
   #   for each node n in CFG in reverse topsort order
      for node in CFG:
   #     in'[n] = in[n]                                        # Save current results
   #     out'[n] = out[n]                                      ##
         in_prime[node] = node.inSet
         out_prime[node] = node.outSet
   #     out[n] = Union in[s] (where s is an element from the set of all successors of the node n)    # Solve data-flow equations
         node.outSet = unionSuccessors(node)
   #     in[n] = use[n] Union (out[n] - def[n])                                                       ##
         node.inSet = newInSet(node, useSet, defSet)
   #until in'[n] = in[n] and out'[n] = out[n] for all n               ## Test for convergence
     # if in_prime == node.inSet and out_prime == node.outSet:

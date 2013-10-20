#!/usr/bin/env python3

## Python module for task 3 of the COMP3109 Assignment 3.
## This module performs dead code elimintation.
## Author: Christopher Rosiak
## Date: 2013-10-17


# Pseudocode of the iterator algorithm.

#for each node n in CFG                 # Initialise solutions
#   in[n] = None ; out[n] = None        ##
   
#repeat
#   for each node n in CFG in reverse topsort order
#     in'[n] = in[n]                                        # Save current results
#     out'[n] = out[n]                                      ##
#     out[n] = Union in[s] (where s is an element from the set of all successors of the node n)    # Solve data-flow equations
#     in[n] = use[n] Union (out[n] - def[n])                                                       ##
#until in'[n] = in[n] and out'[n] = out[n] for all n               ## Test for convergence
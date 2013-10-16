#!/usr/bin/python

# Program that parses LISP-esque intermediate code for the 3rd COMP3109 assignment.
# Why reinvent the wheel?

from pyparsing import OneOrMore, nestedExpr

all_the_text = open('tests/simple.in').read()      # all text from a text file
data = OneOrMore(nestedExpr()).parseString(all_the_text)
data = data[0];                                    # Remove redundant first list layer
print 'Data is length: '
print len(data)
for i in range(0,len(data)):
    #print 'Function: ' + repr(i) + repr(data[i])
    #This is the function layer
    #data[i][0] is the function name
    #data[i][1] is the args
    #data[i][2-len] is the blocks
    print 'Function name is: ' +repr(data[i][0])
    print 'Arguments are: ' + repr(data[i][1])
    for j in range(2,len(data[i])):
        print 'Blocks number is: ' 
        print data[i][j][0]
        print 'Instructions list: '
        for k in range(1,len(data[i][j])):
            print data[i][j][k]

#print data

#!/usr/bin/python

# Program that parses LISP-esque intermediate code for the 3rd COMP3109 assignment.
# Why reinvent the wheel?

from pyparsing import OneOrMore, nestedExpr

all_the_text = open('thefile.txt').read()      # all text from a text file
data = OneOrMore(nestedExpr()).parseString(all_the_text)
print data

#!/bin/bash

# Script needed to run the third COMP3109 Assignment.

# $1 is the first argument.
# $2 is the second argument.

if (($# == 2))
then
if [ -e $1 ]
then
  python backEnd.py $1 > $2 	
else
  echo "ERROR: $1 does not exist."
fi
else
  echo "ERROR: Incorrect number of arguments."
fi

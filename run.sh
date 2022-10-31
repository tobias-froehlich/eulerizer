#!/bin/bash

if [ "$1" = "" ]
then
    echo "Give a config file name as argument!"
else
    if [ "$2" = "" ]
    then
        python3 pedals.py "$1" | python3 eulerizer.py "$1" | python3 gui.py "$1"
    else
        echo "You cannot give two arguments!"
    fi
fi


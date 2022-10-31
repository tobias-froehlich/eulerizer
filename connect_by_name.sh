#!/bin/bash

if [ "$1" = "" ]
then
    echo "Give the name of a midi output device."
else
    if [ "$2" = "" ]
    then
        echo "Give the name of a midi input device."
    else
        if [ "$3" = "" ]
        then
            inputclients=$(aconnect -i | grep "client.*$1")
            if [ $(echo "$inputclients" | wc -l) -gt 1 ]
            then
                echo "There is more than one input client with this name"
            else
                if [ "$inputclients" = "" ]
                then
                    echo "Input client not found."
                else
                    outputclients=$(aconnect -o | grep "client.*$2")
                    if [ $(echo "$outputclients" | wc -l) -gt 1 ]
                    then
                        echo "There is more than one output client with this name"
                    else
                        if [ "$outputclients" = "" ]
                        then
                            echo "Output client not found."
                        else
                            inputport=$(echo "$inputclients" | sed -rn 's/.*client ([0-9]+):.*/\1/p'):0
                            outputport=$(echo "$outputclients" | sed -rn 's/.*client ([0-9]+):.*/\1/p'):0
                            aconnect "$inputport" "$outputport"
                        fi
                    fi
                fi
            fi
        else
            echo "Too many arguments given."
        fi
    fi
fi

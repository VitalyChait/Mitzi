#!/bin/bash

pin1=12
pin2=12

sdelay=0.0001
ldelay=0.0001

Init () {
        gpio mode $pin1 out
        gpio mode $pin2 out

        gpio write $pin1 0
        gpio write $pin2 0
}

Finish () {
        gpio write $pin1 0
        gpio write $pin2 0
}

Step () {
        gpio write $pin1 1
        sleep $sdelay
        gpio write $pin1 0
}

Forward (){
        gpio write $pin2 1
}

Backward (){
        gpio write $pin2 0
}

FullFw (){
        length=$1
        Forward
        for (( i = 0; i < length; i++ ))
        do
                Step
        done
}

FullBw (){
        length=$1
        Backward
        for (( i = 0; i < length; i++))
        do
                Step
        done
}


Run (){
        steps=$1
        loops=$2
        Init
        for (( j = 0; j < loops; j++ ))
        do
                FullFw $steps
                FullBw $steps
        done
        Finish
}

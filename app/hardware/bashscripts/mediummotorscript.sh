#!/bin/bash

pin1=2
pin2=5
pin3=7
pin4=8

sdelay=0.0001
ldelay=0.0001

Init () {
        gpio mode $pin1 out
        gpio mode $pin2 out
        gpio mode $pin3 out
        gpio mode $pin4 out

        gpio write $pin1 0
        gpio write $pin2 0
        gpio write $pin3 0
        gpio write $pin4 0
}

Finish () {
        gpio write $pin1 0
        gpio write $pin2 0
        gpio write $pin3 0
        gpio write $pin4 0
}

Step1 () {
        gpio write $pin2 0
        gpio write $pin4 0
        sleep $sdelay
        gpio write $pin1 1
        gpio write $pin3 1
}

Step2 (){
        gpio write $pin1 0
        gpio write $pin4 0
        sleep $sdelay
        gpio write $pin2 1
        gpio write $pin3 1
}

Step3 (){
        gpio write $pin1 0
        gpio write $pin3 0
        sleep $sdelay
        gpio write $pin2 1
        gpio write $pin4 1
}

Step4 (){
        gpio write $pin2 0
        gpio write $pin3 0
        sleep $sdelay
        gpio write $pin4 1
        gpio write $pin1 1
}

Forward (){
        Step1
        sleep $ldelay
        Step2
        sleep $ldelay
        Step3
        sleep $ldelay
        Step4
        sleep $ldelay
}

Backward (){
        Step4
        sleep $ldelay
        Step3
        sleep $ldelay
        Step2
        sleep $ldelay
        Step1
        sleep $ldelay
}

FullFw (){
        length=$1
        for (( i = 0; i < length; i++ ))
        do
                Forward
        done
}

FullBw (){
        length=$1
        for (( i = 0; i < length; i++))
        do
                Backward
        done
}


Run (){
        steps=$1
        loops=$2
        Init
        for (( j = 0; j < loops; j++))
        do
                FullFw $steps
                FullBw $steps
        done
        Finish
}

case $1 in
    Init) "$@"; exit;;
    Finish) "$@"; exit;;
    FullFw) "$@"; exit;;
    FullBw) "$@"; exit;;
    Run) "$@"; exit;;
esac

#!/bin/bash

ypin1=16
ypin2=13

sdelay=0.0001
ldelay=0.0001

yInit () {
        gpio mode $ypin1 out
        gpio mode $ypin2 out

        gpio write $ypin1 0
        gpio write $ypin2 0
}

yFinish () {
        gpio write $ypin1 0
        gpio write $ypin2 0
}

yStep () {
        gpio write $ypin1 1
        sleep $sdelay
        gpio write $ypin1 0
}

yForward (){
        gpio write $ypin2 1
}

yBackward (){
        gpio write $ypin2 0
}

yFullFw (){
        length=$1
        yForward
        i=0
        while [ "$i" -le "$length" ]; do
                yStep
                i=$(( i + 1 ))
        done
}

yFullBw (){
        length=$1
        yBackward
        i=0
        while [ "$i" -le "$length" ]; do
                yStep
                i=$(( i + 1 ))
        done
}


yRun (){
        steps=$1
        loops=$2
        yInit
        j=0
        while [ "$j" -le "$loops" ]; do
                yFullFw $steps
                yFullBw $steps
                j=$(( j + 1 ))
        done
        yFinish
}

if [ $1 = "yRun" ]; then
    if [[ $# -ne 3 ]]; then
        echo "Illegal number of parameters to Run" >&2
        exit 2
    else
        yRun $2 $3
    fi
elif [ $1 = "yFullBw" ]; then
    if [[ $# -ne 2 ]]; then
        echo "Illegal number of parameters to FullBw" >&2
        exit 2
    else
        yFullBw $2
    fi
elif [ $1 = "yFullFw" ]; then
    if [[ $# -ne 2 ]]; then
        echo "Illegal number of parameters to FullFw" >&2
        exit 2
    else
        yFullFw $2
    fi
elif [ $1 = "yInit" ]; then
    yInit
elif [ $1 = "yFinish" ]; then
    yFinish
fi

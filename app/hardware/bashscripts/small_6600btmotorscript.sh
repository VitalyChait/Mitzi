#!/bin/bash

xpin1=10
xpin2=9

sdelay=0.0001
ldelay=0.0001

xInit () {
        gpio mode $xpin1 out
        gpio mode $xpin2 out

        gpio write $xpin1 0
        gpio write $xpin2 0
}

xFinish () {
        gpio write $xpin1 0
        gpio write $xpin2 0
}

xStep () {
        gpio write $xpin1 1
        sleep $sdelay
        gpio write $xpin1 0
}

xForward (){
        gpio write $xpin2 1
}

xBackward (){
        gpio write $xpin2 0
}

xFullFw (){
        length=$1
        xForward
        i=0
        while [ "$i" -le "$length" ]; do
                xStep
                i=$(( i + 1 ))
        done
}

xFullBw (){
        length=$1
        xBackward
        i=0
        while [ "$i" -le "$length" ]; do
                xStep
                i=$(( i + 1 ))
        done
}


xRun (){
        steps=$1
        loops=$2
        xInit
        j=0
        while [ "$j" -le "$loops" ]; do
                xFullFw $steps
                xFullBw $steps
                j=$(( j + 1 ))
        done
        xFinish
}

if [ $1 = "xRun" ]; then
    if [[ $# -ne 3 ]]; then
        echo "Illegal number of parameters to Run" >&2
        exit 2
    else
        xRun $2 $3
    fi
elif [ $1 = "xFullBw" ]; then
    if [[ $# -ne 2 ]]; then
        echo "Illegal number of parameters to FullBw" >&2
        exit 2
    else
        xFullBw $2
    fi
elif [ $1 = "xFullFw" ]; then
    if [[ $# -ne 2 ]]; then
        echo "Illegal number of parameters to FullFw" >&2
        exit 2
    else
        xFullFw $2
    fi
elif [ $1 = "xInit" ]; then
    xInit
elif [ $1 = "xFinish" ]; then
    xFinish
fi

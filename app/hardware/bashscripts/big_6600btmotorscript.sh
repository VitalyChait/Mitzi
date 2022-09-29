#!/bin/bash

zpin1=5
zpin2=2

sdelay=0.0001
ldelay=0.0001

zInit () {
        gpio mode $zpin1 out
        gpio mode $zpin2 out

        gpio write $zpin1 0
        gpio write $zpin2 0
}

zFinish () {
        gpio write $zpin1 0
        gpio write $zpin2 0
}

zStep () {
        gpio write $zpin1 1
        sleep $sdelay
        gpio write $zpin1 0
}

zForward (){
        gpio write $zpin2 1
}

zBackward (){
        gpio write $zpin2 0
}

zFullFw (){
        length=$1
        zForward
        i=0
        while [ "$i" -le "$length" ]; do
                zStep
                i=$(( i + 1 ))
        done
}

zFullBw (){
        length=$1
        zBackward
        i=0
        while [ "$i" -le "$length" ]; do
                zStep
                i=$(( i + 1 ))
        done
}


zRun (){
        steps=$1
        loops=$2
        zInit
	j=0
        while [ "$j" -le "$loops" ]; do
                zFullFw $steps
                zFullBw $steps
                j=$(( j + 1 ))
        done
	zFinish
}

if [ $1 = "zRun" ]; then
    if [[ $# -ne 3 ]]; then
        echo "Illegal number of parameters to Run" >&2
        exit 2
    else
        zRun $2 $3
    fi
elif [ $1 = "zFullBw" ]; then
    if [[ $# -ne 2 ]]; then
        echo "Illegal number of parameters to FullBw" >&2
        exit 2
    else
        zFullBw $2
    fi
elif [ $1 = "zFullFw" ]; then
    if [[ $# -ne 2 ]]; then
        echo "Illegal number of parameters to FullFw" >&2
        exit 2
    else
        zFullFw $2
    fi
elif [ $1 = "zInit" ]; then
    zInit
elif [ $1 = "zFinish" ]; then
    zFinish
fi

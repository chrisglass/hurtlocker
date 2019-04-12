#!/bin/bash

# A convenient script to just run the python code.
if [ $UID != 0 ] ; then
    echo "You need to run this script as root."
    exit 1
fi

python3 -m hurtlocker

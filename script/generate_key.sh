#!/bin/bash

OUTFILE=${1}

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SECRET_KEY=`python3 ${HERE}/generate_key.py` 

if [ "$#" -ne 1 ]
then
        echo ${SECRET_KEY}
    else
        echo "SECRET_KEY=\"${SECRET_KEY}\"" >> ${OUTFILE}
fi

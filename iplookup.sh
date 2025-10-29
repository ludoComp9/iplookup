#!/bin/sh
#
# Launch IPlookup from the virtual environment

SCRIPT_PATH=`dirname $0`

if [ ! -d "${SCRIPT_PATH}/venv" ]; then
    echo "Virtual environment not found from ${SCRIPT_PATH}"
    exit 1
else
    source ${SCRIPT_PATH}/venv/bin/activate
    python iplookup.py "$@"
    deactivate
fi
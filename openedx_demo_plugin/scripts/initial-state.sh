#!/usr/bin/env bash

####################################################################################
#
#   initial-state.sh
#
#   Create an initial state for the Open edX Demo site databases (MySQL and MongoDB)
#
####################################################################################

mkdir -p /openedx/data/modulestore/Demos/cond_test
python manage.py lms --settings=$SETTINGS import /openedx/data/ $(find / -type d -name "course_openedx_101" 2>/dev/null)

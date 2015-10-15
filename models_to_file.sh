#!/usr/bin/env bash
now=$(date +"%m_%d_%Y")
PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=fortytwo_test_task.settings django-admin.py show_models 2> "$now.dat"

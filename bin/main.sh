#!/bin/bash

python -m src.acquire.acquire
acquire_status=$?

python -m src.preprocess.preprocess
preprocess_status=$?

python -m src.load.load
load_status=$?

if [[$acquire_status -eq 0 && $preprocess_status -eq 0 && $load_status -eq 0]];
then exit 0
else exit 1
fi
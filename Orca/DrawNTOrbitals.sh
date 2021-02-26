#!/bin/bash

echo "5
7
4
60 60 60
10
2
1
10
11" > orca_plot_inputs.txt

for i in {1..29}; do
    orca_plot FeCH.$i.nto -i < orca_plot_inputs.txt
done

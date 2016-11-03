#!/bin/bash

kpoint=$1
nbands=$2

for i in `seq 1 $2`; do

cat << EOF > temp.pp
&INPUTPP
  outdir='calcdir',
  prefix='NaCl',
  plot_num=7,
  kpoint=$1,
  kband=$i,
/

&PLOT
  iflag=3,
  output_format=6,
  fileout='Band$i-k=$1.cub',
/
EOF

pp.x < temp.pp
echo rm temp.pp
done
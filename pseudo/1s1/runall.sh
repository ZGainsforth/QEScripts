#!/bin/bash

ld1.x < V.pbe-spn-kjpaw_psl.1.0.0.1s1xch.in | tee V.pbe-spn-kjpaw_psl.1.0.0.1s1xch.out
python PlotWfc.py
python PlotLd.py
ld1.x < V.pbe-spn-kjpaw_psl.1.0.0.1s1xch.test.in | tee V.pbe-spn-kjpaw_psl.1.0.0.1s1xch.test.out

cd ../ground
./upf2plotcore.sh V.pbe-spn-kjpaw_psl.1.0.0.UPF > V.pbe-spn-kjpaw_psl.1.0.0.wfc

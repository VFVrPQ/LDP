# LDP
Reproduce the mechanism mentioned in the 2017 paper.Implementation of Local Differential Private (LDP) mechanisms, just for fun.
The experiment is based on a 2017 paper named "Locally Differentially Private Protocols for Frequencey Estimation".

Two steps:

1. Verifying Correctness of Analysis: DE,SUE,OUE,SHE,BLH,OLH;
2. Towards Real-world Estimation: RAPPOR(wait),BLH,OLH.

## How to run

```bash
$ python3 main.py
``` 

## Verifying Correctness of Analysis

### numerical/analytical values of $Var[\tilde{c}(i)]$

Compare to Table 2 and Fig. 1($n=10000$) to verify the code.
1. Vary $\varepsilon$,$\varepsilon=0.5,1,1.5,...,5$:
    - DE: $d=2,4,16,128,2048$;
    - OUE;
2. Vary $\varepsilon$,$\varepsilon=0.5,1,1.5,...,5$, fixing $d=2^{10}$:
    - DE, SHE, SUE, OUE, BLH, OLH.

#### Reproduced figures 

<img src="https://github.com/VFVrPQ/LDP/blob/master/pic/Figure1a.png" width="600px" alt="Fig1a"/>
<img src="https://github.com/VFVrPQ/LDP/blob/master/pic/Figure1b.png" width="600px" alt="Fig1b"/>

### Comparing empirical and analytical variance

1. Vary $d$(fixing $\varepsilon=4$), $d=2^2,2^4,...,2^{14}$:(Runs too slowly when $d=2^{16}$)
    - DE, SUE, OUE;
    - SHE, BLH, OLH;
2. Vary $\varepsilon$(fixing $d=2^{10}$),$\varepsilon=0.5,1,1.5,...,5$:
    - DE, SUE, OUE;
    - SHE, BLH, OLH.

#### Reproduced figures 

<img src="https://github.com/VFVrPQ/LDP/blob/master/pic/Figure2a.png" width="600px" alt="2a"/>
<img src="https://github.com/VFVrPQ/LDP/blob/master/pic/Figure2b.png" width="600px" alt="2b"/>
<img src="https://github.com/VFVrPQ/LDP/blob/master/pic/Figure2c.png" width="600px" alt="2c"/>
<img src="https://github.com/VFVrPQ/LDP/blob/master/pic/Figure2d.png" width="600px" alt="2d"/>

## Towards Real-world Estimation

No idea yet.

### datasets

```./data/kosarak.dat.gz``` is from: http://fimi.uantwerpen.be/data/
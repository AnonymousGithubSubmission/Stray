



## STRAY: a Static Type Recommendation Approach for pYthon

This is a prototype package for a paper submission. 
The material mentioned in the paper (i.e., the extended Algorithm 1 and the proof of Theorem 2.1) are in the Appendix folder. 
### Installation
To run STRAY, those packages are required. 

* python3
* typing_extensions
* tqdm
* mypy_extensions
* eventlet
* tomli
* astunparse
* datasets
### Recommendation

#### Install Third-Party Dependency of the Recommending Project
Please ensure that all third-party dependencies have been installed in the same virtual environment as STARY. 

#### Recommendation
##### Modes
For those projects without **heavy** third-party dependency, e.g., *htmlark*, STARY can be employed directly to recommend types: 

python -m predict data/benchmark/htmlark.py predict

For those projects with **heavy** third-party dependency, e.g., *relex* and all other projects in the benchmark, running STARY directly would analyze and recommend types for all third-party packages and the recommending project.
Thus, STARY provide a pre-analysis to only **check** the third-party packages/recommending project and generate type stubs for them. 

python -m predict data/benchmark/relex.py check

Then, running STARY directly would only analyze and recommend types for the recommending project. 

python -m predict data/benchmark/relex.py predict
##### Running
The commend line format is:

python -m predict PROJECT MODE

If the recommending project is a single file (e.g., htmlark, relex, seagull, tinychain), please use the file address directly. 
python -m predict data/benchmark/htmlark.py check/predict
If the recommending project is a folder (e.g., pendulum), please use the folder address. 
python -m predict data/benchmark/pendulum check/predict
### Results
You can reproduce the results following previous instruction. 

The results reported in the paper have been collected in the evaluation folder. You can conveniently check it through evaluate.py. 
python -m evaluation.evaluate
## ExTyper: Towards Robust and Correct Type Prediction


### Installation
ExTyper is built upon [mypy](https://github.com/python/mypy), to run ExTyper, those packages are required. 

* python3
* typing_extensions
* tqdm
* mypy_extensions
* eventlet
* tomli
* astunparse
* datasets

After installing required packages, you should be able to play with ExTyper through this script.
```
python -m predict file
```
The predicted types will be written to result folder. 
### Prediction

Note that all four projects have third-party dependencies, you have to install corresponding dependencies for accurate predicton. We list all needed pakages here: 
* numpy
* torch
* allennlp
* ecdsa
* base58
* matplotlib

The prediction should works fine after the packages are installed, but the result may be slight different from experiment, due to the difference of third-party type stubs. To exactly reproduce the results, you can paste the type stubs in data/pyi to corresponding folder of packages. 

Now, run predict.py with corresponding file:

python -m predict data/benchmark/relex.py

python -m predict data/benchmark/seagull.py

python -m predict data/benchmark/tinychain.py

python -m predict data/benchmark/htmlark.py

### Results

The results reported in the paper have been collected in the evaluation folder. You can conveniently check it. 
# Students Repository for HSLU Module "DevOps"

This project is part of the **DevOps** course at the [Hochschule Luzern (HSLU)](https://www.hslu.ch/en/) as part of the [Master of Science in Applied Information and Data Science](https://www.hslu.ch/en/lucerne-school-of-business/degree-programmes/master/applied-information-and-data-science/)

The following commands are all ment to be executed in the root directory of the project.

## Mac/Linux
### Run your Script
For example, the hangman.py script
````
source ../.venv/bin/activate # if not already activated
export PYTHONPATH=$(pwd)
python server/py/hangman.py
````

### Run the Benchmark
````
source ../.venv/bin/activate # if not already activated
export PYTHONPATH=$(pwd)
python benchmark/benchmark_hangman.py python hangman.Hangman # or battleship.Battleship
````

### Start the Server
````
source ../.venv/bin/activate # if not already activated
uvicorn server.py.main:app --reload
````
Open up your browser and go to http://localhost:8000


## Windows
### Run your Script
For example, the hangman.py script
````
"../.venv\Scripts\activate" # if not already activated
set PYTHONPATH=%cd%
python server/py/hangman.py
````

### Run the Benchmark
````
"../.venv\Scripts\activate" # if not already activated
set PYTHONPATH=%cd%
python benchmark/benchmark_hangman.py python hangman.Hangman # or battleship.Battleship
````

### Start the Server
````
"../.venv\Scripts\activate" # if not already activated
uvicorn server.py.main:app --reload
start chrome http://localhost:8000
````

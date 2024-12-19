# Students Repository for HSLU Module "DevOps"

The following commands are all ment to be executed in the root directory of the project.

## Mac/Linux
<details>

### Run your Script
````
source ../.venv/bin/activate
export PYTHONPATH=$(pwd)
python server/py/hangman.py
python server/py/battleship.py
python server/py/uno.py
python server/py/dog.py
````

### Run the Benchmark
````
source ../.venv/bin/activate
export PYTHONPATH=$(pwd)
python benchmark/benchmark_hangman.py python hangman.Hangman
python benchmark/benchmark_battleship.py python battleship.Battleship
python benchmark/benchmark_uno.py python uno.Uno
python benchmark/benchmark_dog.py python dog.Dog
````

### Start the Server
````
source ../.venv/bin/activate
uvicorn server.py.main:app --reload
````
Open up your browser and go to http://localhost:8000

</details>

## Windows
<details>

### Run your Script
````
"../.venv\Scripts\activate"
set PYTHONPATH=%cd%                    # in Command Prompt
$env:PYTHONPATH = (Get-Location).Path  # in PowerShell
python server/py/hangman.py
python server/py/battleship.py
python server/py/uno.py
python server/py/dog.py
````

### Run the Benchmark
````
# Windows Powershell
$env:PYTHONPATH = (Get-Location).Path

"../.venv\Scripts\activate"
set PYTHONPATH=%cd%                    # in Command Prompt
$env:PYTHONPATH = (Get-Location).Path  # in PowerShell
python benchmark/benchmark_hangman.py python hangman.Hangman
python benchmark/benchmark_battleship.py python battleship.Battleship
python benchmark/benchmark_uno.py python uno.Uno
python benchmark/benchmark_dog.py python dog.Dog
````

### Start the Server
````
"../.venv\Scripts\activate"
uvicorn server.py.main:app --reload
start chrome http://localhost:8000
````
</details>

### Benchmark Results

With date of 19th December 2024, the resutls of the benchmark are as follows:

![Benchmark Results](benchmark_result.png)

We included this image of the benchmark results to show the performance of our scripts as we have noticed that depending on the system the tests **100** and **102** can fail. We noticed this in the shared image from [Revolitics Benchmark Statistics](https://wiki.revolytics.com/569036bb406d40bda8d377bdb608b481/)
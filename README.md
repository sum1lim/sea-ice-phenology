# sea-ice-phenology
Sea Ice Phenology Detection Developed by the ICE Remote Sensing Lab at University of Victoria (UVic)

**Author**: [Sangwon Lim](https://github.com/sum1lim)

## Getting Started

### Install the Package in a Python Virtual Environment

To avoid conflicts, the first step is to isolate this project by creating a Python virtual environment called ```venv```. The virtual environment will have it's own python interpreter, dependencies, and scripts. Commands should only be entered in a terminal that has ```venv``` active. 

#### Apple Silicon (M1)
```
sh M1_install.sh
source ~/miniforge3/bin/activate
```

#### Linux
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
```

#### Windows Powershell
```
pip install -r requirements.txt
pip install .
```
## Graphical User Interface (GUI)
#### Windows
```
# Must run the following at the parent directory (e.g. @ sea-ice-phenology)
python ./scripts/gui
```
#### Linux & OSX
```
gui
```
## Command-line User Interface (CLI)



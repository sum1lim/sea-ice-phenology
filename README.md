# sea-ice-phenology
Sea Ice Phenology Detection Developed by the ICE Remote Sensing Lab at University of Victoria (UVic)

**Author**: [Sangwon Lim](https://github.com/sum1lim)

## Getting Started
### Downloading the Repository
Download this repository using the green `Code` button at the top right 
OR
```
git clone https://github.com/sum1lim/sea-ice-phenology.git
```

### Install the Package in a Python Virtual Environment

Navigate to the parent directory, `sea-ice-phenology`, in the command line interface and run the following commands.

#### Windows Powershell
```
pip install -r requirements.txt
pip install .
```

#### Apple Silicon (M1)
```
sh M1_install.sh
source ~/miniforge3/bin/activate
```

#### Linux & OSX Terminal
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
```

## Graphical User Interface (GUI)
#### Windows
Double-click on `gui.bat`
#### Linux & OSX
```
gui
```
## Command-line User Interface (CLI)
#### Authenticating Google Earth Engine Credentials
```
authenticate
```
#### Get Time Series
```
get_timeseries --coords COORDS COORDS --start-date START_DATE --end-date END_DATE --output OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --coords COORDS COORDS
                        Area of Interest (AOI) defined by lon, lat coordiates
  --start-date START_DATE
                        YYYY-MM-DD
  --end-date END_DATE   YYYY-MM-DD
  --output OUTPUT       Output file path
```
#### Time-Series Interpolation
```
python .\scripts\interpolate --input INPUT [--type {linear,slinear,median,gaussian,random}]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Path to time-series data file (csv)
  --type {linear,slinear,median,gaussian,random}
                        Interpolation type
```
#### Phenology Detection
```
phenology --input INPUT [--type {slope-diff,three-day}]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Path to time-series data file (csv)
  --type {slope-diff,three-day}
                        Phenology detection method
```

# sea-ice-phenology
Sea Ice Phenology Detection Developed by the ICE Remote Sensing Lab at University of Victoria (UVic)

**Author**: [Sangwon Lim](https://github.com/sum1lim)

## Getting Started
### Downloading the Repository
Download this repository using the green `Code` button at the top right 
OR
```
$ git clone https://github.com/sum1lim/sea-ice-phenology.git
```

### Install the Package in a Python Virtual Environment

Navigate to the parent directory, `sea-ice-phenology`, in the command line interface and run the following commands.

#### Windows Powershell
```
$ pip install -r requirements.txt
$ pip install .
```

#### Apple Silicon (M1)
```
$ sh M1_install.sh
$ source ~/miniforge3/bin/activate
```

#### Linux & OSX Terminal
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install .
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
$ authenticate
```
#### Get Time Series
```
$ get_timeseries --help
usage: get_timeseries [-h] [--coords COORDS COORDS]
                      [--coords-csv COORDS_CSV COORDS_CSV COORDS_CSV COORDS_CSV]
                      --start-date START_DATE --end-date END_DATE
                      [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --coords COORDS COORDS
                        Area of Interest (AOI) defined by lon, lat
                        coordiates
  --coords-csv COORDS_CSV COORDS_CSV COORDS_CSV COORDS_CSV
                        Input file (CSV) followed by column names of
                        lon, lat and label
  --start-date START_DATE
                        YYYY-MM-DD
  --end-date END_DATE   YYYY-MM-DD
  --output OUTPUT       Output file/dir path
```
Command line to retrieve time series from a user-defined location:
```
$ get_timeseries --coords [Lon] [Lat] --start-date [YYYY-MM-DD] --end-date [YYYY-MM-DD] --output [Path to output CSV file]
```
Command line to retrieve time series from a CSV file with multiple (Lat, Lon) coordinates:
```
$ get_timeseries --coords-csv [Path to CSV file] [Longitude column] [Latitude column] [Label column] --start-date [YYYY-MM-DD] --end-date [YYYY-MM-DD] --output [Path to output directory]
```
Example(s):
```
# To retrieve time series from a user-defined location:
$ get_timeseries --coords -105.304 69.0435 --start-date 2017-01-01 --end-date 2022-01-01 --output ./example/Cambridge_Bay.csv

# To retrieve time series from a CSV file with multiple (Lat, Lon) coordinates:
$ get_timeseries --coords-csv ./CommunityList.csv Lon_ice Lat_ice Community --start-date 2017-01-01 --end-date 2022-01-01 --output ./example
```
Output: CSV file(s)
| system:time_start | B1                 |
|-------------------|--------------------|
| 2017-02-07        | 0.7299             |
| 2017-02-09        | 0.6476444444444445 |
| 2017-02-10        | 0.8302444444444445 |
| 2017-02-11        | 0.8168555555555556 |
| 2017-02-12        | 0.8367444444444444 |
| 2017-02-18        | 0.7521222222222222 |
| 2017-02-20        | 0.5673111111111111 |
| 2017-02-22        | 0.6707             |

#### Time-Series Interpolation
```
$ interpolate --help
usage: interpolate [-h] --input INPUT [INPUT ...]
                   [--type {linear,slinear,median,gaussian,random}]
                   --output OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT [INPUT ...]
                        Path to time-series data file (csv)
  --type {linear,slinear,median,gaussian,random}
                        Interpolation type
  --output OUTPUT       Output dir path
```
Command Line:
```
$ interpolate --input [Path to input file] --type [Interploation method] --output [Path to output directory]
```
Example(s):
```
# Single Input
$ interpolate --input ./example/Cambridge_Bay.csv --type median --output ./example

# Multiple inputs
$ interpolate --input ./example/Cambridge_Bay.csv ./example/Alert.csv --type median --output ./example

# Multiple inputs (Every file in a directory)
$ interpolate --input ./example/* --type median --output ./example
```
Output: CSV file(s) and graph visualization
| system:time_start | B1                 | B1_interpolate     |
|-------------------|--------------------|--------------------|
| 2017-02-07        | 0.7299             | 0.7299             |
| 2017-02-08        |                    | 0.6887722222222222 |
| 2017-02-09        | 0.6476444444444445 | 0.6476444444444445 |
| 2017-02-10        | 0.8302444444444445 | 0.8302444444444445 |
| 2017-02-11        | 0.8168555555555556 | 0.8168555555555556 |
| 2017-02-12        | 0.8367444444444444 | 0.8367444444444444 |
| 2017-02-13        |                    | 0.7944333333333333 |
| 2017-02-14        |                    | 0.8060799999999999 |
![alt text](https://github.com/sum1lim/sea-ice-phenology/raw/master/example/Cambridge_Bay_interpolate.png)

#### Phenology Detection
```
$ phenology --help
usage: phenology [-h] --input INPUT [INPUT ...] [--type {slope-diff}]
                 --output OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT [INPUT ...]
                        Path to time-series data file (csv)
  --type {slope-diff}   Phenology detection method
  --output OUTPUT       Output dir path
```
Command Line:
```
$ phenology --input [Path to input file] --type [Phenology detection method] --output [Path to output directory]
```
Example(s):
```
# Single Input
$ phenology --input ./example/Cambridge_Bay_interpolate.csv --type slope-diff --output ./example

# Multiple inputs
$ phenology --input ./example/Cambridge_Bay_interpolate.csv ./example/Alert_interpolate.csv --type slope-diff --output ./example

# Multiple inputs (Every file in a directory)
$ phenology --input ./example/* --type slope-diff --output ./example
```
Output: CSV file(s) and graph visualization
| system:time_start | B1                 | B1_interpolate     | B1_phenology |
|-------------------|--------------------|--------------------|--------------|
| 2017-02-07        | 0.7299             | 0.7299             |              |
| 2017-02-08        |                    | 0.6887722222222222 |              |
| 2017-02-09        | 0.6476444444444445 | 0.6476444444444445 |              |
| 2017-02-10        | 0.8302444444444445 | 0.8302444444444445 |              |
| 2017-02-11        | 0.8168555555555556 | 0.8168555555555556 |              |
| 2017-02-12        | 0.8367444444444444 | 0.8367444444444444 |              |
| 2017-02-13        |                    | 0.7944333333333333 |              |
| 2017-02-14        |                    | 0.8060799999999999 |              |
| ...               | ...                | ...                | ...          |
| 2017-05-08        |                    | 0.9531222222222222 | MO           |
| ...               | ...                | ...                | ...          |
| 2017-06-05        | 0.3274563252925873 | 0.3274563252925873 | PO           |
| ...               | ...                | ...                | ...          |
| 2017-06-22        | 0.4115777777777777 | 0.4115777777777777 | PD           |
| ...               | ...                | ...                | ...          |
| 2017-07-19        | 0.0041111111111111 | 0.0041111111111111 | OW           |
| ...               | ...                | ...                | ...          |
| 2017-10-16        | 0.2260666666666666 | 0.2260666666666666 | FO           |
![alt text](https://github.com/sum1lim/sea-ice-phenology/raw/master/example/Cambridge_Bay_phenology.png)

#### Phenological Trend
```
$ trend --help
usage: trend [-h] --input INPUT [INPUT ...] --output OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT [INPUT ...]
                        Path to time-series data file (csv)
  --output OUTPUT       Output dir path
```
Command Line:
```
$ trend --input [Path to input file] --output [Path to output directory]
```
Example(s):
```
# Single Input
$ trend --input ./example/Cambridge_Bay_interpolate.csv --output ./example

# Multiple inputs
$ trend --input ./example/Cambridge_Bay_interpolate.csv ./example/Alert_interpolate.csv --output ./example

# Multiple inputs (Every file in a directory)
$ trend --input ./example/* --output ./example
```
Output: CSV file(s) and graph visualization
| MO  | OW  | FO    | Year |
|-----|-----|-------|------|
|     |     | 289.0 | 2017 |
| 148 | 216 | 287.0 | 2018 |
| 144 |     | 290.0 | 2019 |
| 151 | 221 |       | 2020 |
| 151 | 219 |       | 2021 |
![alt text](https://github.com/sum1lim/sea-ice-phenology/raw/master/example/Cambridge_Bay_trend.png)

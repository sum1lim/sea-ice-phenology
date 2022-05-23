# sea-ice-phenology
Sea Ice Phenology Detection Developed by the ICE Remote Sensing Lab at University of Victoria (UVic).

**Author**: [Sangwon Lim](https://github.com/sum1lim)

Sea ice phenological indicators define starting and ending periods of seasonal ice formation and melt cycle:

- Melt Onset (MO): Starting date of the melt season
- Pond Onset (PO): Starting date of the pond formation
- Pond Drainage (PD): Starting date of the pond drainage
- Open Water (OW): Ending date of the melt season
- Freeze Onset (FO): Starting date of the ice formation

The package offers multiple processes to retrieve such information from [MODIS](https://lpdaac.usgs.gov/products/mod09gqv006/) and [Landsat](https://www.usgs.gov/landsat-missions/landsat-8-data-users-handbook) satellite optical data.
## Getting Started
### Downloading the Repository
Download this repository using the green `Code` button at the top right 
OR
```
$ git clone https://github.com/sum1lim/sea-ice-phenology.git
```

### Install the Package in a Python Virtual Environment
#### Prerequisite
[gcloud CLI](https://cloud.google.com/sdk/docs/install)

#### Windows
Double-click on `install` batch script

#### Apple Silicon (M1)
Navigate to the parent directory in terminal, `sea-ice-phenology`, in the command line interface and run the following commands.
```
$ sh M1_install.sh
$ source ~/miniforge3/bin/activate
```

#### Linux & OSX (Intel)
Navigate to the parent directory in terminal, `sea-ice-phenology`, in the command line interface and run the following commands.
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install .
```

## Graphical User Interface (GUI)
### Windows
Double-click on `gui` batch script
### Linux & OSX
```
gui
```
![alt text](https://github.com/sum1lim/sea-ice-phenology/raw/master/example/Screenshot.png)

## Command-line User Interface (CLI)
### Authenticating Google Earth Engine Credentials
Authentication is required prior to retrieving remote sensing data from Google Earth Engine Data Catalogue. Start the process by running the following command in a CLI:
```
$ authenticate
```
### Get Time Series
Retrieve optical reflectance time series data at a user-defined location from `MOD09GQ.006 Terra Surface Reflectance Daily Global 250m` and `USGS Landsat 8 Collection 2 Tier 1 TOA Reflectance` products. Wavelengths of 0.64-0.67µm and 0.64-0.67µm are selected, respectively. Reflectance mean of 9 points, center point surrounded by points in 8 directions (N, NE, E, SE, S, SW, W and NW) distanced at 125/$\tan$($\pi$/8) meters, are calculated for each date. Invalid pixels with cloud coverage, low solar angle and land contamination are not selected.
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

### Time-Series Interpolation
Data retrieved in the previous step may include voids in the time series, which can be problematic for further processes. Multiple interpolation methods are provided to fill in the gaps.
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

### Phenology Detection
Detects sea ice phenological indicators of MO, PO, PD, OW and FO. 1D-smoothing, Hampel and Lowess filtering on the time series data, is performed before the detection to enhance the performance.
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

### Phenological Trend
Calculates linear trends of annual phenological indicators detected.
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
| Year | MO  | OW  | FO    |
|------|-----|-----|-------|
| 2017 |     |     | 289.0 |
| 2018 | 148 | 216 | 287.0 |
| 2019 | 144 |     | 290.0 |
| 2020 | 151 | 221 |       |
| 2021 | 151 | 219 |       |

![alt text](https://github.com/sum1lim/sea-ice-phenology/raw/master/example/Cambridge_Bay_trend.png)

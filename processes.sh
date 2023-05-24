#!/bin/bash

authenticate

mkdir ./output/reflectance
get_timeseries --coords-csv ./CommunityList.csv Lon_ice Lat_ice Community --start-date 2000-01-01 --end-date 2022-12-31 --output ./output/reflectance

mkdir ./output/interpolate
interpolate --input ./output/reflectance/* --type median --output ./output/interpolate  --save-fig

mkdir ./output/phenology
phenology --input ./output/interpolate/* --type slope-diff --output ./output/phenology  --save-fig

mkdir ./output/trend
trend --input ./output/phenology/* --output ./output/trend  --save-fig

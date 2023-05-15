#!/bin/bash

#!/bin/bash
for i in {2000..2022}
do
   mkdir ./data/"$i"
   mkdir ./data/"$i"/input
   get_timeseries --coords-csv ./CommunityList.csv Lon Lat Community --start-date "$i"-01-01 --end-date "$i"-12-31 --output ./data/"$i"/input
   mkdir ./data/"$i"/interpolate
   interpolate --input ./data/"$i"/input/* --type median --output ./data/"$i"/interpolate --save-fig
   mkdir ./data/"$i"/phenology
   phenology --input ./data/"$i"/interpolate/* --type slope-diff --output ./data/"$i"/phenology --save-fig
   mkdir ./data/"$i"/trend
   trend --input ./data/"$i"/phenology/* --output ./data/"$i"/trend --save-fig
done
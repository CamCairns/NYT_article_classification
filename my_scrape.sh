#!/bin/bash
#
# file: SPOOKIE_reanme_file.sh
#
# description: loops through the SPOOKIE directory structure and renames a file
#
# usage: ./SPOOKIE_rename_file
#
# requirements:
#  None
#
# author: cam cairns
# 

set echo

apikey="599c5ebb1e180f4cd6eb426217a06518:6:72209945"
root_url="http://api.nytimes.com/svc/search/v2/articlesearch.json"
fq_sourceterm="The+New+York+Times" # limit to source of New York times
section_name=("Arts" "Sports")
save_location="/Users/camcairns/Dropbox/Datasets"

## now loop through the above array
for section in "${section_name[@]}"
do

for((i=0; i < 1; i++)) #take 2000 articles for each section
do

# mkdir -p $save_location/$section
url="${root_url}?fq=source%3D%28%22${fq_sourceterm}%22%29%2C+section_name%3A%22$section%22&offset=$i&api-key=$apikey"
echo $base_url

# curl -sS "$url" -o "$save_location/$section/$i.json"
curl "$url" | tidy -i

done
done
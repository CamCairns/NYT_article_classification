# API documentation: http://developer.nytimes.com/docs/read/article_search_api_v2
# requires the JQ parser http://stedolan.github.io/jq/
apikey="YOURKEY"
endpoint="http://api.nytimes.com/svc/search/v2/articlesearch.json"
# limit to source of New York times
fq_sourceterm="New+York"
base_url="${endpoint}?fq=source.contains%3A%28%22${fq_sourceterm}%22%29&api-key=$apikey&begin_date=BEGIN_DATE&end_date=END_DATE&page=PAGENUM"

day1=20150301
day2=20150317
# Note: you have to use the date function to iterate across months/years
# This is just simple incrementing
for day in $seq($day1 $day2); do
  end_date=$day
  begin_date=$day
  mkdir -p data-hold/$day
  
  url=$(echo "$base_url" | sed "s/PAGENUM/0/" | sed "s/BEGIN_DATE/$begin_date/" | sed "s/END_DATE/$end_date/")
  # first page
  curl -sS "$url" -o "data-hold/$day/0.json"
  hits=$(cat "data-hold/$day/0.json"| jq '.response .meta .hits')
  echo "$day has $hits hits ----------------------"
  # there are 10 hits per page
  first_page=1
  last_page=$((hits / 10))
  for pg in $(seq $first_page $last_page); do
    page_url=$(echo $url | sed "s/page=0/page=$pg/")
    echo "$page_url"
    curl -sS "$page_url" -o "data-hold/$day/$pg.json"
  done
done


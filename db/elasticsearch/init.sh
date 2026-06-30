#!/bin/bash
set -e

ES_URL="${ES_URL:-http://localhost:9200}"
INDEX="${ES_INDEX:-documents}"

echo "Waiting for Elasticsearch..."
until curl -s -u "elastic:${ELASTIC_PASSWORD}" "${ES_URL}/_cluster/health" > /dev/null 2>&1; do
  sleep 2
done

echo "Creating index '${INDEX}'..."
curl -s -u "elastic:${ELASTIC_PASSWORD}" -X PUT "${ES_URL}/${INDEX}" -H 'Content-Type: application/json' -d '{
  "mappings": {
    "properties": {
      "id": { "type": "keyword" },
      "text": { "type": "text" }
    }
  }
}'

echo "Done"

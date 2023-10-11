curl 'http://localhost:8080/api/v1/dataresources/edbf964c-f215-4fc6-9ef1-2ff1ea5a811e' -i -X PATCH \
    -H 'Content-Type: application/json-patch+json' \
    -H 'If-Match: "1543949803"' \
    -d '[ {
  "op" : "replace",
  "path" : "/publicationYear",
  "value" : "2017"
} ]'

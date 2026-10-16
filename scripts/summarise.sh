#!/bin/bash
# Purpose: summarise a saved monitor log.
# Usage:   bash scripts/summarise.sh <logfile>
if [ $# -ne 1 ] || [ ! -f "$1" ]; then
  echo "Usage: $0 <monitor-log-file>" >&2
  exit 1
fi
awk '
$2=="OK" || $2=="FAIL" {
  total++
  if (first == "") first = $1
  last = $1
  if ($2=="FAIL") fail++
  if ($2=="OK" && match($0, /"version": *"[^"]*"/)) {
    v = substr($0, RSTART, RLENGTH)
    sub(/.*: *"/, "", v); sub(/"$/, "", v)
    count[v]++
  }
}
END {
  printf "Total requests:  %d\n", total
  printf "Failed requests: %d\n", fail + 0
  printf "First timestamp: %s\n", first
  printf "Last timestamp:  %s\n", last
  print "Responses per version:"
  for (v in count) printf "  %s: %d\n", v, count[v]
}' "$1"
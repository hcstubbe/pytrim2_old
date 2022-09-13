#!/bin/bash

FILES="*.fastq.gz"
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  cat "$f" >> ./out/all.fastq.gz
done

gzip -d ./out/all.fastq.gz

exit
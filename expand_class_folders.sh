#!/bin/bash
# go to the path and take the files in the class folders out

path=$1

# iterate folders
for d in ${path}/*; do
  echo $d
  # iterate files
  for f in $d/*;do
    mv $f ${path}
  done

done

#!/bin/bash
# Moves CORSMAL audio files into class folders; the test data classes are not known.
# NOTE: it will overwrite the files in the target folder, if any.

function move_case(){
  i=$1
  case_path=$2

  echo "object $i"
  cd "${source_path}/$i/audio"

  # iterate classes
  for j in {0,1,2,3}; do
    echo " class $j"

    file_prefix="s[0-9]_fi${j}_fu[0-9]_b[0-9]_l[0-9]_audio\.wav"

    mkdir -p "${case_path}/fi${j}"

    for f in *.wav; do

      # echo $f
      if [[ "$f" =~ ^${file_prefix} ]]; then

        # compressing audio because the library wants mono audio
        ffmpeg -y -v 0 -i "${BASH_REMATCH[0]}" -ac 1 "${case_path}/fi${j}/o${i}_${BASH_REMATCH[0]}"

      fi

    done


  done

}

function move_unlabeled_data(){
  i=$1
  case_path=$2

  echo "object $i"
  cd "${source_path}/$i/audio"

  mkdir -p "${case_path}"

  for f in *.wav; do

    # compressing audio because the library wants mono audio
    ffmpeg -y -v 0 -i "$f" -ac 1 "${case_path}/o${i}_$f"

  done

}

echo "$PWD"
if [ "$#" -ne "2" ]; then
  echo "Usage: gather_dataset <source data path> <target data path>"
  exit 0
fi

initial_path="$PWD"
source_path="$PWD/$1"
target_path="$PWD/$2"

for i in {1,2,3,4,5,6,7,8,9}; do

  # train set
  echo "train"
  move_case "$i" "${target_path}/train"

done

for i in {10,11,12}; do

  # test set
  echo "test"
  move_unlabeled_data "$i" "${target_path}/test"

done

# back to the beginning
echo " back to ${initial_path}"
cd "${initial_path}"

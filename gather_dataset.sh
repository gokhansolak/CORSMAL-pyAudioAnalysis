#!/bin/bash
# Moves CORSMAL audio files into class folders; splits train and test folders.
# NOTE: it will overwrite the files in the target folder, if any.

move_case(){
  i=$1

  echo -e "\nobject $i"
  cd "${source_path}/$i/audio"

  # iterate classes
  for j in {0,1,2,3}; do
    echo -e "\n class $j"

    file_prefix="s[0-9]_fi${j}_fu[0-9]_b[0-9]_l[0-9]_audio\.wav"

    mkdir -p "${target_path}/fi${j}"
    mkdir -p "${target_path}/test/fi${j}"

    set_i=0

    for f in *.wav; do

      # echo $f
      if [[ "$f" =~ ^${file_prefix} ]]; then

        if [[ "$set_i" -eq 4 ]]; then
          # test set
          let "set_i=0"
          # compressing audio because the library wants mono audio
          ffmpeg -y -v 0 -i "${BASH_REMATCH[0]}" -ac 1 "${target_path}/test/fi${j}/o${i}_${BASH_REMATCH[0]}"
        else
          # training set
          ffmpeg -y -v 0 -i "${BASH_REMATCH[0]}" -ac 1 "${target_path}/fi${j}/o${i}_${BASH_REMATCH[0]}"
        fi
        let "set_i++"

        ## progress dots
        echo -n "."

      fi

    done

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

  move_case "$i"

done

# back to the beginning
echo " back to ${initial_path}"
cd "${initial_path}"

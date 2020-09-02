#!/bin/bash
# Moves CORSMAL audio files into class folders; splits train and test folders.
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

    set_i=0

    for f in *.wav; do

      # echo $f
      if [[ "$f" =~ ^${file_prefix} ]]; then

        # compressing audio because the library wants mono audio
        ffmpeg -y -v 0 -i "${BASH_REMATCH[0]}" -ac 1 "${case_path}/fi${j}/o${i}_${BASH_REMATCH[0]}"

        ## progress dots
        # echo -n "."

      fi

    done

    # echo "*"

  done

}

function create_fold(){

  fold_no=$1

  for i in {1,2,3,4,5,6,7,8,9}; do

    # modulus for object types (cup,glass,box)
    mod_i=$(($i % 3))

    if [[ "$mod_i" -eq ${fold_no} ]]; then
      # test set
      echo "test"
      move_case "$i" "${target_path}/test${fold_no}"
    else
      # train set
      echo "train"
      move_case "$i" "${target_path}/train${fold_no}"
    fi

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

# create 3-folds
for fold in {0,1,2}; do
  echo "=== fold $fold"
  create_fold ${fold}

done

# back to the beginning
echo " back to ${initial_path}"
cd "${initial_path}"

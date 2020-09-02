
dataset_path="$PWD/datasets/fillings-audio"


for i in {1,2,3,7,8,9}; do
  echo "object $i"
  cd $i/audio

  for j in {0,1,2,3}; do
    echo "filling $j"

    file_prefix="s[0-9]_fi${j}_fu[0-9]_b[0-9]_l[0-9]_audio\.wav"
    # file_prefix="s0_fi0_fu0_b0_l0_audio.wav"
    # file_prefix="s0.+"

    mkdir -p "${dataset_path}/fi${j}"
    mkdir -p "${dataset_path}/test/fi${j}"

    set_i=0

    for f in *.wav; do

      # echo $f
      if [[ "$f" =~ ^${file_prefix} ]]; then

        if [[ "$set_i" -eq 4 ]]; then
          # test set
          let "set_i=0"
          ffmpeg -y -i "${BASH_REMATCH[0]}" -ac 1 "${dataset_path}/test/fi${j}/o${i}_${BASH_REMATCH[0]}"
        else
          # training set
          ffmpeg -y -i "${BASH_REMATCH[0]}" -ac 1 "${dataset_path}/fi${j}/o${i}_${BASH_REMATCH[0]}"
        fi
        let "set_i++"

      fi

    done

  done

  cd ../..
done

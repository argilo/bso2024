#!/usr/bin/env bash

declare -a flags=(
    "flag{Clayton was seen setting up RFID checkpoints at 6:15 pm.}"
    "flag{Clayton mentioned testing new RFID locks in the lobby.}"
    "flag{Clayton checked into the hotel security system at 9:00 pm.}"
    "flag{Clayton ran into Jenn in the hallway at 9:30 pm.}"
    "flag{Clayton was seen at the main entrance around 10:15 pm.}"
    "flag{Clayton is known for tinkering with RFID for \"testing\" purposes.}"
    "flag{Clayton briefly argued with Gray about access protocols.}"
    "flag{Clayton had equipment issues, making him run back and forth from his room.}"
    "flag{Clayton has a timestamp on a log showing RFID system access.}"
    "flag{Witnesses confirm Clayton was mostly working on equipment tests.}"
)

num_flags=${#flags[@]}

for (( i=0; i<${num_flags}; i++ ))
do
    number=$(($i + 1))
    filename=flag$number
    echo $number "${flags[$i]}"
    qrencode \
        -l H \
        -s 15 \
        -o "${filename}"_tmp.png \
        "${flags[$i]}"
    convert \
        "${filename}"_tmp.png \
        -background white \
        -gravity center \
        -extent 2000x1200 \
        -pointsize 150 \
        -annotate +700-250 "${number}" \
        -pointsize 60 \
        -annotate +700+150 'This device is\npart of the\nBSides Ottawa\nCTF.' \
        "${filename}".png
    rm "${filename}"_tmp.png
done
rm -f final.png
montage \
    flag*.png \
    -geometry +0+0 \
    -tile 2x5 \
    final.png
rm flag*.png

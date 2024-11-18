#!/usr/bin/env bash

convert \
    bsides-ottawa-logo.jpg \
    -extent 1500x550 \
    -font 'Ubuntu-Sans-Medium' \
    -pointsize 36 \
    -gravity SouthWest \
    -draw "text 0,0 'flag{pain'" \
    -pointsize 18 \
    -gravity SouthEast \
    -draw "text 0,0 'VE3IRR'" \
    flag1.png

convert \
    bsides-ottawa-logo.jpg \
    -extent 1500x550 \
    -font 'Ubuntu-Sans-Medium' \
    -pointsize 36 \
    -gravity SouthWest \
    -draw "text 0,0 't_all_th'" \
    -pointsize 18 \
    -gravity SouthEast \
    -draw "text 0,0 'VE3IRR'" \
    flag2.png

convert \
    bsides-ottawa-logo.jpg \
    -extent 1500x550 \
    -font 'Ubuntu-Sans-Medium' \
    -pointsize 36 \
    -gravity SouthWest \
    -draw "text 0,0 'e_things}'" \
    -pointsize 18 \
    -gravity SouthEast \
    -draw "text 0,0 'VE3IRR'" \
    flag3.png

grcc paint_tx.grc

./paint_tx.py --infile flag1.png --outfile paint1
./paint_tx.py --infile flag2.png --outfile paint2
./paint_tx.py --infile flag3.png --outfile paint3
#!/usr/bin/env bash

convert \
    bsides-ottawa-logo.jpg \
    -extent 1500x550 \
    -font 'Ubuntu-Sans-Medium' \
    -pointsize 36 \
    -gravity SouthWest \
    -draw "text 0,0 'flag{foo_BAR_baz}'" \
    -gravity SouthEast \
    -draw "text 0,0 'VE3IRR'" \
    flag.png
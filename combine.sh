#!/usr/bin/env bash

cat \
    paint/paint1.sigmf-data \
    hop/hop.sigmf-data \
    fm/broadcast.sigmf-data \
    paint/paint2.sigmf-data \
    hop/hop.sigmf-data \
    fm/broadcast.sigmf-data \
    paint/paint3.sigmf-data \
    hop/hop.sigmf-data \
    fm/broadcast.sigmf-data \
    > ctf.cs16

scp ctf.cs16 root@ni-e31x-30C91A0.local:/data/ctf.cs16
#!/bin/bash
set -e
cd "$(dirname "$0")"
mkdir -p short; rm -f short/*
SEGS="0.0:9.6 64.0:114.3"
i=0
for s in $SEGS; do
  a=${s%%:*}; b=${s##*:}
  python3 render.py range v $a $b short/v$i.mp4 2>/dev/null
  d=$(python3 -c "print($b-$a)")
  ffmpeg -y -loglevel error -ss $a -t $d -i work/mix_full.wav -af "afade=t=in:d=0.05,afade=t=out:st=$(python3 -c "print($d-0.12)"):d=0.12" -ar 44100 -ac 1 short/a$i.wav
  ffmpeg -y -loglevel error -i short/v$i.mp4 -i short/a$i.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest short/s$i.mp4
  i=$((i+1))
done
python3 endcard.py short/card.mp4 2>/dev/null
ffmpeg -y -loglevel error -i short/card.mp4 -f lavfi -t 2.4 -i anullsrc=r=44100:cl=mono -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest short/s9.mp4
printf "file 's0.mp4'\nfile 's1.mp4'\nfile 's9.mp4'\n" > short/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i short/list.txt -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart /home/user/Ecos-del-oasado/videos/ep03/EP03_short_raw.mp4
echo SHORT_DONE

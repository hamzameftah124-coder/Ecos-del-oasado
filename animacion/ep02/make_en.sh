#!/bin/bash
set -e
cd "$(dirname "$0")"
rm -rf chunks; mkdir -p chunks
python3 - > jobs.txt <<'PY'
import json
tl=json.load(open("work/timeline.json")); end=tl["total"]+1.5; n=16
for k in range(n): print(f"h {end*k/n:.4f} {end*(k+1)/n:.4f} chunks/h_{k:02d}.mp4")
PY
cat jobs.txt | xargs -P 4 -L 1 sh -c 'python3 render.py range $0 $1 $2 $3 2>/dev/null && echo "done $3"'
OUT=/home/user/Ecos-del-oasado/videos/ep02; mkdir -p $OUT
ls chunks/h_*.mp4 | sort | sed "s/^/file '/;s/$/'/" > list_h.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list_h.txt -i work/mix_full.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 -c:a aac -b:a 192k -movflags +faststart $OUT/EP02_Frozen_Supermarket_30_Days_at_-60C.mp4
echo ALL_DONE

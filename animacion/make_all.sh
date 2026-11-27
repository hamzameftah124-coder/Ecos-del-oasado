#!/bin/bash
set -e
cd "$(dirname "$0")"
mkdir -p chunks
python3 - > jobs.txt <<'PY'
import json
tl=json.load(open("work/timeline.json")); o=tl["offs"]; d=tl["durs"]
ends=[o[0]+d[0], o[1]+d[1], o[2]+d[2]+1.5]
a,b=0,ends[2]; n=16
for k in range(n):
    print(f"h {a+(b-a)*k/n:.4f} {a+(b-a)*(k+1)/n:.4f} chunks/h_{k:02d}.mp4")
PY
cat jobs.txt | xargs -P 4 -L 1 sh -c 'python3 render.py range $0 $1 $2 $3 2>/dev/null && echo "done $3"'
OUT=/home/user/Ecos-del-oasado/videos; mkdir -p $OUT
ls chunks/h_*.mp4 | sort | sed "s/^/file '/;s/$/'/" > list_h.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i list_h.txt -i work/mix_full.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -movflags +faststart $OUT/Cucaracha_completo_YouTube_16x9.mp4
echo ALL_DONE

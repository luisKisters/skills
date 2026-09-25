# Usage: words.py <clip> [...] -> ASR word timings for raw/<clip>.json. Timings can be ~0.1-0.3 s off; confirm with energy.py.
import json,sys
for f in sys.argv[1:]:
    d=json.load(open(f'raw/{f}.json'))
    print(f,' '.join(f"{w['text']}@{w['start']:.2f}-{w['end']:.2f}" for w in d['segments']),'\n')

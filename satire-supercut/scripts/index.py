# Build words.json from subs/*.json3: one (video, start_ms, end_ms, word) row per spoken word.
import json,glob,os,re,sys
words=[]
for f in glob.glob('subs/*.json3'):
    vid=os.path.basename(f).split('.')[0]
    d=json.load(open(f))
    evs=[e for e in d['events'] if 'segs' in e]
    for i,e in enumerate(evs):
        t0=e['tStartMs']; dur=e.get('dDurationMs',0)
        segs=[s for s in e['segs'] if s['utf8'].strip()]
        for j,s in enumerate(segs):
            st=t0+s.get('tOffsetMs',0)
            en=t0+segs[j+1].get('tOffsetMs',0) if j+1<len(segs) else t0+dur
            w=re.sub(r"[^a-z0-9']","",s['utf8'].lower())
            if w: words.append((vid,st,en,w))
json.dump(words,open('words.json','w'))
print(len(words))

# Usage: context.py "paid shill" -> every hit with the words around it, to judge meaning and speaker.
import json,sys
W=json.load(open('words.json'))
for q in sys.argv[1:]:
    p=q.split(); n=len(p)
    for i in range(len(W)-n):
        if all(W[i+k][3]==p[k] for k in range(n)):
            v=W[i][0]; a=max(0,i-6); b=i+n+8
            print(f"[{q}] {v}@{W[i][1]/1000:.1f}: "+' '.join(w[3] for w in W[a:b] if w[0]==v))

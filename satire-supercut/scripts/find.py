# Usage: find.py "paid shill" "obsidian" -> hit count and video@start-end for each exact phrase.
import json,sys
W=json.load(open('words.json'))
for q in sys.argv[1:]:
    p=q.lower().split(); n=len(p); hits=[]
    for i in range(len(W)-n+1):
        if all(W[i+k][3]==p[k] and W[i+k][0]==W[i][0] for k in range(n)):
            hits.append(f"{W[i][0]}@{W[i][1]/1000:.2f}-{W[i+n-1][2]/1000:.2f}")
    print(q,'|',len(hits),'|',' '.join(hits[:6]))

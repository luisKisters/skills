# Usage: uvx --with numpy python silences.py -> every silence >= 0.5 s in raw/*.mp4. Use them as natural pauses.
import subprocess,numpy as np,glob
for p in sorted(glob.glob('raw/*.mp4')):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)
    r=np.array([20*np.log10(np.sqrt(np.mean(a[i:i+640]**2))+1)-90 for i in range(0,len(a)-640,640)])
    q=r<-45; out=[];i=0
    while i<len(q):
        if q[i]:
            j=i
            while j<len(q) and q[j]: j+=1
            if (j-i)*0.04>=0.5: out.append(f"{i*0.04:.2f}-{j*0.04:.2f}")
            i=j
        else: i+=1
    if out: print(p[4:-4],' '.join(out))

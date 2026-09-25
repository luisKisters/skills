# Usage: uvx --with numpy python energy.py <clip>,<start>,<end> -> RMS dB every 40 ms. Cut in the valleys.
import subprocess,numpy as np,sys
for arg in sys.argv[1:]:
    f,s,e=arg.split(',')
    raw=subprocess.run(['ffmpeg','-v','error','-ss',s,'-to',e,'-i',f'raw/{f}.mp4','-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)
    r=[int(20*np.log10(np.sqrt(np.mean(a[i:i+640]**2))+1)-90) for i in range(0,len(a)-640,640)]
    print(f,s,' '.join(f"{float(s)+i*0.04:.2f}:{v}" for i,v in enumerate(r)))

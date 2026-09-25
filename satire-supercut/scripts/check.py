# Usage: check.py "clip,s,e;clip,s,e" [...] -> splice the parts and transcribe them.
# The transcript must read exactly like the caption. Leaked or dropped words mean the cut points are wrong.
import subprocess,sys
for arg in sys.argv[1:]:
    parts=[p.split(',') for p in arg.split(';')]
    ins=[];fc=''
    for i,(f,s,e) in enumerate(parts):
        ins+=['-ss',s,'-to',e,'-i',f'raw/{f}.mp4']; fc+=f'[{i}:a]aresample=16000,aformat=channel_layouts=mono[a{i}];'
    fc+=''.join(f'[a{i}]' for i in range(len(parts)))+f'concat=n={len(parts)}:v=0:a=1,adelay=800,apad=pad_dur=0.8[o]'
    subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',fc,'-map','[o]','-ar','16000','check.wav'],check=True)
    print(arg,'->',subprocess.run(['spokenly','transcribe','file','check.wav'],capture_output=True,text=True).stdout.strip())

from time import time
import os
import sys

class tiny_tqdm:
    def __init__(s, iter=None, desc="", mininterval=0.001, unit='it'):
        s.iter=iter; s.mininterval=mininterval; s.min_iter=1; s.prev_time=time(); s.total=len(iter); s.n=0; s.elapsed=1e-6; s.desc=desc; s.unit=unit
    def __iter__(s):
        for obj in s.iter: s.n+=1; s.update() if ((not s.n%s.min_iter) and (time() - s.prev_time) >= s.mininterval) or s.n==1 or s.n==s.total else ""; yield obj
    def update(s):
        BARS, term_w = u" " + u''.join(map(chr, range(0x258F, 0x2587, -1))),os.get_terminal_size()[0]
        s.elapsed += time() - s.prev_time
        avg_it_s = s.n/s.elapsed
        it_s = avg_it_s if (s.n==1 or s.n==s.total) else s.min_iter/ (time() - s.prev_time)
        def _fmt(t):return f"{int(t//3600):02d}:"*int(t>=3600) + ":".join([f"{int(n):02d}" for n in divmod(t%3600,60)])
        prefix, suffix = f"{s.desc}{100*s.n//s.total:3}%|", f"| {s.n}/{s.total} [{_fmt(s.elapsed)}<{'?' if s.n==1 else _fmt((s.total-s.n)//it_s)}, {'?' if s.n==1 else '{:5.2f}'.format(it_s)}{s.unit}/s]"
        bar_len, frac_idx = divmod(int((s.n/s.total) * (term_w -1 - len(prefix+suffix)) * (len(BARS)-1)), (len(BARS)-1))
        sys.stdout.write(f"\n\x1b[A" + prefix + (bar_len * BARS[-1]) + BARS[frac_idx]*(s.n!=s.total) + ' '*(term_w-2 -bar_len-len(prefix+suffix)) + suffix + f"\x1b[{term_w}G"*(s.n!=s.total) + "\n"*(s.n==s.total))
        s.min_iter = 1 if s.n==1 or int(avg_it_s * s.mininterval)==0 else int(avg_it_s * s.mininterval)      
        s.prev_time = time()
    def set_description(s, desc=None):s.desc = desc+": "
    @classmethod
    def write(s,msg,end="\n"):sys.stdout.write("\n\x1b[A" + ' '*os.get_terminal_size()[0] + "\n\x1b[A" + msg+end)     
def trange(*args, **kwargs):
    return tiny_tqdm(range(*args), **kwargs)

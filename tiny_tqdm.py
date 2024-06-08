from time import time
import os
import sys

class tiny_tqdm:
    def __init__(self, iterable=None, desc="",  mininterval=0.001, ascii=None, unit='it',  **kwargs):
        self.iterable=iterable; self.mininterval=mininterval; self.min_iter=1; self.previous_time=time(); self.total=len(iterable); self.n=0; self.elapsed=0; self.desc=desc; self.unit=unit; self.ascii=ascii
    def __iter__(self):
        for obj in self.iterable:
            yield obj
            self.n+=1
            if((not self.n%self.min_iter) and (time() - self.previous_time) >= self.mininterval) or self.n==1 or self.n==self.total :
                    self.update()      
    def update(self):
        BARS = (u" " + u''.join(map(chr, range(0x258F, 0x2587, -1)))) if not self.ascii else " 123456789#"
        prefix = f"{self.desc}"+": "*int(bool(len(self.desc)))+ " "*(3-len(str(int(100*self.n/self.total)))) + str(int(100*self.n/self.total))+"%|"
        self.elapsed += time() - self.previous_time
        avg_it_s = 0 if self.n==1 else self.n/self.elapsed
        it_s = 0 if (self.n==1 or self.n==self.total) else self.min_iter/ (time() - self.previous_time)
        eta = "?" if self.n==1 else (self.total-self.n) // avg_it_s
        def _fmt(t):return f'0{int(t)}' if t<10 else int(t)
        suffix = f"| {self.n}/{self.total} [{_fmt(self.elapsed//60)}:{_fmt(int(self.elapsed)%60)}<{str(_fmt(eta//60))+':'+str(_fmt(eta%60)) if eta!='?' else eta}, {'?' if self.n==1 else '{:5.2f}'.format(avg_it_s if self.n==self.total else it_s)}{self.unit}/s]"
        bar_length, frac_bar_index = divmod(int((self.n/self.total) * (os.get_terminal_size()[0] -1 - len(prefix+suffix)) * (len(BARS)-1)), (len(BARS)-1))
        sys.stdout.write("\n\x1b[A" + prefix + str(bar_length * BARS[-1]) + str(BARS[frac_bar_index])*(self.n!=self.total) + ' '*(os.get_terminal_size()[0] -2  -bar_length-len(prefix+suffix)) + suffix + f"\x1b[{os.get_terminal_size()[0]}G"*int(self.n!=self.total) + "\n"*(self.n==self.total))
        self.min_iter = 1 if self.n==1 or int(avg_it_s * self.mininterval)==0 else int(avg_it_s * self.mininterval)      
        self.previous_time = time()
    def set_description(self, desc=None):
        self.desc = desc
    @classmethod
    def write(self,s,end="\n"):
         sys.stdout.write("\n\x1b[A" + ' '*os.get_terminal_size()[0] + "\n\x1b[A" + s+end)     

def trange(*args, **kwargs):
    return tiny_tqdm(range(*args), **kwargs)

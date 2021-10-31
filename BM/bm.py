class BM():
    def __init__(self,decstr):
        self.decstr = self.dec2bit(decstr)
        self.polomin = [0]
        self.lsttime = [0]
        self.do_BM()

    def output(self):
        out = [0]*(self.polomin[0]+1)
        for i in self.polomin:
            out[self.polomin[0]-i] = 1
        out = [str(i) for i in out]
        return self.polomin[0],''.join(out)

    def dec2bit(self,dec):
        return [int(i) for i in dec]

    def _same(self):
        for i in range(len(self.lsttime)-1):
            if self.lsttime[i]!=self.lsttime[i+1]:
                return False
        return True
    
    def condense(self):
        f = list(set(self.polomin))
        for i in self.polomin:
            if self.polomin.count(i) % 2 ==0:
                if i in f:
                    f.remove(i)
        f = sorted(f, reverse=True)        
        return f

    def do_BM(self):
        for i in range(len(self.decstr)):
            d = 0
            for j in self.polomin:
                d += self.decstr[i+j-max(self.lsttime)]
            d = d%2
            if d == 0:
                self.lsttime.append(self.lsttime[i])
            else:
                if self._same():
                    n = i
                    fn = self.polomin.copy()
                    self.polomin.append(i+1)
                    self.lsttime.append(i+1)
                else:
                    if max(self.polomin) > max(fn):
                        m = n
                        fm = fn.copy()
                    n = i
                    fn = self.polomin.copy()
                    if m - self.lsttime[m] >= n - self.lsttime[n]:
                        self.polomin += [j+(m-self.lsttime[m]-n+self.lsttime[n]) for j in fm]
                    else:
                        self.polomin = [j-(m-self.lsttime[m]-n+self.lsttime[n]) for j in self.polomin] + fm
                    self.lsttime.append(max(self.polomin))
        self.polomin = self.condense()  

if __name__ == "__main__":
    seq = ['10010000111101000011100000011', '1110110101000110111100011', '10101111010001001010111100010']
    for S in seq: 
        print(BM(S).output())
import csv

standard_seq = {
    'A':'ALA',
    'C':'CYS',
    'D':'ASP',
    'E':'GLU',
    'F':'PHE',
    'G':'GLY',
    'H':'HIS',
    'I':'ILE',
    'K':'LYS',
    'L':'LEU',
    'M':'MET',
    'N':'ASN',
    'P':'PRO',
    'Q':'GLN',
    'R':'ARG',
    'S':'SER',
    'T':'THR',
    'V':'VAL',
    'W':'TRP',
    'Y':'TYR'
}
def count_seq(fname):
    aa=[]
    aa_c=[]
    aa_c2=[]
    for k in standard_seq:
        aa.append(standard_seq[k])
        aa_c.append(0)
        aa_c2.append(0)
    f=open(fname,'r').read().split("\n")[:-1]
    for dat in f:
        if '#' in dat:
            n=len(dat.split("|")[1].split(","))
            print (dat)
        else:
            d = dat.split(",")
            aa_c[aa.index(d[1])]+=int(d[2])
            aa_c2[aa.index(d[1])] += (n*int(d[2]))
    fo=open('af_count.csv','w')
    for i in range(len(aa)):
        fo.write('{},{},{}\n'.format(aa[i],aa_c[i],aa_c2[i]))
    fo.close()

if __name__ == "__main__":
    count_seq('af_seq.txt')
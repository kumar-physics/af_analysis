import os
import gzip
import sys
import csv
import plotly.express as px

# ref seq release no 210, taken on Jan 16, 2022
aa={
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

def count_residues(foname):
    cc=0
    c=0
    files = [x for x in os.listdir(".") if x.endswith(".gz")]
    aa_count = {}
    for a in aa:
        aa_count[aa[a]] = 0
    for fname in files:
        print (fname)
        with gzip.open(fname, 'rt') as f:
            dat = str(f.read()).split(">")
            seq = []
            for j in dat:
                d = "".join(j.split("\n")[1:-1])
                cc+=1
                seq.append(d)
            s = "".join(seq)
            for a in aa:
                n = s.count(a)
                aa_count[aa[a]] += n
                c += n
    fo = open(f'{foname}.csv', 'w')
    for a in aa:
        fo.write(f'{aa[a]},{aa_count[aa[a]]},{aa_count[aa[a]]}\n')
    fo.close()
    print (f'{foname} seq = {cc}, total residue = {c}')

def read_csv(fname,flg):
    aa=[]
    aa_c=[]
    aa_c2=[]
    dat=[]
    with open(fname) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            aa.append(row[0])
            aa_c.append(int(row[1]))
            dat.append(flg)
    aa_c2=[i/sum(aa_c) for i in aa_c]
    return aa,aa_c,aa_c2,dat

def plot_csv():
    files = [x for x in os.listdir(".") if x.endswith(".csv")]
    names = [x.split(".")[0] for x in files]
    dat = [read_csv(f'{x}.csv',x) for x in names]
    count=[]
    normalized=[]
    residue=[]
    data_set=[]
    r=[]
    c=[0 for i in range(20)]
    for i in dat:
        residue+=i[0]
        count+=i[1]
        normalized+=i[2]
        data_set+=i[3]
        print (i[3])
        if i[3][0]!= 'complete':
            c=[c[j]+i[1][j] for j in range(20)]
        else:
            r=i[0]
            ds=['all' for _ in range(20)]
    cn=[i/sum(c) for i in c]
    residue+=r
    count+=c
    normalized+=cn
    data_set+=ds



    fig = px.bar(x=residue, y=count, color=data_set, barmode='group', labels={'x': 'Amino acid', 'y': 'Count'})
    fig.show()
    fig.write_html('refseq_count.html')
    fig.write_image('refseq_count.pdf', width=1200, height=800)
    fig2 = px.bar(x=residue, y=normalized, color=data_set, barmode='group', labels={'x': 'Amino acid', 'y': 'Density'})
    fig2.show()
    fig2.write_html('refseq_density.html')
    fig2.write_image('refseq_density.pdf', width=1200, height=800)


def plot_stat(fname):
    genome=[]
    seq_count=[]
    aa_count=[]
    annotation=[]
    group=[]
    with open(fname) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            print (row)
            genome.append(row[0])
            seq_count.append(int(row[1]))
            aa_count.append(int(row[2]))
            annotation.append(row[3])
            group.append(row[4])
    fig=px.bar(x=group,y=seq_count,color=genome)
    fig.write_html('refseq_stat.html')
    fig.show()


if __name__ == "__main__":
    # foname = sys.argv[1]
    # count_residues(foname)
    plot_csv()
    #plot_stat('stat.csv')
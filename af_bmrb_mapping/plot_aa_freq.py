import plotly.express as px
import csv
import re
import gzip

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
            aa_c2.append(int(row[2]))
            dat.append(flg)
    return aa,aa_c,aa_c2,dat


def read_fasta(n):
    aa_count={}
    for a in aa:
        aa_count[aa[a]]=0
    for i in range(1,n):
        fname = f'/Users/kumaranbaskaran/Downloads/complete/complete.nonredundant_protein.{i}.protein.faa.gz'
        with gzip.open(fname,'rt') as f:
            dat = str(f.read()).split(">")
            seq=[]
            for j in dat:
                d="".join(j.split("\n")[1:-1])
                seq.append(d)
            s="".join(seq)
            c=0
            for a in aa:
                n=s.count(a)
                aa_count[aa[a]]+=n
                c+=n

    fo=open('refseq_count.csv','w')
    for a in aa:
        fo.write(f'{aa[a]},{aa_count[aa[a]]},{aa_count[aa[a]]}\n')
    fo.close()



def plot_data():
    pdb,pdb_c1,pdb_c2,pdb_dat = read_csv('pdb_count.csv','PDB')
    af,af_c1,af_c2,af_dat = read_csv('af_count.csv','AF')
    refseq,refseq_c1,refseq_c2,refseq_dat = read_csv('refseq_count.csv','REFSEQ')
    pdb_c1n=[i/sum(pdb_c1) for i in pdb_c1]
    af_c1n=[i/sum(af_c1) for i in af_c1]
    refseq_c1n=[i/sum(refseq_c1) for i in refseq_c1]
    y1=pdb_c1n+af_c1n+refseq_c1n
    x=pdb+af+refseq
    y=pdb_c1+af_c1+refseq_c1
    c = pdb_dat+af_dat+refseq_dat
    fig = px.bar(x=x,y=y,color=c,barmode='group',labels={'x':'Amino acid','y':'Count'})
    fig.show()
    fig.write_html('aa_count.html')
    fig.write_image('aa_count.pdf', width=1200, height=800)
    fig2 = px.bar(x=x, y=y1, color=c, barmode='group',labels={'x':'Amino acid','y':'Density'})
    fig2.show()
    fig2.write_html('aa_density.html')
    fig2.write_image('aa_density.pdf', width=1200, height=800)
    y2=[pdb_c1n[i]/refseq_c1n[i] for i in range(len(pdb_c1n))]+[af_c1n[i]/refseq_c1n[i] for i in range(len(af_c1n))]
    x2=pdb+af
    c2=pdb_dat+af_dat
    fig3 = px.bar(x=x2, y=y2, color=c2, barmode='group', labels={'x': 'Amino acid', 'y': 'Density'})
    fig3.show()
    fig3.write_html('aa_density_norm.html')
    fig3.write_image('aa_density_norm.pdf', width=1200, height=800)


def create_download_links(n):
    fo=open('viral.sh','w')
    for i in range(1,n):
        url=f'wget https://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.{i}.protein.faa.gz'
        fo.write('{}\n'.format(url))
    fo.close()

if __name__ == "__main__":
    # plot_data()
    #read_fasta('refseq.fasta')
    create_download_links(8)
    # read_fasta(100)
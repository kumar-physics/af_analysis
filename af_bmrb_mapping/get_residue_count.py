from mmcif.io.PdbxReader import PdbxReader
import sys
import gzip
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
def get_chain_info(cif_file,in_path,out_path):

    cif_data = []
    if '.gz' in cif_file:
        ifh = gzip.open('{}/{}'.format(in_path,cif_file), 'rt')
    else:
        ifh = open('{}/{}'.format(in_path,cif_file), 'r')
    pRd = PdbxReader(ifh)
    pRd.read(cif_data)
    ifh.close()
    c0 = cif_data[0]
    ref_db = c0.getObj('entity_poly')
    entry_id = c0.getObj('entry').getValue('id')
    col_names = ref_db.getAttributeList()
    seq_idx=col_names.index('pdbx_seq_one_letter_code_can')
    chain_idx = col_names.index('pdbx_strand_id')
    type_idx = col_names.index('type')
    dat=ref_db.data
    fo=open('{}/{}.txt'.format(out_path,entry_id),'w')
    for d in dat:
        if d[type_idx] == 'polypeptide(L)':
            #print (d[chain_idx],d[type_idx],d[seq_idx])
            seq=''.join(d[seq_idx].split("\n"))
            fo.write('#{}|{}|{}\n'.format(entry_id,d[chain_idx],seq))
            for a in standard_seq:
                fo.write('{},{},{}\n'.format(a,standard_seq[a],seq.count(a)))
            #print (seq.count('\n'),len(seq))
    fo.close()

if __name__=="__main__":
    flist=sys.argv[1]
    in_path = sys.argv[2]
    out_path = sys.argv[3]
    fname_list = open(flist).read().split("\n")
    for fname in fname_list:
        print ('collecting seq info from {}'.format(fname))
        get_chain_info(fname,in_path,out_path)
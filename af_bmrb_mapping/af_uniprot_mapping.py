from mmcif.io.PdbxReader import PdbxReader


def get_chain_info(cif_file):
    cif_data = []
    ifh = open(cif_file, 'r')
    pRd = PdbxReader(ifh)
    pRd.read(cif_data)
    ifh.close()
    c0 = cif_data[0]
    ref_db = c0.getObj('entity_poly')
    col_names = ref_db.getAttributeList()
    seq_index=col_names.index('pdbx_seq_one_letter_code_can')
    chain_idx=col_names.index('pdbx_strand_id')
    type_index=col_names.index('pdbx_seq_one_letter_code_can')
    dat=ref_db.data
    for d in dat:
        print (d[db_index])
    return col_names

if __name__=="__main__":
    get_chain_info('AF-Q9Y6Y9-F1-model_v1.cif')
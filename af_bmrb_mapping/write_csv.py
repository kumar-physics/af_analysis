import sys

from mmcif.io.PdbxReader import PdbxReader
import os

def get_cs_info(cif_file):
    cif_data = []
    ifh = open(cif_file, 'r')
    pRd = PdbxReader(ifh)
    pRd.read(cif_data)
    ifh.close()
    c0 = cif_data[0]
    ref_db = c0.getObj('atom_chem_shift')
    col_names = ref_db.getAttributeList()
    dat=ref_db.data
    return col_names,dat


def write_csv(cif_file2,inpath,outpath):
    af_id = cif_file2.split(".cif")[0]
    fo=open('{}/{}.csv'.format(outpath,af_id),'w')
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    cif_file = '{}/{}'.format(inpath,cif_file2)
    col,dat = get_cs_info(cif_file)


    cs_methods = ['shiftx2', 'shifts', 'ucbshift', 'sparta-plus', 'cheshift', 'larmor-ca', 'rcs']
    pred = [i for i in range(len(col)) if col[i] in cs_methods]
    pred_methods = {i:col[i] for i in pred}
    # print (pred_methods)
    exp = range(max(pred_methods)+1, len(col), 3)
    bmrb_ids = {i: col[i].split('_')[0].split('bmr')[-1] for i in exp}
    # print(bmrb_ids)
    # print (col)
    for row in dat:
        if len(bmrb_ids):
            for p in pred_methods:
                for b in bmrb_ids:
                    try:
                        cs_p = float(row[p])
                        cs_e = float(row[b])
                        fo.write('{},{},{},{},{},{},{},{}\n'.format(row[1],row[2],row[3],cs_p,cs_e,pred_methods[p],bmrb_ids[b],af_id))
                    except ValueError:
                        pass
    fo.close()









if __name__ == "__main__":
    in_path=sys.argv[1]
    out_path=sys.argv[2]
    # in_path='/Users/kumaran/alpha_fold'
    # out_path='/Users/kumaran/af'
    flist = [_ for _ in os.listdir(in_path) if _.endswith('.cif')]
    for fname in flist:
        print(fname)
        print('Working on {}'.format(fname))
        write_csv(fname, in_path, out_path)


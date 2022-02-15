import bmrb_uniprot_mapping
import json
import logging
import pynmrstar
from urllib.request import urlopen, Request
import numpy
from typing import Union, List

# Set the log level to INFO
logging.getLogger().setLevel(logging.INFO)

# _API_URL = "http://dev-api.bmrb.io/v2"
_API_URL = "http://api.bmrb.io/v2"


def af_bmrb_mapping():
    uniprot_to_bmrb=bmrb_uniprot_mapping._get_data_from_api()
    f=open('af_files.txt','r').read().split("\n")
    t=0
    a=0
    bmrb_to_af={}
    for row in f:
        t+=1
        try:
            uid=row.split("/")[-1].split("-")[1]
            if uid in uniprot_to_bmrb.keys():
                a+=1
                #print (row,uniprot_to_bmrb[uid])
                bmrb_to_af[row]=uniprot_to_bmrb[uid]
        except IndexError:
            pass
    print (t,a)
    return bmrb_to_af

def check_chains(m):
    i=0
    single={}
    for k in m.keys():
        for bmrb_id in m[k]:
            i+=1
            ent = pynmrstar.Entry.from_database(bmrb_id)
            t=ent.get_tags(['Entity_assembly.Entity_ID','Entity.Polymer_type','Entity.ID'])
            ent_asm={}
            for j in range(len(t['Entity.ID'])):
                ent_asm[t['Entity.ID'][j]]=t['Entity.Polymer_type'][j]
            ent=[]
            for j in t['Entity_assembly.Entity_ID']:
                try:
                    ent.append(ent_asm[j])
                    #print(k, bmrb_id, ent)
                except KeyError:
                    pass
                    #print (bmrb_id)
            if len(ent) == 1:
                if k not in single.keys():
                    single[k] = [bmrb_id]
                single[k].append(bmrb_id)
    for k in single.keys():
        print (k,single[k])
    print ('here',len(single.keys()))


            # print (_API_URL + '/entry/{}?loop=Entity_assembly'.format(bmrb_id))
            # url = Request(_API_URL + '/entry/{}?tag=Entity_assembly.Entity_ID'.format(bmrb_id))
            # url.add_header('Application', 'af_bmrb_analysis')
            # r = urlopen(url)
            # dump = json.loads(r.read())
            # #print (dump)
            # url2 = Request(_API_URL + '/entry/{}?tag=Entity.ID'.format(bmrb_id))
            # url2.add_header('Application', 'af_bmrb_analysis')
            # r2 = urlopen(url2)
            # dump3 = json.loads(r2.read())
            # #print (dump3)
            # url2 = Request(_API_URL + '/entry/{}?tag=Entity.Polymer_type'.format(bmrb_id))
            # url2.add_header('Application', 'af_bmrb_analysis')
            # r2 = urlopen(url2)
            # dump2 = json.loads(r2.read())
            # ents={}
            # #print (dump3[bmrb_id]['Entity.ID'])
            # for j in range(len(dump3[bmrb_id]['Entity.ID'])):
            #     ents[dump3[bmrb_id]['Entity.ID'][j]]=dump2[bmrb_id]['Entity.Polymer_type'][j]
            # ent_asy=[]
            # for k in dump[bmrb_id]['Entity_assembly.Entity_ID']:
            #     try:
            #         ent_asy.append(ents[k])
            #     except KeyError:
            #         print (bmrb_id,dump,dump3)
            # # print (ents)
            # # print (ent_asy)


if __name__=="__main__":
    m=af_bmrb_mapping()
    check_chains(m)
import json
import logging
from urllib.request import urlopen, Request
import numpy
from typing import Union, List

# Set the log level to INFO
logging.getLogger().setLevel(logging.INFO)

# _API_URL = "http://dev-api.bmrb.io/v2"
_API_URL = "http://api.bmrb.io/v2"


def _get_data_from_api() -> list:
    """
    Dumps the BMRB-API return for given residue and atom. Not intend to call directly


    """
    # logging.info('Fetching chemical shift data for {}-{}'.format(residue,atom))
    url = Request(_API_URL+'/mappings/uniprot/bmrb?format=json&match_type=blast')
    url.add_header('Application', 'af_bmrb_analysis')
    r = urlopen(url)
    dump = json.loads(r.read())
    uniprot_to_bmrb={}
    for d in dump:
        if d['uniprot_id'] not in uniprot_to_bmrb.keys():
            uniprot_to_bmrb[d['uniprot_id']]=d['bmrb_ids']
        else:
            print (d)
    return uniprot_to_bmrb




if __name__=="__main__":
    _get_data_from_api()
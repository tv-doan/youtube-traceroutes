""" 
Taken from Steffie Jacob Eravuchira, Vaibhav Bajpai, Juergen Schoenwaelder,
https://github.com/vbajpai/ripe69-python3-toolset/blob/master/ripe69-python3-toolset.ipynb

Modified print statements to work with Python 2.7 and to perform required lookups
"""

import sys
import requests
import json

import sqlite3
import pandas as pd

import codecs


def get_json_resource_from_absolute_uri(url, query_params):
    try: res = requests.get(url, params = query_params)
    except Exception as e: print >> sys.stderr, e
    else:
        try: res_json = res.json()
        except Exception as e: print >> sys.stderr, e
        else:
            return res_json


# ASN lookup by IP address
def get_asn_from_endpoint(endpoint):
    asn = holder = None
    base_uri = 'https://stat.ripe.net'; url = '%s/data/prefix-overview/data.json'%base_uri
    params = {'resource' : endpoint}
    try: res = get_json_resource_from_absolute_uri(url, params)
    except Exception as e: print >> sys.stderr, e; return None
    try:
        asns_holders = []
        for item in res['data']['asns']:
            asn = item['asn']; holder = item['holder']
            asns_holders.append((asn, holder))
    except Exception as e: print >> sys.stderr, e
    return asns_holders


# AS holder lookup by ASN
def get_holder_from_asn(asn):
    base_uri = 'https://stat.ripe.net'; url = '%s/data/as-overview/data.json'%base_uri
    params = {'resource' : asn}
    try: res = get_json_resource_from_absolute_uri(url, params)
    except Exception as e: print >> sys.stderr, e; return None
    try:
        holder = res['data']['holder']
    except Exception as e: print >> sys.stderr, e
    return holder


# Reverse DNS lookup
def get_hostname_from_endpoint(endpoint):
    base_uri = 'https://stat.ripe.net'; url = '%s/data/reverse-dns-ip/data.json'%base_uri
    params = {'resource' : endpoint}
    try: res = get_json_resource_from_absolute_uri(url, params)
    except Exception as e: print >> sys.stderr, e; return None
    try:
        hostnames = []
        if res['data']['result'] is not None:  # result might be None here, i.e. no hostname could be found
            for item in res['data']['result']:
                hostnames.append(item)
    except Exception as e: print >> sys.stderr, e
    return hostnames


""" --- B A T C H --- """

# ========================
# lookup of src AS numbers
# ========================

# src_asns.csv contains all unique ASNs from probes_metadata.txt
with open('src_asns.csv', 'r') as f:
    log = codecs.open('src_asn_holders.csv', 'w', 'utf-8')
    log.write('%s;%s\n' % ('asn', 'holder'))  # header line
    for line in f:
        asn = line[:-1]  # ignore '\n' character at end of line
        
        holder = get_holder_from_asn(asn)  # perform lookup

        log.write('%s;%s\n'%(asn, holder))  # write tuple to log file
    log.close()


# ==============================================
# lookup of destination AS numbers and hostnames
# ==============================================

# get list of unique destination IP addresses from database
conn = sqlite3.connect('../data/youtube-may-2016-2018.db')
destinations = pd.read_sql_query('select distinct destination from traceroute', conn)

# get list of unique destination IP addresses
dst_list = destinations['destination'].unique()

# go through list twice, once for ASNs, once for reverse DNS lookup
# AS numbers:
with codecs.open('dst_ip_to_asn.csv', 'w', 'utf-8') as f:
    f.write('%s;%s;%s\n' % ('ip', 'asn', 'holder'))  # header line
    
    for dst in dst_list:
        asns_holders = get_asn_from_endpoint(dst)  # perform lookup
        for asn, holder in asns_holders:  # loop in case an IP has multiple associations
            f.write('%s;%d;%s\n'%(dst, asn, holder))  # write 3-tuple to log file

# hostnames:
with codecs.open('dst_ip_to_hostname.csv', 'w', 'utf-8') as f:
    f.write('%s;%s\n' % ('ip', 'hostname'))  # header line

    for dst in dst_list:
        hostnames = get_hostname_from_endpoint(dst)  # perform lookup
        for name in hostnames:  # loop in case an IP has multiple associations
            f.write('%s;%s\n'%(dst, name))  # write tuple to log file


# ===============================================
# lookup of AS numbers for intermediate endpoints
# ===============================================

# get list of unique intermediate endpoint IP addresses from database
endpoints = pd.read_sql_query('select distinct endpoint from traceroute', conn)
conn.close()

with codecs.open('endpoint_asn_lookup.csv', 'w', 'utf-8') as f:
    
    f.write('%s;%s;%s\n' % ('endpoint', 'asn', 'holder'))  # header line
    
    for endpoint in endpoints['endpoint'].unique():

        lookup = get_asn_from_endpoint(endpoint)
        
        #if not lookup:  # no result found, most likely private IP address
        #    f.write('%s;;\n' % endpoint)

        for asn, holder in lookup:
            f.write('%s;%d;%s\n' % (endpoint, asn, holder))

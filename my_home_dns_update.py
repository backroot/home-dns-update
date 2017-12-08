#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, yaml, boto, urllib2, json

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/config.yaml', 'rt') as f:
        data = f.read()
    
    config = yaml.safe_load(data)
    service = config['ip_check_service']

    try:
        url = urllib2.urlopen(service)
        res = json.loads(url.read())
    finally:
        url.close()
    
    route53_conn = boto.connect_route53(config['key'], config['secret'])
    zone = route53_conn.get_zone(config['domain_name'])
    record = zone.get_a(config['zone_name'])
    a = record.to_print() 
    if a != res['ip']:
        zone.update_a(config['zone_name'], res['ip'])

if __name__ == '__main__':
    main()

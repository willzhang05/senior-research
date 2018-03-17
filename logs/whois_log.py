#!/usr/bin/python3
import glob, os
import re
import ipwhois

def main():
    unique = dict()
    #unique = set()
    for filename in glob.glob("*.log"):
        with open(filename, 'r') as f:
            line = None
            while line != '':
                line = f.readline().strip()
                attr = line.split('\t')
                new_attr = []
                for a in attr:
                    sub = re.sub(r'[A-z/]+:\s', '', a).strip()
                    new_attr.append(sub)
                if len(new_attr) > 1:
                    new_attr[1] = re.sub(r'/\d{2,4}', '', new_attr[1])
                    if new_attr[1] in unique:
                        unique[new_attr[1]] = (new_attr[0], max(int(unique[new_attr[1]][1]), int(new_attr[3])))
                    else:
                        unique[new_attr[1]] = (new_attr[0], int(new_attr[3]))
                #unique[attr[1]] = 
                #if attr[0] != '':
                #    new_attr = attr[0:2]
                #    new_attr.extend([attr[3]])
                #    unique.add('\t'.join(new_attr))

    #out = sorted(list(unique))
    keys = sorted(unique.keys())
    for k in keys:
        whois = ipwhois.IPWhois(k)
        info = whois.lookup_rdap()
        asn_desc = info['asn_description']
        desc = None
        if info['network']['remarks'] is not None:
            desc = info['network']['remarks'][0]['description']

        output = '{0:7} {1:40}\t\t{2:6} {3:20}\t\t{4:4} {5:4}'.format('Source:', k, 'Group:', unique[k][0], 'PPS:', unique[k][1])
        print(output)
        if asn_desc is not None:
            print(asn_desc)
        if desc is not None:
            print(desc)
        print()
        print()


if __name__ == "__main__":
    main()

#!/usr/bin/python3
import requests
import re
import time


BASE_URL = 'https://routerproxy.grnoc.iu.edu/internet2/'
FILENAME = 'ips.txt'

def main():
    global FILENAME
    global BASE_URL
    devices = set()
    with open(FILENAME, 'r') as f:
        ip = f.readline()
        while ip != '':
            devices.add(ip.strip())
            ip = f.readline()
    devices = list(devices)      
    print(devices)
    output = dict()
    for device in devices:
        print(device)
        r = requests.get(BASE_URL + '?method=submit&device=' + device + '&command=show multicast&menu=0&arguments=route detail')
        new_text = re.sub(r'&[^\s]{2,4};|[\r]', '', r.text)
        s_new_text = new_text.split('\n')
        fields = dict()
        for i in range(1, len(s_new_text) - 1):
            s_line = s_new_text[i].split(':', 1)
            if s_line[0] != '':
                fields[s_line[0]] = ''.join(s_line[1:])
        print(fields)
        if 'Group' in fields:
            output[fields['Group']] = fields['Statistics'].split(',')
            print(output[fields['Group']])
        '''for line in new_text:
            output[device] = dict()
            output[device][s_line[0]] = s_line[1]
        '''

        time.sleep(2)
    print(output)



if __name__ == '__main__':
    main()

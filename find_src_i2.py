#!/usr/bin/python3
import requests
import re
import time

BASE_URL = 'https://routerproxy.grnoc.iu.edu/internet2/'
FILENAME = 'ips.txt'


class Source():
    def __init__(self, source, group, stats):
        self.source = source
        self.group = group
        st = stats.split(',')
        self.speed = int(re.sub(r'[^0-9]', '', st[0]))
        self.pps = int(re.sub(r'[^0-9]', '', st[1]))
        self.packets = int(re.sub(r'[^0-9]', '', st[2]))

    def __repr__(self):
        return 'Source: ' + self.source + '\nGroup: ' + self.group + '\nPPS: ' + str(self.pps)

    def __str__(self):
        return 'Source: ' + self.source + '\nGroup: ' + self.group + '\nPPS: ' + str(self.pps)

    def __eq__(self, other):
        return self.source == other.source and self.group == other.group

    def __hash__(self):
        return hash(self.__repr__())


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
    output = set()
    for device in devices:
        r = requests.get(BASE_URL + '?method=submit&device=' + device + '&command=show multicast&menu=0&arguments=route detail')
        new_text = re.sub(r'&[^\s]{2,4};|[\r]', '', r.text)
        s_new_text = new_text.split('\n')
        fields = dict()
        for i in range(1, len(s_new_text) - 1):
            s_line = s_new_text[i].split(':', 1)
            if s_line[0] == '':
                if 'Group' in fields:
                    s = Source(fields['Source'], fields['Group'], fields['Statistics'])
                    if s.pps > 5:
                        print(s)
                        print()
                        output.add(s)
                fields = dict()
            else:
                fields[s_line[0]] = ''.join(s_line[1:])
        time.sleep(2)
    out_list = list(output)
    print('-' * 10)
    for o in out_list:
        print(o)

if __name__ == '__main__':
    main()

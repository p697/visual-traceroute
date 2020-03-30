import os
import requests
import json
import csv

def traceRoute(ip):
    cmd = 'tracert {}'.format(ip)
    res = os.popen(cmd)
    result = res.read()

    ipList1 = []
    for r in result.split('\n'):
        if 'ms' in r:
            ipList1.append(r)

    ipList = []
    for ipl in ipList1:
        ip = ipl.split(' ')[-2]
        if '.' not in ip or '*' in ip:
            continue
        if '[' in ip:
            ip = ip[1:-1]
        if '192.168' in ip:
            res = requests.get('https://ifconfig.co/ip')
            ip = res.text
        print(ip)
        ipList.append(ip)
    
    return ipList


def getLocation(ipList):
    result = []
    for ip in ipList:
        res = requests.get('https://api.map.baidu.com/location/ip?ak=W5neWQg858cGnB7AtQqSiG0KZSgXObYM&ip={}&coor=bd09ll'.format(ip))
        data = json.loads(res.text)
        # print(data)
        # address = data['address'].encode('utf-8').decode('utf-8')
        try:
            address = data['address']
        except:
            print('出错：{}'.format(ip))
            continue
        result.append( [address, data['content']['point']['x'][:-2], data['content']['point']['y'][:-2]] )
    return result


def generateCSV(info):
    fialInfo = []
    for i in range(len(info)-1):
        i2 = []
        i2.append(info[i][0])
        i2.append(info[i+1][0])
        i2.append('1')
        i2.append('move_out')
        i2 += info[i][1:]
        i2 += info[i+1][1:]
        fialInfo.append(i2)

    with open('info.csv', 'w', encoding="UTF8",newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['from', 'to', 'value', 'type', 'lng1', 'lat1', 'lng2', 'lat2'])
        writer.writerows(fialInfo)


ipList = traceRoute('111.230.251.229')
# print(ipList)
# ipList = traceRoute('219.245.157.9')
info = getLocation(ipList)
# print(info)
generateCSV(info)



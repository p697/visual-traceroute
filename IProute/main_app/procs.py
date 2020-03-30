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
        if '.' not in ip:
            continue
        if '[' in ip:
            ipl = ip.split('[')
            ip = ipl[-1][:-1]
        if '192.168' in ip:
            res = requests.get('https://ifconfig.co/ip')
            ip = res.text.split('\n')[0]
        # print(ip)
        ipList.append(ip)
    
    return ipList


def getLocation(ipList):
    result = []
    for ip in ipList:
        # 将ip地址转化为经纬度的api，网上一大把，这个如果失效了请自己换一个
        res = requests.get('https://api.ipplus360.com/ip/geo/v1/city/?key=Vxe9Y0x8ASe3N0IC1wzYNQISi15m88WOJbyT842xmHScgHsMmTUv0DPsaR0OsAbe&ip={}&coordsys=WGS84'.format(ip))
        data = json.loads(res.text)
        # 更换api之后别忘了把下面几行改一下
        print('------------------')
        print(ip)
        print(data)
        address = data['data']['multiAreas'][0]['prov']
        x = data['data']['multiAreas'][0]['lng']
        y = data['data']['multiAreas'][0]['lat']
        if x:
            result.append( [address, x, y] )
    return result


def generateCSV(info):
    fialInfo = []
    for i in range(len(info)-1):
        i2 = []
        # i2.append(info[i][0])
        # i2.append(info[i+1][0])
        # i2.append('1')
        # i2.append('move_out')
        i2 += info[i][1:]
        i2 += info[i+1][1:]
        fialInfo.append(i2)
    # print(fialInfo)

    with open('main_app/static/route.csv', 'w', encoding="UTF8",newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['lng1', 'lat1', 'lng2', 'lat2'])
        writer.writerows(fialInfo)



def create(ip):
    print('begin --- {}'.format(ip))
    ipList = traceRoute(ip)
    info = getLocation(ipList)
    generateCSV(info)
    return True


# create('219.245.157.9')

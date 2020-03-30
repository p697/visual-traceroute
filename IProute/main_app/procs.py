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


def getInfo(ipList):
    result = []
    for ip in ipList:
        # 将ip地址转化为经纬度的api，网上一大把，这个如果失效了请自己换一个
        res = requests.get('https://api.ipplus360.com/ip/geo/v1/city/?key=Vxe9Y0x8ASe3N0IC1wzYNQISi15m88WOJbyT842xmHScgHsMmTUv0DPsaR0OsAbe&ip={}&coordsys=WGS84'.format(ip))
        data = json.loads(res.text)
        # 更换api之后别忘了把下面几行改一下
        print('------------------')
        print(ip)
        print(data)
        if not data['data']['multiAreas'][0]['prov']:
            continue
        address = '{}-{}-{}-{}'.format(
            data['data']['country'], 
            data['data']['multiAreas'][0]['prov'], 
            data['data']['multiAreas'][0]['city'],
            data['data']['owner']
            )
        x = data['data']['multiAreas'][0]['lng']
        y = data['data']['multiAreas'][0]['lat']
        ip = data['ip']
        if x:
            result.append( [address, x, y, ip] )
    return result


def generateJson(info):
    data = {}
    route = []
    local = []
    dot = []
    for i in range(len(info)-1):
        i2 = {}
        i2['from'] = '{}, {}'.format(info[i][1], info[i][2])
        i2['to'] = '{}, {}'.format(info[i+1][1], info[i+1][2])
        route.append(i2)

        i3 = {}
        i3['from'] = info[i][0]
        i3['fromIP'] = info[i][3]
        i3['to'] = info[i+1][0]
        i3['toIP'] = info[i+1][3]
        local.append(i3)
        
        i4 = {}
        i4['x'] = info[i][1]
        i4['y'] = info[i][2]
        dot.append(i4)
        if i == len(info)-2:
            i4 = {}
            i4['x'] = info[i+1][1]
            i4['y'] = info[i+1][2]
        dot.append(i4)

    data['route'] = route
    data['local'] = local
    data['dot'] = dot
    saveJson(data)
    return data


def saveJson(data):
    jsonData = json.dumps(data)
    with open('main_app/static/route.json', 'w') as f:
        f.write(jsonData)


# def generateCSV(info):
#     fialInfo = []
#     for i in range(len(info)-1):
#         i2 = []
#         i2.append(info[i][0])
#         i2.append(info[i+1][0])
#         # i2.append('1')
#         # i2.append('move_out')
#         i2 += info[i][1:]
#         i2 += info[i+1][1:]
#         fialInfo.append(i2)
#     # print(fialInfo)

#     with open('main_app/static/route.csv', 'w', encoding="UTF8",newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['from', 'to', 'lng1', 'lat1', 'lng2', 'lat2'])
#         writer.writerows(fialInfo)



def create(ip):
    print('begin --- {}'.format(ip))
    ipList = traceRoute(ip)
    info = getInfo(ipList)
    data = generateJson(info)
    
    return data

# create('117.136.87.15')

# create('219.245.157.9')

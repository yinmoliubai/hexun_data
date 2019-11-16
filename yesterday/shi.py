import pandas as pd
import requests
import re
import json
import datetime
import time
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=15)




re_time = '00:00:00'
hour,momount,second = list(map(int,re_time.split(':')))
headers = {
    'Host': 'forex.wiapi.hexun.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://quote.hexun.com/forex/forex.aspx?type=1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9', }


dataframe_list = []

for i in range(19):
    df = pd.DataFrame(columns=(
    '简称', '币种', '现价', '涨跌', '涨幅', '开盘', '最高', '最低', '买价', '卖价', '时间',
    '走势图'))
    dataframe_list.append(df)

num = 0

now_day = ''.join(str(datetime.datetime.now()).split()[0].split('-'))

while True:
    num += 1
    past_time = '%02d%02d%02d'%(hour,momount,second)
    print(past_time)
    # print(now_time)
    huilv_url = 'http://forex.wiapi.hexun.com/forex/sortlist?'
    url_data = 'block=303&number=1000&title=15&commodityid=0&direction=0&start=0&column=code,name,price,updown,updownrate,open,high,low,buyPrice,sellPrice,datetime,PriceWeight&callback=quoteforex&time={}'.format(
        past_time)
    right_url = huilv_url + url_data
    huilv_data = requests.get(url=right_url,
                              headers=headers).content.decode()
    data = re.findall(r'\{.*?\}', huilv_data)[0]
    json_data = json.loads(data)['Data'][0]
    if num == 1:
        for i in range(19):
            new_h = [json_data[i][0], json_data[i][1],
                     float('%0.4f' % (json_data[i][2] / 10000)),
                     json_data[i][4] / 100, json_data[i][3] / 10000,
                     json_data[i][5] / 10000, json_data[i][6] / 10000,
                     json_data[i][7] / 10000,
                     float('%0.4f' % (json_data[i][8][0] / 10000)),
                     float('%0.4f' % (json_data[i][9][0] / 10000)),
                     json_data[i][10], json_data[i][11]]
            dataframe_list[i].loc[new_h[-2]] = new_h
    else:
        for j in range(19):
            for i in range(19):
                if dataframe_list[j]['币种'].values[0] == json_data[i][1]:
                    new_h = [json_data[i][0], json_data[i][1],
                             float('%0.4f' % (json_data[i][2] / 10000)),
                             json_data[i][4] / 100,
                             json_data[i][3] / 10000,
                             json_data[i][5] / 10000,
                             json_data[i][6] / 10000,
                             json_data[i][7] / 10000,
                             float('%0.4f' % (json_data[i][8][0] / 10000)),
                             float('%0.4f' % (json_data[i][9][0] / 10000)),
                             json_data[i][10], json_data[i][11]]
                    dataframe_list[j].loc[new_h[10]] = new_h
    now_time = ''.join(str(datetime.datetime.now()).split()[1].split('.')[0].split(':'))
    if int(past_time) % 10000 == 0 or past_time < now_time:
        for index in range(19):
            dataframe_list[index].to_csv('%s-%s.csv' % (dataframe_list[index]['币种'].values[0],now_day),mode='a',header=True,encoding='utf-8')
    else:
        break
        
    # time.sleep(1)
    second +=  30
    if second == 60 :
        second = 0
        momount += 1
        if momount == 60:
            momount = 0
            hour += 1
            if hour == 60:
                hour = 0
        
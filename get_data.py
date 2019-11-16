import requests
import time
import datetime
import re
import json
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=15)

import pandas as pd

start_urls = ['http://gold.hexun.com/hjxh/',
              'http://gold.hexun.com/byxh/',
              'http://quote.hexun.com/forex/forex.aspx?type=1']

headers = {
    'Host':'forex.wiapi.hexun.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://quote.hexun.com/forex/forex.aspx?type=1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',}


# data_queue = [[[], [], [], [], [], [], [], [], [], [], [], [],[],[],[],[],[],[],[]]]

dataframe_list = []

for i in range(19):
    df = pd.DataFrame(columns=('简称','币种','现价','涨跌','涨幅','开盘','最高','最低','买价','卖价','时间','走势图'))
    dataframe_list.append(df)
    

num = 0

while True:
    num += 1
    now_time = ''.join(str(datetime.datetime.now()).split()[1].split('.')[0].split(':'))
    now_day = ''.join(str(datetime.datetime.now()).split()[0].split('-'))
    print(now_day + now_time)
    # print(now_time)
    huilv_url = 'http://forex.wiapi.hexun.com/forex/sortlist?'
    url_data = 'block=303&number=1000&title=15&commodityid=0&direction=0&start=0&column=code,name,price,updown,updownrate,open,high,low,buyPrice,sellPrice,datetime,PriceWeight&callback=quoteforex&time={}'.format(now_time)
    right_url = huilv_url + url_data
    huilv_data = requests.get(url = right_url,headers=headers).content.decode()
    data = re.findall(r'\{.*?\}',huilv_data)[0]
    json_data = json.loads(data)['Data'][0]
    # data_queue.append(json_data)
    if num == 1:
        for i in range(19):
            df_index = now_day + now_time
            new_h = [json_data[i][0], json_data[i][1],float('%0.4f' % (json_data[i][2] / 10000)),json_data[i][4] / 100, json_data[i][3] / 10000,json_data[i][5] / 10000, json_data[i][6] / 10000,json_data[i][7] / 10000,float('%0.4f' % (json_data[i][8][0] / 10000)),float('%0.4f' % (json_data[i][9][0] / 10000)),json_data[i][10], json_data[i][11]]
            dataframe_list[i].loc[new_h[-2]] = new_h
    else:
        for j in range(19):
            for i in range(19):
                if dataframe_list[j]['币种'].values[0] == json_data[i][1]:
                    df_index = now_day + now_time
                    new_h = [json_data[i][0], json_data[i][1], float('%0.4f' % (json_data[i][2] / 10000)),json_data[i][4] / 100, json_data[i][3] / 10000, json_data[i][5] / 10000,json_data[i][6] / 10000, json_data[i][7] / 10000,float('%0.4f' % (json_data[i][8][0] / 10000)),float('%0.4f' % (json_data[i][9][0] / 10000)), json_data[i][10],json_data[i][11]]
                    dataframe_list[j].loc[new_h[10]] = new_h
                    
    # if len(data_queue) > 100:
    #     data_queue = data_queue[-3:]
    if num == 20:
        for index in range(19):
            dataframe_list[index].to_csv('%s.csv'%dataframe_list[index]['币种'].values[0])
            x = list(map(str,dataframe_list[index].index))
            fig, ax = plt.subplots(1, 1)
            plt.plot(x, dataframe_list[index]['买价'],'r')
            plt.plot(x, dataframe_list[index]['卖价'],'g')
            plt.xticks(x,rotation=90)
            min_number = min(dataframe_list[index]['买价'])
            xiaoshu_number = str(10000 * (max(dataframe_list[index]['卖价']) - min(dataframe_list[index]['买价']))).split('.')[0]
            step = 0.1 ** (5 - len(str(xiaoshu_number)))
            y_kedu = [min_number+i*step for i in range(0,11)]
            print(y_kedu)
            plt.yticks(y_kedu)
            for label in ax.get_xticklabels():
                label.set_visible(False)
            for label in ax.get_xticklabels()[::5]:
                label.set_visible(True)
            for label in ax.get_yticklabels():
                label.set_visible(False)
            for label in ax.get_yticklabels()[::2]:
                label.set_visible(True)
            plt.xlabel('时间',fontproperties=font_set)  # 设置x轴名称
            plt.ylabel('价格',fontproperties=font_set)  # 设置y轴名称
            plt.title(dataframe_list[index]['币种'].values[0],fontproperties=font_set)  # 设置图片名称
            plt.legend(['现价','卖价'],loc="upper right")
            plt.show()
            print(x[0],x[-1])
            print(dataframe_list[index]['现价'])
            print(dataframe_list[index]['卖价'])
            break
        break
    
    time.sleep(15)




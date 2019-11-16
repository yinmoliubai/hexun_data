import requests
import time
import datetime
import re
import json
import pandas as pd
import random
import matplotlib.pylab as plt
from threading import Thread
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)

def picture(df,plt,bizhong):
    x_data = list(map(str, df['时间']))
    print(x_data)
    y_maijia_data = df['买价']
    y_maioutjia_data = df['卖价']
    min_number = y_maijia_data.min()
    max_number = y_maioutjia_data.max()
    print(min_number, max_number)
    xiaoshu_number = str(10000 * (max_number - min_number)).split('.')[0]
    print(xiaoshu_number)
    mid_num = 5 - len(str(xiaoshu_number))
    if mid_num:
        step = 0.1 ** mid_num
    else:
        step = 1 / int(xiaoshu_number[0])
        
    y_kedu = [min_number - step * 2 + i * step for i in range(0, 10)]
    print(y_kedu)
    
    plt.clf()  # 清除刷新前的图表，防止数据量过大消耗内存
    fig, ax = plt.subplots(1, 1)
    plt.plot(x_data, y_maijia_data, 'r')
    plt.plot(x_data, y_maioutjia_data, 'g')
    plt.xticks(x_data, rotation=90)
    plt.yticks(y_kedu)
    for label in ax.get_xticklabels():
        label.set_visible(False)
    for label in ax.get_xticklabels()[::5]:
        label.set_visible(True)
    plt.xlabel('时间', fontproperties=font_set)  # 设置x轴名称
    plt.ylabel('价格', fontproperties=font_set)  # 设置y轴名称
    plt.title(df['币种'].values[0],fontproperties=font_set)  # 设置图片名称
    plt.legend(['买价', '卖价'], loc="upper right", prop=font_set)
    if len(x_data) == 60:
        plt.save('%s.jpg'%bizhong)
    plt.show()
    
    # plt.pause(time)  # 设置暂停时间，太快图表无法正常显示
    # plt.close()
def main(bizhong):
    headers = {
        'Host': 'forex.wiapi.hexun.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://quote.hexun.com/forex/forex.aspx?type=1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9', }
    
    df = pd.DataFrame(columns=(
    '简称', '币种', '现价', '涨跌', '涨幅', '开盘', '最高', '最低', '买价', '卖价', '时间',
    '走势图'))
    
    plt.ion()  # 开启一个画图的窗口进入交互模式，用于实时更新数据
    plt.rcParams['lines.linewidth'] = 0.5  # 设置曲线线条宽度
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
        huilv_data = requests.get(url=right_url,headers=headers).content.decode()
        data = re.findall(r'\{.*?\}', huilv_data)[0]
        json_data = json.loads(data)['Data'][0]
        for item in json_data:
            # if item[1] == '英镑美元':
            if item[1] == bizhong:
                new_h = [item[0], item[1],
                         float('%0.4f' % (item[2] / 10000)),
                         item[4] / 100, item[3] / 10000,
                         item[5] / 10000, item[6] / 10000,
                         item[7] / 10000,
                         float('%0.4f' % (item[8][0] / 10000)),
                         float('%0.4f' % (item[9][0] / 10000)),
                         item[10], item[11]]
                df.loc[now_time] =new_h
        sleep_random =  random.choice([i for i in range(30,61,10)])
        print('start:',datetime.datetime.now())
        if num >= 2:
            df.to_csv('%s.csv'%bizhong,mode='a',header=True,encoding='utf-8')
            t = Thread(target=picture,args=(df, plt,bizhong))
            t.start()
            # t.join()
        if num == 60:
            break
        print('end:', datetime.datetime.now())
        time.sleep(sleep_random)
    
if __name__ == '__main__':
    menu = ['新西兰元美元', '欧元美元', '澳元美元', '美元人民币', '美元俄罗斯卢布', '美元加元', '美元印尼卢比', '美元墨西哥元', '美元巴西雷亚尔', '美元指数', '美元挪威克朗', '美元新土耳其里拉', '美元日元', '美元沙特里亚尔', '美元港元', '美元瑞士法郎', '美元阿根廷比索', '美元韩元', '英镑美元']
    print(menu)
    # bizhong  = input('请输入监测的币种：')
    bizhong = '美元韩元'
    main(bizhong)
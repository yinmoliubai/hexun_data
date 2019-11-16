import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.font_manager import FontProperties
font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=15)

df = pd.read_csv('美元韩元.csv',engine='python',encoding='utf-8').iloc[-50:]
# print(df.iloc[-100:])
df.columns = ['index','简称', '币种', '现价', '涨跌', '涨幅', '开盘', '最高', '最低', '买价', '卖价', '时间', '走势图']



x_data = list(map(str,df['index']))
print(x_data)
y_maijia_data = df['买价']
y_maioutjia_data = df['卖价']
num=2   #计数
plt.ion()    # 开启一个画图的窗口进入交互模式，用于实时更新数据
# plt.rcParams['savefig.dpi'] = 200 #图片像素
# plt.rcParams['figure.dpi'] = 200 #分辨率
plt.rcParams['figure.figsize'] = (12, 9)        # 图像显示大小
# plt.rcParams['font.sans-serif']=['SimHei']   #防止中文标签乱码，还有通过导入字体文件的方法
# plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['lines.linewidth'] = 0.5   #设置曲线线条宽度

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
print(step)
y_kedu = [min_number - 1 + i * step for i in range(0, 10)]
print(y_kedu)

while num<50:
    plt.clf()    #清除刷新前的图表，防止数据量过大消耗内存
    fig, ax = plt.subplots(1, 1)
    plt.plot(x_data[:num+1], y_maijia_data[:num+1], 'r')
    plt.plot(x_data[:num+1], y_maioutjia_data[:num+1], 'g')
    plt.xticks(x_data[:num+1], rotation=40)
    plt.yticks(y_kedu)
    for label in ax.get_xticklabels():
        label.set_visible(False)
    for label in ax.get_xticklabels()[::5]:
        label.set_visible(True)
    # for label in ax.get_yticklabels():
    #     label.set_visible(False)
    # for label in ax.get_yticklabels()[::2]:
    #     label.set_visible(True)
    plt.xlabel('时间', fontproperties=font_set)  # 设置x轴名称
    plt.ylabel('价格', fontproperties=font_set)  # 设置y轴名称
    plt.title(df['币种'].values[0],
              fontproperties=font_set)  # 设置图片名称
    plt.legend(['买价', '卖价'], loc="upper right", prop=font_set)
    if num == 49:
        plt.savefig('picture.png', dpi=300)  # 设置保存图片的分辨率
    plt.pause(0.4)     #设置暂停时间，太快图表无法正常显示

    num=num+1


plt.ioff()       # 关闭画图的窗口，即关闭交互模式
plt.show()       # 显示图片，防止闪退

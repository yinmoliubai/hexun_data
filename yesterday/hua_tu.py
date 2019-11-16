# import pandas as pd
# import matplotlib.pylab as plt
# from matplotlib.font_manager import FontProperties
# font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=15)
#
# df = pd.read_csv('美元韩元.csv',engine='python',encoding='utf-8').iloc[-100:]
# # print(df.iloc[-100:])
# df.columns = ['index','简称', '币种', '现价', '涨跌', '涨幅', '开盘', '最高', '最低', '买价', '卖价', '时间', '走势图']
# x = list(map(str,df['index']))
# fig, ax = plt.subplots(1, 1)
# plt.plot(x, df['买价'], 'r')
# plt.plot(x, df['卖价'], 'g')
# plt.xticks(x, rotation=90)
# min_number = df['买价'].min()
# max_number = df['卖价'].max()
# print(min_number,max_number)
# xiaoshu_number = str(10000 * (max_number - min_number)).split('.')[0]
# mid_num = 5 - len(str(xiaoshu_number))
# if mid_num:
#     step = 0.1 ** mid_num
# else:
#     step = 0.2
# y_kedu = [min_number + i * step for i in range(0, 10)]
# print(y_kedu)
# plt.yticks(y_kedu)
# for label in ax.get_xticklabels():
#     label.set_visible(False)
# for label in ax.get_xticklabels()[::10]:
#     label.set_visible(True)
# for label in ax.get_yticklabels():
#     label.set_visible(False)
# for label in ax.get_yticklabels()[::2]:
#     label.set_visible(True)
# plt.xlabel('时间', fontproperties=font_set)  # 设置x轴名称
# plt.ylabel('价格', fontproperties=font_set)  # 设置y轴名称
# plt.title(df['币种'].values[0],
#           fontproperties=font_set)  # 设置图片名称
# plt.legend(['买价', '卖价'], loc="upper right",prop = font_set)
# plt.show()


import os

name = []
for root, dirs, files in os.walk(".", topdown=False):
    for i in files:
        print(os.path.splitext(i))
        if os.path.splitext(i)[1] == '.csv':
            name.append(os.path.splitext(i)[0])
print(name)



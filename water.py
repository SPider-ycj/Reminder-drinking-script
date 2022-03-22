# date:2022-03-19
# author:marxycj
# reference material: https://blog.csdn.net/xunkhun/article/details/79266283

import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from time import sleep


def GetHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()    # 产生异常时停止程序
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'


def GetData(html):
    final_list = []
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    data = body.find('div', {'id':'7d'})
    ul = data.find('ul')
    lis = ul.find_all('li')

    for day in lis:
        temp_list = []
        date = day.find('h1').string    # 找到日期 h1标签
        temp_list.append(date)

        info = day.find_all('p')    # 找到所有的p标签
        temp_list.append(info[0].string)

        if info[1].find('span') is None:
            temperature_h = ''  # 没有最高气温时
        else:
            temperature_h = info[1].find('span').string
            temperature_h = temperature_h.replace('℃', ' ')

        if info[1].find('i') is None:
            temperature_l = ''  # 没有最低气温时
        else:
            temperature_l = info[1].find('i').string
            temperature_l = temperature_l.replace('℃', ' ')

        temp_list.append(temperature_h)     # 获取最高气温
        temp_list.append(temperature_l)     # 获取最低气温

        wind_scale = info[2].find('i').string
        temp_list.append(wind_scale)    # 获取风级情况
        final_list.append(temp_list)
    return final_list


# 用format()将结果打印输出
def PrintData(final_list,num):
    print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format('日期','天气','最高温度','最低温度','风级'))
    for i in range(num):
        final = final_list[i]
        print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}".format(final[0],final[1],final[2],final[3],final[4]))


def SetTime(Average_temperature):   # 根据当天平均气温设置睡眠（提醒喝水）的间隔时间
    if Average_temperature <= 0:    # 当日平均气温<0,1.5h提醒一次喝水
        sleep_time = 5400
    elif Average_temperature > 0 and Average_temperature <= 10:  # 当日平均气温<=10,1h提醒一次喝水
        sleep_time = 3600
    elif Average_temperature > 10 and Average_temperature <= 20:  # 当日平均气温<=20,45min提醒一次喝水
        sleep_time = 2700
    elif Average_temperature > 20 and Average_temperature <= 35:  # 当日平均气温<=35,30min提醒一次喝水
        sleep_time = 1800
    elif Average_temperature > 35:      # 当日平均气温>35,20min提醒一次喝水
        sleep_time = 1200
    return sleep_time


def main():
    url = 'http://www.weather.com.cn/weather/101300501.shtml'
    html = GetHTMLText(url)
    final_list = GetData(html)
    PrintData(final_list, 7)
    today_temp = final_list[0]
    if today_temp[2] != '':
        print("\n当天最高气温{:^10}".format(today_temp[2]))
        temperature_h = int(today_temp[2])
    else:
        print("没有显示最高气温喔")
        temperature_h = 0
    if today_temp[3] != '':
        print("\n当天最低气温{:^10}".format(today_temp[3]))
        temperature_l = int(today_temp[3])
    else:
        print("没有显示最低气温喔")
        temperature_l = 0
    Average_temperature = (temperature_h + temperature_l)/2.0
    sleep_time = SetTime(Average_temperature)

    print("今日平均气温为：{},喝水间隔为{}s".format(Average_temperature, sleep_time))
    toaster = ToastNotifier()
    toaster.show_toast(u'Hello marxycj', u'记得种树呀，开始努力学习叭！')
    while True:
        sleep(sleep_time)
        toaster = ToastNotifier()
        toaster.show_toast(u'已经过去一个小时了', u'该去喝水活动活动啦~')


main()




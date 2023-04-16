import sys
import warnings
warnings.filterwarnings("ignore")
import requests
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import shutil
import argparse
def copyvideo():
    source = r'C:\Users\mi\Downloads'
    target = '.'
    file_name_list = os.listdir(source)
    # print(file_name_list)
    for i in file_name_list:
        if(".flv" in i):
            while(True):
                size_1 = os.path.getsize(source+'/'+i)
                time.sleep(5)
                size_2 = os.path.getsize(source + '/' + i)
                if(size_1 == size_2):
                    sys.exit(0)
                else:
                    shutil.copy(source+'/'+ i,target+'/'+i)
                    print("已下载："+str(size_2/1024/1024)+"MB");
        else:
            continue
    sys.exit(0)

def down(url):
    try:
        proxy.new_har('fetch', options={'captureContent': True, 'captureContent': True})
        driver.get(url)
        time.sleep(3)
        json_data = proxy.har
        # print(json_data)
        for entry in json_data['log']['entries']:
            # 根据URL找到数据接口
            entry_url = entry['request']['url']
            if (".flv" in entry_url):
                # 获取接口返回内容
                print("已获取流媒体：", entry_url,'\n开始下载...')
                break
        # ts_content = requests.get(url=entry_url, headers=headers).content
        time.sleep(8)
        driver.get(entry_url)
        time.sleep(8)
        copyvideo()
    except:
        print("下载完成，请手动清理Chrome浏览器的下载文件夹!")
        exit(0)

def body(driver,args):
    try:
        driver.get(args.add)
        url = driver.find_element(By.XPATH, "//div[@class='RPhIHafP']/a").get_attribute('href')
        host = driver.find_element(By.CLASS_NAME, 'Nu66P_ba')
        print("主播", host.text, "正在直播...")
        print("直播地址：", url)
        down(url)
    except:
        # host = driver.find_element(By.CLASS_NAME, 'Nu66P_ba')
        print("主播尚未开播,将在1分钟后重试...")
        time.sleep(2)
        body(driver,args)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arg')
    parser.add_argument('--add', type=str)
    args = parser.parse_args()
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    # 开启代理
    server = Server(r'C:\Users\mi\PycharmProjects\live_video\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()

    # 配置Proxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={}'.format(proxy.proxy))
    driver = webdriver.Chrome(options=chrome_options)
    # print(driver.page_source)
    body(driver,args)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/




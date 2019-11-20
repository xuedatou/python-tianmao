# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zfj'
__mtime__ = '2018/7/12 23:22'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻     ┃
            ┗━┓     ┏━┛
                ┃     ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import os
import requests
import json
import re

pwd = "F:\pythonImages"

filterList = [
    '评价方未及时做出评价,系统默认好评!',
    '15天内买家未作出评价',
    '系统默认评论',
    '此用户没有填写评价。'
]

def getimge(url, filepath):
    '''
    下载图片
    :param url:
    :param filepath:
    :return:
    '''
    ir = requests.get(url)
    if ir.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(ir.content)
    else:
        raise Exception("通信异常")


def getCommodityComments():
    id = '4440735535166203'
    urls = 'https://m.weibo.cn/comments/hotflow?id='+id+'&mid='+id+'&max_id_type=0&page='


    product_dir = os.path.join(pwd, id)
    print(product_dir)
    if not os.path.exists(product_dir):
        os.mkdir(product_dir)
    i=1
    count = 1000
    num =1


    while i <= count:
        fp = open(os.path.join(product_dir, "content.txt"), "a", encoding='utf-8')
        try:
            url = urls + str(i)
            resp = requests.get(url)
            resp.encoding = resp.apparent_encoding
            comment_json = json.loads(resp.text)
            comments_list = comment_json["data"]["data"]
            print(comments_list)
            for commment_item in comments_list:
                username = commment_item["user"]["screen_name"]
                comment = commment_item["text"]
                print(comment)
                label_filter = re.compile(r'</?\w+[^>]*>', re.S)
                comment = re.sub(label_filter, '', comment)
                print(comment)
                fp.write(str(num) + ':' + comment + '\n')
                num += 1
        except Exception as e:
            print(e)
            print(str(i) + "遇到异常")
            continue
        i += 1
        fp.close()



getCommodityComments()

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
    id = '4440720863417426'
    urls = 'https://m.weibo.cn/comments/hotflow?id='+id+'&mid='+id


    product_dir = os.path.join(pwd, id)
    print(product_dir)
    if not os.path.exists(product_dir):
        os.mkdir(product_dir)
    i=1
    num =1
    max_id=''
    session = requests.session()
    session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    session.headers['Host'] = 'm.weibo.cn'
    session.headers['MWeibo-Pwa'] = '1'
    session.headers['TE'] = 'Trailers'
    session.headers['Connection'] = 'keep-alive'
    session.headers['Cache-Control'] = 'max-age=0'
    session.headers['X-Requested-With'] = 'X-Requested-With'
    session.headers['proc_node'] = 'mweibo-10-22-3-103.xxg.intra.weibo.cn'
    session.headers['cookie'] = 'SUHB=02MvihdCbNt7pJ; ALF=1576858280; SCF=AlgBPenUgfLvd61J8Zao5kdm0McW93cui6HTaoZmMZT-qsgnucb43RcRaSnoBxRC7UPBouIMWQ0gkBdWSGToRYM.; _T_WM=80332013453; SUB=_2A25w0RX4DeRhGeFP6VUQ-S_PzziIHXVQPbuwrDV6PUNbktAKLW2nkW1NQT9JhnVa60CqM14RP1e61Wc27fHiS9VZ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhQ2hKYIq2EYZUWB4Ymq1iP5JpX5KMhUgL.FoMpeoMp1K20ShB2dJLoI0eLxKBLB.2L12eLxKML1-2L1hBLxKBLBo.L1-BLxKqLB-eLBK2LxKqL1KqLBo.Eeh5NeK5t; WEIBOCN_FROM=1110006030; SSOLoginState=1574266280; MLOGIN=1; XSRF-TOKEN=6f8f7d; M_WEIBOCN_PARAMS=uicode%3D20000061%26fid%3D4440720863417426%26oid%3D4440720863417426'
    while i <= 2000:
        fp = open(os.path.join(product_dir, "content.txt"), "a", encoding='utf-8')

        try:
            print(max_id)
            url = urls + "&max_id=" +max_id+'&max_id_type=0'
            if len(max_id)==0 :
                url = urls+'&max_id_type=0'
            print(url)
            resp = session.get(url)
            resp.encoding = resp.apparent_encoding
            print(resp.text)
            comment_json = json.loads(resp.text)
            print(comment_json)
            comments_list = comment_json["data"]["data"]
            max_id = str(comment_json["data"]["max_id"])
            print(max_id)
            print(comments_list)
            for commment_item in comments_list:
                username = commment_item["user"]["screen_name"]
                comment = commment_item["text"]
                print(comment)
                label_filter = re.compile(r'</?\w+[^>]*>', re.S)
                comment = re.sub(label_filter, '', comment)
                fp.write(str(num) + ':' + comment + '\n')
                num += 1
        except Exception as e:
            print(e)
            print(str(i) + "遇到异常")
            continue
        i += 1
        fp.close()



getCommodityComments()

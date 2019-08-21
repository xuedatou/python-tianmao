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
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import os
import requests
import json

pwd = os.getcwd()

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


def getCommodityComments(url):
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=599318528552&spuId=1145879902&sellerId=2002722824&order=3&currentPage=1'
    if url[url.find('itemId=') + 14] != '&':
        id = url[url.find('itemId=') + 3:url.find('itemId=') + 15]
    else:
        id = url[url.find('itemId=') + 3:url.find('itemId=') + 14]

    product_dir = os.path.join(pwd, id)
    print(product_dir)
    if not os.path.exists(product_dir):
        os.mkdir(product_dir)


    session = requests.session()
    session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    session.headers['cookie'] = ''
    session.headers['upgrade-insecure-requests'] = '1'
    session.headers['Referer'] = 'https://detail.tmall.com/item.htm?spm=a221t.1476805.6299412507.50.18836769FO7H38&id=599318528552&scm=1003.1.03175.ITEM_599318528552_428331&acm=03175.1003.1.428331&uuid=7NeaqH15&pos=5&crid=37'
    session.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    res = session.get(url)
    jc = json.loads(res.text.strip().strip('jsonp128').strip('()'))
    print(jc)
    max = jc['rateDetail']['rateCount']['total']
    users = []
    comments = []
    count = 0
    page = 1
    print('该商品共有评论' + str(max) + '条,具体如下: loading...')
    while count < max:
        res = session.get(url[:-1] + str(page))
        page = page + 1
        jc = json.loads(res.text.strip().strip('jsonp128').strip('()'))
        jc = jc['rateDetail']['rateList']
        print(jc)
        for j in jc:
            if j['rateContent'] not in filterList:
                if not os.path.exists(product_dir):
                    os.mkdir(product_dir)
                with open(os.path.join(product_dir, "content.txt"), "a", encoding='gb18030') as f:
                    f.write(str(count + 1) + ':' + j['rateContent'] + '\n')

                if len(j['pics']) > 0:
                    num = 0
                    for img in j['pics']:
                        try:
                            imgurl = 'http:' + str(img)
                            getimge(imgurl, os.path.join(product_dir, str(count + 1) + '_' + str(num + 1) + '.jpg'))
                            num = num + 1
                        except:
                            continue





            users.append(j['displayUserNick'])
            comments.append(j['rateContent'])
            print(count + 1, '>>', users[count], '\n        ', comments[count])
            count = count + 1


getCommodityComments(
    'https://detail.tmall.com/item.htm?spm=a230r.1.14.396.40287295Ob25Ig&id=572691274585')

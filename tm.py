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
    if url[url.find('id=') + 14] != '&':
        id = url[url.find('id=') + 3:url.find('id=') + 15]
    else:
        id = url[url.find('id=') + 3:url.find('id=') + 14]

    product_dir = os.path.join(pwd, id)
    print(product_dir)
    if not os.path.exists(product_dir):
        os.mkdir(product_dir)

    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId='+id+'&spuId=997779061&sellerId=3434140772&order=3&picture=1&currentPage=1'
    session = requests.session()
    session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    session.headers['cookie'] = 'cna=EMqUFNOc8QoCAXzKqHpcLCiW; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; enc=qnf6W0IsyrPvOUZYJKjFHfYnvcJLSo%2Fiwz5t3YS%2FPDu3IirKSjJeUOc2jhDscG%2BIsQ27PMTNzfrjp3uVGwkA9A%3D%3D; lid=xuexindong512; _m_h5_tk=ea5da97ad21862667b096b2cd6c79caf_1550548890552; _m_h5_tk_enc=a24f17f90604ffff16c3474d9847f6a7; uss=""; hng=CN%7Czh-CN%7CCNY%7C156; t=3d167db83257dbfce2ea2a3eef4f9661; uc3=vt3=F8dByEzfjpnLBuWQpyE%3D&id2=UoYWPA6Oi4Vh2g%3D%3D&nk2=G5Ve6f57q2lJEIfIrw%3D%3D&lg2=URm48syIIVrSKA%3D%3D; tracknick=xuexindong512; lgc=xuexindong512; _tb_token_=3ef9538f865e; cookie2=14041820d15a42c648bad4ceeec7774e; l=bBTo4HT4vPUOWJvvBOfNVuI-CC_tiIRb8sPzw4Nw9ICPO_5w5FWCWZZEit8eC3GVa6EyR3o7dQR0B4Ys7yUIh; isg=BICAdM6kyC3bwrRJmbmGWQY4UQ6SoX3cXpUNZ_oRyRssdSGfoht8Y4oDjZ0QRRyr'
    session.headers['upgrade-insecure-requests'] = '1'
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
                        imgurl = 'http:' + str(img)
                        getimge(imgurl, os.path.join(product_dir, str(count + 1) + '_' + str(num + 1) + '.jpg'))
                        num = num + 1

            users.append(j['displayUserNick'])
            comments.append(j['rateContent'])
            print(count + 1, '>>', users[count], '\n        ', comments[count])
            count = count + 1


getCommodityComments(
    'https://detail.tmall.com/item.htm?spm=a230r.1.14.396.40287295Ob25Ig&id=572691274585')

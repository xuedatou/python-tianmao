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


def getCommodityComments(url):
    itemId = '562308467814'
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=' + itemId + '&spuId=1145879902&sellerId=2002722824&order=3&picture=1&currentPage=1'
    if url[url.find('itemId=') + 14] != '&':
        id = url[url.find('itemId=') + 3:url.find('itemId=') + 15]
    else:
        id = url[url.find('itemId=') + 3:url.find('itemId=') + 14]

    product_dir = os.path.join(pwd, id)
    print(product_dir)
    if not os.path.exists(product_dir):
        os.mkdir(product_dir)


    session = requests.session()
    session.headers['user-agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Mobile Safari/537.36'
    session.headers['cookie'] = 'cna=N1IVFV5q/0gCAd5VatpSBfAy; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; lid=xuexindong512; enc=cRxD%2FuWRsGVP3EzrwedV%2FInQm44KLmHNE%2FV5M9%2B7cdLiohvYoFNyfiu8%2BrLBGqY6tgnuTiPTx7%2FQZ6YN954%2FkQ%3D%3D; uc1=cookie14=UoTbmVRweSSVPA%3D%3D; t=694f001ec72b65ac70a4c805df354087; tracknick=xuexindong512; _tb_token_=Nr1ilHMGzDHBtyZoacQi; cookie2=56001efdfcf755790240bee4551ad65b; _m_h5_tk=2f7644472f0d07269ade6514a1c0094c_1574445507094; _m_h5_tk_enc=e1ad236784fba5b9122e14af48ed75e3; l=dBP0d-igvoJl1ViLBOCwCuI8LG_9LIRfguPRwCqMi_5N8_LCte_OkdpGMEp6cjWcTqYB40wBaIvtfFiaJy_bXMJA-9cdvdnDBef..; isg=BHt7CbXrolp6NZ-nTBOmhT6JCl8leI7Zn02mDW04VnqyzJqu9aEBIlZK4ionbOfK'
    session.headers['upgrade-insecure-requests'] = '1'
    session.headers['Referer'] = 'https://detail.m.tmall.com/item.htm?id=603859730042&abtest=28&rn=ab0de6c20830b4fc2de0ac787cc459ec&sid=56001efdfcf755790240bee4551ad65b'
    session.headers['accept'] = '*/*'
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
        print(jc)
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
                videoU = j['videoList']
                print("mp4: "+str(videoU))
                if len(videoU) > 0:
                    print("mp4: ")
                    try:
                        videourl = 'http:' + str(j['videoList'][0]["cloudVideoUrl"])
                        print("mp4:  "+videourl)

                        getimge(videourl, os.path.join(product_dir, str(count + 1) + '_' + str(1) + '.mp4'))

                    except:
                         continue





            users.append(j['displayUserNick'])
            comments.append(j['rateContent'])
            print(count + 1, '>>', users[count], '\n        ', comments[count])
            count = count + 1


getCommodityComments(
    'https://detail.tmall.com/item.htm?spm=a230r.1.14.396.40287295Ob25Ig&id=572691274585')

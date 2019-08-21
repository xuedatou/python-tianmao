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

    url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId='+id+'&rateType=3&currentPageNum=1'
    session = requests.session()
    session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    session.headers['cookie'] = 't=3d167db83257dbfce2ea2a3eef4f9661; cna=EMqUFNOc8QoCAXzKqHpcLCiW; thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; enc=XzKJXnbxrqUiblthrU%2FUZ7wRbRbKDyYfchg%2F%2BMlKRnEfyKDdPuedK2%2F%2BJOfK6%2FLWrzvpTPVzHG84pLOKmEMo3A%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=1679d1bb25224a-0291ea7161bb99-b78173e-240000-1679d1bb253790; cookie2=16deea3cd902aadbbc72495f7d7db326; v=0; _tb_token_=56e1e6003e9e6; _m_h5_tk=703cd31b5f106872fcbcc1a0f48be152_1550486296287; _m_h5_tk_enc=58c30401d94792ef297788498750018c; unb=1781022371; sg=210; _l_g_=Ug%3D%3D; skt=f939b695397c1679; cookie1=VWZ3cOA6VY3E2v3iUB%2FIWxSSpnHxgwZd5gVgcjrhXV4%3D; csg=f11b93b6; uc3=vt3=F8dByEze47UaB2fadOM%3D&id2=UoYWPA6Oi4Vh2g%3D%3D&nk2=G5Ve6f57q2lJEIfIrw%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D; existShop=MTU1MDQ3NzYxNQ%3D%3D; tracknick=xuexindong512; lgc=xuexindong512; _cc_=UIHiLt3xSw%3D%3D; dnk=xuexindong512; _nk_=xuexindong512; cookie17=UoYWPA6Oi4Vh2g%3D%3D; tg=0; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=URm48syIYB3rzvI4Dim4&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTZ5OSr7O4xKw%3D%3D&tag=8&lng=zh_CN; mt=ci=19_1; x5sec=7b22726174656d616e616765723b32223a226365386662613132636262636236333462396466626266313733666432343135434a505771654d46454a666e775076656a3776686d514561444445334f4445774d6a497a4e7a45374d513d3d227d; whl=-1%260%260%261550478197003; l=bBThf6lgvPUO618LBOCiVuI-CC_OGIRfguPRw5SMi_5Qt_86Z3bOlllXWEJ6Vj5P9XLB40wBaI2t1FNa-ykf.; isg=BIWF-yTddW6Y01FVK4u7N8VPlMF_6iDb246omIfqLLzLHqeQT5A_pT-8KAJNXlGM'
    res = session.get(url)
    print(url)
    print(res)
    jc = json.loads(res.text.strip().strip('()'))
    print(jc)
    max = jc['total']
    users = []
    comments = []
    count = 0
    page = 1
    print('该商品共有评论' + str(max) + '条,具体如下: loading...')
    while count < max:
        res = session.get(url[:-1] + str(page))
        page = page + 1
        jc = json.loads(res.text.strip().strip('()'))
        jc = jc['comments']
        for j in jc:
            if j['content'] not in filterList:
                if not os.path.exists(product_dir):
                    os.mkdir(product_dir)
                with open(os.path.join(product_dir, "content.txt"), "a", encoding='gb18030') as f:
                    f.write(str(count + 1) + ':' + j['content'] + '\n')

                if len(j['photos']) > 0:
                    num = 0
                    for img in j['photos']:
                        imgurl = 'http:' + str(img['url']).replace("_400x400.jpg", "")
                        getimge(imgurl, os.path.join(product_dir, str(count + 1) + '_' + str(num + 1) + '.jpg'))
                        num = num + 1

            users.append(j['user']['nick'])
            comments.append(j['content'])
            print(count + 1, '>>', users[count], '\n        ', comments[count])
            count = count + 1


getCommodityComments(
    'https://item.taobao.com/item.htm?spm=a230r.1.14.146.75f37023RZA9MA&id=567099726475')

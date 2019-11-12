"""
    爬取微博评论区图片
    url：
    https://weibo.com/1595142854/Hswee0sdj?refer_flag=1001030103_&type=comment

"""
import csv
import json
from urllib.parse import parse_qs

import requests
from lxml import etree
import time
import random


def write_comment(string):
    with open('./pinglun.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(string)


class WeiboSpider():
    def __init__(self):
        self.page = 1
        self.headers = {
            'Cookie': 'SINAGLOBAL=3467122848249.176.1571052407611; un=15612317021; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBZxey-YvQUw0bs-GriblC5JpX5KMhUgL.FoqXS0.4S0-7ShB2dJLoIEXLxK-L12BL122LxKML1KeLBoqLxKnL1h5L1h2LxK-L12qLB-qLxKBLBo.L1K5t; UOR=,,login.sina.com.cn; ULV=1572600405887:5:3:3:6243056033503.578.1572600405869:1572599839464; ALF=1604403071; SSOLoginState=1572867072; SCF=Al2RMMOB2j_O2Oa3jsvsSG4cUZoB9RIALeZc7GXpIUVbyO0PA94yU5sCMx6EOe3QZ8jZ2-1rzUI-hK0cF--9S2s.; SUB=_2A25wxHxQDeRhGeBK7FsY9yvMzziIHXVTsOqYrDV8PUNbmtANLVPzkW9NR5L6XkGtuoDZLGjD44BotUcSrJsij5xr; SUHB=00xp-zxvLpka4s; YF-Page-G0=96c3bfa80dc53c34a567607076bb434e|1572867073|1572867070; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; YF-V5-G0=b1b8bc404aec69668ba2d36ae39dd980',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.params = {
            'ajwvr': '6',
            'page': self.page,
            'id': '4367970740108457',
            'from': 'singleWeiBo',
            'root_comment_max_id': '',
        }
        self.url = 'https://weibo.com/aj/v6/comment/big'
        self.comment_id = 0

    def get_page(self):
        resp = requests.get(self.url, params=self.params, headers=self.headers)
        resp = json.loads(resp.text)
        if resp['code'] == '100000':
            html = resp['data']['html']
            html = etree.HTML(html)

            # 获取该页面的root_comment_max_id，为下次请求提供参数
            max_id_json = html.xpath('//div[@node-type="comment_loading"]/@action-data')[0]
            node_params = parse_qs(max_id_json)

            # max_id
            max_id = node_params['root_comment_max_id'][0]
            self.params['root_comment_max_id'] = max_id
            # 获取每条动态id图片
            data = html.xpath('//div[@node-type="root_comment"]')
            # 遍历每一条东岱
            for i in data:
                # 评论人昵称
                nick_name = i.xpath('.//div[@class="WB_text"]/a/text()')[0]
                # 评论内容。
                wb_text = i.xpath('.//div[@class="WB_text"][1]/text()')
                # 简单的清洗，出去空格和换行符
                string = ''.join(wb_text).strip().replace('\n', '')
                # 封装了一个方法，将留言信息写入文本
                write_comment(string)
                # 评论id , 用于获取评论内容
                self.comment_id = i.xpath('./@comment_id')[0]
                # 评论的图片地址

                pic_url = i.xpath('/html/body/div/div/div/div[2]/div[2]/div/ul/li/img/@src')
                for i in pic_url:
                    pic_url = 'https:' + i if i else ''
                    # 封装的下载图片方法
                    self.download_pic(pic_url, str(time.time()))
            self.get_child_comment(self.comment_id)

    def get_child_comment(self, root_comment_id):
        self.params['root_comment_id'] = root_comment_id
        resp = requests.get(self.url, params=self.params, headers=self.headers)
        resp = resp.json()
        if resp['code'] == '100000':
            html = resp['data']['html']
            from lxml import etree
            html = etree.HTML(html)
            # 每个子评论的节点
            data = html.xpath('//div[@class="WB_text"]')
            for i in data:
                nick_name = ''.join(i.xpath('./a/text()')).strip().replace('\n', '')
                comment = ''.join(i.xpath('./text()')).strip().replace('\n', '')
                write_comment(comment)
                # 获取图片对应的html节点
                pic = i.xpath('.//a[@action-type="widget_photoview"]/@action-data')
                pic = pic[0] if pic else ''
                if pic:
                    # 拼接另外两个必要参数
                    pic = pic + 'ajwvr=6&uid=5648894345'
                    # 构造出一个完整的图片url
                    url = 'https://weibo.com/aj/photo/popview?' + pic
                    resp = requests.get(url, headers=self.headers)
                    print(resp)
                    resp = resp.json()
                    if resp.get('code') == '100000':
                        # 从突然url中，第一个就是评论中的图
                        url = resp['data']['pic_list'][0]['clear_picSrc']
                        # 下载图片
                        self.download_pic(url, nick_name)

    def download_pic(self, pic_url, nick_name):
        html = requests.get(pic_url).content
        with open("./kk/" + nick_name + ".jpg", 'wb') as f:
            f.write(html)
            print('%s爬取成功' % nick_name)


if __name__ == '__main__':
    Weibo = WeiboSpider()
    i = 0
    while i < 5:
        i += 1
        Weibo.get_page()

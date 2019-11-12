"""
@Time    : 2019/11/5 0005 10:22
@Author  : Linyue
@Email   : l_inyue@163.com
@File    : 大V评论爬取.py
@name    ：https://weibo.com/1595142854/Hswee0sdj?refer_flag=1001030103_&type=comment
https://wx3.sinaimg.cn/bmiddle/dc46fb4egy1g2ojh1pon5j20rs32xk1x.jpg
//wx3.sinaimg.cn/thumb180/dc46fb4egy1g2ojh1pon5j20rs32xk1x.jpg
"""
import os
import re
import sys
import time

import requests
from lxml import etree


class Dv_Spider(object):
    def __init__(self):
        self.headers = {
            'Cookie': 'SINAGLOBAL=3467122848249.176.1571052407611; un=15612317021; wvr=6; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; ALF=1604456347; SSOLoginState=1572920348; SCF=Al2RMMOB2j_O2Oa3jsvsSG4cUZoB9RIALeZc7GXpIUVbcx6o2FrAmA0vIh-N_VZ-G0SfidBEaYOuZ9_trbR6Ig4.; SUB=_2A25wxKxNDeRhGeBK7FsY9yvMzziIHXVTs5qFrDV8PUNbmtANLW_NkW9NR5L6XlMZXLzS6VRSq4YmBnbENqjcfaSV; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBZxey-YvQUw0bs-GriblC5JpX5KzhUgL.FoqXS0.4S0-7ShB2dJLoIEXLxK-L12BL122LxKML1KeLBoqLxKnL1h5L1h2LxK-L12qLB-qLxKBLBo.L1K5t; SUHB=0JvgDE3IkaQJKK; YF-V5-G0=bae6287b9457a76192e7de61c8d66c9d; wb_timefeed_6479975044=1; _s_tentry=login.sina.com.cn; UOR=,,www.baidu.com; Apache=3180558112077.9204.1572920360798; ULV=1572920360805:7:5:2:3180558112077.9204.1572920360798:1572867081124; wb_view_log_6479975044=1536*8641.25; webim_unReadCount=%7B%22time%22%3A1572923637042%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A39%2C%22msgbox%22%3A0%7D; YF-Page-G0=7f483edf167a381b771295af62b14a27|1572923635|1572923635',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.params = {
            'ajwvr': '6',
            'id': '4367970740108457',
            'from': 'singleWeiBo',
            'root_comment_max_id': '',
        }
        self.url = 'https://weibo.com/aj/v6/comment/big'

    def get_html(self, url):
        html = requests.get(url, params=self.params, headers=self.headers).json()
        return html['data']['html']

    def parse_html(self):
        re_ = '.*?root_comment_max_id=(.*?)&.*?page=(.*?)&filter=hot&sum_comment_number=(.*?)&.*?">'
        html = self.get_html(self.url)
        pattern = re.compile(re_, re.S)  # re.I 表示忽略大小写
        next_url_data = pattern.findall(html)
        try:
            self.params['root_comment_max_id'] = next_url_data[0][0]
            self.params["page"] = next_url_data[0][1]
            self.params["sum_comment_number"] = next_url_data[0][2]
            self.params["__rnd"] = str(time.time())[:14].replace('.', '')
        except:
            sys.exit()
        parse = etree.HTML(html)
        img_list = parse.xpath("//ul[@class='WB_media_a WB_media_a_m1 clearfix']/li/img/@src")
        for img in img_list:
            img_url = "https:" + img
            img_url = img_url.replace('thumb180', 'bmiddle')
            img_name = img_url.split('/')[-1]
            img_ = requests.get(img_url, headers=self.headers)
            with open('./kk/' + img_name, 'wb') as f:
                f.write(img_.content)
        print('第' + self.params["page"] + "页爬取完成")


if __name__ == '__main__':
    Dv = Dv_Spider()
    while True:
        Dv.parse_html()
    else:
        print("爬取完成")

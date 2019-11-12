"""
微博个人信息爬取

//*[@id="Pl_Official_MyProfileFeed__20"]/div/div/div/div/div/div/ul/li/img

高清：
https://wx3.sinaimg.cn/mw690/006SnOSwly1g6sa22u3vaj32ds1sgb29.jpg
缩小：
https://wx1.sinaimg.cn/orj360/006SnOSwly1g5ycrw2lr6j32o82o81kx.jpg
"""
import random
import time

import requests
from lxml import etree
from fake_useragent import UserAgent

class Weibospider():
    def __init__(self):
        self.url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&from=myfollow_all&is_all=1&pagebar={}&pl_name=Pl_Official_MyProfileFeed__20&id=1005056300396260&script_uri=/u/6300396260&feed_type=0&page=1&pre_page=1&domain_op=100505&__rnd=1571053992630'
        self.header = {
            'User-Agent': UserAgent().ie,
            'Cookie': 'SINAGLOBAL=3467122848249.176.1571052407611; un=15188778855; Ugrow-G0=e1a5a1aae05361d646241e28c550f987; ALF=1602635760; SSOLoginState=1571099761; SCF=Al2RMMOB2j_O2Oa3jsvsSG4cUZoB9RIALeZc7GXpIUVbSZHbnYJbufRV_nd0f4OZF-h4metinMcieygAahjT0lw.; SUB=_2A25woWQhDeRhGeNI6FUV9yfJyzSIHXVT19LprDV8PUNbmtBeLXPjkW9NSGwCrI6fcCZUbMcQtMoaottlH2TUnSRl; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5xPO4_xFD2f8s925eBhoy15JpX5KzhUgL.Fo-ce0MXS0.fehn2dJLoI7yFdGHL9-p0M7tt; SUHB=0P1MtOq3WSwk1j; wvr=6; YF-V5-G0=4e19e5a0c5563f06026c6591dbc8029f; wb_view_log_5637479508=1536*8641.25; YF-Page-G0=aedd5f0bc89f36e476d1ce3081879a4e|1571099766|1571099766; _s_tentry=login.sina.com.cn; UOR=,,www.baidu.com; Apache=8864762472146.115.1571095993819; ULV=1571095993871:2:2:2:8864762472146.115.1571095993819:1571052407620; webim_unReadCount=%7B%22time%22%3A1571095994394%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D',
            'Host': 'weibo.com',
            'Referer': 'https://weibo.com/u/6300396260?from=myfollow_all&is_all=1'

        }

    def get_html(self, page):
        html = requests.get(self.url.format(page), headers=self.header)

        return html

    def parse_html(self):
        for i in range(0, 2):
            print('*' * 100)
            json = self.get_html(i).json()
            html = json['data']
            parse = etree.HTML(html)
            # print(html)
            img_list = parse.xpath('//div/div/div/div/div/ul/li/img/@src')
            img_list = list(map(lambda x: x.replace("orj360", 'mw690'), img_list))
            img_list = list(map(lambda x: x.replace("thumb150", 'mw690'), img_list))
            for img in img_list:
                print('=' * 50)
                new_url = 'https:' + img
                print(new_url)
                time.sleep(random.randint(1,3))
                img_url = requests.get(new_url).content
                print(img_url)
                with open(new_url[-36:], 'wb') as f:
                    f.write(img_url)


if __name__ == '__main__':
    weibo = Weibospider()
    weibo.parse_html()

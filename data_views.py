"""
   名称：爬虫武器库
        
   简介：将爬取出来的数据进行可视化展示的类
        1.
"""

from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Scatter
from pyecharts import Gauge
from pyecharts import Funnel
from pyecharts import Geo
from pyecharts import WordCloud
from pyecharts import Line, Grid

from pyecharts import Page


class SpiderViews(object):
    def __init__(self):
        self.page = Page()

    # 柱状图
    def bar(self, title=None, attr=None, b1name=None, b2name=None, b1=None, b2=None):
        """
        柱状图
            title:数据可视化的标题(字符串)
            attr:名称列表[列表]
            b1name:图表上b1数据对应的名称
            b2name:图表上b2数据对应的名称
        :param b1: 名称attr列表对应的数据[列表]
        :param b2: 名称attr列表对应的数据[列表]
        :return: 生成一个柱状图
        """
        b1 = b1
        b2 = b2
        bar = Bar(title)
        bar.add(b1name, attr, b1, is_stack=True, is_more_utils=True)  # 显示工具
        bar.add(b2name, attr, b2, is_stack=True)
        # bar.render()
        self.page.add(bar)
        self.page.render()

    # 饼图
    def pie(self, title=None, attr=None, p1=None):
        """
        饼图
        :param title: 数据可视化的标题(字符串)
        :param attr:  attr:名称列表[列表]
        :param p1: 名称attr列表对应的数据[列表]
        :return:生成一个饼图
        """
        p1 = p1
        pie = Pie(title)
        pie.add('', attr, p1, is_label_show=True)
        self.page.add(pie)
        self.page.render()

    # 圆饼图
    def pie2(self, title=None, attr=None, p2=None):
        """
        饼图
        :param title: 数据可视化的标题(字符串)
        :param attr:  名称列表[列表]
        :param p2: 名称attr列表对应的数据[列表]
        :return: 生成一个圆饼图
        """
        p2 = p2
        pie2 = Pie(title, title_pos='center')
        pie2.add('', attr, p2, radius=[40, 75], label_text_color=None, is_label_show=True, legend_orient='vertical',
                 legend_pos='left')
        self.page.add(pie2)
        self.page.render()

    # 散点图
    def scatter(self, title=None, s1name=None, s2name=None, s1=None, s2=None, ):
        """
        散点图
        :param title: 数据可视化的标题(字符串)
        :param s1name: s1标题
        :param s2name: s2标题
        :param s1: s1name对应数据
        :param s2: s2name对应数据
        :return:散点图
        """
        s1 = s1
        s2 = s2
        scatter = Scatter(title)
        scatter.add(s1name, s1, s2)
        scatter.add(s2name, s1[::-1], s2)
        self.page.add(scatter)
        self.page.render()

    # 仪表盘
    def gauge(self, title=None, index=None, accomplish=None, rate=None):
        """
        :param title: 数据可视化的标题(字符串)
        :param index: 业务指标(字符串)
        :param accomplish: 完成率(字符串)
        :param rate: 百分比(int类型)
        :return: 仪表盘
        """
        gauge = Gauge(title)
        gauge.add(index, accomplish, rate)
        self.page.add(gauge)
        self.page.render()

    # 漏斗图
    def funnel(self, title=None, attr=None, value=None, two_title=None):
        """
        漏斗图
        :param title: 数据可视化的标题(字符串)
        :param attr: 名称列表[列表]
        :param value: 名称列表对应数据
        :param two_title: 二级小标题(鼠标悬浮显示小标题)
        :return:漏斗图
        """
        attr2 = attr
        value = value
        funnel = Funnel(title)
        funnel.add(two_title, attr2, value, is_label_show=True, label_pos='inside', label_text_color='#fff')
        self.page.add(funnel)
        self.page.render()

    # 地图
    def geo(self, title=None, data=None):
        """
         地图
        :param title: 数据可视化的标题(字符串)
        :param data: {地名:value}    字典{'宿迁市': 89, '安康市': 46, '佳木斯市': 50,}
        :return:地图
        """
        data = data
        geo = Geo(title, 'data from AQI', title_color='#fff', \
                  title_pos='center', width=1200, height=600, background_color='#404a59')
        attr, value = geo.cast(data)  # data is not.0
        geo.add('', attr, value, visual_range=[0, 200], visual_text_color='#fff', symbol_size=15, is_visualmap=True,
                is_piecewise=True, visual_split_number=6)
        self.page.add(geo)
        self.page.render()

    # 词云图
    def wordcloud(self, name=None, values=None, width=1200, height=620):
        """
        词云图
        :param name: 词云列表
        :param values: 词云列表权重值,与词云列表对应
        :param width: 宽度默认1200
        :param height: 高度默认600
        :return:词云图
        """
        name = name
        value = values
        wordcloud = WordCloud(width, height)
        wordcloud.add('', name, value, word_size_range=[20, 100])
        self.page.add(wordcloud)
        self.page.render()

    # 组合图
    def grid(self):
        line = Line('折线图', width=1200)
        attr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        line.add('最高气温', attr, [11, 12, 14, 11, 12, 15, 16], mark_point=['max', 'min'], \
                 mark_line=['average'])
        line.add('最低气温', attr, [1, -1, 2, 5, 2, 3, 0], mark_point=['max', 'min'], \
                 mark_line=['average'], legend_pos='20%')
        attr = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        v1 = [11, 12, 14, 10, 11, 10]
        pie = Pie('饼图', title_pos='55%')
        pie.add('', attr, v1, radius=[45, 65], center=[65, 50], legend_pos='80%', \
                legend_orient='vertical')
        grid = Grid()
        grid.add(line, grid_right='55%')
        grid.add(pie, grid_left='60%')
        # grid.render()

# encoding=utf-8
import re
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import InformationItem
import os
from os import path
import urllib.request

class Spider(CrawlSpider):
    name = "sinaSpider"
    host = "https://weibo.com"
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    LOG_FILE = logs_path + 'log'
    custom_settings = {
        'LOG_FILE': logs_path + 'log',
    }

    start_urls = [
        5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 5780802073, 2159807003,
        1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
        2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    ]
    scrawl_ID = set(start_urls)  # 记录待爬的微博ID
    finish_ID = set()  # 记录已爬的微博ID

    def start_requests(self):
        while self.scrawl_ID.__len__():
            ID = self.scrawl_ID.pop()
            self.finish_ID.add(ID)  # 加入已爬队列
            ID = str(ID)
            url_follows = "https://weibo.com/%s/follow" % ID
            yield Request(url=url_follows, callback=self.parse3)  # 去爬关注人

    def parse3(self, response):
        item = InformationItem()
        html = response.text
        text2 = html.split("<script>FM.view")
        for index in range(len(text2)):
            follow_tab = text2[index]
            if "followTab.index" in follow_tab:
                sf = follow_tab.replace("\\r", "").replace("\\t", "").replace("\\n", "").replace("\\", "")
                follw_list = Selector(text=sf).xpath(u"//ul[@class='follow_list']/li[@class='follow_item S_line2']").extract()
                for elem in follw_list:
                    elem_id = re.findall('uid=(\d+)', elem)
                    if elem_id:  #将关注人的id加入未爬列表
                        ID = int(elem_id[0])
                        if ID not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
                            self.scrawl_ID.add(ID)
                    item["_id"] = ID
                    Pic_Url = Selector(text=str(elem)).xpath("//dt[@class='mod_pic']/a/img/@src").extract()
                    if len(Pic_Url) == 1:
                        item["Pic_Url"] = str(Pic_Url[0])
                    else:
                        item["Pic_Url"] = ""
                    NickName = Selector(text=elem).xpath(u"//div[@class='info_name W_fb W_f14']/a[@class='S_txt1']/text()").extract()
                    if len(NickName) == 1:
                        item["NickName"] =str(NickName[0])
                    else:
                        item["NickName"] = ""
                    gender_str = Selector(text=elem).xpath(u"//div[@class='info_name W_fb W_f14']").extract()
                    if "icon_male" in str(gender_str):
                        item["Gender"] = "男"
                    elif "icon_female" in str(gender_str):
                        item["Gender"] = "女"
                    else:
                        item["Gender"] = ""
                    info_connect = Selector(text=elem).xpath("//div[@class='info_connect']/span/em/a/text()").extract()
                    if 3 == len(info_connect):
                        item["Num_Follows"] = info_connect[0]
                        item["Num_Fans"] = info_connect[1]
                        item["Num_Tweets"] = info_connect[2]
                    else:
                        item["Num_Follows"] = 0
                        item["Num_Fans"] = 0
                        item["Num_Tweets"] = 0
                    Signature = Selector(text=elem).xpath("//div[@class='info_intro']/span/text()").extract()
                    if len(Signature) == 1:
                        item["Signature"] = str(Signature[0])
                    else:
                        item["Signature"] = ""
                    Info_Add = Selector(text=elem).xpath("//div[@class='info_add']/span/text()").extract()
                    if len(Info_Add)==1:
                        item["Info_Add"] = str(Info_Add[0])
                    else:
                        item["Info_Add"] = ""
                    yield item
                url_next = Selector(text=sf).xpath(u"//div[@class='WB_cardpage S_line1']/div[@class='W_pages']/a[last()]/@href").extract()
                if url_next:
                    yield Request(url=self.host + url_next[0], callback=self.parse3)


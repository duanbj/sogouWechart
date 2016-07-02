#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from sogouWechart.items import WechartAccount
import json
class SogouWechartSpider(BaseSpider):
    name = 'sogou_wehchart'
    allowed_domains = ["weixin.sogou.com", "mp.weixin.qq.com"]
    start_key = ['python']
    start_urls = []

    def __init__(self):
        fileObj = open('F:/scrapy/it_key.json')
        str = fileObj.read()
        keys = json.loads(str)
        for key in keys:
            self.start_key.append(key['name'])
            for c in key['children']:
                self.start_key.append(c['name'])
        for key in self.start_key:
            for i in range(1, 10):
                url = 'http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&_sug_=n&_sug_type_=page=%s' % (key, i)
                self.start_urls.append(url)

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@id="main"]/div/div[2]/div/div')
        for l in links:
            link = ''.join(l.xpath('div[2]/h4/a/@href').extract())
            yield Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        item = WechartAccount()
        sel = Selector(response)
        user_name = sel.re('<span class="profile_meta_value">([^<]*)</span>')
        nickname = sel.re('var nickname = "([^"]*)";')
        image_url = sel.re('hd_head_img : "([^"]*)"')
        item['nickname'] = ''.join(nickname)
        item['user_name'] = user_name[0]
        item['image_url'] = ''.join(image_url)
        return item





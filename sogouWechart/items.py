# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class WechartAricle(Item):

    title = Field()
    link = Field()
    nickname = Field()
    user_name = Field()

class WechartAccount(Item):

    nickname = Field()
    user_name = Field()
    image_url = Field()
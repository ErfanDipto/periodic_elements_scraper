# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


class PelemsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    symbol = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
        )
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    anum = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, int),
        output_processor=TakeFirst()
    )
    amass = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, float),
        output_processor=TakeFirst()
    )
    cgrp = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )

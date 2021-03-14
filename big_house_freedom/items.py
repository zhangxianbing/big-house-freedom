# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Join


def get_number(values: list):
    for value in values:
        if value is not None and value != "":
            return float(value)


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    community = scrapy.Field(output_processor=Join("- "))
    address = scrapy.Field()
    follow_info = scrapy.Field()
    tag = scrapy.Field()
    total_price = scrapy.Field(output_processor=get_number)
    unit_price = scrapy.Field(output_processor=get_number)
    house_type = scrapy.Field(output_processor=TakeFirst())
    area = scrapy.Field(output_processor=get_number)
    orientation = scrapy.Field(output_processor=TakeFirst())
    decoration = scrapy.Field(output_processor=TakeFirst())
    floor = scrapy.Field(output_processor=TakeFirst())
    building_age = scrapy.Field(output_processor=TakeFirst())
    building_type = scrapy.Field(output_processor=TakeFirst())
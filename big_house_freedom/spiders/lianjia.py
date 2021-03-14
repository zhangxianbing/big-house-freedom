import re
from itemloaders.processors import TakeFirst
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from big_house_freedom.items import HouseItem

url = "https://bj.lianjia.com/ershoufang/pg{page}l2bp0ep420rs武夷花园"


class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    i = 1
    start_urls = [url.format(page=i)]

    def parse(self, response: HtmlResponse):
        sells = response.xpath('//*[@class="info clear"]')
        if sells:
            title = response.xpath("/html/head/title/text()").get()
            print(title)
            self.i += 1
            yield scrapy.Request(url.format(page=self.i), self.parse)

        for sell in sells:
            # print(sell.get())
            loader = ItemLoader(item=HouseItem(), selector=sell)
            loader.add_xpath("id", 'div[@class="title"]/a/@data-housecode')
            loader.add_xpath("url", 'div[@class="title"]/a/@href')
            loader.add_xpath("title", 'div[@class="title"]/a/text()')
            loader.add_xpath("community", 'div[@class="flood"]/div/a/text()')
            # loader.add_xpath("address", 'div[@class="address"]/div/text()')
            loader.add_xpath("follow_info", 'div[@class="followInfo"]/div/text()')
            loader.add_xpath("tag", 'div[@class="tag"]/span/text()')
            loader.add_xpath(
                "total_price",
                'div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()',
            )
            loader.add_xpath(
                "unit_price",
                'div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price',
            )
            address = loader.get_xpath(
                'div[@class="address"]/div/text()', TakeFirst()
            ).split("|")

            for v in map(str.strip, address):
                if v in ("板楼", "塔楼", "板塔结合"):
                    loader.add_value("building_type", v)
                elif any(k in v for k in ("室", "厅", "房间", "卫")):
                    loader.add_value("house_type", v)
                elif "平米" in v:
                    loader.add_value("area", float(v.rstrip("平米")))
                elif any(k in v for k in ("东", "南", "西", "北")):
                    loader.add_value("orientation", v)
                elif "层" in v:
                    loader.add_value("floor", v)
                elif "装" in v:
                    loader.add_value("decoration", v)
                elif "建" in v:
                    loader.add_value("building_age", v)

            yield loader.load_item()

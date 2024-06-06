import scrapy
import items
from scrapy.http import HtmlResponse
from items import UnsplashItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from itemloaders.processors import TakeFirst, MapCompose, Compose


class UnsplashImgSpider(scrapy.Spider):
    name = 'unsplash_img'
    allowed_domains = ['unsplash.com']
    # start_urls = ['https://unsplash.com/s/photos/cosmos']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://unsplash.com/s/photos/{kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div/a[@class='Prxeh']//@href")
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('discription', '//p[@class="wMjKq N46Vv pvKRl"]/text()')
        loader.add_xpath('photos', "//@srcset")

        yield loader.load_item()
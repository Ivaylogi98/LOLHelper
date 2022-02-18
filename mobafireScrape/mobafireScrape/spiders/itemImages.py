import scrapy

from mobafireScrape.items import ImageItem


class ItemimagesSpider(scrapy.Spider):
    name = 'itemImages'
    allowed_domains = ['leagueoflegends.fandom.com']
    start_urls = ['https://leagueoflegends.fandom.com/wiki/Item_']

    def parse(self, response):
        urls = response.xpath("//div[@id='grid']//img/@data-src").extract()
        print('URLS:', urls)
        return {'image_urls': urls}

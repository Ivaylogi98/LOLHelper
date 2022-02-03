import scrapy


class ItemsscrapeSpider(scrapy.Spider):
    name = 'itemsScrape'
    allowed_domains = ['mobafire.com/league-of-legends/items']
    start_urls = ['http://mobafire.com/league-of-legends/items/']

    def parse(self, response):
        names = []
        for name in response.xpath('//div[@class="comments"]/following-sibling::span/text()').getall():
            if name != "" and name.find("\n") == -1:
                print(name)
                names.append(name)
        
        with open('assets/itemNames.txt', 'w') as f:
            f.write(",".join(names))
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChampionguidescrapeSpider(CrawlSpider):
    name = 'championGuideScrape'
    allowed_domains = ['www.mobafire.com']
    start_urls = ['https://www.mobafire.com/league-of-legends/browse']

    rules = (
        Rule(LinkExtractor(allow=r'&page=[0-9]+'), callback='parse_page', follow=True),
    )


    def parse_page(self, response):
        guide_url = response.xpath("//div[@class='mf-listings']//@href").getall()
        print(guide_url)
        for url in guide_url:
            yield scrapy.Request(url=url, callback=self.parse_guide)
        

        # next_page_url = response.xpath('//div[@class="browse-pager__next"]/a/@href').get()
        # return response.follow(next_page_url, self.parse_page)


    def parse_guide(self, response, champion):
        print(response.url)
        # TODO: get the name of the guide
        guide_name = response.xpath('//h1[@class="view-guide__banner__title tablet-up guide-h1"]/span/text()').get()
        champion = response.xpath("//span[@class='mobile-sr']/text()").get()[0]
        guide_text = response.xpath("//div[@class='view-guide__chapters '").getall()

        with open(f'assets/{champion}/guides/{guide_name}', 'w+') as f:
            f.write(guide_text)
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChampionguidesSpider(CrawlSpider):
    name = 'championGuides'
    allowed_domains = ['mobafire.com']
    start_urls = ['https://www.mobafire.com/league-of-legends/browse?page=1']

    # rules = (
    #     Rule(LinkExtractor(allow=r'/browse&page=[0-9]+'), callback='parse_page', follow=True),
    # )

    def parse(self, response):
        print('~~~~ In parse ~~~~')
        guides_urls = response.xpath("//div[@class='mf-listings']//@href").getall()
        print(guides_urls)
        for guide_url in guides_urls:
            yield scrapy.Request(guide_url, callback=self.parse_guide)
        

        next_page_url = response.xpath('//div[@class="browse-pager__next"]/a/@href').get()
        yield scrapy.Request(next_page_url, self.parse)


    def parse_guide(self, response):
        print('~~~~ In parse_guide ~~~~')
        print(response.url)
        # TODO: get the name of the guide
        guide_name = response.xpath('//h1[@class="view-guide__banner__title tablet-up guide-h1"]/span/text()').get()
        champion = response.xpath("//span[@class='mobile-sr']/text()").get()[0]
        guide_text = response.xpath("//div[@class='view-guide__chapters '").getall()

        with open(f'assets/{champion}/guides/{guide_name}', 'w+') as f:
            f.write(guide_text)
import scrapy

class GuidesSpider(scrapy.Spider):
    name = 'guides'
    # allowed_domains = ['www.mobafire.com/league-of-legends']
    start_urls = ['https://www.mobafire.com/league-of-legends/browse?page=1']
    base_url = 'https://www.mobafire.com'
    guide_id = 0
    # rules = (
    #     Rule(LinkExtractor(allow=r'/browse&page=[0-9]+'), callback='parse_page', follow=True),
    # )

    def parse(self, response):
        self.logger.info('~~~~ In parse ~~~~')
        guides_urls = response.xpath("//div[@class='mf-listings']//@href").getall()
        for guide_url in guides_urls:
            if(self.guide_id > 10): return
            yield scrapy.Request(self.base_url + guide_url, callback=self.parse_guide)
        

        next_page_url = response.xpath('//div[@class="browse-pager__next"]/a/@href').get()
        self.logger.info(self.base_url + next_page_url)
        return response.follow(self.base_url + next_page_url, self.parse)


    def parse_guide(self, response):
        self.logger.info(response.url)
        # TODO: get the name of the guide
        guide_name = response.xpath('//h1[@class="view-guide__banner__title tablet-up guide-h1"]/span/text()').get()
        champion = response.xpath("//span[@class='mobile-sr']/text()").get()[0]
        guide_text = response.xpath("//div[@class='view-guide__chapters ']").getall()

        with open(f'assets/guides/{self.guide_id}', 'w+') as f:
            f.write(str(guide_text))
        self.guide_id += 1

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

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
        guide_link = response.xpath("//div[@class='mf-listings']//@href").getall()
        guide_title = response.xpath("//div[@class='mf-listings']//h3/text()").getall()
        guide_title = [title.strip() for title in guide_title if title not in ['', '\n']]
        # print(f"guide_link{len(guide_link)}~", guide_link)
        # print(f"guide_title{len(guide_title)}~", guide_title)
        guides = '\n'.join( ''.join(x) for x in zip(guide_link, guide_title))

        filename = '{champion}guides-names-links.txt'
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(guides)
        self.log(f'Saved file {filename}')
        url = response.xpath('//div[@class="browse-pager__next"]/a/@href').get()
        return response.follow(url, self.parse_page, cb_kwargs=dict(item=item))


    def parse_guide(self, response, champion):
        print(response.url)
        item = {}
        champion = response.xpath("//span[@class='mobile-sr']/text()").get()[0]

        with open('assets/{champion}/guides', 'w') as f:
            f.write(response.url)
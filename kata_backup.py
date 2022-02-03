import scrapy
import json

class MobafireSpider(scrapy.Spider):
    name = 'mobafire_katarina_guides'
    def start_requests(self):
        allowed_domains = ['mobafire.com']
        urls = [
            'https://www.mobafire.com/league-of-legends/browse?champion=Katarina',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        guide_link = response.xpath("//div[@class='mf-listings']//@href").getall()
        guide_title = response.xpath("//div[@class='mf-listings']//h3/text()").getall()

        guide_title = [title.strip() for title in guide_title if title not in ['', '\n']]
        # print(f"guide_link{len(guide_link)}~", guide_link)
        # print(f"guide_title{len(guide_title)}~", guide_title)
        guides = '\n'.join( ''.join(x) for x in zip(guide_link, guide_title))

        filename = 'Katarina-guides-names-links.txt'
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(guides)
        self.log(f'Saved file {filename}')

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

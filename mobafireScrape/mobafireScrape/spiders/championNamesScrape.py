import scrapy


class ChampionnamesscrapeSpider(scrapy.Spider):
    name = 'championNamesScrape'
    allowed_domains = ['mobafire.com/league-of-legends/champions']
    start_urls = ['http://mobafire.com/league-of-legends/champions/']

    def parse(self, response):
        names = []
        for name in response.xpath('//*[@class="champ-list__item__name"]/b/text()').getall():
            names.append(name)
        
        with open('assets/championNames.txt', 'w') as f:
            f.write(",".join(names))
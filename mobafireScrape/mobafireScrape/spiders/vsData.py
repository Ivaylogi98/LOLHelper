from traceback import print_tb
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
from lxml import html
from os.path import isfile

class VsdataSpider(CrawlSpider):
    name = 'vsData'
    allowed_domains = ['https://www.mobachampion.com/counter/']

    def start_requests(self):
        url = 'https://www.mobachampion.com/counter/'

        champions = []
        with open('assets/championNames.txt') as f:
            champions = f.read().split(',')
            
        # monkeyking
        for champion1 in champions[30:]:
            for champion2 in champions:
                # print(url + f'{champion1}-vs-{champion2}')
                if champion1 != champion2:
                    yield scrapy.Request(url=url + f'{champion1}-vs-{champion2}', callback=self.parse_page)


    def parse_page(self, response):
        hero, enemy = map(lambda x: x.strip(), response.xpath('//span[@class="text-indigo-500"]/../text()').getall())
        print(hero + ' VS ' + enemy)

        data_vs_enemy = {}
        data_vs_enemy['summary'] = response.xpath('//h3[contains(text(), "Matchup Summary")]/../following-sibling::span/text()').get().strip()
        data_vs_enemy['tips'] = list(map(lambda x: x.strip(), response.xpath('//h3[contains(text(), "Tips for Playing")]/../following-sibling::span//text()').getall()))
        
        build_elements = {}
        build_elements['starter_items'] = list(map(lambda x: x.strip(), response.xpath("//div[@class='flex flex-col w-52']/div[2]/img/@alt").getall()))
        build_elements['early_items'] = list(map(lambda x: x.strip(), response.xpath("//div[@class='flex flex-col w-52']/div[4]/img/@alt").getall()))
        build_elements['core_items'] = list(map(lambda x: x.strip(), response.xpath("//div[@class='flex flex-col w-52']/div[6]/img/@alt").getall()))
        build_elements['optional_items'] = list(map(lambda x: x.strip(), response.xpath("//div[@class='flex flex-col w-52']/div[7]/img/@alt").getall()))
        build_elements['summoner_spells'] = list(map(lambda x: x.strip(), response.xpath("//div[@class='flex flex-col w-52']/div[8]//img/@alt").getall()))
        build_elements['skill_order'] = list(map(lambda x: x.strip(), response.xpath("//div[@class='v-popper v-popper--theme-tooltip']/div/span/text()").getall()[:3]))
        data_vs_enemy['build'] = build_elements

        print(f"saving data for {hero} vs {enemy}")
        data = {}
        if isfile(f'../lolApp/assets/vsData/{hero}.json'):
            with open(f'../lolApp/assets/vsData/{hero}.json', 'r') as f:
                data = json.load(f)

        with open(f'../lolApp/assets/vsData/{hero}.json', 'w+') as f:
            data[enemy] = data_vs_enemy
            json.dump(data, f)
        print("saved data")
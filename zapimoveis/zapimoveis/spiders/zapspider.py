import re, sys, os
import psycopg2 as pg
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from zapimoveis.items import ZapItem
from scrapy.loader import ItemLoader
import datetime as dt
abspt = os.path.abspath('../../..')
sys.path.append(abspt)
from query import Database


class ZapimoveisSpider(CrawlSpider):

    name = "zapimoveis"
    allowed_domains = ["www.zapimoveis.com.br"]
    start_urls = [
                  "https://www.zapimoveis.com.br/aluguel/apartamentos/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/quitinetes/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/studio/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/casas/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/sobrados/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/cobertura/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/casas-de-condominio/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/casas-de-vila/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/flat/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/loft/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/terrenos-lotes-condominios/sc+florianopolis/",
                  "https://www.zapimoveis.com.br/aluguel/fazendas-sitios-chacaras/sc+florianopolis/"
                  ]

    page_number = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    rules = (
        Rule(LinkExtractor(allow='florianopolis'), callback="parse_item"),
    )

    def parse_item(self, response):

        for card in response.css('.card-container'):
            loader = ItemLoader(item=ZapItem())

            location = card.css('.simple-card__address::text').get(default="None")

            loader.add_value('id', card.css('.card-container').xpath('@data-id').get())
            loader.add_value('address', location)
            loader.add_value('region', location)
            loader.add_value('housing_type', response.url)
            loader.add_value('rent_type', card.css('.simple-card__price strong small::text').get().strip())
            loader.add_value('price', card.css('.simple-card__price strong::text').get().strip())
            loader.add_value('condominium', card.css('.condominium').css('.card-price__value::text').get(default="None"))
            loader.add_value('iptu_price', card.css('.iptu span::text').get(default="None"))
            loader.add_value('size_m2', card.css('.js-areas span::text').get(default="None"))
            loader.add_value('bedroom_count', card.css('.js-bedrooms span::text').get(default="None"))
            loader.add_value('parking_count', card.css('.js-parking-spaces span::text').get(default="None"))
            loader.add_value('bathroom_count', card.css('.js-bathrooms span::text').get(default="None"))
            loader.add_value('datetime', dt.datetime.now())

            yield loader.load_item()

        if response.css(".simple-card__address"):
            page = response.url[:response.url.index('lis/')+4]
            self.page_number[self.start_urls.index(page)] += 1
            next_page = f'{page}?pagina={self.page_number[self.start_urls.index(page)]}'
            yield response.follow(next_page, callback=self.parse_item)

    def closed(self, reason):

        stats = self.crawler.stats.get_stats()

        if stats.get('item_drop_count'):
            a = [self.name, stats["item_scraped_count"], stats["item_dropped_count"], stats["start_time"], stats["finish_time"], 
                 stats["elapsed_time_seconds"], stats['downloader/request_count'], stats['downloader/response_count'],
                 stats['finish_reason'], stats["request_depth_max"]]
        else:
            a = [self.name, stats["item_scraped_count"], 0, stats["start_time"], stats["finish_time"], 
                 stats["elapsed_time_seconds"], stats['downloader/request_count'], stats['downloader/response_count'],
                 stats['finish_reason'], stats["request_depth_max"]]

        db = Database()
        db.insert_into_job_stats(a)
        db.update_rent_data_on_finish()


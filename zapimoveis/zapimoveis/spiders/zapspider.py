import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from zapimoveis.items import ZapItem
from scrapy.loader import ItemLoader
import datetime as dt

class ZapimoveisSpider(CrawlSpider):

    name = "zapimoveis"
    allowed_domains = ["www.zapimoveis.com.br"]
    start_urls = [
                  "https://www.zapimoveis.com.br/aluguel/apartamentos/sc+florianopolis",
                  "https://www.zapimoveis.com.br/aluguel/quitinetes/sc+florianopolis",
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

            loader.add_value('address',  card.css('.simple-card__address::text').get(default="None"))
            loader.add_value('region', card.css('.simple-card__address::text').get(default="None"))
            loader.add_value('housing_type', response.url)
            loader.add_value('price', card.css('.simple-card__price strong::text').get().strip())
            loader.add_value('rent_type', card.css('.simple-card__price strong small::text').get().strip())
            loader.add_value('price_cond', card.css('.condominium').css('.card-price__value::text').get(default='0'))
            loader.add_value('price_iptu', card.css('.iptu span::text').get(default='0'))
            loader.add_value('area', card.css('.js-areas span::text').get().strip())
            loader.add_value('bedroom_count', card.css('.js-bedrooms span::text').get(default='None').strip())
            loader.add_value('parking_spaces', card.css('.js-parking-spaces span::text').get(default='None').strip())
            loader.add_value('bathroom_count', card.css('.js-bathrooms span::text').get(default='None').strip())
            loader.add_value('id', card.css('.card-container').xpath('@data-id').get())
            loader.add_value('datetime', dt.datetime.now().strftime("%d/%m/%y %H:%M"))

            yield loader.load_item()

        if response.css(".simple-card__address"):
            for page in self.start_urls:
                self.page_number[self.start_urls.index(page)] += 1
                next_page = f'{page}?pagina={self.page_number[self.start_urls.index(page)]}'
                yield response.follow(next_page, callback=self.parse_item)

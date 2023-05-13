import scrapy
from itemloaders.processors import TakeFirst, MapCompose
import re

def get_address(value):
    x = value.strip().split(', ')
    if x[-1] == "Florianópolis":
        return "None"
    else:
        return x[0]

def get_region(value):
    x = value.strip().split(', ')
    if x[-1] == "Florianópolis":
        return x[0]
    else:
        return x[-1]

def price_convert(value):
    if value and value != "None":
        x = value.replace('R$ ','').replace('.','')
        return int(x)
    else:
        return "None"

def area_convert(value):
    if value and value != "None":
        return int(value.strip().split()[0])
    else:
        return "None"

def get_housing(value):
    r = re.compile(r'[a-zA-Z]+/sc')
    housing_type = r.findall(value)[0]
    if housing_type[-4] == 's':
        return housing_type[:-4]
    else:
        return housing_type[:-3]

def strip_(value):
    if value and value != "None":
        return int(value.strip())
    else:
        return "None"

def rent_type_convert(value):
    if 'dia' in value:
        return 'D'
    else:
        return 'M'

class ZapItem(scrapy.Item):

    address = scrapy.Field(input_processor=MapCompose(get_address), output_processor=TakeFirst())
    region = scrapy.Field(input_processor=MapCompose(get_region), output_processor=TakeFirst())
    housing_type = scrapy.Field(input_processor=MapCompose(get_housing), output_processor=TakeFirst())
    rent_type = scrapy.Field(input_processor=MapCompose(rent_type_convert),output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_convert), output_processor=TakeFirst())
    condominium = scrapy.Field(input_processor=MapCompose(price_convert), output_processor=TakeFirst())
    iptu_price = scrapy.Field(input_processor=MapCompose(price_convert), output_processor=TakeFirst())
    size_m2 = scrapy.Field(input_processor=MapCompose(area_convert), output_processor=TakeFirst())
    bedroom_count = scrapy.Field(input_processor=MapCompose(strip_), output_processor=TakeFirst())
    parking_count = scrapy.Field(input_processor=MapCompose(strip_), output_processor=TakeFirst())
    bathroom_count = scrapy.Field(input_processor=MapCompose(strip_), output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    datetime = scrapy.Field(output_processor=TakeFirst())

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AnimeItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    image_url_2x = scrapy.Field()
    score = scrapy.Field()
    type_episodes = scrapy.Field()
    airing_period = scrapy.Field()
    members = scrapy.Field()
    episodes = scrapy.Field()
    information = scrapy.Field()
    status_button = scrapy.Field()

from scrapy.item import Item, Field


class Tweet(Item):
    body = Field()
    author = Field()
    author_id = Field()
    pubdate = Field()
    url = Field()
    item_id_in_source = Field()
    shares = Field()
    source_name = Field()
    source_url = Field()
    source_id_in_source = Field()
    language = Field()
    extraction_method = Field()
    stats = Field()

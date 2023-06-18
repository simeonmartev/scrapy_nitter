import scrapy
import dateparser
from datetime import datetime
from urllib.parse import urlparse, unquote
from xml.sax.saxutils import escape as xml_escape
from nitter.items import Tweet


def get_author_id(banner_href: str) -> int:
    return int(
        urlparse(unquote(urlparse(banner_href).path.split("/")[2])).path.split("/")[2]
    )


def get_iamge_id(img_str: str) -> str:
    return unquote(img_str).split("/")[-1].split(".")[0]


class NitterSpider(scrapy.Spider):
    name = "nitter"
    last_crwaled_id = 1642558950376722433  # TODO get this from db
    crawling_user = "zloban"  # TODO get this from db
    allowed_domains = ["nitter.net"]
    start_urls = ["https://nitter.it/zloban/with_replies"]

    def parse(self, response):
        banner_href = response.xpath('//div[@class="profile-banner"]/a/@href').get()
        try:
            author_id = source_id_in_source = (
                get_author_id(banner_href) if banner_href else None
            )
        except Exception:
            author_id = source_id_in_source = None
            self.logger.exception("Failed to extract author_id")

        for tweet in response.xpath('//div[@class="tweet-body"]'):
            username = tweet.xpath('.//a[@class="username"]/text()').get()
            username = (
                username.strip().replace("@", "") if username else None
            )  # # TODO get this from db
            fullname = tweet.xpath('.//a[@class="fullname"]/text()').get()
            fullname = fullname.strip() if fullname else username

            url_str = tweet.xpath('.//span[@class="tweet-date"]/a/@href').get()
            item_id_in_source = int(urlparse(url_str).path.split("/")[-1])
            url = f"https://twitter.com{url_str}" if url_str else None
            body = tweet.xpath('.//div[has-class("tweet-content")]/text()').get()

            # pubdate and url
            publication_date_str = tweet.xpath(
                './/span[@class="tweet-date"]/a/@title'
            ).get()
            publication_date = (
                dateparser.parse(publication_date_str)
                if publication_date_str
                else datetime.now()
            )

            url_str = tweet.xpath('.//span[@class="tweet-date"]/a/@href').get()
            url = f"https://twitter.com{url_str}".rstrip("#m") if url_str else None
            body = tweet.xpath('.//div[has-class("tweet-content")]/text()').get()
            body = body if body else ""

            # getting tweet stats comments, retweets, quotes, likes
            tweet_stats_classes = (
                ("comments", "comment"),
                ("shares", "retweet"),
                ("quotes", "quote"),
                ("likes", "heart"),
            )
            tweet_stats_xpath = './/span[@class="tweet-stat"]//span[@class="icon-{}"]/parent::div/text()'.format
            stats = dict()
            for db_name, tsc in tweet_stats_classes:
                stat_str = tweet.xpath(tweet_stats_xpath(tsc)).get()
                stats[db_name] = (
                    int(stat_str.replace(",", "").strip()) if stat_str else 0
                )

            # change body and url if retweets
            is_retweeted = tweet.xpath(
                './/div[@class="retweet-header"]/span/div/text()'
            ).get()
            if is_retweeted:
                body = f"RT @{username}: {body}"
                url = f"{url}#retweeted"

            # get image attachments
            image_strs = tweet.xpath(
                './/div[@class="attachments"]//a[@class="still-image"]/@href'
            ).getall()
            if image_strs:
                img_link = "https://pbs.twimg.com/media/{}?format=jpg".format
                img_links = [img_link(get_iamge_id(img_str)) for img_str in image_strs]
                body = f"{body} {' '.join(img_links)}"

            tweet = Tweet(
                extraction_method="nitter",
                pubdate=publication_date,
                stats=stats,
                body=xml_escape(f"{body}"),
                url=url,
                source_url=f"https://twitter.com/{username}",
                author_id=author_id,
                source_name=username,
                author=xml_escape(f"{fullname}"),
                item_id_in_source=item_id_in_source,
                source_id_in_source=source_id_in_source,
            )
            # check when to stop crawling
            if (
                item_id_in_source <= self.last_crwaled_id
                and self.crawling_user == username
            ):
                return
            yield tweet

        next_page_url = response.xpath('//div[@class="show-more"]/a/@href').get()
        if next_page_url:
            yield response.follow(next_page_url)

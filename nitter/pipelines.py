import sqlite3
from nitter.items import Tweet
from scrapy.exporters import CsvItemExporter


class SqlitePipeline:
    # Name of the SQLite database
    def __init__(self):
        self.name = "tweets.db"
        self.conn = None
        self.cursor = None

    # Initialize the pipeline by creating the database connection and the table
    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY,
                body TEXT,
                author TEXT,
                author_id TEXT,
                pubdate TEXT,
                url TEXT,
                item_id_in_source TEXT,
                shares INTEGER,
                source_name TEXT,
                source_description TEXT,
                source_url TEXT,
                source_id_in_source TEXT,
                source_country_id TEXT,
                language TEXT,
                extraction_method TEXT,
                stats TEXT
            )
        """
        )
        self.conn.commit()

    # Process the item and store it in the database
    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            self.insert_db(item)
        return item

    # Insert the item into the database
    def insert_db(self, item):
        data = (
            item.get("body"),
            item.get("author"),
            item.get("author_id"),
            item.get("pubdate"),
            item.get("url"),
            item.get("item_id_in_source"),
            item.get("shares"),
            item.get("source_name"),
            item.get("source_description"),
            item.get("source_url"),
            item.get("source_id_in_source"),
            item.get("source_country_id"),
            item.get("language"),
            item.get("extraction_method"),
        )
        self.cursor.execute(
            """
            INSERT INTO tweets (
                body,
                author,
                author_id,
                pubdate,
                url,
                item_id_in_source,
                shares,
                source_name,
                source_description,
                source_url,
                source_id_in_source,
                source_country_id,
                language,
                extraction_method
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            data,
        )
        self.conn.commit()

    # Close the database connection
    def close_spider(self, spider):
        self.conn.close()


class CsvPipeline:
    def __init__(self):
        self.file = open("tweets.csv", "wb")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            self.exporter.export_item(item)
        return item

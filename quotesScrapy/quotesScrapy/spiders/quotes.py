import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        json_res = json.loads(response.body)
        quotes = json_res.get("quotes")
        for quote in quotes:
            yield {
                "author": quote.get("author").get("name"),
                "tags": quote.get("tags"),
                "quotes": quote.get("text"),
            }

        # pagination
        has_next = json_res.get("has_next")
        if has_next:
            next_page_num = json_res.get("page")+1
            yield scrapy.Request(
                url=f"https://quotes.toscrape.com/api/quotes?page={next_page_num}",
                callback=self.parse
            )


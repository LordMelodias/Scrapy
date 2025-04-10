import scrapy


class AppSpider(scrapy.Spider):
    name = "app"
    # This tells the spider to only look at pages from this website and not go to any other sites.
    allowed_domains = ["quotes.toscrape.com"]
    # This is the first page the spider will visit when it starts. It's like saying, "Start your work here."
    start_urls = ["http://quotes.toscrape.com/",
                "http://quotes.toscrape.com/page/2/"]



    # response contains the HTML of the page that Scrapy downloaded.
    # But Scrapy does not save the HTML file by default — it just loads it into memory to extract data from it.
    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }

import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        for book in response.css('article.product_pod'):
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('p.price_color::text').get(),
                'availability': book.css('p.instock.availability::text').getall()[-1].strip(),
                'rating': book.css('p.star-rating').attrib['class'].split()[-1]
            }

        # Pagination: go to next page if available
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            # callback=self.parse It tells Scrapy to use the same parse function again to scrape that new page too.
            yield response.follow(next_page, callback=self.parse)
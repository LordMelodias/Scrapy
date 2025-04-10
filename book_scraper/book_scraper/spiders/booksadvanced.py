import scrapy


class BooksadvancedSpider(scrapy.Spider):
    name = "booksadvanced"
    allowed_domains = ["books.toscrape.com"]
    
    def start_requests(self):
        urls = {
            'travel': 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html',
            'music': 'https://books.toscrape.com/catalogue/category/books/music_14/index.html',
        }

        for category,url in urls.items():
            # Scrapy, go visit this URL. When the page loads, call my parse() function. Oh — and here’s a tag (like ‘travel’) to remember what type of books this is for.
            yield scrapy.Request(url=url, callback=self.parse, meta={'category': category})
    
    def parse(self, response):
        category = response.meta['category']
        
        for book in response.css('article.product_pod'):
            yield{
                'category': category,
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('p.price_color::text').get(),
                'availability': book.css('p.instock.availability::text').getall()[-1].strip(),
                'rating': book.css('p.star-rating').attrib['class'].split()[-1],
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
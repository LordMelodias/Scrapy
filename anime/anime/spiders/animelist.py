import scrapy
from anime.items import AnimeItem

class AnimelistSpider(scrapy.Spider):
    name = "animelist"
    allowed_domains = ["myanimelist.net"]
    start_urls = ['https://myanimelist.net/topanime.php']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 3,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'detailed_anime_data.json',
        'CONCURRENT_REQUESTS': 1  # Be gentle with their servers
    }
    
    def parse(self, response):
        for anime in response.css('tr.ranking-list'):
            item = AnimeItem()
            
            # Basic info
            item['rank'] = anime.css('span.top-anime-rank-text::text').get().strip()
            item['title'] = anime.css('h3.anime_ranking_h3 a::text').get().strip()
            item['url'] = anime.css('h3.anime_ranking_h3 a::attr(href)').get()
            
            # Image URLs
            item['image_url'] = anime.css('img.lazyload::attr(data-src)').get()
            item['image_url_2x'] = anime.css('img.lazyload::attr(data-srcset)').re_first(r'https[^\s]+2x')
            
            # Score
            item['score'] = anime.css('span.score-label::text').get().strip()
            
            # Detailed information
            info_text = anime.css('div.information::text').getall()
            info_text = [text.strip() for text in info_text if text.strip()]
            
            if len(info_text) >= 3:
                item['type_episodes'] = info_text[0]
                item['airing_period'] = info_text[1]
                item['members'] = info_text[2]
            
            # Extract episode count if available
            if 'eps' in item['type_episodes']:
                item['episodes'] = item['type_episodes'].split('(')[1].split(' eps')[0]
            
            # Store information text as is
            item['information'] = ' '.join(info_text)
            
            # Status/Add to List button
            item['status_button'] = anime.css('td.status a::text').get().strip()
            
            yield item
        
        # Handle pagination - get next 50 anime
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
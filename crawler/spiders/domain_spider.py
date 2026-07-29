import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import PageItem
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class DomainSpider(CrawlSpider):
    """
    Spider for crawling a specific domain.
    Respects robots.txt and handles rate limiting.
    """
    name = "domain_spider"
    
    def __init__(self, domain=None, start_urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = domain or kwargs.get('domain')
        
        if not self.domain or not start_urls:
            raise ValueError("Domain and start_urls must be provided")
        
        self.start_urls = [start_urls]
        self.allowed_domains = [urlparse(start_urls).netloc]
        
        # Configure rules for crawling
        self.rules = (
            Rule(
                LinkExtractor(
                    allow_domains=self.allowed_domains,
                    deny_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp3', 'mp4'],
                    unique=True
                ),
                callback='parse_page',
                follow=True
            ),
        )
        
        # Rate limiting
        self.crawl_delay = kwargs.get('crawl_delay', 1.0)
    
    def parse_page(self, response):
        """Parse a single page and extract content"""
        loader = ItemLoader(item=PageItem(), response=response)
        
        # Extract basic metadata
        loader.add_value('url', response.url)
        loader.add_value('status_code', response.status)
        loader.add_value('content_type', response.headers.get('Content-Type', '').decode('utf-8'))
        
        # Extract title
        title = response.xpath('//title/text()').get()
        if title:
            loader.add_value('title', title.strip())
        
        # Extract meta description
        meta_desc = response.xpath('//meta[@name="description"]/@content').get()
        if meta_desc:
            loader.add_value('meta_description', meta_desc.strip())
        
        # Extract meta keywords
        meta_keywords = response.xpath('//meta[@name="keywords"]/@content').get()
        if meta_keywords:
            loader.add_value('meta_keywords', meta_keywords.strip())
        
        # Extract main content (simplified for example)
        content_parts = []
        
        # Get paragraph text
        paragraphs = response.xpath('//p//text()').getall()
        if paragraphs:
            content_parts.extend([p.strip() for p in paragraphs if p.strip()])
        
        # Get heading text
        headings = response.xpath('//h1//text() | //h2//text() | //h3//text()').getall()
        if headings:
            content_parts.extend([h.strip() for h in headings if h.strip()])
        
        loader.add_value('content', ' '.join(content_parts))
        
        # Add domain info
        loader.add_value('domain_id', self.domain)
        
        # Add crawl timestamp
        loader.add_value('crawled_at', datetime.utcnow().isoformat())
        
        yield loader.load_item()
    
    def closed(self, reason):
        """Log when spider completes"""
        logger.info(f"Spider closed for {self.domain}: {reason}")

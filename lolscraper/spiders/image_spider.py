import scrapy
from scrapy.pipelines.images import ImagesPipeline
from lolscraper.items import ImageItem


class ImageSpider(scrapy.Spider):
    name = "image"
    
    def start_requests(self):
        url = 'http://leagueoflegends.wikia.com/wiki/Category:Concept_art'
        debugAttr = getattr(self,'debug',None)
        self.debug = False
        if debugAttr is not None:
            self.debug =debugAttr.lower() == "true"

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        print response.url
        with open('out.html','wb') as f:
            f.write(response.body)
            self.log('saved file to out.html')
        links = response.css('div.gallerytext a::attr(href)').extract()
        self.log('yield %d links' % len(links))

        if self.debug:
            links = links[:3]

        for l in links:        
            self.log(l)
            image_page_url = response.urljoin(l)
            yield scrapy.Request(image_page_url, 
                                 callback=self.parse_image_page)
        # debug: scrape the first 3 pages only
        curr_page =response.css('a.paginator-page.active::text').extract_first()
        
        if (self.debug and curr_page=='4'):
            self.log('STOP SCRAPING after reading 3 pages')
            return
        
        # go to the next page
        next_page = response.css('a.paginator-next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)


    def parse_image_page(self, response):
        url = response.css('a.internal::attr(href)').extract_first()
        if url is not None:
            #yield scrapy.Request(url,callback=self.parse_image)
            name_str=response.url.split('/')[-1].split(':')[-1]
            self.log(name_str)
            yield ImageItem(image_urls=[url],fname=[name_str])


   

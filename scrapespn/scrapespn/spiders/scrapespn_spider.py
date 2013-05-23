from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapespn.items import ScrapespnItem
import re

class ScrapespnSpider(CrawlSpider):

    #it was quicker to see how many pages of results for each president
    #than to learn enough scrapy to write the logic to stop when there's no new results
    presidents = { 'obama' : 54,
                   'bush' : 22,
                   'clinton' : 5,
                   'reagan' : 1,
                   'carter' : 1,
                   'ford' : 2,
                   'nixon' : 2,
                   'johnson' : 0, # false positives
                   'kennedy' : 1,
                   'eisenhower' : 1,
                   'truman' : 1,
                   'roosevelt' : 1,
                   'hoover' : 0, # false positives
                   'coolidge' : 1,
                   'harding' : 0, # false positives
                   'wilson' : 0, # false positives
                   'taft' : 1 }
                   
    name = 'espn'
    allowed_domains = ['espn.com','grantland.com','espn.go.com']
    start_urls = ['http://search.espn.go.com/results?page=' + str(page) + '&searchString=president+' + president + '&dims=5'
                  for president,pages in presidents.iteritems()
                  for page in range(pages)]

    rules = (

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('/story/','/post/','/columns/story/' )), callback='parse_item'),
    )
    
    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        
        def clean_and_join(selector):
            """remove html tags from the results and glue them together"""
            return ' '.join([re.sub('(<[^<]+?>|\n)', '', unicode(line.strip().encode('utf-8'), errors = "ignore")) for line in hxs.select(selector).extract()])
          
        i = ScrapespnItem()
        i['URL'] = response
        i['title'] = clean_and_join('//title')
        
        # different types of items have their story text marked up in different ways
        # the following cases seem to cover all the items in our data
        i['text'] = (clean_and_join('//div[contains(@style, "hidden")]//p') or
                     clean_and_join('//div[contains(@class, "mod-blog-post")]//div[contains(@class, "mod-content")]//text()') or
                     clean_and_join('//article[contains(@class, "story")]//p') or
                     clean_and_join('//div[contains(@class, "article-body")]//p') or
                     clean_and_join('//div[contains(@class, "post-entry")]'))
        i['date'] = clean_and_join('//div[contains(@class, "date")]//text()')
        return i
 
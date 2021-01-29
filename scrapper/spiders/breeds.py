import scrapy
from itertools import chain


class QuotesSpider(scrapy.Spider):
    name = "breeds"

    def __init__(self, url='', **kwargs):
        self.urls = [url]
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        breeds = []
        MAIN_SELECTOR = 'div.rc-padding-y--sm'

        for size in response.css(MAIN_SELECTOR):
            NAME_SELECTOR = 'a.rc-card__link'
            names = []

            for name in size.css(NAME_SELECTOR):
                if name:
                    names.append(name.attrib['href'].split('/')[-1])

            # add breed to breeds
            breeds.append(names)
        
        with open(self.output, 'w') as fl:
            fl.write("\n".join(sorted(chain(*breeds))))

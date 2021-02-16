import scrapy
import csv


class QuotesSpider(scrapy.Spider):
    name = "keywords"

    def __init__(self, url='', breeds='./data/breeds.csv', **kwargs):
        with open(breeds, 'r') as fl:
            breeds = fl.readlines()

        # create list of url and breed
        breeds = map(lambda b: b.strip(), breeds)
        breeds = map(lambda b: '{0}/{1}'.format(url, b), breeds)
        breeds = list(breeds)

        # assign value
        self.urls = breeds

        # call father
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        TAGS = '//div[@class="rc-column"]/ul[@class="rc-list rc-list--blank rc-list--large-icon"]/li/text()'

        # descripotions
        tags = response.xpath(TAGS).getall()
        tags = map(lambda x: x.strip().lower(), tags)
        tags = map(lambda x: x.replace('.', ''), tags)
        tags = list(tags)

        # save data
        with open("./data/keywords.csv", 'a', newline='\n') as fl:
            fl_breeds_details = csv.writer(fl, delimiter="|", quotechar='\\', quoting=csv.QUOTE_MINIMAL)
            for tag in tags:
              fl_breeds_details.writerow([tag])

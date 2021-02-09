import scrapy
import csv


class QuotesSpider(scrapy.Spider):
    name = "breed_details"

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
        NAME = '//div[@class="rc-column"]/div/h1/text()'
        SHORT_DESCRIPTION = '//div[@class="rc-column"]/div/p/text()'
        DESCRIPTION = '//div[@class="rc-column"]/p/text()'
        CHARACTERISTICS = '//div[@class="rc-column"]/dl[@class="definition-list"]/dd/text()'
        TAGS = '//div[@class="rc-column"]/ul[@class="rc-list rc-list--blank rc-list--large-icon"]/li/text()'
        
        # details
        name = response.xpath(NAME).get().strip()
        short_description = response.xpath(SHORT_DESCRIPTION).get()
        description = "".join(response.xpath(DESCRIPTION).getall())
        characteristics = response.xpath(CHARACTERISTICS).getall()
        tags = map(lambda x: x.strip(), response.xpath(TAGS).getall())

        # save data
        with open("./data/breeds_details.csv", 'a', newline='') as fl:
            fl_breeds_details = csv.writer(fl, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            fl_breeds_details.writerow([
                name,
                short_description,
                description,
                characteristics,
                list(tags)
            ])

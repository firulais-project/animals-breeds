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
        KEYS_CHARACTERISTICS = '//div[@class="rc-column"]/dl[@class="definition-list"]/dt/text()'
        TAGS = '//div[@class="rc-column"]/ul[@class="rc-list rc-list--blank rc-list--large-icon"]/li/text()'

        # pre-value
        country = None
        size = None
        lifetime = None

        # descripotions
        description_all = response.xpath(DESCRIPTION).getall()
        description = description_all[0:-1]
        virtues = description_all[-1]

        
        # details
        name = response.xpath(NAME).get().strip()
        short_description = response.xpath(SHORT_DESCRIPTION).get().replace('"', "'").replace("\n", "")
        
        # parser description
        description = map(lambda p: p.replace('"', "'").replace("\n", ""), description)
        description = " ".join(description)
        
        # characteristics
        characteristics = response.xpath(CHARACTERISTICS).getall()

        # parser keys
        keys_characteristics = response.xpath(KEYS_CHARACTERISTICS).getall()
        keys_characteristics = map(lambda x: x.lower(), keys_characteristics)
        keys_characteristics = list(keys_characteristics)
        
        # parser tags
        tags = response.xpath(TAGS).getall()
        tags = map(lambda x: x.strip(), tags)
        tags = map(lambda x: x.replace('.', '', tags))
        tags = "=".join(tags)

        if ("país" in keys_characteristics):
            country = characteristics[keys_characteristics.index("país")]
        if ("categoría de tamaño" in keys_characteristics):
            size = characteristics[keys_characteristics.index("categoría de tamaño")]
        if ("esperanza de vida promedio" in keys_characteristics):
            lifetime = characteristics[keys_characteristics.index("esperanza de vida promedio")]

        # save data
        with open("./data/breeds_details.csv", 'a', newline='\n') as fl:
            fl_breeds_details = csv.writer(fl, delimiter="|", quotechar='\\', quoting=csv.QUOTE_MINIMAL)
            fl_breeds_details.writerow([
                name,
                short_description,
                description,
                country,
                size,
                lifetime,
                tags,
                virtues
            ])

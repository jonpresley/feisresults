from scrapy import Spider, Request
from feisresults.items import FeisresultsItem
import re


class FeisresultsSpider(Spider):
    name = 'feisresults_spider'
    allowed_urls = ['https://www.feisresults.com/']
    start_urls = ['http://www.feisresults.com/results1.php']



    def parse(self, response):
        # years posted on website
        result_years_lst = list(range(2019,2007,-1))

        # List comprehension to construct all the urls for the years
        result_years_urls = ['http://www.feisresults.com/results1.php?year={}'.format(x) for x in result_years_lst]
        print('level 1')
        # Yield the requests to different year urls, 
        # using parse_year_page function to parse the response.
        for url in result_years_urls[:]:
            print(url)
            yield Request(url=url, callback=self.parse_year_page)


    def parse_year_page(self, response):
        #now on the year page with different feis listed
        feis_urls = response.xpath('//*[@id="box1"]/p[3]/a/@href').extract()

        print('level 2')
        for url in feis_urls:
            print(url)
            yield Request(url='http://www.feisresults.com/'+url, callback=self.parse_feis_page)

    def parse_feis_page(self, response):
        #now on page where all the competitions are listed
        comp_urls = response.xpath('//*[@id="sidebar1"]/p/a/@href').extract()

        print('level 3')
        for url in comp_urls:
            print('http://www.feisresults.com/'+url)
            yield Request(url='http://www.feisresults.com/'+url, callback=self.parse_comp_page)

    def parse_comp_page(self, response):

        feis_yr = response.xpath('//span[@class="bluetext"]/text()').extract_first()
        date = response.xpath('//span[@class="bluetext"]/text()[2]').extract_first()
        year = date.split()[-1]
        #month = date.split()[-2]
        #days = ' '.join(date.split()[:-2])
        feis = ' '.join(feis_yr.split()[:-1])
        comp_name_ugly = response.xpath('//*[@id="box1"]/h3/text()').extract_first()
        wq_wmh_str = response.xpath('//*[@id="box1"]/h3/span/text()').extract_first()
        competition = ' '.join(comp_name_ugly.split(' ')[3:]).strip()


        #print(feis, competition)

        dancer_rows = response.xpath('//table/tr')
        #dancer_rows.xpath('.//td[2]/text()').extract()
        for dancer in dancer_rows[1:]:
            name_wq_wmh = dancer.xpath('.//td[2]/text()').extract_first()
            school_region = dancer.xpath('.//td[3]/text()').extract_first()
            place = dancer.xpath('.//td[4]/text()').extract_first()
            
            #Finds all alpha num hyphens, spaces, and apostrophes plus unicode for special letters.
            pattern = "[ \-'\w\u00C0-\u00FF]+"
            name = re.findall(pattern, name_wq_wmh)[0].strip()

            if (('*' or '+') in name_wq_wmh) & ('world medal' in wq_wmh_str.lower()):
                wq = 1
                wmh = 1
            elif (('*' or '+') in name_wq_wmh) & ('qualifier' in wq_wmh_str.lower()):
                wq = 1
                wmh = 0
            elif (('*' or '+') not in name_wq_wmh) & ('world medal' in wq_wmh_str.lower()):
                wq = 1
                wmh = 0
            else:
                wq = 0
                wmh = 0
            
            
            if ':' in school_region:
                school = school_region.split(':')[0].strip()
                region = school_region.split(':')[1].strip()
            else:
                school = school_region       
                region = ' '.join(feis.split()[:-1]).replace('Oireachtas','').replace('Rince','').strip()
            



            item = FeisresultsItem()
            item['feis'] = feis
            item['date'] = date
            item['year'] = year
            #item['month'] = month
            #item['days'] = days
            item['name'] = name
            item['school'] = school
            item['region'] = region
            item['place'] = place
            item['competition'] = competition
            item['wq'] = wq
            item['wmh'] = wmh
            #processing: gender, categories: solo/group/ceili/dance_drama/choreo
            #categories: world championship/secondary qualifier/primary qualifier/neither
            #is it better to store these categories in the csv file or do it
            #post-scraping?

            #Get results from other secondary and primary competitions NOT listed there.
            


            yield item




























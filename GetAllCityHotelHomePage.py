#coding=utf-8

# -------------------------------------------------------------------- #
# Get All cities homepage in TripAdvisor
# Add Time: 2017-04-24
# -------------------------------------------------------------------- #

import bs4
from UsefulLibs import usefulForCrawl
import os

def get_all_cities_homepage(hotel_homepage_url,hotel_homepage_file,out_file):
    out_file_con_list = []
    if os.path.exists(hotel_homepage_file) == False:
        usefulForCrawl.download_page(hotel_homepage_url,hotel_homepage_file)
    url_content = open(hotel_homepage_file,'r').read()
    page_content_bs = bs4.BeautifulSoup(url_content)
    interior_xxa_bs = page_content_bs.find('div',attrs={'class':'interior xxa'})
    if interior_xxa_bs != None:
        li_bs_list = interior_xxa_bs.findAll('li')
        for li_bs in li_bs_list:
            if len(li_bs.findAll('a')) != 0:
                city_hotel = li_bs.findAll('a')[0].text.replace('\r','').replace('\n','')
                city_hotel_html = 'https://www.tripadvisor.com' + li_bs.findAll('a')[0]['href']
                out_file_con_list.append(city_hotel + '\t' + city_hotel_html)
    open(out_file,'w').write('\n'.join(out_file_con_list))

if __name__ == '__main__':
    hotel_homepage_url = 'https://www.tripadvisor.com/Hotels'
    hotel_homepage_file = '../Data/HtmlData/TripAdvisorHotelHomePage/TripAdvisorHotelHomePage.html'
    out_file = '../Data/TxtData/TripAdvisorHotelHomePage/TripAdvisorHotelHomePage.txt'
    get_all_cities_homepage(hotel_homepage_url,hotel_homepage_file,out_file)



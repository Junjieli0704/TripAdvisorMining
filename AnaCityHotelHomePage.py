#coding=utf-8

# -------------------------------------------------------------------- #
# Analyize City-Hotel homepage to get hotel information
# Add Time: 2017-04-24
# -------------------------------------------------------------------- #

import bs4
import os
from UsefulLibs import usefulAPI
import json

def get_hotel_init_info():
    hotel_init_info_dict = {}
    hotel_init_info_dict['hotel_name'] = 'NULL'
    hotel_init_info_dict['hotel_city'] = 'NULL'
    hotel_init_info_dict['hotel_homepage'] = 'NULL'
    hotel_init_info_dict['review_numbers'] = 'NULL'
    hotel_init_info_dict['star_number'] = 'NULL'
    hotel_init_info_dict['hotel_id'] = 'NULL'
    return hotel_init_info_dict

def ana_city_hotel_homepage(page_file,city_name,home_info_list):
    url_content = open(page_file,'r')
    page_content_bs = bs4.BeautifulSoup(url_content)
    hotel_bs_list = page_content_bs.findAll('div',attrs={'class':'listing easyClear  p13n_imperfect'})
    # there is no need to deal with Sponsored hotel bs
    # sponsored_hotel_bs = page_content_bs.find('div',attrs={'class':'listing_info popIndexValidation styleguide_ratings'})
    # if sponsored_hotel_bs != None:
    #    hotel_bs_list.append(sponsored_hotel_bs)

    for hotel_bs in hotel_bs_list:
        hotel_init_info_dict = get_hotel_init_info()
        hotel_init_info_dict['hotel_city'] = city_name
        try:
            hotel_init_info_dict['hotel_id'] = hotel_bs['id']
        except Exception,e:
            print e
            print 'An error occur in get hotel_id'
            print page_file
        try:
            hotel_init_info_dict['hotel_name'] = hotel_bs.find('div',attrs={'class':'listing_title'}).find('a').text
            hotel_init_info_dict['hotel_homepage'] = hotel_bs.find('div',attrs={'class':'listing_title'}).find('a')['href']
            hotel_init_info_dict['hotel_homepage'] = 'https://www.tripadvisor.com' + hotel_init_info_dict['hotel_homepage']
        except Exception,e:
            print e
            print 'An error occur in get hotel_name and hotel_homepage'
            print page_file
        try:
            hotel_rating_bs = hotel_bs.find('div',attrs={'data-prwidget-name':'common_bubble_rating'}).find('span')
            hotel_init_info_dict['star_number'] = str(hotel_rating_bs['alt'].strip())
            #hotel_init_info_dict['star_number'] = str(hotel_rating_bs['alt'].strip().replace(' of 5 bubbles',''))
            review_num_bs = hotel_bs.find('span',attrs={'class':'more review_count'}).find('a')
            #hotel_init_info_dict['review_numbers'] = review_num_bs.text.strip().replace(',','').replace(' Reviews','')
            hotel_init_info_dict['review_numbers'] = review_num_bs.text.strip()
        except Exception,e:
            print e
            print 'An error occur in get star_number and review_numbers'
            print page_file
        home_info_list.append(hotel_init_info_dict)

def check_repeat(home_info_list):
    city_hotel_name_dict = {}
    is_has_repeat = False
    for home_info in home_info_list:
        key = home_info['hotel_id']
        if city_hotel_name_dict.has_key(key):
            print 'Repeat:'
            print key
            is_has_repeat = True
        else:
            city_hotel_name_dict[key] = 1
    if is_has_repeat:
        print 'there are some repeat hotels in our dataset'
    else:
        print 'there are no repeat hotels in our dataset'


def ana_all_hotel_pages(
        all_dat_filefold = '../Data/HtmlData/TripAdvisorHotelInCitesHomePage/',
        out_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info.json'):
    page_file_list = usefulAPI.get_dir_files(all_dat_filefold,False)
    home_info_list = []
    for i in range(0,len(page_file_list)):
        city_name = ''
        page_name_list = page_file_list[i].split('_')
        for page_name in page_name_list:
            if page_name == 'Hotels': break
            city_name = city_name + page_name
        if i % 50 == 0:
            print 'pageNum: ' + str(i) + ' / ' + str(len(page_file_list))
            print 'page_file: ' + page_file_list[i]
            print 'city_name: ' + city_name
        ana_city_hotel_homepage(all_dat_filefold + page_file_list[i],city_name,home_info_list)
    print 'length of all home info list = ' + str(len(home_info_list))
    check_repeat(home_info_list)
    usefulAPI.print_out_dat_json(home_info_list,out_json_file)

if __name__ == '__main__':
    ana_all_hotel_pages()


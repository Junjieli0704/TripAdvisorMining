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

def delete_same_hotel(in_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info.json',
                      out_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info_dele_same.json'):
    src_hotel_info_dict_list = load_hotel_homepage_info(in_json_file)
    hotel_id_dict = {}
    dst_hotel_info_dict_list = []
    for hotel_info_dict in src_hotel_info_dict_list:
        hotel_id = hotel_info_dict['hotel_id']
        if hotel_id_dict.has_key(hotel_id) == False:
            hotel_id_dict[hotel_id] = 1
            dst_hotel_info_dict_list.append(hotel_info_dict)
        else:
            print 'Same hotel id: ' + hotel_id
    usefulAPI.print_out_dat_json(dst_hotel_info_dict_list,out_json_file)

def load_hotel_homepage_info(in_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info.json'):
    return json.loads(open(in_json_file,'r').read())['data']

def is_in_review_number_condition(hotel_info_dict,review_compare_mode = 'review_number', number_range = 'NULL'):
    number_range = number_range.replace(' ','')
    if number_range == 'NULL':
        return True
    else:
        if review_compare_mode == 'review_number':
            if hotel_info_dict['review_numbers'] == 'NULL': return False
            review_number = float(hotel_info_dict['review_numbers'].strip().replace(',','').replace(' Reviews',''))
        elif review_compare_mode == 'review_star':
            if hotel_info_dict['star_number'] == 'NULL': return False
            review_number = float(hotel_info_dict['star_number'].strip().replace(' of 5 bubbles',''))
        else:
            if hotel_info_dict['review_numbers'] == 'NULL': return False
            review_number = float(hotel_info_dict['review_numbers'].strip().replace(',','').replace(' Reviews',''))

        if number_range.find('+') != -1:
            if review_number > float(number_range.split('+')[0]):
                return True
        if number_range.find('-') != -1:
            if number_range.split('-')[1] == '':
                if review_number < float(number_range.split('-')[0]):
                    return True
            else:
                if review_number >= float(number_range.split('-')[0]) and review_number <= float(number_range.split('-')[1]):
                    return True
    return False


def is_in_hotel_city(hotel_info_dict,hotel_city_str = 'NULL'):
    if hotel_city_str == 'NULL':
        return True

def get_hotel_info_statics(
        in_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info.json',
        out_txt_file = ''
    ):
    review_star_dict = {}
    review_star_key_list = ['0.0-2.4','2.5-3.9','4.0-4.4','4.5-5.0']
    for review_star_key in review_star_key_list:
        review_star_dict[review_star_key] = []

    review_number_dict = {}
    review_number_key_list = ['0-499','500-999','1000-1999','2000-2999','3000-3999','4000+']
    for review_number_key in review_number_key_list:
        review_number_dict[review_number_key] = []

    hotel_info_dict_list = load_hotel_homepage_info(in_json_file)
    for hotel_info_dict in hotel_info_dict_list:
        for review_star_key in review_star_key_list:
            if is_in_review_number_condition(hotel_info_dict,review_compare_mode = 'review_star', number_range = review_star_key) == True:
                review_star_dict[review_star_key].append(hotel_info_dict)
                break
        for review_number_key in review_number_key_list:
            if is_in_review_number_condition(hotel_info_dict,review_compare_mode = 'review_number', number_range = review_number_key) == True:
                review_number_dict[review_number_key].append(hotel_info_dict)
                break

    out_file_con_list = []
    out_file_con_list.append('------------------ Review Star Distribution --------------------')
    for review_star_key in review_star_key_list:
        out_file_con_list.append(review_star_key + '\t' + str(len(review_star_dict[review_star_key])))

    out_file_con_list.append('------------------ Review number Distribution --------------------')
    for review_number_key in review_number_key_list:
        out_file_con_list.append(review_number_key + '\t' + str(len(review_number_dict[review_number_key])))

    open(out_txt_file,'w+').write('\n'.join(out_file_con_list))

def filter_hotel_info_dict(
        in_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info.json',
        review_number_range = 'NULL',       # 200 - 300
        review_star_range = 'NULL',         # 3.5 - 4.2
        hotel_city_range = 'NULL',          # [a,b,c]
        out_json_file = '',
        out_txt_file = ''):
    hotel_info_dict_list = load_hotel_homepage_info(in_json_file)
    out_hotel_info_dict_list = []
    for hotel_info_dict in hotel_info_dict_list:
        review_number_res = is_in_review_number_condition(hotel_info_dict,review_compare_mode = 'review_number', number_range = review_number_range)
        review_star_res = is_in_review_number_condition(hotel_info_dict,review_compare_mode = 'star_number', number_range = review_star_range)
        hotel_city_res = is_in_hotel_city(hotel_info_dict,hotel_city_range)
        if review_number_res and review_star_res and hotel_city_res:
            out_hotel_info_dict_list.append(hotel_info_dict)

    usefulAPI.print_out_dat_json(out_hotel_info_dict_list,out_json_file)
    #usefulAPI.print_out_hotel_info_txt(out_hotel_info_dict_list,out_txt_file)




if __name__ == '__main__':
    src_hotel_homepage_info_json = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info.json'
    dele_same_hotel_homepage_info_json = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info_dele_same.json'
    delete_same_hotel(in_json_file=src_hotel_homepage_info_json,out_json_file=dele_same_hotel_homepage_info_json)
    get_hotel_info_statics(in_json_file=dele_same_hotel_homepage_info_json,out_txt_file='../Data/TxtData/TripAdvisorHotelInCitesHomePage/hotel_homepage_info_stantics.txt')
    filter_hotel_info_dict(out_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/filter_hotel_homepage_info.json',
                           in_json_file  = dele_same_hotel_homepage_info_json,
                           review_number_range = '1000+')
    usefulAPI.json_split(in_json_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/filter_hotel_homepage_info.json',
                         split_number=5)

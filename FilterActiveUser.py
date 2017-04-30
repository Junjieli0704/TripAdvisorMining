#coding=utf-8

# -------------------------------------------------------------------- #
# Get All hotel homepage in TripAdvisor
# Add Time: 2017-04-24
# -------------------------------------------------------------------- #

from UsefulLibs import usefulAPI,usefulDataStruct
import json

def get_all_user_info(in_user_file_fold):
    uid_dict = {}
    file_name_list = usefulAPI.get_dir_files(in_user_file_fold,True)
    user_info_dict_list = []
    for file_name in file_name_list:
        temp_user_info_dict_list = usefulDataStruct.load_user_info_dat_txt(user_info_file=file_name)
        for user_info_dict in temp_user_info_dict_list:
            if uid_dict.has_key(user_info_dict['uid']) == False:
                    user_info_dict_list.append(user_info_dict)
            uid_dict[user_info_dict['uid']] = 0
    return user_info_dict_list


def is_in_hotel_review_number_condition(user_info_dict, hotel_review_number_condition = 'NULL'):
    hotel_review_number_condition = hotel_review_number_condition.replace(' ','')
    if hotel_review_number_condition == 'NULL':
        return True
    else:
        if user_info_dict['hotel_review_number'] == 'NULL': return False
        hotel_review_number = int(user_info_dict['hotel_review_number'])
        if hotel_review_number_condition.find('+') != -1:
            if hotel_review_number > float(hotel_review_number_condition.split('+')[0]):
                return True
        if hotel_review_number_condition.find('-') != -1:
            if hotel_review_number_condition.split('-')[1] == '':
                if hotel_review_number < float(hotel_review_number_condition.split('-')[0]):
                    return True
            else:
                if hotel_review_number >= float(hotel_review_number_condition.split('-')[0]) and \
                                hotel_review_number <= float(hotel_review_number_condition.split('-')[1]):
                    return True
    return False


def filter_active_user(user_info_dict_list,hotel_review_number_condition,out_file):
    out_user_info_dict_list = []
    for i in range(0,len(user_info_dict_list)):
        if i % 100000 == 0:
            print str(i) + ' / ' + str(len(user_info_dict_list))
        user_info_dict = user_info_dict_list[i]
        if is_in_hotel_review_number_condition(user_info_dict,hotel_review_number_condition):
            out_user_info_dict_list.append(user_info_dict)
    usefulDataStruct.print_out_user_info_dat_to_txt(out_user_info_dict_list,out_file)

def filter_demo_users(in_file_fold = '../Data/TxtData/TripAdvisorActiveUserPageInfoNew/',
                      out_file = 'a.json'):
    all_user_dict_list = []
    filter_user_dict_list = []
    file_list = usefulAPI.get_dir_files(in_file_fold,True)
    for file in file_list:
        user_info_dict = json.loads(open(file,'r').read())
        all_user_dict_list.append(user_info_dict)
    print len(all_user_dict_list)
    for user_dict_info in all_user_dict_list:
        if user_dict_info['user_info_str'] == 'NULL': continue
        user_info_str_list = user_dict_info['user_info_str'].split('-_-_-_-_-')
        if len(user_info_str_list) == 2:
            user_info_str_list[1] = user_info_str_list[1].replace('From','from').replace('Man','man').replace('Woman','woman')
            if user_info_str_list[1].split('from')[0] == '': continue
            #print user_info_str_list[1].split('from')[0]
            filter_user_dict_list.append(user_dict_info)
    print len(filter_user_dict_list)
    usefulDataStruct.print_out_user_info_dat_to_json(filter_user_dict_list,out_file)




if __name__ == '__main__':
    #in_user_file_fold = '../Data/TxtData/TripAdvisorUserPageInfo/'
    #user_info_dict_list = get_all_user_info(in_user_file_fold)
    #filter_active_user(user_info_dict_list=user_info_dict_list,
    #                   hotel_review_number_condition='20+',
    #                   out_file='active_user.txt')
    filter_demo_users()

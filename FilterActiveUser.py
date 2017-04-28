#coding=utf-8

# -------------------------------------------------------------------- #
# Get All hotel homepage in TripAdvisor
# Add Time: 2017-04-24
# -------------------------------------------------------------------- #

from UsefulLibs import usefulAPI,usefulDataStruct

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


if __name__ == '__main__':
    in_user_file_fold = '../Data/TxtData/TripAdvisorUserPageInfo/'
    user_info_dict_list = get_all_user_info(in_user_file_fold)
    filter_active_user(user_info_dict_list=user_info_dict_list,
                       hotel_review_number_condition='20+',
                       out_file='active_user.txt')

#coding=utf-8

# -------------------------------------------------------------------- #
# A File to record useful data struct
# Add Time: 2017-04-28
# -------------------------------------------------------------------- #


def get_user_init_info():
    user_init_info_dict = {}
    user_init_info_dict['hotel_id'] = 'NULL'
    user_init_info_dict['user_name'] = 'NULL'
    user_init_info_dict['uid'] = 'NULL'
    user_init_info_dict['src'] = 'NULL'
    user_init_info_dict['all_review_number'] = 'NULL'
    user_init_info_dict['hotel_review_number'] = 'NULL'
    user_init_info_dict['more_info_page'] = 'NULL'
    user_init_info_dict['user_info_str'] = 'NULL'
    user_init_info_dict['full_profile_page'] = 'NULL'
    user_init_info_dict['all_review_dis'] = 'NULL'
    return user_init_info_dict

def print_out_user_info_dat_to_txt(user_info_dict_list,
                                   out_txt_file,
                                   is_need_print_head_line = True,
                                   id_range_list = [],
                                   write_mode = 'w+',
                                   dict_str = 'user_name\tuid\tsrc\thotel_id\tall_review_number\thotel_review_number\tmore_info_page'):
    if id_range_list == []:
        id_range_list = range(0,len(user_info_dict_list))
    out_file_con_list = []
    if is_need_print_head_line:
        out_file_con_list.append(dict_str)
    for i in id_range_list:
        temp_list = []
        for key in dict_str.split('\t'):
            temp_list.append(user_info_dict_list[i][key])
        out_file_con_list.append('\t'.join(temp_list).encode('utf-8'))
    out_file_con_list.append('\n')
    open(out_txt_file,write_mode).write('\n'.join(out_file_con_list))

def load_user_info_dat_txt(user_info_file,
                           dict_str = 'user_name\tuid\tsrc\thotel_id\tall_review_number\thotel_review_number\tmore_info_page'):
    user_info_dict_list = []
    line_con_list = open(user_info_file,'r').readlines()
    for line_con in line_con_list:
        line_con = line_con.strip()
        user_info_dict = get_user_init_info()
        word_con_list = line_con.split('\t')
        key_list = dict_str.split('\t')
        if len(key_list) == len(word_con_list):
            if word_con_list[0] == 'user_name': continue
            for k in range(0,len(key_list)):
                user_info_dict[key_list[k]] = word_con_list[k]
            user_info_dict_list.append(user_info_dict)
    return user_info_dict_list

def split_user_info_file(in_file,split_number,file_suffix = '.txt'):
    out_file_list = []
    each_txt_dict_list = []
    in_file_con_list = [line_con.strip() for line_con in open(in_file,'r').readlines()]
    for i in range(0,split_number):
        each_txt_dict_list.append([])
        out_file_list.append(in_file.replace(file_suffix, '_' + str(i+1) + '_' + str(split_number) + file_suffix))
        each_txt_dict_list[i].append(in_file_con_list[0])
    for i in range(1,len(in_file_con_list)):
        each_txt_dict_list[i%split_number].append(in_file_con_list[i])
    for i in range(0,split_number):
        open(out_file_list[i],'w+').write('\n'.join(each_txt_dict_list[i]))
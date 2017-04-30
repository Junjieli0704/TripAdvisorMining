#coding=utf-8

# -------------------------------------------------------------------- #
# Analyize User homepage to get user info
# Add Time: 2017-04-26
# -------------------------------------------------------------------- #

import bs4
from UsefulLibs import usefulAPI,usefulDataStruct
from multiprocessing import Process, Pool
import re

class anaUserHomePage:
    def __init__(self,thread_num,user_home_file_list,out_file_fold,active_user_info_list):
        self.thread_num = thread_num
        self.user_home_file_list = user_home_file_list
        self.out_file_fold = out_file_fold
        self.active_user_info_list = active_user_info_list

    def ana_single_user_home_page(self,user_home_file,user_info_dict,out_file):
        url_content = open(user_home_file,'r').read()
        page_content_bs = bs4.BeautifulSoup(url_content,'html.parser')
        user_info_bs = page_content_bs.find('ul',attrs={'class':re.compile(r'memberdescription*')})
        if user_info_bs != None:
            user_info_dict['user_info_str'] = user_info_bs.text.strip().replace('\n','-_-_-_-_-')
        user_profile_bs = page_content_bs.find('a',attrs={'href':re.compile(r'/members/*')})
        if user_profile_bs != None:
            user_info_dict['full_profile_page'] = user_profile_bs['href']
        try:
            review_dis_info_bs = page_content_bs.find('div',attrs={'class':'reviewchart wrap container'})
            span_bs_list = review_dis_info_bs.findAll('span')
            txt_list = [span_bs.text.strip() for span_bs in span_bs_list]
            user_info_dict['all_review_dis'] = '---'.join(txt_list)
        except Exception, e:
            pass
            #print 'Error in Get Review Dis Info:' + str(e)
        user_info_dict_list = []
        user_info_dict_list.append(user_info_dict)
        try:
            usefulDataStruct.print_out_user_info_dat_to_json(user_info_dict_list = user_info_dict_list,
                                                             out_json_file=out_file)
        except Exception, e:
            print 'Error in Print Out Txt Dat' + str(e)
            print user_info_dict


    def ana_all_user_page_files(self):
        for i in range(0,len(self.user_home_file_list)):
            if i % 100 == 0:
                print 'user_num: ' + str(i) + ' / ' + str(len(self.user_home_file_list)) + '     processing_num(' + str(self.thread_num) + ')'
            out_file = self.out_file_fold + self.active_user_info_list[i]['uid'] + '.txt'
            self.ana_single_user_home_page( user_home_file = self.user_home_file_list[i],
                                            out_file = out_file,
                                            user_info_dict = self.active_user_info_list[i])




def get_hotel_review_files(in_file_fold = '../Data/HtmlData/TripAdvisorHotelReviewPage/hotel_206921/'):
    return usefulAPI.get_dir_files(in_file_fold,True)

def dealwith_user_info_one_processing(thread_num,user_home_file_list,active_user_info_list,out_file_fold):
        ana_user_home_page = anaUserHomePage(
                                          thread_num = thread_num,
                                          user_home_file_list = user_home_file_list,
                                          active_user_info_list = active_user_info_list,
                                          out_file_fold = out_file_fold)
        ana_user_home_page.ana_all_user_page_files()


def dealwith_user_info_one_multi_processing(user_home_file_list,
                                            active_user_info_list,
                                            processing_number=5,
                                            out_file_fold='./'):

    user_home_file_list_per_thread = []
    active_user_info_list_per_thread = []
    for i in range(0,processing_number):
        user_home_file_list_per_thread.append([])
        active_user_info_list_per_thread.append([])

    for k in range(0,len(user_home_file_list)):
        user_home_file_list_per_thread[k % processing_number].append(user_home_file_list[k])
        active_user_info_list_per_thread[k % processing_number].append(active_user_info_list[k])

    pool = Pool(processing_number)

    for i in range(0,processing_number):
        pool.apply_async(dealwith_user_info_one_processing, (i,
                                                             user_home_file_list_per_thread[i],
                                                             active_user_info_list_per_thread[i],
                                                             out_file_fold))

    pool.close()
    pool.join()


def get_prepare_info(in_file_fold,all_user_info_dict_file):
    user_home_file_list = []
    active_user_info_list = []
    user_info_dict_list = usefulDataStruct.load_user_info_dat_txt(all_user_info_dict_file)
    user_id_to_user_info_dict = {}
    for user_info_dict in user_info_dict_list:
        user_id_to_user_info_dict[user_info_dict['uid']] = user_info_dict

    uid_files = usefulAPI.get_dir_files(in_file_fold,False)
    for uid_file in uid_files:
        uid = uid_file.replace('.html','')
        #if user_id_to_user_info_dict.has_key(uid) == False:
        #    print uid
        #else:
        user_home_file_list.append(in_file_fold + uid_file)
        active_user_info_list.append(user_id_to_user_info_dict[uid])
    return user_home_file_list,active_user_info_list



def change_dat(in_file_fold = '../Data/TxtData/TripAdvisorActiveUserPageInfo/',
               out_file_fold = '../Data/TxtData/TripAdvisorActiveUserPageInfoNew/'):
    file_name_list = usefulAPI.get_dir_files(in_file_fold,True)
    for file_name in file_name_list:
        user_info_dict_list = usefulDataStruct.load_user_info_dat_txt(
                            user_info_file = file_name,
                            dict_str = 'user_name\tuid\tsrc\thotel_id\tall_review_number\thotel_review_number\tmore_info_page\tuser_info_str\tfull_profile_page\tall_review_dis')
        for user_info_dict in user_info_dict_list:
            out_file = out_file_fold + user_info_dict['uid'] + '.json'
            user_info_dict_list = []
            user_info_dict_list.append(user_info_dict)
            usefulDataStruct.print_out_user_info_dat_to_json(user_info_dict_list = user_info_dict_list,
                                                             out_json_file=out_file)


if __name__ == '__main__':
    #change_dat()
    in_file_fold = '../Data/HtmlData/ErrorTripAdvisorUserHomePage/'
    all_user_info_dict_file = 'active_user.txt'
    user_home_file_list , active_user_info_list = get_prepare_info(in_file_fold,all_user_info_dict_file)
    out_file_fold = '../Data/TxtData/TripAdvisorActiveUserPageInfoNew/'
    usefulAPI.mk_dir(out_file_fold)

    dealwith_user_info_one_multi_processing(user_home_file_list = user_home_file_list,
                                            active_user_info_list = active_user_info_list,
                                            processing_number = 5,
                                            out_file_fold = out_file_fold)

    '''

    ana_user_home_page = anaUserHomePage(thread_num = 1,
                                          user_home_file_list = user_home_file_list,
                                          active_user_info_list = active_user_info_list,
                                          out_file_fold = out_file_fold)
    ana_user_home_page.ana_all_user_page_files()
    '''






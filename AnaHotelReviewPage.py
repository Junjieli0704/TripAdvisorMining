#coding=utf-8

# -------------------------------------------------------------------- #
# Analyize Hotel_review Page to get User homepage info
# Add Time: 2017-04-26
# -------------------------------------------------------------------- #

import bs4
from UsefulLibs import usefulAPI
import CrawlHotelReviewPage
from multiprocessing import Process, Pool
from UsefulLibs import usefulDataStruct

class anaHotelReview:
    def __init__(self,thread_num,hotel_reviw_file_fold,hotel_id,out_file_fold):
        self.thread_num = thread_num
        self.hotel_reviw_file_fold = hotel_reviw_file_fold
        self.hotel_id = hotel_id
        self.hotel_review_file_list = []
        self.out_file_fold = out_file_fold
        self.user_info_list = []

    def get_hotel_review_file_list(self):
        file_fold = self.hotel_reviw_file_fold + self.hotel_id + '/'
        self.hotel_review_file_list = usefulAPI.get_dir_files(file_fold,is_contain_dir=True)

    def get_uid_src(self,uid_str):
        uid = uid_str.split('-')[0].replace('UID_','')
        src = uid_str.split('-')[1].replace('SRC_','')
        return uid,src

    def get_more_info_page(self,uid,src):
        temp_str = 'https://www.tripadvisor.com/MemberOverlay?Mode=owa&uid=' + uid
        temp_str = temp_str + '&c=&src=' + src + '&fus=false&partner=false&LsoId=&metaReferer=Hotel_Review'
        return temp_str

    def ana_single_hotel_review_page(self,hotel_review_file):
        url_content = open(hotel_review_file,'r')
        page_content_bs = bs4.BeautifulSoup(url_content)
        user_bs_list = page_content_bs.findAll('div',attrs={'class':'member_info'})
        for i in range(0,len(user_bs_list)):
            user_bs = user_bs_list[i]
            user_info_dict = usefulDataStruct.get_user_init_info()
            uid_src_info_bs = user_bs.find('div',attrs={'class':'memberOverlayLink'})
            if uid_src_info_bs == None: continue
            user_info_dict['uid'] , user_info_dict['src'] = self.get_uid_src(uid_src_info_bs['id'])
            review_num_bs = user_bs.find('div',attrs={'class':'reviewerBadge badge'})
            if review_num_bs != None:
                user_info_dict['all_review_number'] = review_num_bs.text.strip().replace(' review','').replace('s','')
            hotel_review_num_bs = user_bs.find('div',attrs={'class':'contributionReviewBadge badge'})
            if hotel_review_num_bs != None:
                user_info_dict['hotel_review_number'] = hotel_review_num_bs.text.strip().replace(' hotel review','').replace('s','')
            user_name_bs = user_bs.find('span',attrs={'class':'expand_inline scrname'})
            if user_name_bs != None:
                user_info_dict['user_name'] = user_name_bs.text
            user_info_dict['more_info_page'] = self.get_more_info_page(user_info_dict['uid'],user_info_dict['src'])
            user_info_dict['hotel_id'] = self.hotel_id
            self.user_info_list.append(user_info_dict)


    def ana_all_hotel_review_files(self):
        for i in range(0,len(self.hotel_review_file_list)):
            if i % 10 == 0:
                #print 'hotel_review_num: ' + str(i) + ' / ' + str(len(self.hotel_review_file_list)) + '     hotel_id(' + self.hotel_id + ')'
                print 'hotel_review_num: ' + str(i) + ' / ' + str(len(self.hotel_review_file_list)) + '     processing_num(' + str(self.thread_num) + ')'
            self.ana_single_hotel_review_page(self.hotel_review_file_list[i])

    def print_out_json_dat(self):
        usefulAPI.print_out_dat_json(self.user_info_list,'aaa.json')

    def print_out_txt_dat(self):
        txt_file = self.out_file_fold + self.hotel_id + '_ana_user.txt'
        usefulDataStruct.print_out_user_info_dat_to_txt(user_info_dict_list = self.user_info_list,
                                                        dict_str = 'user_name\tuid\tsrc\thotel_id\tall_review_number\thotel_review_number\tmore_info_page',
                                                        out_txt_file = txt_file)

def get_hotel_review_files(in_file_fold = '../Data/HtmlData/TripAdvisorHotelReviewPage/hotel_206921/'):
    return usefulAPI.get_dir_files(in_file_fold,True)

def dealwith_hotel_review_info_one_processing(thread_num,hotel_reviw_file_fold,hotel_id_list,out_file_fold):
    for i in range(0,len(hotel_id_list)):
        print 'hotel_num: ' + str(i) + ' / ' + str(len(hotel_id_list)) + '     processing_num(' + str(thread_num) + ')'
        ana_hotel_review = anaHotelReview(
                                        thread_num = thread_num,
                                        hotel_reviw_file_fold = hotel_reviw_file_fold,
                                        hotel_id = hotel_id_list[i],
                                        out_file_fold = out_file_fold)
        ana_hotel_review.get_hotel_review_file_list()
        ana_hotel_review.ana_all_hotel_review_files()
        ana_hotel_review.print_out_txt_dat()


def dealwith_hotel_review_info_multi_processing(hotel_finish_id_file,hotel_review_filefold,processing_number=5,out_file_fold='./'):
    finish_hotel_id_dict = CrawlHotelReviewPage.load_finish_id_file(hotel_finish_id_file)
    finish_hotel_id_list = [key for key, value in finish_hotel_id_dict.items()]
    hotel_id_list_per_thread = []
    for i in range(0,processing_number):
        hotel_id_list_per_thread.append([])

    for k in range(0,len(finish_hotel_id_list)):
        hotel_id_list_per_thread[k % processing_number].append(finish_hotel_id_list[k])

    pool = Pool(processing_number)

    for i in range(0,processing_number):
        pool.apply_async(dealwith_hotel_review_info_one_processing, (i,
                                                               hotel_review_filefold,
                                                               hotel_id_list_per_thread[i],
                                                               out_file_fold))

    pool.close()
    pool.join()




if __name__ == '__main__':
    hotel_finish_id_file = 'finish_hotel_id.txt'
    dealwith_hotel_review_info_multi_processing(
        hotel_finish_id_file = hotel_finish_id_file,
        hotel_review_filefold = '../Data/HtmlData/TripAdvisorHotelReviewPage/',
        processing_number=3,
        out_file_fold = '../Data/TxtData/TripAdvisorUserPageInfo/')







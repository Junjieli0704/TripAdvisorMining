#coding=utf-8

# -------------------------------------------------------------------- #
# Crawl User homepage Info and Parse Them
# Add Time: 2017-04-27
# -------------------------------------------------------------------- #

import bs4
from UsefulLibs import usefulForCrawl,usefulDataStruct,usefulAPI
import time
import threading
import re
import socket

class crawlUserHomePage:
    def __init__(self,thread_num,user_info_dict_list,out_user_info_file, time_sleep = 10):
        self.time_sleep = time_sleep
        self.user_info_dict_list = user_info_dict_list
        self.out_user_info_file = out_user_info_file
        self.thread_num = thread_num

    def crawl_user_home_page(self,user_info_dict,out_file,time_sleep):
        url_content = usefulForCrawl.get_html_content_from_a_page(user_info_dict['more_info_page'],time_sleep = time_sleep)
        open(out_file,'w+').write(url_content)
        if usefulAPI.get_file_size(out_file) <= 50000:
            return False
        else:
            return True

        '''
        page_content_bs = bs4.BeautifulSoup(url_content)
        user_info_bs = page_content_bs.find('ul',attrs={'class':'memberdescription'})
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
            print 'Error in Get Review Dis Info:' + str(e)

        if user_info_bs == None and user_profile_bs == None:
            open(out_file,'w+').write(url_content)
            return False
        else:
            return True
        '''

    def crawl_all_user_page(self):
        error_back_times = 0
        is_need_print_head_line = True
        for i in range(0,len(self.user_info_dict_list)):
            #print_id_number = 1
            #if i % print_id_number == 0:
            temp_str = 'PageNum: ' + str(i) + ' / ' + str(len(self.user_info_dict_list)) + '  ThreadNum(' + str(self.thread_num) + ')'
            temp_str = temp_str + '   Time:' + usefulAPI.get_current_date_time()
            print temp_str
            #print 'PageNum: ' + str(i) + ' / ' + str(len(self.user_info_dict_list)) + '  ThreadNum(' + str(self.thread_num) + ')'
            '''
                if i > 0:
                    if i != print_id_number:
                        is_need_print_head_line = False
                    id_range_list = range(i-print_id_number,i)
                    usefulDataStruct.print_out_user_info_dat_to_txt(is_need_print_head_line = is_need_print_head_line,
                                                                    user_info_dict_list = self.user_info_dict_list,
                                                                    id_range_list = id_range_list,
                                                                    dict_str = 'user_name\tuid\tsrc\thotel_id\tall_review_number\thotel_review_number\tmore_info_page\tuser_info_str\tfull_profile_page\tall_review_dis',
                                                                    out_txt_file = self.out_user_info_file,
                                                                    write_mode='a+')
            '''
            try:
                out_file = '../Data/HtmlData/ErrorTripAdvisorUserHomePage/' + self.user_info_dict_list[i]['uid'] + '.html'
                crawl_res = self.crawl_user_home_page(user_info_dict = self.user_info_dict_list[i],
                                                      out_file = out_file,
                                                      time_sleep = 10)
                if crawl_res:
                    error_back_times = 0
                else:
                    error_back_times = error_back_times + 1
                if error_back_times == 5:
                    time.sleep(60*30)
                    error_back_times = 0
            except Exception, e:
                print e


class crawl_home_page_thread(threading.Thread):
    def __init__(self,thread_num,user_info_dict_list,out_user_info_file, time_sleep = 10):
        threading.Thread.__init__(self)
        self.thread_num = thread_num
        self.time_sleep = time_sleep
        self.user_info_dict_list = user_info_dict_list
        self.out_user_info_file = out_user_info_file
        self.thread_stop = False

    def run(self):
        crawl_user_home_page = crawlUserHomePage(user_info_dict_list = self.user_info_dict_list,
                                                 time_sleep = self.time_sleep,
                                                 out_user_info_file = self.out_user_info_file,
                                                 thread_num = self.thread_num)
        crawl_user_home_page.crawl_all_user_page()

    def stop(self):
        self.thread_stop = True


def crawl_hotel_review_info_multi_thread(user_info_dict_list, out_user_info_file, time_sleep = 10,thread_number=5):
    user_info_list_per_thread = []
    out_user_info_file_list = []
    for i in range(0,thread_number):
        user_info_list_per_thread.append([])
        out_user_info_file_list.append(out_user_info_file.replace('.txt', '_' + str(i+1) + '_' + str(thread_number) + '.txt'))
    for k in range(0,len(user_info_dict_list)):
        user_info_list_per_thread[k % thread_number].append(user_info_dict_list[k])

    thread_pool = []
    if len(user_info_dict_list) != 0:
        for i in range(0,thread_number):
            thread_pool.append(crawl_home_page_thread(thread_num = str(i+1),
                                                      user_info_dict_list = user_info_list_per_thread[i],
                                                      out_user_info_file  = out_user_info_file_list[i],
                                                      time_sleep = time_sleep))
        for th in thread_pool:
            th.start()
        for th in thread_pool:
            th.join()


def crawl_user_home_page(user_page,time_sleep):
    url_content = open('test.html','r').read()
    page_content_bs = bs4.BeautifulSoup(url_content)
    user_info_bs = page_content_bs.find('ul',attrs={'class':'memberdescription'})
    print user_info_bs.text.strip().split('\n')
    user_profile_bs = page_content_bs.find('a',attrs={'href':re.compile(r'/members/*')})
    print user_profile_bs



def load_active_user_list(active_user_file):
    return usefulDataStruct.load_user_info_dat_txt(active_user_file)

def filter_finish_user(active_user_list,finish_user_id_list):
    print 'before delete finish active user......'
    print 'len(active_user_list): ' + str(len(active_user_list))
    finish_user_id_dict = {}
    for id in finish_user_id_list:
        finish_user_id_dict[id] = 1
    new_active_user_list = []
    for active_user in active_user_list:
        if finish_user_id_dict.has_key(active_user['uid']) == False:
            new_active_user_list.append(active_user)
    print 'before delete finish active user......'
    print 'len(active_user_list): ' + str(len(new_active_user_list))
    return new_active_user_list


def split_active_user_file(active_user_file,split_number):
    usefulDataStruct.split_user_info_file(active_user_file,split_number,'.txt')


def crawl_test():
    url_content = open('test.html').read()
    page_content_bs = bs4.BeautifulSoup(url_content)
    review_dis_info_bs = page_content_bs.find('div',attrs={'class':'reviewchart wrap container'})
    span_bs_list = review_dis_info_bs.findAll('span')
    print span_bs_list
    txt_list = [span_bs.text.strip() for span_bs in span_bs_list]
    print '---'.join(txt_list)
    #print user_info_bs

def get_finish_active_user_list(in_file_fold = '../Data/TxtData/TripAdvisorActiveUserPageInfo/',
                                out_finish_file = 'finish_active_user_list.txt'):
    file_name_list = usefulAPI.get_dir_files(in_file_fold,True)
    out_user_id_list = []
    for file in file_name_list:
        line_con_list = [line_con.strip() for line_con in open(file,'r').readlines()]
        for line_con in line_con_list:
            word_con_list = line_con.split('\t')
            if len(word_con_list) == 10:
                if word_con_list[0] == 'user_name': continue
                elif word_con_list[7] == 'NULL': continue
                elif word_con_list[8] == 'NULL': continue
                elif word_con_list[9] == 'NULL': continue
                out_user_id_list.append(word_con_list[1])
    open(out_finish_file,'w+').write('\n'.join(out_user_id_list))
    return out_user_id_list



if __name__ == '__main__':

    active_user_file = 'active_user_1_3.txt'
    finish_active_file = 'finish_active_user_list.txt'
    active_user_list = load_active_user_list(active_user_file)
    new_active_user_list = filter_finish_user(active_user_list,get_finish_active_user_list())
    out_file_fold = '../Data/TxtData/TripAdvisorActiveUserPageInfo/'
    out_user_info_file = out_file_fold + socket.gethostname() + '_active_user_info.txt'
    crawl_hotel_review_info_multi_thread(user_info_dict_list = new_active_user_list,
                                         out_user_info_file = out_user_info_file,
                                         time_sleep = 10,
                                         thread_number = 5)






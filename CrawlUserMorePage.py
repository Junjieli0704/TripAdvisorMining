#coding=utf-8

# -------------------------------------------------------------------- #
# Get All hotel review page in TripAdvisor
# Add Time: 2017-04-26
# -------------------------------------------------------------------- #

import bs4
from UsefulLibs import usefulForCrawl,usefulAPI,usefulDataStruct
import os
from selenium import webdriver
import time
import threading
import selenium.webdriver.support.ui as ui

class getUserMorePage:
    def __init__(self,thread_num,user_info_dict_list,out_file_fold,time_sleep = 20):
        self.thread_num = thread_num
        self.out_file_fold = out_file_fold
        self.time_sleep = time_sleep
        self.user_info_dict_list = user_info_dict_list
        self.cap = webdriver.DesiredCapabilities.PHANTOMJS
        self.cap["phantomjs.page.settings.loadImages"] = False


    def crawl_one_user_more_page(self,user_info_dict,time_sleep):
        user_page = 'https://www.tripadvisor.com' + user_info_dict['full_profile_page']
        print 'user_page: ' + user_page
        user_id = user_info_dict['uid']
        self.driver = webdriver.PhantomJS(desired_capabilities=self.cap)
        wait = ui.WebDriverWait(self.driver,5)
        page_num = 1
        out_file = self.out_file_fold + user_id + '_page_' + str(page_num) + '.html'
        is_error_back = True
        try:
            self.driver.get(user_page)
            wait.until(lambda driver: self.driver.find_element_by_xpath('//li[@data-filter="REVIEWS_HOTELS"]'))
            nextpage_url = self.driver.find_element_by_xpath('//li[@data-filter="REVIEWS_HOTELS"]')
            nextpage_url.click()
            print 'time_sleep begin......'
            time.sleep(time_sleep)
            print 'time_sleep end......'
            open(out_file,'w+').write(self.driver.page_source.encode('utf-8'))
        except Exception,e:
            print e
            is_error_back = False

        self.driver.quit()
        if is_error_back:
            return 'Error'
        else:
            return 'Correct'

        '''
        is_error_back = False
        while True:
            try:
                wait.until(lambda driver: self.driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]'))
                nextpage_url = self.driver.find_element_by_xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]')
                nextpage_url.click()
                page_num = page_num + 1
                print 'time_sleep begin......'
                time.sleep(time_sleep)
                print 'time_sleep end......'
                out_file = out_file_fold + hotel_id + '_page_' + str(page_num) + '.html'
                open(out_file,'w+').write(self.driver.page_source.encode('utf-8'))
                if page_num >= self.crawl_page_max:
                    break
                print 'HotelNum: ' + str(hotel_num) + ' / ' + str(all_hotel_num) + \
                      '  PageNum: ' + str(page_num) + ' / ' + str(self.crawl_page_max)

            except Exception,e:
                print e
                is_error_back = True
                break

        self.driver.quit()

        if is_error_back:
            return 'Error'
        else:
            return 'Correct''
        '''

    def crawl_all_user_more_page(self):
        error_back_times = 0
        for i in range(0,len(self.user_info_dict_list)):
            print 'UserNum: ' + str(i) + ' / ' + str(len(self.user_info_dict_list)) \
                  + ' threadNum(' + str(self.thread_num) + ')   ' + usefulAPI.get_current_date_time()
            try:
                back_str = self.crawl_one_user_more_page(self.user_info_dict_list[i],self.time_sleep)
                if back_str == 'Error':
                    error_back_times = error_back_times + 1
                else:
                    error_back_times = 0
                if error_back_times == 5:
                    # 估计被封了，休息 一会 30分钟
                    time.sleep(60*30)
            except Exception, e:
                print e


class crawl_user_more_page_thread(threading.Thread):
    def __init__(self,thread_num,user_info_dict_list,out_file_fold,time_sleep = 20):
        threading.Thread.__init__(self)
        self.thread_num = thread_num
        self.time_sleep = time_sleep
        self.out_file_fold = out_file_fold
        self.user_info_dict_list = user_info_dict_list
        self.thread_stop = False
    def run(self):
        get_user_more_page = getUserMorePage(thread_num=self.thread_num,
                                             user_info_dict_list=self.user_info_dict_list,
                                             time_sleep = self.time_sleep,
                                             out_file_fold = self.out_file_fold)
        get_user_more_page.crawl_all_user_more_page()
    def stop(self):
        self.thread_stop = True


def crawl_user_more_page_multi_thread(user_info_dict_list,out_file_fold,time_sleep = 20,thread_number=5):
    user_info_list_per_thread = []
    for i in range(0,thread_number):
        user_info_list_per_thread.append([])

    for k in range(0,len(user_info_dict_list)):
        user_info_list_per_thread[k % thread_number].append(user_info_dict_list[k])

    thread_pool = []
    if len(user_info_dict_list) != 0:
        for i in range(0,thread_number):
            thread_pool.append(crawl_user_more_page_thread(thread_num = i,
                                                           user_info_dict_list = user_info_list_per_thread[i],
                                                           out_file_fold = out_file_fold,
                                                           time_sleep = time_sleep))
        for th in thread_pool:
            th.start()
        for th in thread_pool:
            th.join()

def load_all_user_info_dict_list(in_file_fold = '../Data/TxtData/TripAdvisorActiveUserPageInfoNew/',
                                 out_file = '../Data/TxtData/TripAdvisorActiveUserPageInfoJson/active_user_more_info.json'):
    file_name_list = usefulAPI.get_dir_files(in_file_fold,True)
    all_user_info_dict_list = []
    for file_name in file_name_list:
        user_info_dict_list = usefulDataStruct.load_user_info_dict_json(file_name)
        all_user_info_dict_list = all_user_info_dict_list + user_info_dict_list
    print len(all_user_info_dict_list)
    usefulDataStruct.print_out_user_info_dat_to_json(all_user_info_dict_list,out_file)
    return all_user_info_dict_list


if __name__ == '__main__':
    #load_all_user_info_dict_list()
    usefulDataStruct.json_split(
        in_file = '../Data/TxtData/TripAdvisorActiveUserPageInfoJson/active_user_more_info.json',
        split_number = 3)

    json_file = '../Data/TxtData/TripAdvisorActiveUserPageInfoJson/active_user_more_info_1_3.json'
    user_info_dict_list = usefulDataStruct.load_user_info_dict_json(json_file)
    out_file_fold = '../Data/HtmlData/TripAdvisorActiveUserMorePage/'
    crawl_user_more_page_multi_thread(user_info_dict_list = user_info_dict_list ,
                                      out_file_fold = out_file_fold,
                                      time_sleep = 10,
                                      thread_number = 5)




#coding=utf-8

# -------------------------------------------------------------------- #
# Get All hotel review page in TripAdvisor
# Add Time: 2017-04-26
# -------------------------------------------------------------------- #

import bs4
from UsefulLibs import usefulForCrawl
from UsefulLibs import usefulAPI
import os
from selenium import webdriver
import time
import threading
import selenium.webdriver.support.ui as ui

class getHotelReview:
    def __init__(self,hotel_info_dict_list,time_sleep = 20,crawl_page_max=15):
        self.time_sleep = time_sleep
        self.crawl_page_max = crawl_page_max
        self.hotel_info_dict_list = hotel_info_dict_list
        self.cap = webdriver.DesiredCapabilities.PHANTOMJS
        self.cap["phantomjs.page.settings.loadImages"] = False


    def crawl_hotel_review_page(self,hotel_num,all_hotel_num,hotel_id,hotel_review_homepage_url,out_file_fold,time_sleep):
        out_file_fold = out_file_fold + str(hotel_id) + '/'
        if os.path.exists(out_file_fold) == False:
            os.mkdir(out_file_fold)

        self.driver = webdriver.PhantomJS(desired_capabilities=self.cap)
        wait = ui.WebDriverWait(self.driver,10)
        page_num = 1
        out_file = out_file_fold + hotel_id + '_page_' + str(page_num) + '.html'
        self.driver.get(hotel_review_homepage_url)
        print 'time_sleep begin......'
        time.sleep(time_sleep)
        print 'time_sleep end......'
        open(out_file,'w+').write(self.driver.page_source.encode('utf-8'))
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
            return 'Correct'

    def crawl_all_hotel_home_page(self):
        error_back_times = 0
        for i in range(0,len(self.hotel_info_dict_list)):
            print 'HotelNum: ' + str(i) + ' / ' + str(len(self.hotel_info_dict_list))
            print 'HotelName: ' + self.hotel_info_dict_list[i]['hotel_name']
            print 'HotelID: ' + self.hotel_info_dict_list[i]['hotel_id']
            hotel_id = self.hotel_info_dict_list[i]['hotel_id']
            homepage = self.hotel_info_dict_list[i]['hotel_homepage'].replace('https://www.tripadvisor.com/','https://www.tripadvisor.com/LangRedirect?auto=1&TAPD=tripadvisor.com&origin=null&returnTo=/')
            out_file_fold = '../Data/HtmlData/TripAdvisorHotelReviewPage/'
            print 'homepage: ' + homepage
            try:
                back_str = self.crawl_hotel_review_page(i,len(self.hotel_info_dict_list),hotel_id,homepage,out_file_fold,time_sleep = self.time_sleep)
                if back_str == 'Error':
                    error_back_times = error_back_times + 1
                else:
                    error_back_times = 0
                if error_back_times == 5:
                    # 估计被封了，休息 一会 30分钟
                    time.sleep(60*30)
            except Exception, e:
                print e


    def quit_phantomjs(self):
        pass
        #self.driver.quit()

class crawl_home_page_thread(threading.Thread):
    def __init__(self,hotel_info_dict_list,time_sleep = 20,crawl_page_max=15):
        threading.Thread.__init__(self)
        self.time_sleep = time_sleep
        self.crawl_page_max = crawl_page_max
        self.hotel_info_dict_list = hotel_info_dict_list
        self.thread_stop = False
    def run(self):
        get_hotel_home_page = getHotelReview(hotel_info_dict_list=self.hotel_info_dict_list,time_sleep = self.time_sleep,crawl_page_max=self.crawl_page_max)
        get_hotel_home_page.crawl_all_hotel_home_page()
        get_hotel_home_page.quit_phantomjs()
    def stop(self):
        self.thread_stop = True


def crawl_hotel_review_info_multi_thread(hotel_info_dict_list,time_sleep = 20,crawl_page_max=15,thread_number=5):
    hotel_info_list_per_thread = []
    for i in range(0,thread_number):
        hotel_info_list_per_thread.append([])

    for k in range(0,len(hotel_info_dict_list)):
        hotel_info_list_per_thread[k % thread_number].append(hotel_info_dict_list[k])

    thread_pool = []
    if len(hotel_info_dict_list) != 0:
        for i in range(0,thread_number):
            thread_pool.append(crawl_home_page_thread(hotel_info_dict_list=hotel_info_list_per_thread[i],time_sleep = time_sleep,crawl_page_max=crawl_page_max))
        for th in thread_pool:
            th.start()
        for th in thread_pool:
            th.join()



def load_all_cities_homepage_info(hotel_homepage_file):
    line_con_list = open(hotel_homepage_file,'r').readlines()
    city_homepage_list = [(line_con.strip().split('\t')[0],line_con.strip().split('\t')[1]) for line_con in line_con_list]
    return city_homepage_list

def get_finish_hotel_id_file(out_file = 'finish_hotel_id.txt'):
    in_file_fold = '../Data/HtmlData/TripAdvisorHotelReviewPage/'
    hotel_id_list = usefulAPI.get_dir_files(in_file_fold,False)
    finish_hotel_id_dict = {}
    for hotel_id in hotel_id_list:
        file_list = usefulAPI.get_dir_files(in_file_fold + hotel_id + '/',True)
        if len(file_list) < 10:
            for file in file_list:
                print file
                os.remove(file)
            os.rmdir(in_file_fold + hotel_id + '/')
        else:
            finish_hotel_id_dict[hotel_id] = 1
    out_line_con_list = []
    for key ,value in finish_hotel_id_dict.items():
        out_line_con_list.append(key)
    open(out_file,'w+').write('\n'.join(out_line_con_list))


def get_unfinish_hotel_id_list(hotel_info_dict_list,finish_hotel_id_file):
    print 'before delete finish hotel id......'
    print 'len(hotel_list): ' + str(len(hotel_info_dict_list))
    line_con_list = open(finish_hotel_id_file,'r').readlines()
    finish_hotel_id_dict = {}
    for line_con in line_con_list:
        finish_hotel_id_dict[line_con.strip()] = 1
    unfinish_hotel_info_dict_list = []
    for hotel_info_dict in hotel_info_dict_list:
        if finish_hotel_id_dict.has_key(hotel_info_dict['hotel_id']) == False:
            unfinish_hotel_info_dict_list.append(hotel_info_dict)
    print 'after delete finish hotel id......'
    print 'len(hotel_list): ' + str(len(unfinish_hotel_info_dict_list))
    return unfinish_hotel_info_dict_list

def load_finish_id_file(finish_hotel_id_file):
    line_con_list = open(finish_hotel_id_file,'r').readlines()
    finish_hotel_id_dict = {}
    for line_con in line_con_list:
        finish_hotel_id_dict[line_con.strip()] = 1
    return finish_hotel_id_dict

if __name__ == '__main__':
    get_finish_hotel_id_file()
    '''
    finish_hotel_id_file = 'finish_hotel_id.txt'

    filter_hotel_info_file = '../Data/TxtData/TripAdvisorHotelInCitesHomePage/filter_hotel_homepage_info_2_5.json'
    hotel_info_dict_list = usefulAPI.load_hotel_home_info_json(in_json_file=filter_hotel_info_file)
    unfinish_hotel_info_dict_list = get_unfinish_hotel_id_list(hotel_info_dict_list,finish_hotel_id_file)

    crawl_hotel_review_info_multi_thread(hotel_info_dict_list=unfinish_hotel_info_dict_list,
                                         time_sleep=10,
                                        crawl_page_max=100,
                                         thread_number=5)
    '''


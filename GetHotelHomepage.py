#coding=utf-8

# -------------------------------------------------------------------- #
# Get All hotel homepage in TripAdvisor
# Add Time: 2017-04-24
# -------------------------------------------------------------------- #

import bs4
from UsefulLibs import usefulForCrawl
import os
from selenium import webdriver
import time
import threading

class getHotelHomePage:
    def __init__(self,city_homepage_list,time_sleep = 20,crawl_page_max=15):
        self.time_sleep = time_sleep
        self.crawl_page_max = crawl_page_max
        self.city_homepage_list = city_homepage_list
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=cap)

    def get_page_number(self,page_content_bs):
        last_page_bs = page_content_bs.find('a',attrs={'class':'pageNum last taLnk '})
        if last_page_bs != None:
            return int(last_page_bs['data-page-number'])
        last_page_bs = page_content_bs.find('a',attrs={'class':'pageNum last current '})
        if last_page_bs != None:
            return int(last_page_bs['data-page-number'])
        return -1

    def get_next_page_url(self,page_num,basic_offset_value,begin_page_url):
        offset_value = (page_num - 1) * basic_offset_value
        temp_list = begin_page_url.split('-')
        out_list = []
        for i in range(0,len(temp_list)):
            out_list.append(temp_list[i])
            if i == 1:
                temp_str = 'oa' + str(offset_value)
                out_list.append(temp_str)
        next_page_url = '-'.join(out_list) + '#ACCOM_OVERVIEW'
        print next_page_url
        return next_page_url


    def crawl_hotel_home_page(self,city_name,city_hotel_homepage_url,out_file_fold,time_sleep = 0):
        if os.path.exists(out_file_fold) == False:
            os.mkdir(out_file_fold)
        page_num = 1
        out_file = out_file_fold + city_name + '_page_' + str(page_num) + '.html'
        if os.path.exists(out_file) == True:
            return
        self.driver.get(city_hotel_homepage_url)
        open(out_file,'w+').write(self.driver.page_source.encode('utf-8'))
            #url_content = self.driver.page_source
            #url_content = usefulForCrawl.get_html_content_from_a_page(city_hotel_homepage_url,time_sleep = time_sleep)
            #open(out_file,'w+').write(url_content)
        #else:
        #url_content = open(out_file,'r')
        while True:
            try:
                nextpage_url = self.driver.find_element_by_xpath('//a[@class="nav next taLnk ui_button primary"]')
                if nextpage_url == None: break
                nextpage_url.click()
                page_num = page_num + 1
                print 'time_sleep begin......'
                time.sleep(self.time_sleep)
                print 'time_sleep end......'
                out_file = out_file_fold + city_name + '_page_' + str(page_num) + '.html'
                open(out_file,'w+').write(self.driver.page_source.encode('utf-8'))
                if page_num >= self.crawl_page_max:
                    break
                print 'city_name: ' + city_name + '  PageNum: ' + str(page_num) + ' / ' + str(self.crawl_page_max)

            except Exception,e:
                print e
                break


        '''
        basic_offset_value = 30
        page_content_bs = bs4.BeautifulSoup(url_content,"html.parser")

        # next_page_bs = page_content_bs.find('a',attrs={'class':'nav next taLnk ui_button primary'})
        # if next_page_bs == None: return
        # if page_num == 1: basic_offset_value = int(next_page_bs['data-offset'])

        all_page_num = self.get_page_number(page_content_bs)
        if all_page_num == -1: return

        for page_num in range(2,all_page_num+1):
            print 'PageNum: ' + str(page_num) + ' / ' + str(all_page_num)
            self.get_next_page_url(page_num,basic_offset_value,city_hotel_homepage_url)
            out_file = out_file_fold + city_name + '_page_' + str(page_num) + '.html'
            if os.path.exists(out_file) == False:
                self.driver.get(city_hotel_homepage_url)
                open(out_file,'w+').write(self.driver.page_source.encode('utf-8'))
                #usefulForCrawl.download_page_using_phantomjs(self.driver,city_hotel_homepage_url,out_file,time_sleep=time_sleep)
                #url_content = usefulForCrawl.get_html_content_from_a_page(city_hotel_homepage_url,time_sleep = time_sleep)
                #open(out_file,'w+').write(url_content)
            if page_num == crawl_page_max: break
        '''
        #print 'Finished'

    def crawl_all_hotel_home_page(self):
        for i in range(0,len(self.city_homepage_list)):
            print 'CityNum: ' + str(i) + ' / ' + str(len(self.city_homepage_list))
            print 'CityName: ' + self.city_homepage_list[i][0].replace(' ','_')
            city_homepage = self.city_homepage_list[i]
            city = city_homepage[0].replace(' ','_')
            homepage = city_homepage[1].replace('https://www.tripadvisor.com/','https://www.tripadvisor.com/LangRedirect?auto=1&TAPD=tripadvisor.com&origin=null&returnTo=/')
            #homepage = city_homepage[1]
            out_file_fold = '../Data/HtmlData/TripAdvisorHotelInCitesHomePage/'
            print 'homepage: ' + homepage
            self.crawl_hotel_home_page(city,homepage,out_file_fold,time_sleep = self.time_sleep)

    def quit_phantomjs(self):
        self.driver.quit()


class crawl_home_page_thread(threading.Thread):
    def __init__(self,city_homepage_list,time_sleep = 20,crawl_page_max=15):
        threading.Thread.__init__(self)
        self.time_sleep = time_sleep
        self.crawl_page_max = crawl_page_max
        self.city_homepage_list = city_homepage_list
        self.thread_stop = False
    def run(self):
        get_hotel_home_page = getHotelHomePage(city_homepage_list=self.city_homepage_list,time_sleep = self.time_sleep,crawl_page_max=self.crawl_page_max)
        get_hotel_home_page.crawl_all_hotel_home_page()
        get_hotel_home_page.quit_phantomjs()
    def stop(self):
        self.thread_stop = True


def crawl_home_page_multi_thread(city_homepage_list,time_sleep = 20,crawl_page_max=15,thread_number=5):

    city_homepage_list_per_thread = []
    for i in range(0,thread_number):
        city_homepage_list_per_thread.append([])

    for k in range(35,len(city_homepage_list)):
        city_homepage_list_per_thread[k % thread_number].append(city_homepage_list[k])

    thread_pool = []
    if len(city_homepage_list) != 0:
        for i in range(0,thread_number):
            thread_pool.append(crawl_home_page_thread(city_homepage_list=city_homepage_list_per_thread[i],time_sleep = time_sleep,crawl_page_max=crawl_page_max))
        for th in thread_pool:
            th.start()
        for th in thread_pool:
            th.join()


def load_all_cities_homepage_info(hotel_homepage_file):
    line_con_list = open(hotel_homepage_file,'r').readlines()
    city_homepage_list = [(line_con.strip().split('\t')[0],line_con.strip().split('\t')[1]) for line_con in line_con_list]
    return city_homepage_list


if __name__ == '__main__':

    hotel_homepage_txt_file = '../Data/TxtData/TripAdvisorHotelHomePage/TripAdvisorHotelHomePage.txt'
    city_homepage_list = load_all_cities_homepage_info(hotel_homepage_txt_file)
    #get_hotel_home_page = getHotelHomePage(city_homepage_list=city_homepage_list,time_sleep = 20,crawl_page_max=15)
    #get_hotel_home_page.crawl_all_hotel_home_page()
    #get_hotel_home_page.quit_phantomjs()
    crawl_home_page_multi_thread(city_homepage_list=city_homepage_list,time_sleep = 10,crawl_page_max=15,thread_number=2)
#!/usr/bin/env python
#coding=utf8

import urllib2
import time


def get_html_content_from_a_page(url,time_sleep = 0):
    try:
        time.sleep(time_sleep)
        req = urllib2.Request(url)
        browser='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
        req.add_header('User-Agent',browser)
        response = urllib2.urlopen(req) 
        html_content=response.read()
        return html_content
    except:
        return ''

def get_html_content_from_a_page_multi_times(url,time_sleep,max_try_num):
    urllib2.socket.setdefaulttimeout(10)
    htmlContent = ''
    response = ''
    for tries in range(max_try_num):
        try :
            time.sleep(time_sleep)
            req = urllib2.Request(url)
            browser='Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
            req.add_header('User-Agent',browser)
            response = urllib2.urlopen(req)    
            break
        except :
            if tries < (max_try_num - 1) :
                time.sleep(6 * tries)
                continue
            else :
                print "Has tried " + str(max_try_num) + " times to access url " + url + ", all failed!";
                return htmlContent
    try:
        html_content=response.read()
        return html_content
    except:
        return ''


def download_page(filename,url,mode_type = 'w+',time_sleep = 0):
    content = get_html_content_from_a_page(url,time_sleep = time_sleep)
    open(filename,mode_type).write(content)


def download_page_using_phantomjs(phantomjs_driver,url,out_file,time_sleep = 20):
    phantomjs_driver.get(url)
    time.sleep(time_sleep)
    open(out_file,'w+').write(phantomjs_driver.page_source.encode('utf-8'))

if __name__ == '__main__':
    con = get_html_content_from_a_page('https://www.tripadvisor.com/MemberOverlay?Mode=owa&uid=02529ADBAA682501D747BC0F64FAB3C0&c=&src=LT_2555064&fus=false&partner=false&LsoId=&metaReferer=Hotel_Review',time_sleep = 0)
    download_page('a.html',con,mode_type = 'w+')


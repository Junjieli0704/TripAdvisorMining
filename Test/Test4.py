#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys    
import selenium.webdriver.support.ui as ui    
from selenium.webdriver.common.action_chains import ActionChains    
import time        
import re        
import os    
    
#打开Firefox浏览器 设定等待加载时间 访问URL    
driver = webdriver.PhantomJS()
driver_detail = webdriver.PhantomJS()
wait = ui.WebDriverWait(driver,10)    
driver.get("http://download.csdn.net/user/eastmount/uploads")    
SUMRESOURCES = 0 #全局变量 记录资源总数(尽量避免)
    
#获取列表页数 <div class="page_nav>共46个 共8页..</div>
def getPage():
    number = 0    
    wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='page_nav']"))    
    texts = driver.find_element_by_xpath("//div[@class='page_nav']").text    
    print texts    
    m = re.findall(r'(\w*[0-9]+)\w*',texts) #正则表达式寻找数字
    print m
    print '页数：' + str(m[1])
    print str(m[1])
    return int(m[1])
    
    
#获取URL和文章标题     
def getURL_Title(num):    
    global SUMRESOURCES    
    url = 'http://download.csdn.net/user/eastmount/uploads/' + str(num)    
    print unicode('下载列表URL: ' + url,'utf-8')    
    '''
    ' 等待最下面页面加载成功 获取URL和标题  
    ' 源码  
    ' <div class='list-container mb-bg'>  
    '     <dl>  
    '        <dt>  
    '           <div class="icon"><img src="xxx"></img></div>  
    '           <h3><a href="/detail/eastmount/8757243">MFC显示BMP图片</a></h3>  
    '        </dt>  
    '     </dl>  
    ' </div>  
    ' get_attribute('href')获取URL且自动补齐  
    ' unicode防止报错 - s.encode('utf8')unicode转换成utf8编码 decode表示utf8转换成unicode  
    '''    
    driver.get(url)    
    wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='page_nav']"))    
    list_container = driver.find_elements_by_xpath("//div[@class='list-container mb-bg']/dl/dt/h3/a")   
    for title in list_container:    
        print 'Num' + str(SUMRESOURCES +1)    
        print u'标题: ' + title.text    
        print u'链接: ' + title.get_attribute('href')    
        SUMRESOURCES = SUMRESOURCES +1    
        #    
        #获取具体内容和评论    
        getDetails( str(title.get_attribute('href')) )
    else:    
        print ' ' #换行    
            
    
#获取详细信息 因前定义的driver正在使用中 故调用driver_detail    
#否则报错 Message: Error Message => 'Element does not exist in cache'    
def getDetails(url):
    print url
    #获取infobox    
    driver_detail.get(url)    
    details = driver_detail.find_element_by_xpath("//div[@class='conLi clearfix']").text
    print details    
    #加载评论 <dl><dt></dt><dd></dd></dl>    
    comments = driver_detail.find_elements_by_xpath("//dd[@class='detal']")
    print comments
    for com in comments:    
        print u'评论：' + com.text    
    else:    
        print ' ' #换行    
         
    
#主函数    
def main():    
    start = time.clock()    
    pageNum = getPage()    
    i=3
    #循环获取标题和URL    
    while(i<=pageNum):    
        getURL_Title(i)     
        i = i + 1    
    else:    
        print 'SUmResouces: ' + str(SUMRESOURCES)    
        print 'Load Over'    
    end = time.clock()    
    print "Time: %f s" % (end - start)    
            
main()    
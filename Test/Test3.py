from selenium import webdriver
import time
import selenium.webdriver.support.ui as ui

print '--------------------------------'
cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.loadImages"] = False
driver = webdriver.PhantomJS(desired_capabilities=cap)
#driver.get('https://www.tripadvisor.com/LangRedirect?auto=1&TAPD=tripadvisor.com&origin=null&returnTo=/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html')
#driver.get('https://www.tripadvisor.com/MemberOverlay?Mode=owa&uid=02529ADBAA682501D747BC0F64FAB3C0&c=&src=LT_2555064&fus=false&partner=false&LsoId=&metaReferer=Hotel_Review')
driver.get('https://www.tripadvisor.com/members/JamesE339')
#wait.until(lambda driver: self.driver.find_element_by_xpath('//li[@data-filter="REVIEWS_HOTELS"]'))
nextpage_url = driver.find_element_by_xpath('//li[@data-filter="REVIEWS_HOTELS"]')
nextpage_url.click()
time.sleep(10)
print '--------------------------------'
wait = ui.WebDriverWait(driver,10)
wait.until(lambda driver: driver.find_element_by_xpath('//button[@id="cs-paginate-next"]'))
nextpage_url = driver.find_element_by_xpath('//button[@id="cs-paginate-next"]')
nextpage_url.click()
print '--------------------------------'
time.sleep(10)
data = driver.page_source
data = data.encode('utf-8')
open('georgiamelissa.html','w+').write(data)
#print data
driver.quit()
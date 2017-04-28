from selenium import webdriver


cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.loadImages"] = False
driver = webdriver.PhantomJS(desired_capabilities=cap)
#driver.get('https://www.tripadvisor.com/LangRedirect?auto=1&TAPD=tripadvisor.com&origin=null&returnTo=/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html')
driver.get('https://www.tripadvisor.com/MemberOverlay?Mode=owa&uid=02529ADBAA682501D747BC0F64FAB3C0&c=&src=LT_2555064&fus=false&partner=false&LsoId=&metaReferer=Hotel_Review')
data = driver.page_source
data = data.encode('utf-8')
open('ddd2.html','w+').write(data)
#print data
driver.quit()
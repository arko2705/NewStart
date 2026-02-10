import csv
from selenium.webdriver.common.by import By
from CodeLogic import EdgeCases, search as s
import undetected_chromedriver as udc
from newstartapp.models import Num,QueryStartStat,Num1,UserChoice,OutputFile
from django.core.files import File
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from urllib.parse import quote_plus
from django.conf import settings
import os
##locators have been used btw
def commonEL(self,Website,Company,driven,prompt): ##special character '&' is messing urls up. Google has its own encoding
        initial_query="https://www.google.com/search?q="
        if prompt !=" business" and Website and Website.startswith("https") and Website.endswith("/"):
               #print("i was here in website")
               iweb=Website[:len(Website)-1]
               fweb=iweb.replace("https://","")
               final_query=initial_query+fweb+prompt
        else:     
              final_query=initial_query+quote_plus(Company)+prompt
        print(final_query)
        sleep=random.randrange(3,10)
        time.sleep(sleep)
        try:
            driven.uc_open_with_reconnect(final_query, reconnect_time=sleep/10)
            driven.find_element(By.XPATH,"//div[@class='sjVJQd pt054b']").click()  ##That give your location prompt that comes up in incognito so that they can give more accurate results
        except:
            pass
        WebDriverWait(driven, 10).until(
             EC.presence_of_element_located((By.XPATH, "//body"))
        )
        
def linkedin(driven):
        linkedin="Not present on google business profiles"
        try:
          webelements= driven.find_elements(By.CSS_SELECTOR, "a[href*='linkedin']")
          for x in webelements:
                     linkedin=x.get_attribute("href")
                     break         #breaking cuz the first link is the most accurate one usually
        except:
               driven.save_screenshot('ss_Ldebug.png')
               linkedin="Trouble rendering linkedin"
        driven.save_screenshot('ss_Ldebug.png')
        return linkedin

def email(driven):
        emaillist=[]
        try:
              emailwebelements = driven.find_elements(By.XPATH, "//em[contains(text(),'@')]") 
              for b in emailwebelements:
                  if b.text not in emaillist:
                    emaillist.append(b.text)
        except:
               emailwebelements="Trouble rendering email"
        driven.save_screenshot('ss_Edebug.png')
        return emaillist

def commonStart(a):
        googling_it,your_query=s.search(a)
        #driver=udc.Chrome(headless=True,use_subprocess=False,version_main=144)
        options = udc.ChromeOptions()
        options.binary_location = "/usr/bin/chromium"
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver=udc.Chrome(options=options,use_subprocess=True,version_main=144)##version_main=144
        driver.get(googling_it)
        try:
          wait = WebDriverWait(driver, 15)
          accept_btn = wait.until(
          EC.element_to_be_clickable((
          By.XPATH,
          "//button[.//text()[contains(., 'Godkänn alla')]]"
    ))
)
          driver.execute_script("arguments[0].click();", accept_btn)
        except:
            try: 
                  accept_btn = wait.until(
                  EC.element_to_be_clickable((
        By.XPATH,
        "//*[@role='button' and .//text()[contains(., 'Godkänn alla')]]"
    ))
)

                  driver.execute_script("arguments[0].click();", accept_btn)
            except:
               pass
            pass
        cond=True
        z=0
        while cond:
            try:
                driver.find_element(By.CLASS_NAME,"HlvSq")#to indicate end to it all
                cond=False
            except:
                pass
            try:
              panel = driver.find_element(By.XPATH, '//div[@role="feed"]')
              panel.send_keys(Keys.PAGE_DOWN)
              time.sleep(0.05)
            except:
                 driver.save_screenshot('ss_debug.png')
                 pass
            driver.save_screenshot(os.path.join(settings.MEDIA_ROOT, "outputs", "screenshots", "ss_debug1.png"))
            try:
                driver.title   #just to check if driver is alive. Gotta create a "driver is closed" page and find a way to handle it seperately from the spamming requests thingie.
            except:
                EdgeCases.model_update(-1,"RESTING")
                return "kill","this","process"
            try:   ##this one's to just check if some bullshit search query got made that has no results at all
                 driver.find_element(By.CSS_SELECTOR,".m6QErb.Pf6ghf.XiKgde.ecceSd.tLjsW")
                 EdgeCases.model_update(-2,"RESTING")   ###means no results found for the query
                 return "kill","this","process" 
            except:
                 pass
            try:
                 driver.find_element(By.CSS_SELECTOR,".Q2vNVc.fontHeadlineSmall")
                 EdgeCases.model_update(-2,"RESTING")  ###means no results found for the query
                 return "kill","this","process" 
            except:
                 pass
            z=z+1
            time.sleep(1)
            if z==60:
                break
        try:
          finder=driver.find_elements(By.CLASS_NAME,"hfpxzc") #to find all the links once end reached
        except:
           EdgeCases.model_update(-1,"RESTING")    ###means captcha is open and we are cooked.
           return "kill","this","process"
        return finder,your_query,driver

def commonWait():
   c=0
   while True:##this waits till a user inputs some value inside the num1's limit.Else it will progress before the user inputs anything.
      if Num1.objects.last():
         break
      else:
             time.sleep(5) ##saving cpu power lmao
             c=c+1
      print(c)
      if QueryStartStat.objects.last() and QueryStartStat.objects.last().stat=="RESTING" :
            return "kill"

      if c==60 :                            ##If people enter a query more late than 5 minutes,then that shi terminates.
         QueryStartStat(stat="TOOLONG").save()  ##In case people request but dont enter anything, and are at the number.html page.Also to indicate process ended for when it took too long to load(next line)
         UserChoice(choice=0).save()
         return "kill"
   return "continue" 

def csv_store(element_list,your_query,headers):
        path = f"media/outputs/{your_query}.csv"
        with open(path,'w',newline='',encoding='UTF-8') as f: 
            write=csv.writer(f)
            write.writerow(headers)
            write.writerows(element_list)
        with open(path, "rb") as f:
            obj = OutputFile.objects.create(
            file=File(f, name=f"{your_query}.csv")
        )
        print("Remember to extend your row width in the csv files,for it to look prettier and better!")
        return obj

def website(driver):
           driver.save_screenshot('ss_Wdebug.png')
           ProbableWebSites=[]
           WebSite=None                  #new concept here
           try:
              WebFinder=driver.find_elements(By.CSS_SELECTOR,".lcr4fd.S9kvJb")
              for g in WebFinder:
                 ProbableWebSites.append(g.get_attribute("href"))
              for h in ProbableWebSites:
                 if h.startswith("http") and not h[-1].isdigit() and not h.startswith("https://api.whatsapp"):
                     WebSite=h
                     break
              if WebSite is None:
                  WebSite="Not present on google business profiles"   
           except:
              WebSite="Not present on google business profiles"
           return WebSite
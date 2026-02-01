import csv
from selenium.webdriver.common.by import By
from CodeLogic import search as s
import undetected_chromedriver as udc
from newstartapp.models import Num,QueryStartStat,Num1,UserChoice,OutputFile
from django.core.files import File
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
##locators have been used btw
def commonEL(self,Website,Company,driven,prompt):
        initial_query="https://www.google.com/search?q="
        if prompt !=" business" and Website and Website.startswith("https") and Website.endswith("/"):
               print("i was here in website")
               iweb=Website[:len(Website)-1]
               fweb=iweb.replace("https://","")
               final_query=initial_query+fweb+prompt
        else:     
              print("I was here in company")  
              if '|' in Company:
                OnlyCompany=Company.split('|')
                Company_array=OnlyCompany[0].split(' ')
              else:
                   Company_array=Company.split(' ')
              for f in Company_array:
                 initial_query=initial_query+"+"+f
              final_query=initial_query+prompt
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
                     break
        except:
               driven.save_screenshot('Ldebug.png')
               linkedin="Trouble rendering linkedin"
        driven.save_screenshot('Ldebug.png')
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
        driven.save_screenshot('Edebug.png')
        return emaillist

def commonStart(a):
        b=0
        print("Starting headless browser for link extraction")
        googling_it,your_query=s.search(a)
        driver=udc.Chrome(headless=True,use_subprocess=False,version_main=144)
        if QueryStartStat.objects.last() and QueryStartStat.objects.last().stat=="RESTING":
            driver.quit()
            return "kill","this","process",
        driver.get(googling_it)
        cond=True
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
                 driver.save_screenshot('debug.png')
                 pass
            driver.save_screenshot('debug1.png')
            try:
                driver.title   #just to check if driver is alive. Gotta create a "driver is closed" page and find a way to handle it seperately from the spamming requests thingie.
            except:
                Num(companynumber=-1).save()
                QueryStartStat(stat="RESTING").save()
                return "kill","this","process"
            b=b+1
            if b==100:
                break
        try:
          finder=driver.find_elements(By.CLASS_NAME,"hfpxzc") #to find all the links once end reached
        except:
           Num(companynumber=-1).save()    ###means captcha is open and we are cooked.
           QueryStartStat(stat="RESTING").save()
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
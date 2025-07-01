from threading import Thread
from selenium.webdriver.chrome.service import Service
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import pyautogui # type: ignore
import undetected_chromedriver as udc # type: ignore
import time
from seleniumbase import Driver
import os
import csv
import sys
import search as s
import sys
#didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs page
class returningThread(Thread):
    def __init__(self,group=None,target=None,name=None,args=(),kwargs={}):
        Thread.__init__(self,group,target,name,args,kwargs)
        self._returnit=None
    def run(self):
        if self._target is not None:  
            self._returnit=self._target(*self._args,**self._kwargs)
    def join(self, timeout = None):
        Thread.join(self)
        return self._returnit

class Logic:
  
    def link_generation(self):##python automatically gives a positional arguement when we call it,so we must write "self"
        googling_it,your_query=s.search()
        driver=udc.Chrome(version_main=137,use_subprocess=False)
        driver.get(googling_it)
        cond=True
        while cond:
            try:
                driver.find_element(By.CLASS_NAME,"HlvSq")#to indicate end to it all
                cond=False
            except:
                pass
            time.sleep(0.05)
            pyautogui.scroll(-400)
        finder=driver.find_elements(By.CLASS_NAME,"hfpxzc") #to find all the links once end reached
        link_list=[]
        company_list=[]
        phone_list=[]
        for i in finder:
            if i.get_attribute("href") not in link_list:
                company_list.append(i.get_attribute("aria-label"))
                link_list.append(i.get_attribute("href"))
        driver.quit()
        print(f"{len(link_list)} companies found.")
        print("Enter the number of companies you would like to get the information for: ")
        loop_number=input()
        return link_list,your_query,loop_number,company_list
       
    def InstanceProvider(self):
       GBPdriver=Driver(uc=True, headless=True,block_images=True)
       emaildriver=Driver(uc=True,headless=True,block_images=True)
       linkedindriver=Driver(uc=True,headless=True,block_images=True)
       return GBPdriver,emaildriver,linkedindriver
    def link_getter(self,i,driver):
        driver.uc_open_with_reconnect(i, reconnect_time=0.1)
        return
    def company(self,i,driven):
           time.sleep(0.3)
           try: 
            CFinder=driven.find_element(By.CSS_SELECTOR, ".m6QErb.Pf6ghf.XiKgde.ecceSd.tLjsW")
            time.sleep(0.1)
            NeedToStrip=CFinder.get_attribute("aria-label")
            Company=NeedToStrip.replace("Actions for ","")
           except:
             print("Trouble rendering company")
             Company="Not present on google business profiles"
           return Company
    def website(self,driver):
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

    def address_PhoneNumber(self,driven):#Gotta fix the address logic by a bit
           try:   
             AFinder=driven.find_element(By.CLASS_NAME,"CsEnBe")
             time.sleep(0.1)
             NeedToClean=AFinder.get_attribute("aria-label")
             Address="Not present on google business profiles"
             if NeedToClean.startswith("Address: "):
                Address=NeedToClean.replace("Address: ","")
           except:
              print("Trouble rendering address")
              Address="Not present on google business profiles"
            
           PFinders=driven.find_elements(By.CSS_SELECTOR,".Io6YTe.fontBodyMedium.kR99db.fdkmkc")
           PhoneNumber="Not present on google business profiles"
           for f in PFinders:
             try: 
                 b=int(f.text.replace(" ",""))+1 
                 PhoneNumber=f.text.replace(" ","")
                 break
             except:
               PhoneNumber="Not present on google business profiles"
           return Address,PhoneNumber
    
    def email(self,Company,Website,driven):
        initial_query="https://www.google.com/search?q="
        if Website and Website.startswith("https") and Website.endswith("/"):
               iweb=Website[:len(Website)-1]
               fweb=iweb.replace("https://","")
               final_query=initial_query+fweb+"+email+address"

        else:       
              OnlyCompany=Company.split('|')
              Company_array=OnlyCompany[0].split(' ')
              for f in Company_array:
                 initial_query=initial_query+"+"+f
              final_query=initial_query+"+email+address"
        try:
            driven.uc_open_with_reconnect(final_query, reconnect_time=0.1)
            driven.find_element(By.XPATH,"//div[@class='sjVJQd pt054b']").click()  ##That give your location prompt that comes up in incognito so that they can give more accurate results
        except:
            pass
        emaillist=[]
        try:
              emailwebelements = driven.find_elements(By.XPATH, "//em[contains(text(),'@')]") 
              for b in emailwebelements:
                  if b.text not in emaillist:
                    emaillist.append(b.text)
        except:
               emailwebelements="Not found"
        return emaillist
    
    def linkedin(self,Website,Company,driven):
        initial_query="https://www.google.com/search?q="
        if Website and Website.startswith("https") and Website.endswith("/"):
               iweb=Website[:len(Website)-1]
               fweb=iweb.replace("https://","")
               final_query=initial_query+fweb+"+linkedin"

        else:       
              OnlyCompany=Company.split('|')
              Company_array=OnlyCompany[0].split(' ')
              for f in Company_array:
                 initial_query=initial_query+"+"+f
              final_query=initial_query+"+linkedin"
        try:
            driven.uc_open_with_reconnect(final_query, reconnect_time=0.1)
            driven.find_element(By.XPATH,"//div[@class='sjVJQd pt054b']").click()  ##That give your location prompt that comes up in incognito so that they can give more accurate results
        except:
            pass
        linkedin="Could not render"
        try:
              webelement= driven.find_element(By.CLASS_NAME, "zReHs") 
              linkedin=webelement.get_attribute("href")
        except:
               linkedin="Not found"
        return linkedin


    
    def csv_store(self,element_list,your_query):
        with open(f'ABusiness Profile-{your_query}.csv','w',newline='',encoding='UTF-8') as file: 
            Columns=['Company Name','Address','Phone Number','Google business profile link','Website','E-Mail','Linkedin-Link']
            write=csv.writer(file)
            write.writerow(Columns)
            write.writerows(element_list)
            print("Remember to extend your row width in the csv files,for it to look prettier and better!")

def main():
   logic=Logic()  ##need to make an instance first
   link_list,your_query,loop_number,company_list=logic.link_generation()    ##gotta access a class's methods like this,how else
   GBPdriver,emaildriver,ldriver=logic.InstanceProvider()
   GBPdriver.implicitly_wait(5)
   emaildriver.implicitly_wait(5)
   ldriver.implicitly_wait(5)
   start=time.time()
   loop_count=0
   element_list=[]

   for i in link_list:
      if loop_count<int(loop_number):
         #LT=returningThread(target=logic.link_getter,args=(i,GBPdriver))
         #LT.start()
         #LT.join()
         Company=company_list[loop_count]
         logic.link_getter(i,GBPdriver)
         WT=returningThread(target=logic.website,args=(GBPdriver,))
         APT=returningThread(target=logic.address_PhoneNumber,args=(GBPdriver,))##arguement must be a tuple,hence the comma
         WT.start()
         APT.start()
         website=WT.join()
         ET=returningThread(target=logic.email,args=(Company,website,emaildriver))
         LIT=returningThread(target=logic.linkedin,args=(website,Company,ldriver))
         ET.start()
         LIT.start()
         emaillist=ET.join()
         linkedin=LIT.join()
         Address,PhoneNumber=APT.join()

         element_list.append([Company,Address,PhoneNumber,i,website,emaillist,linkedin])
         loop_count=loop_count+1
      else:
        GBPdriver.quit()
        emaildriver.quit()
        ldriver.quit()
        break

   print(element_list)
   end=time.time()
   print(f"{end-start} seconds taken")
   store_in_csv=input("Store in csv:Yes or no:\n")
   if store_in_csv.lower()=="yes":
       logic.csv_store(element_list,your_query)
  
if __name__=='__main__':
    main()  

from selenium.webdriver.common.by import By
import time
from seleniumbase import Driver
from newstartapp.models import Num
from CodeLogic import common
from django.shortcuts import render
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Logic:
    def link_generation(self,a):                               ##python automatically gives a positional arguement when we call it,so we must write "self"
        finder,your_query,driver=common.commonStart(a)
        if(finder=='kill'):
            return 'kill','this'
        link_list=[]
        for i in finder:
            if i.get_attribute("href") not in link_list:
                link_list.append(i.get_attribute("href"))
        driver.quit()
        Num(companynumber=len(link_list)).save()
        return link_list,your_query
       
    def InstanceProvider(self):
       GBPdriver=Driver(uc=True, headless=True,block_images=True)
       emaildriver=Driver(uc=True,headless=True,block_images=True)
       linkedindriver=Driver(uc=True,headless=True,block_images=True)
       return GBPdriver,emaildriver,linkedindriver
    def link_getter(self,i,driver):
        driver.uc_open_with_reconnect(i, reconnect_time=0.1)
        return
    def company(self,driven):
           WebDriverWait(driven, 10).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, ".m6QErb.Pf6ghf.XiKgde.ecceSd.tLjsW"))
        )
           try: 
            CFinder=driven.find_element(By.CSS_SELECTOR, ".m6QErb.Pf6ghf.XiKgde.ecceSd.tLjsW")
            NeedToStrip=CFinder.get_attribute("aria-label")
            Company=NeedToStrip.replace("Actions for ","")
           except:
             print("Trouble rendering company")
             Company="Could not render from google business profiles"
           return Company

    def address_PhoneNumber(self,driven):#Gotta fix the address logic by a bit
           try:   
             AFinder=driven.find_element(By.CLASS_NAME,"CsEnBe")
             #time.sleep(0.1)
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
        common.commonEL(self,Website,Company,driven,prompt="+email+address")    
        emaillist=common.email(driven)
        return emaillist
    
    def linkedin(self,Website,Company,driven):
        common.commonEL(self,Website,Company,driven,prompt=" business")
        linkedin=common.linkedin(driven)
        return linkedin

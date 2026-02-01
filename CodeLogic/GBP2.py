from selenium.webdriver.common.by import By
import time
from seleniumbase import Driver
import csv
from newstartapp.models import Num,HeaderList
from CodeLogic import common   
class Logic:
    def link_generation(self,a):                         ##python automatically gives a positional arguement when we call it,so we must write "self"
        finder,your_query,driver=common.commonStart(a)        
        if(finder=='kill'):
            return 'kill','this','process'
        link_list=[]
        company_list=[]
        for i in finder:
            if i.get_attribute("href") not in link_list:
                company_list.append(i.get_attribute("aria-label"))
                link_list.append(i.get_attribute("href"))
        driver.quit()
        Num(companynumber=len(link_list)).save()
        return link_list,your_query,company_list
    
    def G_InstanceProvider(self):
       GBPdriver=Driver(uc=True, headless=True,block_images=True)
       return GBPdriver
    
    def E_InstanceProvider(self):
       emaildriver=Driver(uc=True,headless=True,block_images=True)
       return emaildriver
    
    def L_InstanceProvider(self):
       linkedindriver=Driver(uc=True,headless=True,block_images=True)
       return linkedindriver
    
    def link_getter(self,i,driver):
        driver.uc_open_with_reconnect(i, reconnect_time=0.1)
        return

    def address(self,driven):#Gotta fix the address logic by a bit
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
           return Address
    
    def PhoneNumber (self,driven):
           PFinders=driven.find_elements(By.CSS_SELECTOR,".Io6YTe.fontBodyMedium.kR99db.fdkmkc")
           PhoneNumber="Not present on google business profiles"
           for f in PFinders:
             try: 
                 b=int(f.text.replace(" ",""))+1 
                 PhoneNumber=f.text.replace(" ","")
                 break
             except:
               PhoneNumber="Not present on google business profiles"
           return PhoneNumber
    
    def email(self,Company,Website,driven):
        common.commonEL(self,Website,Company,driven,prompt="+email+address")    
        emaillist=common.email(driven)
        return emaillist
    
    def linkedin(self,Website,Company,driven):
        common.commonEL(self,Website,Company,driven,prompt="+linkedin+profile")
        linkedin=common.linkedin(driven)
        return linkedin
    
    def headers(self,user_choices): #email is alwyas appended first,hence email comes early,but in one of the results i saw email being appended later,and idk how's that happening.
           HeaderList.objects.all().delete()
           heading_list=[]
           Company="Company"
           email=''
           linkedin=''
           address=''
           phonenumber=''
           maplink=''
           website=''
           for x in user_choices:
            match x:
              case '1':
                 address="Address"
              case '2':
                  phonenumber="Phone Number"
              case '3':
                 maplink="Map Link"
              case '4':
                 website="Website"
              case '5':
                  email="E mail"
              case '6':
                  linkedin="Linkedin"
           for i in [Company,address,phonenumber,maplink,website,email,linkedin]:
               if(i!=''):
                   heading_list.append(i)
           HeaderList(Company="Company",Address=address,PhoneNumber=phonenumber,MapLink=maplink,Website=website,Email=email,Linkedin=linkedin).save()
           return heading_list
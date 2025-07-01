from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as udc
import time
import csv
import pyautogui

##Its done here,i took all the values of a single page and could get back names,addresses and phone numbers in abt 6-7 mins.Around 120 companies
def sick():
    driver=udc.Chrome(use_subprocess=False,)
    driver.implicitly_wait(1)
    driver.get("https://www.google.com/maps/search/digital+marketing+companies+in+kolkata/@22.5987975,88.3832932,13z?entry=ttu&g_ep=EgoyMDI1MDYxMS4wIKXMDSoASAFQAw%3D%3D")
    pyautogui.click(308,441)
    cond=True
    while cond:
        try:
            driver.find_element(By.CLASS_NAME,"HlvSq")#to indicate end to it all
            cond=False
        except:
            pass
        time.sleep(0.1)
        pyautogui.scroll(-300)
    finder=driver.find_elements(By.CLASS_NAME,"hfpxzc") #to find all the links once end reached
    link_list=[]
    for i in finder:
        link_list.append(i.get_attribute("href"))
    element_list=[]
    driver.quit()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driven=webdriver.Chrome(options=options)
    driven.implicitly_wait(5)
    for i in link_list:
        driven.get(i)
        time.sleep(0.2)
        try: 
            finding=driven.find_element(By.CSS_SELECTOR, ".hh2c6.G7m0Af")
            NeedToStrip=finding.get_attribute("aria-label")
            time.sleep(0.3)
            Company=NeedToStrip.replace("Overview of ","")
        except:
            print("Trouble rendering company")#I tried for 70 profiles.Around 6-7/70 values were missed
            Company="Not present on google business profiles"

        try:   
            find=driven.find_element(By.CLASS_NAME,"CsEnBe")
            time.sleep(0.3)
            Address=find.get_attribute("aria-label")
        except:
            print("Trouble rendering address")
            Address="Not present on google business profiles"

        finders=driven.find_elements(By.CSS_SELECTOR,".Io6YTe.fontBodyMedium.kR99db.fdkmkc")
        time.sleep(0.3)
        for i in finders:
             try: 
              a=i.text.replace(" ","")
              b=int(a)+1 
              PhoneNumber=i.text
              break
             except:
              PhoneNumber="Not present on google business profiles"
        condition=True
        for x in element_list:
            if Company in x:
               condition=False
        if condition==True:
            element_list.append([Company,Address,PhoneNumber])
        
    print(element_list)

    

    with open('Test4.csv','w',newline="") as file:
        write=csv.writer(file)
        write.writerow(link_list)

if __name__=='__main__':
    sick()

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#This code prooves i can extract values using headless browser
 
def anothertest():
    link_list=['https://www.google.com/maps/place/Digitalsouvik.in+%7C+Best+Digital+Marketing+Consultant+In+Kolkata+%7C+Best+Digital+Marketing+Agency+In+Kolkata/@31.6534075,-15.0170731,3z/data=!4m10!1m2!2m1!1sdigital+marketing+agencies+near+me!3m6!1s0x39f89dcf771233df:0x3866547448048742!8m2!3d22.6246532!4d88.3849642!15sCiJkaWdpdGFsIG1hcmtldGluZyBhZ2VuY2llcyBuZWFyIG1lIgOQAQFaJCIiZGlnaXRhbCBtYXJrZXRpbmcgYWdlbmNpZXMgbmVhciBtZZIBGmludGVybmV0X21hcmtldGluZ19zZXJ2aWNlqgF0CggvbS8wZzRnchABKh4iGmRpZ2l0YWwgbWFya2V0aW5nIGFnZW5jaWVzKAAyHhABIhoW9BLDIQlx4npEMojpt7QmHC_EiEbMrtuo_TImEAIiImRpZ2l0YWwgbWFya2V0aW5nIGFnZW5jaWVzIG5lYXIgbWXgAQA!16s%2Fg%2F11j2fllw3s?entry=ttu&g_ep=EgoyMDI1MDYxMS4wIKXMDSoASAFQAw%3D%3D',
               'https://www.google.com/maps/place/Aspire+Digital+Media+%7C+Digital+Marketing+Agency+in+Kolkata/@31.6534075,-15.0170731,2z/data=!4m10!1m2!2m1!1sdigital+marketing+agencies+near+me!3m6!1s0x3a02778db61fc687:0xbcb4d7b570b71376!8m2!3d22.5965172!4d88.3992741!15sCiJkaWdpdGFsIG1hcmtldGluZyBhZ2VuY2llcyBuZWFyIG1lIgOQAQFaJCIiZGlnaXRhbCBtYXJrZXRpbmcgYWdlbmNpZXMgbmVhciBtZZIBGmludGVybmV0X21hcmtldGluZ19zZXJ2aWNlmgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVU5LZEUxNlozZEJSUkFCqgF0CggvbS8wZzRnchABKh4iGmRpZ2l0YWwgbWFya2V0aW5nIGFnZW5jaWVzKAAyHhABIhoW9BLDIQlx4npEMojpt7QmHC_EiEbMrtuo_TImEAIiImRpZ2l0YWwgbWFya2V0aW5nIGFnZW5jaWVzIG5lYXIgbWXgAQD6AQUI_AIQRQ!16s%2Fg%2F11fp1dm745?entry=ttu&g_ep=EgoyMDI1MDYxMS4wIKXMDSoASAFQAw%3D%3D']
    element_list=[]
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

if __name__=="__main__":
    anothertest()
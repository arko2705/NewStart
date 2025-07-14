import time
from CodeLogic.GBP2 import Logic   #WOW
from CodeLogic.customthread import returningThread
from newstartapp.models import Num1,GBPInfo
                                                                 #didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs page
def main(a,user_choices):
   user_choices.sort()
   logic=Logic()                                                 ##need to make an instance first
   link_list,your_query,company_list=logic.link_generation(a)    ##gotta access a class's methods like this,how else
   c=0
   while True:                                                   ##this waits till a user inputs some value inside the num1's limit.Else it will progress before the user inputs anything.
      if Num1.objects.last():
         break
      else:
           if c<5:
             time.sleep(5)                                       ##saving cpu power lmao

           else:
             time.sleep(2)
           c=c+1
   start=time.time()
   loop_number=Num1.objects.last().limit
   heading_list=logic.headers(user_choices)    
   GBPdriver=logic.G_InstanceProvider()
   GBPdriver.implicitly_wait(5)
   emaildriver=None
   ldriver=None
   if '1' in user_choices:
      emaildriver=logic.E_InstanceProvider()
      emaildriver.implicitly_wait(5)
   if '2' in user_choices:
      ldriver=logic.L_InstanceProvider()
      ldriver.implicitly_wait(5) 
   loop_count=0
   element_list=[]
   Address=''
   PhoneNumber=''
   MapLink=''
   Web=''
   email=''
   linkedin=''
   for i in link_list:
     if loop_count<int(loop_number):
        logic.link_getter(i,GBPdriver)         ##opens us the link of profile in each iteration
        if  '1' in user_choices or '2' in user_choices or '6' in user_choices:
           Website=logic.website(GBPdriver)
        threds=[]             ##Storing threads in a list,damn.
        result=[]          
        result.append(company_list[loop_count])
        for x in user_choices:
            match x:
              case '1':
                  ET=returningThread(target=logic.email,args=(company_list[loop_count],Website,emaildriver))
                  ET.start()
                  threds.append(ET)
              case '2':
                  LIT=returningThread(target=logic.linkedin,args=(Website,company_list[loop_count],ldriver))
                  LIT.start()
                  threds.append(LIT)
                    
              case '3':
                  Address=logic.address(GBPdriver)
                  GBPInfo(Address=Address).save()
                  result.append(Address)
              case '4':
                  PhoneNumber=logic.PhoneNumber(GBPdriver)
                  GBPInfo(PhoneNumber=PhoneNumber).save()
                  result.append(PhoneNumber)

              case '5':
                   MapLink=i
                   GBPInfo(MapLink=i).save()
                   result.append(i)

              case '6':
                  Web=Website
                  GBPInfo(Website=Website).save()
                  result.append(Website)
        if '1' in user_choices:
           email=ET.join()
        
        if '2' in user_choices:
           linkedin=LIT.join()
                   #for a in threds:
           #result.append(a.join())  
        GBPInfo(Company=company_list[loop_count],Address=Address,PhoneNumber=PhoneNumber,MapLink=MapLink,Wesbite=Web,Email=email,Linkedin=linkedin)
        element_list.append(result) 
        loop_count=loop_count+1
     else:
        GBPdriver.quit()
        if emaildriver is not None:
           emaildriver.quit()
        if ldriver is not None:
           ldriver.quit()
        break
                  
   print(element_list)
   end=time.time()
   print(user_choices)
   print("user list printed")
   print(f"{end-start} seconds taken")
   store_in_csv=input("Store in csv:Yes or no:\n")
   if store_in_csv.lower()=="yes":
       logic.csv_store(element_list,your_query,heading_list)
   return
  
if __name__=='__main__':
    main()  

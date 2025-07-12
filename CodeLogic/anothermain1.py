import time
from CodeLogic.GBP2 import Logic   #WOW
from CodeLogic.customthread import returningThread
#didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs page
def main(a,user_choices):
   logic=Logic()  ##need to make an instance first
   link_list,your_query,loop_number,company_list=logic.link_generation(a)    ##gotta access a class's methods like this,how else
   print("Enter which of the fields you would like:")
   print("1.E-mail 2.Linkedin 3.Address  4.Phone Number 5.Maplink 6.Website 7.Only Company\n Enter a number from 1-6")
   #user_choices=logic.UserChoices()
   start=time.time()
   heading_list=logic.headers(user_choices)    
   GBPdriver=logic.G_InstanceProvider()
   GBPdriver.implicitly_wait(5)
   emaildriver=None
   ldriver=None
   if 1 in user_choices:
      emaildriver=logic.E_InstanceProvider()
      emaildriver.implicitly_wait(5)
   if 2 in user_choices:
      ldriver=logic.L_InstanceProvider()
      ldriver.implicitly_wait(5) 
   loop_count=0
   element_list=[]
   for i in link_list:
     if loop_count<int(loop_number):
        logic.link_getter(i,GBPdriver)
        if  1 in user_choices or 2 in user_choices or 6 in user_choices:
           Website=logic.website(GBPdriver)
        threds=[]
        result=[]
        result.append(company_list[loop_count])
        for x in user_choices:
            match x:
              case 1:
                  ET=returningThread(target=logic.email,args=(company_list[loop_count],Website,emaildriver))
                  ET.start()
                  threds.append(ET)
              case 2:
                  LIT=returningThread(target=logic.linkedin,args=(Website,company_list[loop_count],ldriver))
                  LIT.start()
                  threds.append(LIT)
                    
              case 3:
                  Address=logic.address(GBPdriver)
                  result.append(Address)
              case 4:
                  PhoneNumber=logic.PhoneNumber(GBPdriver)
                  result.append(PhoneNumber)

              case 5:
                   result.append(i)


              case 6:
                  result.append(Website)

        
        for a in threds:
           result.append(a.join())  
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
   print(f"{end-start} seconds taken")
   store_in_csv=input("Store in csv:Yes or no:\n")
   if store_in_csv.lower()=="yes":
       logic.csv_store(element_list,your_query,heading_list)
   return
  
if __name__=='__main__':
    main()  

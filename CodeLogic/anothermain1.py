import time
from CodeLogic.GBP2 import Logic   #WOW
from CodeLogic.customthread import returningThread
from newstartapp.models import Num1,GBPInfo,Num,QueryStartStat,UserChoice
                                                                 #didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs page
def main(a,user_choices):
   QueryStartStat(stat="STARTED").save()
   logic=Logic()                                                 
   link_list,your_query,company_list=logic.link_generation(a)
   if link_list=='kill' and your_query=='this' and company_list=='process':
      return 
   heading_list=logic.headers(user_choices)    ##gotta access a class's methods like this,how else
   c=0
   while True:     ##this waits till a user inputs some value inside the num1's limit.Else it will progress before the user inputs anything.
      if Num1.objects.last():
         break
      else:
             time.sleep(5)     ##saving cpu power lmao
             c=c+1
      print(c)
      if QueryStartStat.objects.last() and QueryStartStat.objects.last().stat=="STOP IT":
            QueryStartStat(stat="STOPPED").save()
            return

      if c==60 :             ##If people enter a query more late than 5 minutes,then that shi terminates.UserChoice name might be a bit misleading,it is only to track whether number of companies has been entered w/i 5 minutes
         UserChoice(choice=0).save()
         return
   start=time.time()
   try:
     loop_number=Num1.objects.last().limit
   except:
      Num1(limit=Num.objects.last().companynumber)     ##if people enter no limit then.WILL HAVE TO FIX THE AUTOMATIC REDIRECT FOR THIS.
      loop_number=Num1.objects.last().limit  
   GBPdriver=logic.G_InstanceProvider()
   GBPdriver.implicitly_wait(5)
   emaildriver=None
   ldriver=None
   if '5' in user_choices:
      emaildriver=logic.E_InstanceProvider()
      emaildriver.implicitly_wait(5)
   if '6' in user_choices:
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
        if QueryStartStat.objects.last() and QueryStartStat.objects.last().stat=="STOP IT":
            GBPdriver.quit()
            if emaildriver is not None:
              emaildriver.quit()
            if ldriver is not None:
               ldriver.quit()
            QueryStartStat.objects.all().delete()
            return        
        logic.link_getter(i,GBPdriver)         ##opens us the link of profile in each iteration
        if  '1' in user_choices or '2' in user_choices or '6' in user_choices:
           Website=logic.website(GBPdriver)
        threds=[]             ##Storing threads in a list,damn.
        result=[] 
        rev=user_choices.copy()
        rev.reverse()   ##to maintain order of fields in csv  
            
        result.append(company_list[loop_count])
        for x in rev:
            match x:
              case '5':
                  ET=returningThread(target=logic.email,args=(company_list[loop_count],Website,emaildriver))
                  ET.start()
                  threds.append(ET)
              case '6':
                  LIT=returningThread(target=logic.linkedin,args=(Website,company_list[loop_count],ldriver))
                  LIT.start()
                  threds.append(LIT)
                    
              case '1':
                  Address=logic.address(GBPdriver)
                  #GBPInfo(Address=Address).save()
                  result.append(Address)
              case '2':
                  PhoneNumber=logic.PhoneNumber(GBPdriver)
                  #GBPInfo(PhoneNumber=PhoneNumber).save()
                  result.append(PhoneNumber)

              case '3':
                   MapLink=i
                  # GBPInfo(MapLink=i).save()
                   result.append(i)

              case '4':
                  Web=Website
                  #GBPInfo(Website=Website).save()
                  result.append(Website)
        if '5' in user_choices:
           email=ET.join()
           result.append(email)
        
        if '6' in user_choices:
           linkedin=LIT.join()
           result.append(linkedin)
        #print(company_list[loop_count],Address,PhoneNumber,MapLink,Web,email,linkedin)
        if loop_count==loop_number-1:
         GBPInfo(Company=company_list[loop_count],Address=Address,PhoneNumber=PhoneNumber,MapLink=MapLink,Website=Web,Email=email,Linkedin=linkedin,Stat='done').save()
        else:
           GBPInfo(Company=company_list[loop_count],Address=Address,PhoneNumber=PhoneNumber,MapLink=MapLink,Website=Web,Email=email,Linkedin=linkedin,Stat='None').save()
           
        element_list.append(result) 
        loop_count=loop_count+1
     else:
        GBPdriver.quit()
        if emaildriver is not None:
           emaildriver.quit()
        if ldriver is not None:
           ldriver.quit()
        break
                  
   end=time.time()
   print(f"{end-start} seconds taken")
   #store_in_csv=input("Store in csv:Yes or no:\n")
   #if store_in_csv.lower()=="yes":
   logic.csv_store(element_list,your_query,heading_list)
   QueryStartStat.objects.all().delete()
   QueryStartStat(stat="STOPPED").save()
   return
  
if __name__=='__main__':
    main()  

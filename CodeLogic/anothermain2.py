import time
from CodeLogic.GBP import Logic   #WOW
from CodeLogic.customthread import returningThread
from newstartapp.models import GBPInfo,Num,Num1
logic=None
link_list=None
your_query=None
#didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs page
def main(a):
   logic=Logic()  ##need to make an instance first
   link_list,your_query=logic.link_generation(a)   ##gotta access a class's methods like this,how else
   c=0
   while True:##this waits till a user inputs some value inside the num1's limit.Else it will progress before the user inputs anything.
      if Num1.objects.last():
         break
      else:
           if c<5:
             time.sleep(5) ##saving cpu power lmao

           else:
             time.sleep(1)
           c=c+1

   GBPdriver,emaildriver,ldriver=logic.InstanceProvider()
   GBPdriver.implicitly_wait(5)
   emaildriver.implicitly_wait(5)
   ldriver.implicitly_wait(5)
   start=time.time()
   loop_count=0
   element_list=[]
   loop_number=Num1.objects.last().limit
   

   for i in link_list:
      if loop_count<loop_number:
         logic.link_getter(i,GBPdriver)
         CT=returningThread(target=logic.company,args=(i,GBPdriver))
         WT=returningThread(target=logic.website,args=(GBPdriver,))
         APT=returningThread(target=logic.address_PhoneNumber,args=(GBPdriver,))##arguement must be a tuple,hence the comma
         APT.start()                               
         CT.start()
         WT.start()
         Company=CT.join()
         Website=WT.join()
         ET=returningThread(target=logic.email,args=(Company,Website,emaildriver))
         LIT=returningThread(target=logic.linkedin,args=(Website,Company,ldriver))
         ET.start()
         LIT.start()
         emaillist=ET.join()
         linkedin=LIT.join()
         Address,PhoneNumber=APT.join()

         element_list.append([Company,Address,PhoneNumber,i,Website,emaillist,linkedin])
         if loop_count==int(loop_number)-1:
           GBPInfo(Company=Company,Address=Address,PhoneNumber=PhoneNumber,MapLink=i,Website=Website,Email=emaillist,Linkedin=linkedin,Stat="done").save()
         else:
            GBPInfo(Company=Company,Address=Address,PhoneNumber=PhoneNumber,MapLink=i,Website=Website,Email=emaillist,Linkedin=linkedin,Stat="None").save()

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
   return element_list
  
if __name__=='__main__':
    main()  

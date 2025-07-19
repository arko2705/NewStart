import time
from CodeLogic.GBP import Logic   #WOW
from CodeLogic.customthread import returningThread
from newstartapp.models import GBPInfo,Num,Num1,ProcessKeeper,UserChoice,QueryStartStat  #It's supposed to be procstat,table names are a bit misleading.UserChoice was initially for OP-1,OP-2,now here its been used to termiante
logic=None
link_list=None
your_query=None
#didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs page
def main(a):
   QueryStartStat(stat="STARTED").save()
   logic=Logic()  ##need to make an instance first
   link_list,your_query=logic.link_generation(a)   ##gotta access a class's methods like this,how else
   if link_list=='kill' and your_query=='this':
      return
   c=0
   while True:##this waits till a user inputs some value inside the num1's limit.Else it will progress before the user inputs anything.
      if Num1.objects.last():
         break
      else:
             time.sleep(5) ##saving cpu power lmao
             c=c+1
      print(c)
      if QueryStartStat.objects.last():
         if QueryStartStat.objects.last().stat=="STOP IT":
            QueryStartStat(stat="STOPPED").save()
            return

      if c==60 :                            ##If people enter a query more late than 5 minutes,then that shi terminates.
         UserChoice(choice=0).save()
         return

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
        if QueryStartStat.objects.last():
         if QueryStartStat.objects.last().stat=="STOP IT":
            GBPdriver.quit()
            emaildriver.quit()
            ldriver.quit()
            QueryStartStat.objects.all().delete()
            return
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
   #tore_in_csv=input("Store in csv:Yes or no:\n")
   #if store_in_csv.lower()=="yes":
       #logic.csv_store(element_list,your_query)
   QueryStartStat.objects.all().delete()
   QueryStartStat(stat="STOPPED").save()
   return
  
if __name__=='__main__':
    main()  

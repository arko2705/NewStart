import time
from CodeLogic.GBP import Logic   #WOW
from CodeLogic.customthread import returningThread
from newstartapp.models import GBPInfo,Num1,UserChoice,QueryStartStat  #It's supposed to be procstat,table names are a bit misleading.UserChoice was initially for OP-1,OP-2,now here its been used to termiante
#didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs 
from CodeLogic import common
def main(a):
   QueryStartStat(stat="STARTED").save()
   logic=Logic()  ##need to make an instance first
   link_list,your_query=logic.link_generation(a)   ##gotta access a class's methods like this,how else
   if link_list=='kill':
      return
   status=common.commonWait()
   if status=="kill":
      return
   GBPdriver,emaildriver,ldriver=logic.InstanceProvider()
   for i in [GBPdriver,emaildriver,ldriver]:
      i.implicitly_wait(5)
   start=time.time()
   loop_count=0
   element_list=[]
   loop_number=Num1.objects.last().limit  #number of companies to process
   headers=['Company Name','Address','Phone Number','Google business profile link','Website','E-Mail','Linkedin-Link']  

   for i in link_list:
      if loop_count<loop_number:
         if QueryStartStat.objects.last() and QueryStartStat.objects.last().stat=="RESTING":
            for a in [GBPdriver,emaildriver,ldriver]:
               a.quit()
            QueryStartStat.objects.all().delete()
            return
         logic.link_getter(i,GBPdriver)
         CT=returningThread(target=logic.company,args=(GBPdriver,))  ##stores a thread
         WT=returningThread(target=common.website,args=(GBPdriver,))
         APT=returningThread(target=logic.address_PhoneNumber,args=(GBPdriver,))##arguement must be a tuple,hence the comma
         for b in [CT,WT,APT]:
           b.start() 
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
        for c in [GBPdriver,emaildriver,ldriver]:  ##never reuse loop iterating variables
          c.quit()
        break
   print(element_list)

   end=time.time()
   print(f"{end-start} seconds taken")
   common.csv_store(element_list,your_query,headers)
   QueryStartStat.objects.all().delete()
   QueryStartStat(stat="RESTING").save()
   return

if __name__=='__main__':
    main()  

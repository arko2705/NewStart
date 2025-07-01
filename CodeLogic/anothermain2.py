import time
from GBP import Logic   #WOW
from customthread import returningThread
#didnt use beautiful soup,i used selenium cuz google maps is javascript rendered,beautiful soup and requests would haave given back a bs page
def main():
   logic=Logic()  ##need to make an instance first
   link_list,your_query,loop_number=logic.link_generation()    ##gotta access a class's methods like this,how else
   GBPdriver,emaildriver,ldriver=logic.InstanceProvider()
   GBPdriver.implicitly_wait(5)
   emaildriver.implicitly_wait(5)
   ldriver.implicitly_wait(5)
   start=time.time()
   loop_count=0
   element_list=[]
   
   

   for i in link_list:
      if loop_count<int(loop_number):
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
  
if __name__=='__main__':
    main()  

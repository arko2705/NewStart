from celery import shared_task
import time
from CodeLogic import anothermain1,anothermain2
@shared_task(bind=True)         #bind=True means no retries.Also,we have to pass a "self" parameter to every bind=True @shared_task
def start1(self,quer):
    print(f"task id is {self.request.id}")
    status="starting"
    print("starting 1st process") 
    anothermain2.main(quer) ##a is the query being passed
    return

@shared_task(bind=True)
def start2(self,quer,user_choices):
    status="starting"
    print("starting 2nd process")
    #print("printing user choices")
    #print(user_choices)
    anothermain1.main(quer,user_choices)
    return
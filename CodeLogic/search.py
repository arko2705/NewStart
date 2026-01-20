from newstartapp.models import ProcessKeeper

def search(a):
  initial_query="https://www.google.com/maps/search/"
  query_list=a.split(" ")
  for i in query_list:
    initial_query=initial_query+"+"+i
  final_query=initial_query
  return final_query,a
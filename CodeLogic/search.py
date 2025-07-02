def search(a):
  initial_query="https://www.google.com/maps/search/"
  #print("Enter your query")
  #your_query=input()
  query_list=a.split(" ")
  for i in query_list:
    initial_query=initial_query+"+"+i
  final_query=initial_query
  return final_query,a
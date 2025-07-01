def search():
  initial_query="https://www.google.com/maps/search/"
  print("Enter your query")
  your_query=input()
  query_list=your_query.split(" ")
  for i in query_list:
    initial_query=initial_query+"+"+i
  final_query=initial_query
  return final_query,your_query
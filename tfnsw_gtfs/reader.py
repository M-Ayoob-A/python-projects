import sqlite3

query1 = '''
SELECT s.stop_name, COUNT(*) as stop_frequency
FROM stop_times st
JOIN stops s
ON s.stop_id = st.stop_id
GROUP BY st.stop_id
ORDER BY stop_frequency DESC
LIMIT 6;
'''

query2 = '''
SELECT s.stop_name, COUNT(*) as stop_frequency
FROM stop_times st
JOIN stops s
ON s.stop_id = st.stop_id
GROUP BY st.stop_id
ORDER BY stop_frequency DESC
LIMIT 6;
'''

def find_busiest_stops(cur):
  cur.execute(query1)
  results = cur.fetchall()
  #print(results)
  for i in range(len(results)):
    print(f"{i}. {results[0]} - {results[1]}")




if __name__ == "__main__":
  connection = sqlite3.connect("gtfs.db")
  cursor = connection.cursor()

  print("GTFS Data Summary Stats")
  print("Enter 1 for the busiest train stops")
  print("Enter 2 for the average headway per stop per route")

  
  while True:
    data_view = input("Select an option to view data: ")

    match data_view:
      case "1": # Find busiest stop
        find_busiest_stops(cursor)
      case "2": # 
        pass
      case "q":
        break
      case _:
        print("Unknown command, please try again")

  connection.close()
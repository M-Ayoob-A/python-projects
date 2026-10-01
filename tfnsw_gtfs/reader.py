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
SELECT r.route_long_name, COUNT(*) as trip_count
FROM trips t
JOIN routes r
ON t.route_id = r.route_id
GROUP BY t.route_id;
'''

query3 = '''
SELECT trip_id, COUNT(*) as num_stops
FROM stop_times
GROUP BY trip_id 
ORDER BY num_stops DESC
LIMIT 10;
'''

query4 = '''
SELECT COUNT(*)
FROM agency;
'''

def find_busiest_stops(cur):
  cur.execute(query1)
  results = cur.fetchall()
  for i in range(len(results)):
    print(f"{i}. {results[i][0]} - {results[i][1]}")

def find_trips_per_route(cur):
  cur.execute(query2)
  results = cur.fetchall()
  for i in range(len(results)):
    print(f"{results[i][0]} - {results[i][1]}")

def longest_trips_by_stops(cur):
  cur.execute(query3)
  results = cur.fetchall()
  for i in range(len(results)):
    print(f"{i+1}. {results[i][0]} - {results[i][1]}")

def active_agencies(cur):
  cur.execute(query4)
  results = cur.fetchall()
  print(results[0][0])

if __name__ == "__main__":
  connection = sqlite3.connect("gtfs.db")
  cursor = connection.cursor()

  print("GTFS Data Summary Stats")
  print("Enter 1 for the busiest train stops")
  print("Enter 2 for number of trips per route")
  print("Enter 3 for longest trips by number of stops")
  print("Enter 4 for number of active agencies")
  #print("Enter 2 for the average headway per stop per route")

  
  while True:
    data_view = input("Select an option to view data: ")

    match data_view:
      case "1": # Find busiest stop
        find_busiest_stops(cursor)
      case "2": # 
        find_trips_per_route(cursor)
      case "3": # 
        longest_trips_by_stops(cursor)
      case "4": # 
        active_agencies(cursor)
      case "q":
        break
      case _:
        print("Unknown command, please try again")

  connection.close()
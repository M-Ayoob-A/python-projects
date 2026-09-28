import urllib.request
import zipfile
import os
import sqlite3
import pandas as pd
import glob

zip_folder_url = "https://opendata.transport.nsw.gov.au/data/dataset/d1f68d4f-b778-44df-9823-cf2fa922e47f/resource/67974f14-01bf-47b7-bfa5-c7f2f8a950ca/download/full_greater_sydney_gtfs_static_0.zip"
local_zip_folder_name = "gtfs_data.zip"
db_file = "gtfs.db"


try:
  print("Downloading the ZIP folder from TfNSW's site")
  urllib.request.urlretrieve(zip_folder_url, local_zip_folder_name)

  print("Unzipping the ZIP folder into the local directory")
  with zipfile.ZipFile(local_zip_folder_name, 'r') as zip_ref:
    zip_ref.extractall(".")
    #csv_files = [f for f in zip_ref.nameList() if f.endsWith('.csv')]
  
  print("Removing original zip folder")
  os.remove(local_zip_folder_name)

  conn = sqlite3.connect(db_file)

  routes = pd.read_csv("routes.txt")
  routes = routes[routes["route_type"] == 2] # Filter to trains only

  trips = pd.read_csv("trips.txt")
  trips = trips[trips["route_id"].isin(routes["route_id"])] # Train trips only
  trip_ids = set(trips["trip_id"])

  calendar = pd.read_csv("calendar.txt")
  calendar = calendar[calendar["service_id"].isin(trips["service_id"])]

  routes.to_sql("routes", conn, if_exists="replace", index=False)
  trips.to_sql("trips", conn, if_exists="replace", index=False)
  calendar.to_sql("calendar", conn, if_exists="replace", index=False)

  for name in ["agency", "stops"]:
    df = pd.read_csv(f"{name}.txt")
    df.to_sql(name, conn, if_exists="replace", index=False)

  for chunk in pd.read_csv("stop_times.txt", chunksize=50000):
    chunk[chunk["trip_id"].isin(trip_ids)].to_sql("stop_times", conn, if_exists="append", index=False)

  conn.execute("CREATE INDEX idx_trip_id ON stop_times(trip_id)")
  conn.commit()

  for file in glob.glob("*.txt"):
    print(f"removing {file}")
    os.remove(file)

except Exception as e:
  print(e)
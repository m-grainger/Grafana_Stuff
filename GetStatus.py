import influxdb
import re
import threading
import urllib.request
from datetime import datetime
from robobrowser import RoboBrowser

def do_it():

	threading.Timer(60.0, do_it).start()
	current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	for server_num in range(1,10):
		try:
			print("test1")
			if server_num >= 6:
				url = f"<url...{server_num}...rest of url>"
			else:	
				url = f"<url...{server_num}...rest of url>"
			br = RoboBrowser(history=True, parser="html.parser")
			br.open(url)
			if server_num >= 6:
				first_url = f"<url...{server_num}...rest of url>"
			else:	
				first_url = f"<url...{server_num}...rest of url>"
			
			end_scrape = str(br.select('a')[9])[9:48]
			combo_url = first_url+end_scrape
			br2 = RoboBrowser(history=True,parser="html.parser")
			br2.open(combo_url)
			
				
			try:
			# [15] is status code [17] is exit code
				code_dict = {}
				strp_val = str(br2.select('td')[15]).replace("<td>","").replace("</td>","").replace(",","")
				status_code = str(strp_val)
				print(status_code)
				
				if status_code == "STARTED":
					status_code = 1
				elif status_code == "COMPLETED":
					status_code = 2
				elif status_code == "STOPPED" or status_code == "STOPPING":
					status_code = 3
				elif status_code == "UNKNOWN":
					status_code = 4
				else:
					status_code = 5

				code_dict["measurement"] = f"0{server_num}_status"
				code_dict["time"] = current_time
				field_vals = {}
				code_dict["fields"] = field_vals
				field_vals[f"C_0{server_num}_Status"] = status_code

				data = [code_dict]

				influx = influxdb.InfluxDBClient(host='<influx db here>', 
                                 port='<port num here>',
                                 database='<db name here>')
				try:
					influx.write_points(data)
				except:
					print(f"data for Cluster 0{server_num} could not be entered.")
          print(f" {data} could not be entered.")
					continue

				field_vals ={}
				strp_val = str(br2.select('td')[17]).replace("<td>","").replace("</td>","").replace(",","")
				print(strp_val)
				status_code = str(strp_val)

				if status_code == "STARTED":
					status_code = 1
				elif status_code == "COMPLETED":
					status_code = 2
				elif status_code == "STOPPED" or status_code == "STOPPING":
					status_code = 3
				elif status_code == "UNKNOWN":
					status_code = 4
				else:
					status_code = 5

				print(f"status code: {status_code}")	
				code_dict["measurement"] = f"0{server_num}_exit"
				code_dict["fields"] = field_vals
				field_vals[f"C_0{server_num}_Exit"] = status_code

				data = [code_dict]
				print(data)

				influx = influxdb.InfluxDBClient(host='<influx db here>', 
                                 port='<port num here>',
                                 database='<db name here>')
				try:
					influx.write_points(data)
				except:
					print(f"data for Cluster 0{server_num} could not be entered.")
          print(f" {data} could not be entered.")
					continue

			except:
				code_dict = {}
				field_vals = {}
				print(f"There was a problem processing the values for server 0{server_num}")
				continue
		except:
			print(f"Unable to reach Spring Batch on Cluster_0{server_num}")			
do_it()			

import influxdb
import pytz
import re
import threading
from datetime import datetime
from robobrowser import RoboBrowser


def big_loop():
	threading.Timer(3600.0,big_loop).start()
	influx = influxdb.InfluxDBClient(host='<influxdbhost>', 
	                     port=<port num>,
	                     database='<db name>')
	current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	server_list = [1,2,3,4,5,7,8,9]
	for server_num in server_list:
		def parse_url(server_num):
			try:
				if server_num >= 6:
					url = f"<url f string with {server num} injected>"
					first_url = f"<url f string with {server num} injected>"
				else:	
					url = f"<url f string with {server num} injected>"
					first_url = f"<url f string with {server num} injected>"
			except:
				print(f"Something went wrong loading SB for C0{server_num}")				
			br = RoboBrowser(history=True, parser="html.parser")
			try:
				br.open(url) # attempt to open url with RoboBrowser
			except:
				print(f"Unable to open {url}")						
			if server_num == 7:
				end_scrape = str(br.select('a')[9])[9:46]
			else:	
				end_scrape = str(br.select('a')[9])[9:48]
			combo_url = first_url+end_scrape # combine both strings to create URL for most recent job


			return combo_url
			
		parsed_url = parse_url(server_num)	

		def scrape_td(parsed_url):
			br2 = RoboBrowser(history=True,parser="html.parser")
			try:
				br2.open(parsed_url) # attempt to open up parsed URL
			except:
				print(f"Unable to open{parsed_url}")	
			col_list = [28,29,30, # 1
						35,36,37, # 2
						42,43,44, # 3
						49,50,51, # 4
						56,57,58, # 5 
						63,64,65, # 6
						70,71,72, # 7
						77,78,79, # 8
						84,85,86, # 9
						91,92,93, # 10
						98,99,100, # 11
						105,106,107, # 12
						112,113,114, # 13
						119,120,121, # 14
						126,127,128, # 15
						133,134,135, # 16
						140,141,142, # 17
						147,148,149, # 18
						154,155,156, # 19
						161,162,163, # 20
						168,169,170, # 21
						175,176,177, # 22
						182,183,184, # 23
						189,190,191, # 24
						196,197,198, # 25 
						203,204,205, # 26
						210,211,212, # 27
						217,218,219, # 28 
						224,225,226, # 29
						231,232,233, # 30
						238,239,240, # 31
						245,246,247, # 32
						252,253,254] # 33
			temp_list = [] # empty list to insert writes for each consumer
			for nums in col_list:
				try:
					strp_val = str(br2.select('td')[nums]).replace("<td>","").replace("</td>","").replace(",","") # parses string so we can turn 
					temp_list.append(int(strp_val))																  #	value into an int
				except:
					print(f"Less than 33 threads for cluster 0{server_num}")
			writes_ = temp_list[0::3]
			writes_totals = sum(writes_) # total of writes located in temp list

			return writes_totals						

		total_writes = scrape_td(parsed_url)

		def create_dict(total_writes):
			main_dict = {}
			field_vals = {}			
			main_dict["measurement"] = f"Cluster 0{server_num} Writes"
			main_dict["time"] = current_time
			main_dict["fields"] = field_vals
			field_vals[f"C_0{server_num}_writes"] = total_writes			
			data = [main_dict]

			return data

		final_dict = create_dict(total_writes)	
		# check for started?  Maybe here?

		def push_data(final_dict):
			try:
				influx.write_points(final_dict)
			except:
				print(f"Data could not be writted to InfluxDB for C0{server_num}")	
		
		final_run = push_data(final_dict)	

big_loop()

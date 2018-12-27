import influxdb
import pytz
import re
import threading
import urllib.request
from datetime import datetime
from robobrowser import RoboBrowser

def do_it():

	threading.Timer(3600.0, do_it).start()

	influx = influxdb.InfluxDBClient(host=<insert host name here>, 
	                     port=<port here>,
	                     database=<db name here>)

	current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	for server_num in range(1,10):
		try:
			if server_num >= 6:
				url = f"<url...{server_num}...rest of the url>"
			else:	
				url = f"<url...{server_num}...rest of the url>"
			br = RoboBrowser(history=True, parser="html.parser")
			br.open(url)
			if server_num >= 6:
				first_url = f"<url...{server_num}...rest of the url>"
			else:	
				first_url = f"<url...{server_num}...rest of the url>"
			end_scrape = str(br.select('a')[9])[9:48]
			combo_url = first_url+end_scrape
			br2 = RoboBrowser(history=True,parser="html.parser")
			br2.open(combo_url)
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

			temp_list = []
			for nums in col_list:
				try:
					strp_val = str(br2.select('td')[nums]).replace("<td>","").replace("</td>","").replace(",","")
					#sb_dict = {f"reads_cl_0{server_num}": int(strp_val)}
					temp_list.append(int(strp_val))
					#print(sb_dict)
				except:
					print(f"Less than 33 threads for cluster 0{server_num}")	

			reads_ = temp_list[1::3]
			reads_totals = sum(reads_)
			
			writes_ = temp_list[0::3]
			writes_totals = sum(writes_)
			
			commits_ = temp_list[2::3]
			commits_totals = sum(commits_)
			
			main_dict = {}
      main_dict["measurement"] = f"Cluster 0{server_num} Writes"
			main_dict["time"] = current_time
			field_vals = {}
			main_dict["fields"] = field_vals
			field_vals[f"C_0{server_num}_writes"] = writes_totals
			data = [main_dict]


		except:
			print(f"Not working for Cluster {server_num}")			
		  print(data)

		try:
			influx.write_points(data)
		except:
			print(f"data for {data} could not be entered.")
			continue
	
do_it()

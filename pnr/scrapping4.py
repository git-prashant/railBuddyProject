import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
import sys
import datetime
import  os
def get_trains_between_stn(src,des,date):
		# if len(sys.argv) < 6:
		# 	print('Less arguments provided')
		# 	print('5 arguments needed => source_stn_code dest_stn_code travel_date travel_month travel_year')
		# 	sys.exit()

		with open("pnr/reverseStation.json")as f:
			temp = json.load(f)
		src=str(temp[src])
		des=str(temp[des])
		print()
		print()
		print()
		print()
		print()
		print()
		print()

		print(src) 
		print(des)

		print()
		print()
		print()
		print()
		print()
		print()
		print()


		with open("pnr/stations.json") as stations:
			stns = json.load(stations)

		source_stn = src.upper()

		if source_stn not in stns:
			print('Source station code is invalid')
			sys.exit()
		dest_stn = des.upper()
		if dest_stn not in stns:
			print('Destination station code is invalid')
			sys.exit()

		day = date[0]
		month = date[1]
		year = date[2]

		try:
			print("inside scrapping ", int(year), int(month), int(day))
			datetime.datetime(int(year), int(month), int(day))
		except:
			print('The date you entered is not valid')
			sys.exit()

		url = 'https://www.railyatri.in/booking/trains-between-stations?from_code='+source_stn+'&from_name='+ stns[src] +'+&journey_date='+day+'%2F'+month+'%2F'+year+'%2F'+'&to_code='+dest_stn+'&to_name='+stns[des]+'+&user_id=1&user_token=6'
		print(url)
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		trains = []
		for row in soup.select('tr.tbs-main-row'):
			data = {}
			title = row.find('p', {'class': 'train-name-title'}).text.strip('\n')
			data['trn_no'] = title[:5]
			data['trn_name'] = title[8:]
			data['schedule'] = 'https://erail.in/train-enquiry/'+title[:5]
			spans = row.find_all('span')[:6]
			data['source'] = stns[spans[0].text]
			data['departure time'] = spans[1].text
			data['destination'] = stns[spans[3].text]
			data['arrival time'] = spans[4].text
			data['duration'] = spans[5].text
			data['fares'] = []
			classes = row.find_all('div', {'class': 'coach'})
			for i in range(len(classes)//2):
				pair = {}
				deets = classes[i].find_all('p')
				pair['Class'] = deets[0].text
				pair['Price'] = deets[1].text
				if pair['Price'] == '₹ NA':
					continue
				data['fares'].append(pair)
			if len(data['fares']) != 0:		#railyatri shows some trains with no availabilities
				trains.append(data)

		# if len(trains) > 0:
		# 	with open(source_stn+'to'+dest_stn+'.json', 'w') as out:
		# 		json.dump(trains, out)
		# 	pprint(trains)
		# 	print('Output has been generated and stored in', source_stn+'to'+dest_stn+'.json')
		# else:
		# 	print('Sorry! No trains match your search criteria, please choose different city')
		# print(len(trains))
		return stns[source_stn],stns[dest_stn],trains
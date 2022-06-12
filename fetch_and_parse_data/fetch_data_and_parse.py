import re
import requests
import json
import logging
import csv

def get_for_sale_content_by_params(top_area,area,rooms,sqr_meter):
	# url= f'https://gw.yad2.co.il/feed-search-legacy/realestate/forsale?topArea=25&area=5&propertyGroup=apartments&rooms=4-4&squaremeter=120-120&forceLdLoad=true'
	url= f'https://gw.yad2.co.il/feed-search-legacy/realestate/forsale?topArea={top_area}&area={area}&propertyGroup=apartments&rooms={rooms}-{rooms}&squaremeter={sqr_meter}-{sqr_meter}&forceLdLoad=true'
	res= requests.request('GET', url)
	# return as dict the raw response
	return json.loads(res.content.decode("UTF_8"))
	# with open('file.txt') as f:
	# 	return json.loads(f.read())

def is_content_valid(content):
	if not content.get('data'):
		logging.error('Object response has changed- no data to parse')
		return False
	if not content.get('data').get('feed'):
		logging.error('Object response has changed- no feed to parse')
		return False
	if content.get('data').get('feed').get('feed_items') is None:
		logging.error('Object response has changed- no feed item to parse')
		return False
	return True

def is_parse_raw_content_and_inject_csv(content):
	is_valid= is_content_valid(content)
	if not is_valid:
		logging.info('Content is not vaild')
		return False
	feed_items= content.get('data').get('feed').get('feed_items')
	with open('csv_real_estate_files/parsed_content.csv','w+',encoding='UTF8') as p:
		writer= csv.writer(p)
		cols_names=['ad_id','city_name','street_name','date_last_updated','date_first_added','price','floor_num','rooms_num','sqr_meter',
					'primary_area_id','area_id','city_code','deal_info']

		# writes the header of the csv file
		writer.writerow(cols_names)

		for item in feed_items:
			ad_id = item.get('ad_number')
			if not ad_id:
				continue
			city_name = item.get('city')
			street_name = item.get('street')
			date_last_updated = item.get('date')
			date_first_added= item.get('date_added')
			# parse the price to have only number without spaces or other
			price = item.get('price').replace(',', '').replace(' ', '')[:-1] if item.get('price') and re.search('[0-9]+',item.get('price')) is not None else None
			# parse the floor level out of the text ignoring all text
			floor_num_str= item.get('line_2')
			floor_num = re.findall('[0-9]+', floor_num_str)[0] if floor_num_str is not None and re.search('[0-9]+',floor_num_str) else None
			rooms_num = item.get('Rooms_text')
			sqr_meter = item.get('square_meters')
			primary_area_id= item.get('PrimaryAreaID')
			area_id=item.get('area_id')
			city_code=item.get('city_code')
			deal_info= item.get('deal_info')

			# write each item of content into the csv after parsed,
			writer.writerow([ad_id,city_name,street_name,date_last_updated,date_first_added,price,floor_num,rooms_num,sqr_meter,primary_area_id,area_id,city_code,deal_info])
		logging.info('all records were injected to csv')
	return True



if __name__ == '__main__':
	content= get_for_sale_content_by_params()
	print(is_parse_raw_content_and_inject_csv(content))
	i = 0
	# map of ares:
	# top area + area nums : haifa top 25, area:5


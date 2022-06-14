import logging
from fetch_and_parse_data.fetch_data_and_parse import get_for_sale_content_by_params, \
	is_parse_raw_content_and_inject_csv
from pd_data_processing import is_create_pdf, get_clean_data
import re

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def is_params_valid(params):
	area_name = params.get('area_name').upper() if params.get('area_name') else None
	sqr_meter_str = params.get('sqr_meter')
	sqr_meter = sqr_meter_str if sqr_meter_str and re.match('[0-9]+', sqr_meter_str) else None
	rooms_num_str = params.get('rooms_num')
	rooms_num = rooms_num_str if rooms_num_str and re.match('[0-9]+', rooms_num_str) else None
	return (not None in (area_name, sqr_meter, rooms_num))


def is_evaluation_succeeded(params):
	if not is_params_valid(params):
		logging.error('URL params are not valid')
		return False

	content = get_for_sale_content_by_params(params.get('area_name').upper(),
											 params.get('rooms_num'), params.get('sqr_meter'))
	is_csv_created = is_parse_raw_content_and_inject_csv(content)
	if not is_csv_created:
		return False

	return is_create_pdf(get_clean_data(), params)

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# from sklearn.linear_model import LinearRegression
import numpy as np


def get_clean_data():
	df = pd.read_csv('csv_real_estate_files/parsed_content.csv')
	df.drop_duplicates('ad_id')
	# remove all rows with null price
	df = df[df['price'].notnull()]
	df['date_last_updated'] = pd.to_datetime(df.date_last_updated)
	return df


def create_plot_by_price_and_date(df: pd.DataFrame, pdf: PdfPages):
	fig = plt.figure(figsize=(9, 5))
	plt.title('Price by Month')
	df.set_index('date_last_updated').resample('1M')['price'].mean().plot()
	pdf.savefig()
	plt.close()


def create_plot_by_price_and_floor_num(df: pd.DataFrame, pdf: PdfPages):
	fig = plt.figure(figsize=(9, 5))
	ax = fig.gca()
	plt.title('Price by Floor Number')
	floor_data_record_count = df.groupby('floor_num')['price'].size()
	df.groupby('floor_num')['price'].mean().plot(ax=ax, kind='bar')
	# add to each bar the count of the records
	x_offset = -0.07
	y_offset = 0.02
	for index, p in enumerate(ax.patches):
		b = p.get_bbox()
		val = "{:.0f}".format(floor_data_record_count.iloc[index])
		ax.annotate(val, ((b.x0 + b.x1) / 2 + x_offset, b.y1 + y_offset))
	ax.set_ylabel('price M')
	pdf.savefig()
	plt.close()


def add_text_to_pdf(text: str, font_size: int, x_position: int, y_position: int, pdf: PdfPages):
	fig = plt.figure(figsize=(9, 5))
	fig.clf()
	fig.text(x_position, y_position, text, transform=fig.transFigure, size=font_size, wrap=True, ha='left')
	pdf.savefig()
	plt.close()


def generate_evaluation_summary_text(df: pd.DataFrame, proparty_params):
	prices_avg = df['price'].mean()
	round_avg = round(prices_avg, 0)

	location = proparty_params.get('area_name')
	sqr_meter = proparty_params.get('sqr_meter')
	roomNum = proparty_params.get('rooms_num')

	text = f'Evaluation Summary: \n' \
		   f'Propary Description:\nLocation: {location}\nSqrMeter Size: {sqr_meter}\nNumber of Rooms:{roomNum} \n\n' \
		   f'your avg price of the proparty is: {round_avg}\n\nThe evaluation is based on yad2.co.il website'
	return text


def create_pdf(df: pd.DataFrame, proparty_params):
	with PdfPages('property_evaluation.pdf') as pdf:
		text = generate_evaluation_summary_text(df, proparty_params)
		add_text_to_pdf(text, 20, 0.2, 0.3, pdf)
		create_plot_by_price_and_date(df, pdf)
		create_plot_by_price_and_floor_num(df, pdf)


if __name__ == '__main__':
	df = get_clean_data()

	from fetch_and_parse_data.areas_enum import Geo_areas

	create_pdf(df, {'area_name': Geo_areas["HAIFA"].name, 'rooms_num': 4, "sqr_meter": 120})

	i = 0
# df_raw = get_raw_data_from_csv_as_df()
#
# df_raw = df_raw.dropna()
# X = df_raw[['bed', 'house_size']]
# y = df_raw['price']
#
# model = LinearRegression()
#
# model.fit(X, y)
#
# model_prdict = model.predict(X)
#
# df_raw['model_result'] = model_prdict
#
# plt.scatter(df_raw['bed'], df_raw['price'])

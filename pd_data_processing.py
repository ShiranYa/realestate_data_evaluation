import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from utils.utils import random_dates


def get_raw_data_from_csv():
	df_raw = pd.read_csv('csv_real_estate_files/parsed_content.csv')
	np.random.seed(0)
	start = pd.to_datetime('2015-01-01')
	end = pd.datetime.now()
	df_raw["upload_date"] = random_dates(start, end, len(df_raw.index))
	return df_raw


def get_aggregated_data():
	df_raw = get_raw_data_from_csv()


if __name__ == '__main__':
	df_raw = get_raw_data_from_csv()

	df_raw = df_raw.dropna()
	X = df_raw[['bed', 'house_size']]
	y = df_raw['price']

	model = LinearRegression()

	model.fit(X, y)

	model_prdict = model.predict(X)

	df_raw['model_result'] = model_prdict

	plt.scatter(df_raw['bed'], df_raw['price'])

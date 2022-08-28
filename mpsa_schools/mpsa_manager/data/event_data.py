import pandas as pd

def process_data():
	data = {}
	cur_day_data = pd.read_csv(f'data/day_1.csv')
	cur_day_data.columns=cur_day_data.iloc[3]
	data[f'day_1'] = cur_day_data[4:]
	return data
	
data = process_data()
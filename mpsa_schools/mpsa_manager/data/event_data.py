import pandas as pd
DAYS = 4

def process_data():
	data = {}
	for i in range(DAYS):
		cur_day_data = pd.read_csv(f'data/day_{i+1}.csv')
	
		data[f'day_{i+1}'] = cur_day_data
	return data
	
data = process_data()

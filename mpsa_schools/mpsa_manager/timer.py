import xlsxwriter
from data.event_data import *

PLACE = 'School'
DAY = 1

days = []
for i in range(DAYS):
	days.append(f"day_{i+1}")
idx_col = 0
lane_col = 1
name_col = 2
dob_col = 3
district_col = 4
mm_col = 5
ss_col = 6
ms_col = 7

def append_in_sheet(df, worksheet, row):	
	for i in range(len(df)):
		worksheet.write(row+i, lane_col, i+1)
		worksheet.write(row+i, name_col, df.iloc[i]['Name'])
		try:
			worksheet.write(row+i, dob_col, df.iloc[i]['Date of Birth'])
			worksheet.write(row+i, district_col, df.iloc[i][PLACE])
		except:
			pass
		# worksheet.write(row+i, district_col, df.iloc[i][PLACE])
		worksheet.write(row+i, mm_col, df.iloc[i]['mm'])
		worksheet.write(row+i, ss_col, df.iloc[i]['ss'])
		worksheet.write(row+i, ms_col, df.iloc[i]['ms'])
	

def create_result_chart(chart_name='Lane_order_MPSA_2022'):
	workbook = xlsxwriter.Workbook(f'results/{chart_name}.xlsx')
	bold = workbook.add_format({'bold': True})
	
	for day in days:
		row = 0
		worksheet = workbook.add_worksheet(f'Day {day[-1]}')
		for sn in range(len(data[day])):
			cur_event = data[day].iloc[sn]
			cur_event_name = f"{cur_event['Event Name']} {cur_event['Category']} {cur_event['Group']}"
			# print(f"{cur_event['Event Name']} {cur_event['Category']} {cur_event['Group']}")
			
			cur_df = pd.read_csv(f"data/csv_event_list/{day}/{cur_event_name}.csv")	
			
			worksheet.write(row, idx_col, cur_event['S.N.'], bold)
			worksheet.write(row, name_col, f"{cur_event_name} Results", bold)
			row += 1
			worksheet.write(row, lane_col, "Position", bold)
			worksheet.write(row, name_col, "Name", bold)
			worksheet.write(row, dob_col, 'DOB', bold)
			worksheet.write(row, district_col, PLACE, bold)
			worksheet.write(row, mm_col, "mm", bold)
			worksheet.write(row, ss_col, "ss", bold)
			worksheet.write(row, ms_col, "ms", bold)
			row += 1
			append_in_sheet(cur_df, worksheet, row)
			row += len(cur_df)+1
	workbook.close()

def update_time(df_path):
	df = pd.read_csv(df_path)
	for athlete in range(len(df)):
		print(f"Athlete Name : {df.iloc[athlete]['Name']}")
		mm = int(input("Enter mm : "))
		ss = int(input("Enter ss : "))
		ms = int(input("Enter ms : "))
		df.loc[athlete, 'mm'] = mm
		df.loc[athlete, 'ss'] = ss
		df.loc[athlete, 'ms'] = ms
	
	# df = df[['Name', PLACE, 'mm', 'ss', 'ms']].sort_values(by=['mm', 'ss', 'ms'], ascending=True, na_position='last', ignore_index=True)
	df = df[['Name', 'Date of Birth', 'mm', 'ss', 'ms']].sort_values(by=['mm', 'ss', 'ms'], ascending=True, na_position='last', ignore_index=True)
	print('\n',df, '\n')
	confirm = input("\nConfirm ?\ny: Yes, n : NO\n")
	if confirm == 'y':
		df.to_csv(df_path)
	else:
		while not confirm == 'y':
			idx = int(input("Enter Index to make amends : "))
			print(f"Athlete Name : {df.iloc[idx]['Name']}")
			mm = int(input("Enter mm : "))
			ss = int(input("Enter ss : "))
			ms = int(input("Enter ms : "))
			df.loc[idx, 'mm'] = mm
			df.loc[idx, 'ss'] = ss
			df.loc[idx, 'ms'] = ms
			df = df[['Name','Date of Birth', 'mm', 'ss', 'ms']].sort_values(by=['mm', 'ss', 'ms'], ascending=True, na_position='last', ignore_index=True)
			print('\n',df, '\n')
			confirm = input("\nConfirm ?\ny: Yes, n : NO\n")
		df.to_csv(df_path)


def find_event():
	
	cur_day_events = data[days[DAY-1]]
	cur_event_number = int(input("Enter Current Event Number : "))
	print("Current Event Details")
	print(cur_day_events.iloc[cur_event_number-1]['S.N.'], cur_day_events.iloc[cur_event_number-1]['Event Name'], cur_day_events.iloc[cur_event_number-1]['Category'], cur_day_events.iloc[cur_event_number-1]['Group'], '\n')
	cur_event_path = f"data/csv_event_list/{days[DAY-1]}/{cur_day_events.iloc[cur_event_number-1]['Event Name']} {cur_day_events.iloc[cur_event_number-1]['Category']} {cur_day_events.iloc[cur_event_number-1]['Group']}.csv"

	update_time(cur_event_path)
	create_result_chart('Final Results')

find_event()
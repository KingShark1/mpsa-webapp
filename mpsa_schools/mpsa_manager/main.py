import pandas as pd

from data.event_data import *

PLACE = 'School/Club'

def process_events(df):
    r = ['0'] * len(df)
    ser = pd.Series(r, copy=False)
    for i in range(len(df)):
      if df.iloc[i]['Group'] == 'Senior':
        ser.iloc[i] = df.iloc[i]['Events (Max 5) for Seniors'].split(", ")
      elif df.iloc[i]['Group'] == 'I':
        ser.iloc[i] = df.iloc[i]['Events for group 1'].split(", ")
      elif df.iloc[i]['Group'] == 'II':
        print(df.iloc[i]['Name'], '\t',df.iloc[i]['Events for group 2'])
        ser.iloc[i] = df.iloc[i]['Events for group 2'].split(", ")
      elif df.iloc[i]['Group'] == 'III':
        ser.iloc[i] = df.iloc[i]['Events for group 3'].split(", ")
      elif df.iloc[i]['Group'] == 'IV':
        ser.iloc[i] = df.iloc[i]['Events for group 4'].split(", ")
    df['Events'] = ser
    return df

def update_events(responses='data/Schools MPSA 2022 Form - 1 (Responses) - Form responses 1.csv'):
  raw_data = {	
  'Name': [],
  PLACE: [],
  'dob': [],
  'mm': [],
  'ss': [],
  'ms': [],}

  event_ref = {}
  for day in data:
    for event in range(len(data[day])):
      df = pd.DataFrame(raw_data, columns=['Name', 'dob', PLACE, 'mm', 'ss', 'ms'])
      event_name = f"{data[day].iloc[event]['Event Name']} {data[day].iloc[event]['Category']} {data[day].iloc[event]['Group']}"
      event_ref[event_name] = day
      df.to_csv(f'data/csv_event_list/{day}/{event_name}.csv', index=False)
  
  responses_df = pd.read_csv(responses)
  responses_df = process_events(responses_df)
  responses_df = responses_df[['Name', 'Date of Birth', 'Category', 'Group', PLACE, 'Events']]
  for athlete in range(len(responses_df)):
    for event in responses_df['Events'].iloc[athlete]:
      cur_event_name= f"{event} {responses_df.iloc[athlete]['Category']} {responses_df.iloc[athlete]['Group']}"
      cur_event_day = event_ref[cur_event_name]
      cur_event_path = f"data/csv_event_list/{cur_event_day}/{cur_event_name}.csv"
      print(cur_event_path)
      cur_event_df = pd.read_csv(cur_event_path)
      raw_data = {	
                'Name': responses_df.iloc[athlete]['Name'],
                'Date of Birth': responses_df.iloc[athlete]['Date of Birth'],
                PLACE: responses_df.iloc[athlete][PLACE],
                'mm': ' ',
                'ss': ' ',
                'ms': ' ',}
      cur_event_df = cur_event_df.append(raw_data, ignore_index=True)
      cur_event_df.to_csv(cur_event_path, index=False)

def main():
  update_events()

if __name__=="__main__":
  main()

# data/csv_event_list/day_4/50 mt. Free Style Men Senior.csv
# data/csv_event_list/day_4/50 mt. Free Style Men Senior.csv
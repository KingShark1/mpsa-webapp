import pandas as pd
from datetime import date, datetime
from data.event_data import *

import warnings
warnings.filterwarnings("ignore")

PLACE = 'School/Club'

def get_age_group_from_birthdate(birthdate: str) -> str:
  birthdate = datetime.strptime(birthdate, '%d/%m/%Y')
  today = date.today()
  age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
  if age >= 15:
    return 'Elite'
  elif age >= 13 and age <=14:
    return '13 - 14 Year'
  elif age >= 11 and age <= 12:
    return '11 - 12 Year'
  elif age >= 9 and age <= 10:
    return '9 - 10 Year'
  elif age >= 6 and age <= 8:
    return '6 - 8 Year'
  elif age >= 4 and age <= 5:
    return '4 - 5 Year'
  
  
  
def process_age_group(df: pd.DataFrame) -> pd.DataFrame:
  r = ['0'] * len(df)
  ser = pd.Series(r, copy=False)
  for i in range(len(df)):
    ser.iloc[i] = get_age_group_from_birthdate(df.iloc[i]['Date of Birth'])
  df['Group'] = ser
  return df


def process_events(df):
    df = process_age_group(df)
    df['Events'] = df['Events'].apply(lambda x: x.split(", "))
    return df

def update_events(responses="data/indore_kids_comp (Responses) - Form responses 1.csv"):
  print("Initializing Data Buffer ...")
  raw_data = {	
  'Name': [],
  'Date of Birth': [],
  'mm': [],
  'ss': [],
  'ms': [],}

  event_ref = {}
  try:
    for day in data:
      for event in range(len(data[day])):
        df = pd.DataFrame(raw_data, columns=['Name', 'Date of Birth', 'mm', 'ss', 'ms'])
        event_name = f"{data[day].iloc[event]['Event Name']} {data[day].iloc[event]['Category']} {data[day].iloc[event]['Group']}"
        event_ref[event_name] = day
        df.to_csv(f'data/csv_event_list/{day}/{event_name}.csv', index=False)
  except Exception as e:
    print("something went wrong in initializing data")
    print(e)
  
  responses_df = pd.read_csv(responses)
  responses_df = process_events(responses_df)
  responses_df = responses_df[['Name', 'Date of Birth', 'Category', 'Group', 'Events']]
  try:
    for athlete in range(len(responses_df)):
      for event in responses_df['Events'].iloc[athlete]:
        cur_event_name= f"{event} {responses_df.iloc[athlete]['Category']} {responses_df.iloc[athlete]['Group']}"
        cur_event_day = event_ref[cur_event_name]
        cur_event_path = f"data/csv_event_list/{cur_event_day}/{cur_event_name}.csv"
        cur_event_df = pd.read_csv(cur_event_path)
        
        # cur_event_df = cur_event_df.append(raw_data)
        if responses_df.iloc[athlete]['Name'] in cur_event_df['Name']:
          pass
        else:
          raw_data = {	
                  'Name': responses_df.iloc[athlete]['Name'],
                  'Date of Birth': responses_df.iloc[athlete]['Date of Birth'],
                  'mm': ' ',
                  'ss': ' ',
                  'ms': ' ',}
          cur_event_df = cur_event_df.append(raw_data, ignore_index=True)
          cur_event_df.to_csv(cur_event_path, index=False)
  except KeyError:
    print(f"KeyError mismatch :\n{cur_event_name} \nAthlete - {responses_df['Name'].iloc[athlete]}\nRow Number - {athlete+2}")
  print("Finished creating dataset")

def main():
  update_events()

if __name__=="__main__":
  main()


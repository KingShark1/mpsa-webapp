import pandas as pd
from datetime import date, datetime
from data.event_data import *
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore")

PLACE = 'Divison'
GROUPS = {"I": "U-19",
          "II": "U-17",
          "III": "U-14",
          }
EVENT_COLS = {"I":"Events for group 1",
              "II":"Events for group 2",
              "III":"Events for group 3",}

def get_age_group_from_birthdate(group): # birthdate: str) -> str:
  # birthdate = datetime.strptime(birthdate, '%d/%m/%Y')
  # today = date.today()
  # age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
  return GROUPS[group]
  
def process_age_group(df: pd.DataFrame) -> pd.DataFrame:
  r = ['0'] * len(df)
  ser = pd.Series(r, copy=False)
  for i in range(len(df)):
    ser.iloc[i] = get_age_group_from_birthdate(df.iloc[i]['Group'])
  df['Group'] = ser

  return df

def get_key(my_dict, val):
  for key, value in my_dict.items():
    if val == value:
      return key
  return "Key doesnt exist in constant GROUPS"

def merge_events(df):
  r = ['0']*len(df)
  ser = pd.Series(r, copy=False)
  for i in range(len(df)):
    # if df.iloc[i]["Events for group 1"]:
    #   ser.iloc[i] = df.iloc[i]["Events for group 1"]
    # elif df.iloc[i]["Events for group 2"]:
    #   ser.iloc[i] = df.iloc[i]["Events for group 2"]
    # elif df.iloc[i]["Events for group 3"]:
    #   ser.iloc[i] = df.iloc[i]["Events for group 3"]
    if type(df.iloc[i][EVENT_COLS[get_key(GROUPS, df.iloc[i]['Group'])]]) != float:
      ser.iloc[i] = df.iloc[i][EVENT_COLS[get_key(GROUPS, df.iloc[i]['Group'])]]
    else:
      print("ERROR AT INDEX : ", i)
    df['Events'] = ser
  return df

def process_events(df):
    df = process_age_group(df)
    df = merge_events(df)
    df['Events'] = df['Events'].apply(lambda x: x.split(", "))
    return df

def update_events(responses="data/Schools MPSA State 2022 (Responses) - Form responses 1.csv"):
  print("Initializing Data Buffer ...")
  raw_data = {	
  'Name': [],
  'Date of Birth': [],
  PLACE: [],
  'mm': [],
  'ss': [],
  'ms': [],}

  event_ref = {}
  try:
    for day in data:
      for event in range(len(data[day])):
        df = pd.DataFrame(raw_data, columns=['Name', 'Date of Birth', PLACE, 'mm', 'ss', 'ms'])
        event_name = f"{data[day].iloc[event]['Event Name']} {data[day].iloc[event]['Category']} {data[day].iloc[event]['Group']}"
        event_ref[event_name] = day
        df.to_csv(f'data/csv_event_list/{day}/{event_name}.csv', index=False)
  except Exception as e:
    print("something went wrong in initializing data")
    print(e)
  
  responses_df = pd.read_csv(responses)
  responses_df = process_events(responses_df)
  responses_df = responses_df[['Name', 'Date of Birth', 'Category', 'Group', PLACE, 'Events']]
  try:
    for athlete in tqdm(range(len(responses_df))):
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
                  PLACE: responses_df.iloc[athlete][PLACE],
                  'mm': ' ',
                  'ss': ' ',
                  'ms': ' ',}
          cur_event_df = cur_event_df.append(raw_data, ignore_index=True)
          cur_event_df.to_csv(cur_event_path, index=False)
  except Exception as e:
    print(e)
    print(f"KeyError mismatch :\n{cur_event_name} \nAthlete - {responses_df['Name'].iloc[athlete]}\nRow Number - {athlete+2}")
  print("Finished creating dataset")

def main():
  update_events()

if __name__=="__main__":
  main()


import pandas as pd
from datetime import date, datetime
from data.event_data import *
from tqdm import tqdm
import traceback
import warnings
warnings.filterwarnings("ignore")

PLACE = 'School/Club'
RESPONSE_PATH = "data/Schools 2023 District (indore) - Athete Responses.csv"
# GROUPS = {"Senior": "Senior",
#           "Group 1  (Born in 2006/2007/2008)": "I",
#           "Group 2  (Born in 2009/2010/2011)": "II",
#           "Group 3  (Born in 2012/2013)": "III",
#           "Group 4  (Born in 2014/2015)": "IV"
#           }
GROUPS = {"Senior": "Senior",
          "I": "I",
          "II": "II",
          "III": "III",
          "Group 4  (Born in 2014/2015)": "IV"
          }
EVENT_COLS = {"Senior": "Events (Max 5) for Seniors",
          "I": "Events for group 1",
          "II": "Events for group 2",
          "III": "Events for group 3",
          "Group 4  (Born in 2014/2015)": "Events (Max 6) for group 4"
          }
# EVENT_COLS = {"Senior": "Events (Max 5) for Seniors",
#           "Group 1  (Born in 2006/2007/2008)": "Events (Max 5) for group 1",
#           "Group 2  (Born in 2009/2010/2011)": "Events (Max 5) for group 2",
#           "Group 3  (Born in 2012/2013)": "Events (Max 5) for Group 3",
#           "Group 4  (Born in 2014/2015)": "Events (Max 6) for group 4"
#           }

SENIOR = ["Men", "Women"]
JUNIOR = ["Boys", "Girls"]

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
  try:
    for key, value in my_dict.items():
      if val == value:
        return key
  except:
    print("Key doesnt exist in constant GROUPS")
    traceback.print_exc()

def merge_events(df):
  r = ['0']*len(df)
  ser = pd.Series(r, copy=False)
  for i in range(len(df)):
    ser.iloc[i] = df.iloc[i][EVENT_COLS[get_key(GROUPS, df.iloc[i]['Group'])]]
  
  df['Events'] = ser
  return df

def process_events(df):
    df = process_age_group(df)
    df = merge_events(df)
    df['Events'] = df['Events'].apply(lambda x: x.split(", "))
    return df

def get_category_from_gender(event, day):
  if data[day].iloc[event]['Category'] == 'Boys':
          if data[day].iloc[event]['Group'] == 'Senior':
            category = SENIOR[0]
          else:
            category = JUNIOR[0]
  else:
    if data[day].iloc[event]['Group'] == 'Senior':
      category = SENIOR[1]
    else:
      category = JUNIOR[1]
  # print(category)
  return category

def get_category_from_string(gender, group):
  # print(gender)
  if gender == 'Boys':
          if group == 'Senior':
            category = SENIOR[0]
          else:
            category = JUNIOR[0]
  else:
    if group == 'Senior':
      category = SENIOR[1]
    else:
      category = JUNIOR[1]
  # print(category)
  return category

def update_events(responses=RESPONSE_PATH):
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
        
        # event_name = f"{data[day].iloc[event]['Event Name']} {data[day].iloc[event]['Category']} {data[day].iloc[event]['Group']}"
        event_name = f"{data[day].iloc[event]['Event Name']} {data[day].iloc[event]['Category']} {data[day].iloc[event]['Group']}"
        event_ref[event_name] = day
        df.to_csv(f'data/csv_event_list/{day}/{event_name}.csv', index=False)
  except Exception as e:
    print("something went wrong in initializing data")
    print(e)
  
  responses_df = pd.read_csv(responses)
  responses_df = process_events(responses_df)
  responses_df = responses_df[['Name', 'Date of Birth', 'Category', 'Group', PLACE, 'Events']]

  column_names = ['Name', 'Category', 'Group', 'Score']
  scores = pd.DataFrame(columns=column_names)
  try:
    for athlete in tqdm(range(len(responses_df))):
      category = get_category_from_string(responses_df.iloc[athlete]['Category'], responses_df.iloc[athlete]['Group'])
      # Keep another database for maintaining Scores.
      athlete_data = {'Name': responses_df.iloc[athlete]['Name'],
                      'Category': category,
                      'Group': responses_df.iloc[athlete]['Group'],
                      'Score': 0}
      scores = scores.append(athlete_data, ignore_index=True)
      # print(scores)
      # Add in the database.
      for event in responses_df['Events'].iloc[athlete]:
        cur_event_name= f"{event} {category} {responses_df.iloc[athlete]['Group']}"
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
    traceback.print_exc()
    print(e)
    # print(f"KeyError mismatch :\n{cur_event_name} \nAthlete - {responses_df['Name'].iloc[athlete]}\nRow Number - {athlete+2}")
  scores.to_csv('data/scores.csv', index=False)
  print("Finished creating dataset")

def main():
  update_events()

if __name__=="__main__":
  main()


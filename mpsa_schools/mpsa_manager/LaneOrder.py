from data.event_data import *
import xlsxwriter
PLACE = 'School/Club'
days = ['day_1']
idx_col = 0
lane_col = 1
name_col = 2
dob_col = 3
district_col = 4
mm_col = 5
ss_col = 6
ms_col = 7

# TODO : Create DOB
def append_in_sheet(df, worksheet, row):
  lane_fill_order = [3, 4, 2, 5, 1, 6, 0, 7]
  
  for j in range(8):
    worksheet.write(row+j, lane_col, j+1)
  
  for i in range(len(df)):
    worksheet.write(row+lane_fill_order[i], name_col, df.iloc[i]['Name'])
    worksheet.write(row+lane_fill_order[i], district_col, df.iloc[i][PLACE])
    worksheet.write(row+lane_fill_order[i], dob_col, df.iloc[i]['Date of Birth'])
    worksheet.write(row+lane_fill_order[i], mm_col, df.iloc[i]['mm'])
    worksheet.write(row+lane_fill_order[i], ss_col, df.iloc[i]['ss'])
    worksheet.write(row+lane_fill_order[i], ms_col, df.iloc[i]['ms'])
  

def create_heats(cur_df):
  i = 0
  heats = []
  if (len(cur_df) > 8):
    for i in range(0, len(cur_df)-1, 8):
      heats.append(cur_df.iloc[i:i+8])
  else:
    heats.append(cur_df)
  
  return heats

def create_lane_chart(chart_name='Lane_order_MPSA_2022'):
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
      
      heats = create_heats(cur_df)
      for heat in range(len(heats)):
        worksheet.write(row, idx_col, cur_event['S.N.'], bold)
        if (len(heats) == 1):
          worksheet.write(row, name_col, f"{cur_event_name} Final", bold)
        else:
          worksheet.write(row, name_col, f"{cur_event_name} Heat {heat+1}", bold)
        row += 1
        worksheet.write(row, lane_col, "Lane", bold)
        worksheet.write(row, name_col, "Name", bold)
        worksheet.write(row, district_col, PLACE, bold)
        worksheet.write(row, dob_col, "DOB", bold)
        worksheet.write(row, mm_col, "mm", bold)
        worksheet.write(row, ss_col, "ss", bold)
        worksheet.write(row, ms_col, "ms", bold)
        row += 1
        append_in_sheet(heats[heat], worksheet, row)
        row += 9
  workbook.close()
    
    
create_lane_chart()

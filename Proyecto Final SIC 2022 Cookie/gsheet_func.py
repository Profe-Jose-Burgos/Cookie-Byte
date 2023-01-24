import gspread
from oauth2client.service_account import ServiceAccountCredentials

s=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name("chatbot_GCA.json",s)
client = gspread.authorize(creds)

sheet = client.open("Citas").sheet1
row_values = sheet.row_values(1)
col_values = sheet.col_values(1)
row_filled = len(col_values)
col_filled = len(row_values)

def guardar_fecha_cita(date):
    sheet.update_cell(row_filled+1,1,date)
    print("Fecha Guardada!")
    return 0

def guardar_info_cita(msg):
    sheet.update_cell(row_filled+1,2,msg)
    print("Info de cita guardada")
    return 0

    
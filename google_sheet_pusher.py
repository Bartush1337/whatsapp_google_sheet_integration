from google.oauth2 import service_account
import gspread
import json

class SpreadSheetCommunicator():
    def __init__(self, config):
        service_account.Credentials.from_service_account_file(
            config['permissions_file'],
            scopes=['https://www.googleapis.com/auth/spreadsheets'],
        )
        gc = gspread.service_account(filename=config['permissions_file'])
        self.sheet = gc.open_by_url(config["spreadsheet_url"])

    def communicate_message(self, message):
        if 'driver' in message.keys():
            worksheet = self.sheet.worksheet('drivers')
            del message['driver']
        elif 'passanger' in message.keys():
            worksheet = self.sheet.worksheet('passangers')
            del message['passanger']
        elif 'error' in message.keys() :
            worksheet = self.sheet.worksheet('other')
            del message['error']
        print(list(message.values()))
        worksheet.append_rows([list(message.values())])



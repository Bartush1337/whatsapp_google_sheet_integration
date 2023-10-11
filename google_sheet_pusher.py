from google.oauth2 import service_account
import gspread
import json


class SpreadSheetCommunicator:
    def __init__(self, config):
        service_account.Credentials.from_service_account_file(
            config["permissions_file"],
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        gc = gspread.service_account(filename=config["permissions_file"])
        self.sheet = gc.open_by_url(config["spreadsheet_url"])

    def next_available_row(self, worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return str(len(str_list) + 1)

    def communicate_message(self, message):
        case = ""
        if "driver" in message.keys():
            worksheet = self.sheet.worksheet("drivers")
            case = "driver"
            del message["driver"]

        elif "passanger" in message.keys():
            worksheet = self.sheet.worksheet("passangers")
            case = "passenger"
            del message["passanger"]

        elif "error" in message.keys():
            worksheet = self.sheet.worksheet("other")
            del message["error"]

        print(list(message.values()))

        values = []
        if case == "driver":
            values = [
                "נהג פעיל",
                message["name"],
                message["number"],
                message["start_location"],
                message["end_location"],
                "",
                message["date"],
                message["time"],
            ]
        elif case == "passenger":
            values = [
                "מחכה לטיפול",
                message["name"],
                message["number"],
                message["start_location"],
                message["end_location"],
                message["date"],
                message["time"],
            ]

        worksheet.append_row(
            values,
            table_range=f"A{self.next_available_row(worksheet)}",
        )

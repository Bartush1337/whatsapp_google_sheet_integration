from google.oauth2 import service_account
import gspread
import logging


class SpreadSheetCommunicator:
    def __init__(self, config):
        service_account.Credentials.from_service_account_file(
            config["permissions_file"],
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        gc = gspread.service_account(filename=config["permissions_file"])

        self.demo_sheet = gc.open_by_url(config["demo_spreadsheet_url"])
        self.main_sheet =gc.open_by_url(config["main_spreadsheet_url"])

    def next_available_row(self,worksheet):
        cols = worksheet.range(1, 1, worksheet.row_count, 10)
        return max([cell.row for cell in cols if cell.value]) + 1
        


    def communicate_message(self, message, stopped):
        try:
            sheet = self.demo_sheet if stopped else self.main_sheet
            
            case = ""
            if "driver" in message.keys():
                worksheet = sheet.worksheet("Drivers")
                case = "driver"
                del message["driver"]

            elif "passanger" in message.keys():
                worksheet = sheet.worksheet("Hitchhikers")
                case = "passenger"
                del message["passanger"]

            elif "error" in message.keys():
                worksheet = sheet.worksheet("bot-errors")
                case = "error"
                del message["error"]

            print(list(message.values()))
            values = []

            if case == "driver":
                values = [
                    "נהג פעיל",                             #A
                    message["name"],                        #B
                    message["number"],                      #C
                    message["start_location"],              #D
                    message["end_location"],                #E
                    "",                                     #F
                    message["date"],                        #G
                    message["time"],                        #H
                    "",                                     #I
                    "",                                     #J
                    "",                                     #K
                    "",                                     #L
                    message["armed"],                       #M
                    "",                                     #N
                    message["hour"]                         #O
                ]

            if case == "passenger":
                values = [
                    "מחכה לטיפול",
                    message["name"],
                    message["number"],
                    message["start_location"],
                    message["end_location"],
                    message["date"],
                    message["time"],
                    "",
                    "",
                    "",
                    message["hour"]
                ]

            if case == "error":
                values = [message.values()]


            worksheet.append_row(
                values,
                table_range=f"A{self.next_available_row(worksheet)}",
            )

        except Exception as exc:
            logging.error(f"Failed to communicate message: {message}")
            raise exc

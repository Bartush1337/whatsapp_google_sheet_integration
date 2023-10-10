import google_sheet_pusher
import parser
import json

def main():
    par = parser.Parser()
    config = json.load(open("config.json", "rb"))
    sheet_pusher = google_sheet_pusher.SpreadSheetCommunicator(config)
    test_message = """
          מחפשת טרמפ
        שם: נוי
        מספר: 0502502955
        מיקום: ביסלח
        למיקום: מבשרת ציון
        זמן: עכשיו
        """
    message_dict = par.pattern_match(test_message)
    sheet_pusher.communicate_message(message_dict)

if __name__ == "__main__":
    main()

import unittest
from dataclasses import dataclass
import deepdiff
from parameterized import parameterized

from message_parser import MessageParser

class TestParser(unittest.TestCase):
    @parameterized.expand([
        (
            "happy flow driver", 
            """
            מציע טרמפ
            שם: אוהד
            מספר: 057654
            מיקום: תל אביב
            למיקום: ירושלים
            זמן: עכשיו
            """, 
            {
                'driver' : True, 'name' :  'אוהד', 
                'number' : '057654', 'start_location' : 'תל אביב', 
                'end_location':'ירושלים', 'time' : 'עכשיו'
            },
        ),
        (
            "happy flow with whitespaces",
            """
            שם:        אוהד
            מספר:  057654
            מיקום: תל אביב
            למיקום: ירושלים    
            זמן:     עכשיו 
            """,
            {'name' :  'אוהד', 'number' : '057654', 
            'start_location' : 'תל אביב', 'end_location':'ירושלים', 
            'time' : 'עכשיו'},
        ),
        (
            "dash in number",
            """
            שם:        אוהד
            מספר:  050-76-54
                מיקום: תל אביב
            למיקום: ירושלים    
            זמן:     עכשיו 
            """,
            {'name': 'אוהד', 'number': '050-76-54', 
            'start_location': 'תל אביב', 'end_location': 'ירושלים', 
            'time': 'עכשיו'},
        ),
        (
            "modified params order",
            """
                מיקום: תל אביב
                        שם:        אוהד
            מספר:  050-76-54
            למיקום: ירושלים    
            זמן:     עכשיו
            """,
            {'name': 'אוהד', 'number': '050-76-54', 
            'start_location': 'תל אביב', 'end_location': 'ירושלים', 
            'time': 'עכשיו'},
        ),
        (
            "alternative field names",
            """
            מחפש טרמפ:
            שם: ליה
            נייד: 05189
            ממקום: מהמכולת
            למקום: בבית
            בתאריך: היום
            בשעה: עכשיו
            """,
            {'name': 'ליה', 'number': '05189', 
            'start_location': 'מהמכולת', 'end_location': 'בבית', 
            'time': 'עכשיו', 'date': 'היום', 'passanger': True},
        ),
        (
            "uneven spaces in format",
            """
            מציעה טרמפ:
            שם : בוב
            נייד:999999
            ממקום : אני באזור הבנאי
            למקום: לכבאית
            תאריך: כל הזמן שבעולם
            זמן: 5
            חמוש: לא
            מספר מקומות : 4
            """,
            {'name': 'בוב', 'number': '999999', 
            'start_location': 'אני באזור הבנאי', 'end_location': 'לכבאית', 
            'date': 'כל הזמן שבעולם', 'time': '5', 'driver': True}
        ),
        (
            "message with '*' charecters",
            """
            *מציע טרמפ*
            *שם:* גופי
            *נייד:* 666
            *ממקום:* דיסני
            *למקום:* מארוול
            *בתאריך:* היום
            *בשעה:* 17:00 -+
            *מקומות* 2-3
            """,
            {'name': 'גופי', 'number': '666', 
            'start_location': 'דיסני', 'end_location': 'מארוול', 
            'time': '17:00 -+', 'date': 'היום', 'driver': True}
        ),
        (
            "message with '-' spacers",
            """
            מבקשת טרמפ
            שם : ציפי
            נייד- 123123
            ממקום: קן הציפור
            למקום: ערימת הגרעינים
            זמן -  מחרתיים
            בתאריך - שיש לכם זמן
            """,
            {'name': 'ציפי', 'number': '123123', 
            'start_location': 'קן הציפור', 'end_location': 'ערימת הגרעינים', 
            'date': 'שיש לכם זמן', 'time': 'מחרתיים', 'passanger': True}
        ),
        (
            "alternative phone field name",
            """
            מציע טרמפ
            שם: מוש השור
            טל: 1234
            ממקום: עובד ו-
            למקום: טוב לו
            מתי: עכשיו 
            """,
            {'name': 'מוש השור', 'number': '1234', 
            'start_location': 'עובד ו-', 'end_location': 'טוב לו', 
            'time': 'עכשיו', 'driver': True}
        ),
    ])
    def test_parser(self, name, message, expected_result):
        parser = MessageParser()
        
        diff = deepdiff.DeepDiff(
            expected_result, 
            parser.pattern_match(message), 
            exclude_paths={"root['hour']"},
        )
        
        if diff:
            raise AssertionError(f"Unexpected differences: {diff}")

if __name__ == "__main__":
    unittest.main()
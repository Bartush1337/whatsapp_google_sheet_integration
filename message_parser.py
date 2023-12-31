import re
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Pattern:
    # List of keys to search for.
    keys: List[str]
    # Regex pattern for the content.
    content: str
    # If this pattern is required.
    required: bool = True


class MessageParser:
    def __init__(self):
        # Define regular expressions for each piece of information
        self.driver_passenger_patterns = {
            "driver": [r"מציע", r"מציעה״"],
            "passanger": [r"מחפש", r"מבקשת", r"מחפשת"],
        }

        self.mandatory_patterns = {
            "name": Pattern(keys=["שם"], content=r"(.+)"),
            "number": Pattern(keys=["מספר", "נייד", "טל","טלפון"], content=r"(\s*[\d-]+\d+)"),
            "armed" : Pattern(keys=["חמושה","חמוש"], content=r"(.+)", required=False),
            "start_location": Pattern(keys=["מיקום", "ממקום"], content=r"(.+)"),
            "end_location": Pattern(keys=["למיקום", "למקום"], content=r"(.+)"),
            "time": Pattern(keys=["שעה", "זמן", "מתי","בשעה"], content=r"(.+)"),
            "date": Pattern(keys=["תאריך","בתאריך"], content=r"(.+)", required=False),
        }

        self.banned_words = {
            "stuff": Pattern(keys=["ציוד", "שינוע"], content=r"(.+)", required=False),

        }

    def pattern_match(self, message):
        # Search for matches using regular expressions
        to_return = {}
        is_driver_passanger_set = False
        message = message.replace("*", "")  # Remove '*' to make regex more stable.
        for pattern_key, pattern in self.mandatory_patterns.items():
            for key in pattern.keys:
                search_result = re.search(f"{key}\s*[:-]\s*{pattern.content}", message)
                if search_result is not None:
                    to_return[pattern_key] = search_result.group(1).strip()
                    break

            if pattern_key not in to_return:
                to_return[pattern_key] = ""
                if pattern.required:
                    raise ValueError(f"Couldn't find pattern {pattern_key}")

        for pattern_key, values in self.driver_passenger_patterns.items():
            for value in values:
                if re.search(value, message) is not None:
                    if is_driver_passanger_set:
                        raise ValueError(f"Can't decide if this is a driver or a passanger")
                    to_return[pattern_key] = True
                    is_driver_passanger_set = True

        for pattern_key, pattern in self.banned_words.items():
            for key in pattern.keys:
                search_result = re.search(f"{key}", message)
                if search_result is not None:
                    raise ValueError(f"Banned usage {pattern_key}")

        now = datetime.now()

        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        to_return["hour"] = dt_string

        return to_return

import re
import unittest

# The Hebrew message

class Parser():
    def __init__(self):
        # Define regular expressions for each piece of information
        self.optional_patterns = {
                'driver' : r'מציע',
                'passanger' : r'מחפש'}

        self.mandatory_patterns = {'name' :  r'שם: (.+)' ,
                'number' : r'מספר: (\s*[\d-]+\d+)',
                'start_location' : r'מיקום: (.+)',
                'end_location' : r'למיקום: (.+)',
                'time' : r'זמן: (.+)'}

    def pattern_match(self, message):
        #Search for matches using regular expressions
        to_return = {}
        for pattern_key in self.mandatory_patterns.keys():
            if re.search(self.mandatory_patterns[pattern_key], message) is None:
                raise(Exception("Couldn't find pattern {}".format(pattern_key)))
            to_return[pattern_key] = re.search(self.mandatory_patterns[pattern_key], message).group(1).strip()
        for pattern_key in self.optional_patterns.keys():
            if re.search(self.optional_patterns[pattern_key], message) is None:
                continue
            to_return[pattern_key] = True


        return to_return

class TestParser(unittest.TestCase):
    def test_happy_flow_driver(self):
        parser = Parser()
        message ="""
          מציע טרמפ
        שם: אוהד
        מספר: 057654
        מיקום: תל אביב
        למיקום: ירושלים
        זמן: עכשיו
        """
        expected_result = {'is_driver' : True, 'name' :  'אוהד', 'number' : '057654', 'start_location' : 'תל אביב',
                           'end_location':'ירושלים', 'time' : 'עכשיו'}
        self.assertEquals(expected_result, parser.pattern_match(message))
    def test_happy_flow_with_whitespaces(self):
        parser = Parser()
        message ="""
        שם:        אוהד
        מספר:  057654
         מיקום: תל אביב
        למיקום: ירושלים    
        זמן:     עכשיו 
        """
        expected_result = {'name' :  'אוהד', 'number' : '057654', 'start_location' : 'תל אביב',
                           'end_location':'ירושלים', 'time' : 'עכשיו'}
        self.assertEquals(expected_result, parser.pattern_match(message))

    def test_happy_flow_with_dash_in_number(self):
        parser = Parser()
        message = """
           שם:        אוהד
           מספר:  050-76-54
            מיקום: תל אביב
           למיקום: ירושלים    
           זמן:     עכשיו 
           """
        expected_result = {'name': 'אוהד', 'number': '050-76-54', 'start_location': 'תל אביב',
                           'end_location': 'ירושלים', 'time': 'עכשיו'}
        self.assertEquals(expected_result, parser.pattern_match(message))
    def test_happy_flow_modified_params_order(self):
        parser = Parser()
        message = """
            מיקום: תל אביב
                       שם:        אוהד
           מספר:  050-76-54
           למיקום: ירושלים    
           זמן:     עכשיו 
           """
        expected_result = {'name': 'אוהד', 'number': '050-76-54', 'start_location': 'תל אביב',
                           'end_location': 'ירושלים', 'time': 'עכשיו'}
        self.assertEquals(expected_result, parser.pattern_match(message))
if __name__ == "__main__":
    unittest.main()
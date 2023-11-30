"""
This module contains unit tests for the Roma Paradigm Generator application.

It includes test cases for the following modules and functions:
- search_handler:   clean_text, replace_special_characters, get_pos_category, 
                    get_gender_category, search_word.
- language_processor: generate_obliquus, generate_noun_paradigms.


To run the tests, execute this module directly.

"""


import unittest
import csv
from search_handler import clean_text, replace_special_characters, get_pos_category, get_gender_category, search_word
from language_processor import generate_obliquus, generate_noun_paradigms
# from user_interface import perform_search


class TestSearchHandler(unittest.TestCase):
    '''Test cases for the search_handler module.'''
    def test_clean_text(self):
        '''Test clean_text function.'''
        input_text = "\u00a0 \t This iS a Te\tst String. \r \n"
        expected_output = "this is a test string."
        result = clean_text(input_text)
        self.assertEqual(result, expected_output)

    def test_replace_special_characters(self):
        '''Test replace_special_characters function.'''
        input_word = "čťľšžýáíéóúŕäôĺňď"
        expected_output = "ctlszyaieouraolnd"
        result = replace_special_characters(input_word)
        self.assertEqual(result, expected_output)

    def test_get_pos_category(self):
        '''Test get_pos_category function.'''
        pos_rom_verb = "(sloveso, regionálny výraz)"
        pos_rom_noun = "(podstatné meno, mužský rod, zdrobnenina)"
        pos_rom_other = "(prídavné meno, mužský rod)"
        
        result_verb = get_pos_category(pos_rom_verb)
        result_noun = get_pos_category(pos_rom_noun)
        result_other = get_pos_category(pos_rom_other)
        
        self.assertEqual(result_verb, "verb")
        self.assertEqual(result_noun, "noun")
        self.assertEqual(result_other, "other")

    def test_get_gender_category(self):
        '''Test the get_gender_category function.'''
        pos_rom_feminine = "(podstatné meno, ženský rod)"
        pos_rom_masculine = "(podstatné meno, mužský rod, zdrobnenina)"
        pos_rom_other = "(príslovka)"
        
        result_feminine = get_gender_category(pos_rom_feminine)
        result_masculine = get_gender_category(pos_rom_masculine)
        result_other = get_gender_category(pos_rom_other)
        
        self.assertEqual(result_feminine, "feminine")
        self.assertEqual(result_masculine, "masculine")
        self.assertEqual(result_other, "other")
    
    def test_search_word(self):
        '''Test search_word function with existing words.'''
        result1 = search_word("kher")
        result2 = search_word("čambel")
        result3 = search_word("žila")
        result4 = search_word("arminakeri zumin / jarminakeri zumin")
        result5 = search_word("grisoskeri zamiška")

        expected_output1 = {"word": "kher", "part_of_speech": "noun", "gender": "masculine"}
        expected_output2 = {"word": "čambel", "part_of_speech": "verb", "gender": "other"}
        expected_output3 = {"word": "žila", "part_of_speech": "noun", "gender": "feminine"}
        expected_output4 = {"word": "arminakeri zumin / jarminakeri zumin", "part_of_speech": "other", "gender": "feminine"}
        expected_output5 = {"word": "grisoskeri zamiška", "part_of_speech": "other", "gender": "other"}
        
        self.assertEqual(result1, expected_output1)
        self.assertEqual(result2, expected_output2)
        self.assertEqual(result3, expected_output3)
        self.assertEqual(result4, expected_output4)
        self.assertEqual(result5, expected_output5)



class TestLanguageProcessor(unittest.TestCase):
    '''Test cases for the language_processor module.'''
    def test_generate_obliquus(self):
        '''Test the generate_obliquus function.'''
        # Read data from the CSV file
        with open('obliquus_test.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Extract input values and expected outputs
                input_word = row['input_word']
                input_gender = row['input_gender']
                expected_obl_sg = row['expected_obl_sg']
                expected_obl_pl = row['expected_obl_pl']
                expected_gender = row['expected_gender']
                expected_noun_type = row['expected_noun_type']

                # Call the generate_obliquus function
                result = generate_obliquus(input_word, input_gender)

                # Create the expected output tuple
                expected_output = (expected_obl_sg, expected_obl_pl, expected_gender, expected_noun_type)

                # Perform the assertion
                self.assertEqual(result, expected_output)
    
    def test_generate_noun_paradigms(self):
        '''Test the generate_noun_paradigms function.'''
        # Read data from the CSV file
        with open('paradigms_test.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Extract input values and expected outputs
                input_word = row['input_word']
                input_obl_sg = row['input_obl_sg']
                input_obl_pl = row['input_obl_pl']
                input_gender = row['input_gender']
                input_noun_type = row['input_noun_type']
                input_animacy = row['input_animacy']

                expected_outputs = {
                    'Singulár': {
                        'nominatív': row['nom_sg'],
                        'genitív': row['gen_sg'],
                        'datív': row['dat_sg'],
                        'akuzatív': row['aku_sg'],
                        'vokatív': row['voc_sg'],
                        'lokál': row['lok_sg'],
                        'ablativ': row['abl_sg'],
                        'inštrumentál': row['ins_sg'],
                    },
                    'Plurál': {
                        'nominatív': row['nom_pl'],
                        'genitív': row['gen_pl'],
                        'datív': row['dat_pl'],
                        'akuzatív': row['aku_pl'],
                        'vokatív': row['voc_pl'],
                        'lokál': row['lok_pl'],
                        'ablativ': row['abl_pl'],
                        'inštrumentál': row['ins_pl'],
                    },
                }

                # Call the generate_noun_paradigms function
                result = generate_noun_paradigms(input_word, input_obl_sg, input_obl_pl, input_gender, input_noun_type, input_animacy)

                # Perform the assertion
                self.assertEqual(result, expected_outputs)




# class TestUserInterface(unittest.TestCase):
#     def test_perform_search(self):
#         # Add test cases for the perform_search function
#         pass


if __name__ == '__main__':
    unittest.main()

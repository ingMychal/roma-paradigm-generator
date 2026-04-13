"""
This module contains unit tests for the Roma Paradigm Generator application.

"""

import os
import unittest
import csv
from search_handler import clean_text, replace_special_characters, get_pos_category, get_gender_category, search_word
import search_handler
from nouns import generate_obliquus, generate_noun_paradigms

# Resolve paths relative to this file so tests pass regardless of working directory
_HERE = os.path.dirname(os.path.abspath(__file__))


class TestSearchHandler(unittest.TestCase):
    '''Test cases for the search_handler module.'''

    def setUp(self):
        # Reset XML cache so each test gets a clean parse (important if xml_file_path changes)
        search_handler._xml_root_cache = None

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

        self.assertEqual(get_pos_category(pos_rom_verb), "verb")
        self.assertEqual(get_pos_category(pos_rom_noun), "noun")
        self.assertEqual(get_pos_category(pos_rom_other), "other")

    def test_get_gender_category(self):
        '''Test the get_gender_category function.'''
        pos_rom_feminine = "(podstatné meno, ženský rod)"
        pos_rom_masculine = "(podstatné meno, mužský rod, zdrobnenina)"
        pos_rom_other = "(príslovka)"

        self.assertEqual(get_gender_category(pos_rom_feminine), "feminine")
        self.assertEqual(get_gender_category(pos_rom_masculine), "masculine")
        self.assertEqual(get_gender_category(pos_rom_other), "other")

    def test_search_word_sample_data(self):
        '''Test search_word with words present in the bundled sample SRO.xml.'''
        # "phral" (brother) and "učiťeľka" (teacher) are in the sample XML.
        result_phral = search_word("phral")
        self.assertEqual(result_phral, {"word": "phral", "part_of_speech": "noun", "gender": "masculine"})

        result_ucitelka = search_word("učiťeľka")
        self.assertEqual(result_ucitelka, {"word": "učiťeľka", "part_of_speech": "noun", "gender": "feminine"})

    def test_search_word_full_dictionary(self):
        '''
        Test search_word with words from the full dictionary.
        NOTE: These tests require the complete SRO.xml, not just the bundled sample.
        They are expected to fail when running against the limited demo data.
        '''
        result1 = search_word("kher")
        result2 = search_word("čambel")
        result3 = search_word("žila")
        result4 = search_word("arminakeri zumin / jarminakeri zumin")
        result5 = search_word("grisoskeri zamiška")

        # Skip gracefully if words are not in the current data file
        if not isinstance(result1, dict):
            self.skipTest("Full dictionary not available; skipping full-dictionary search tests.")

        self.assertEqual(result1, {"word": "kher", "part_of_speech": "noun", "gender": "masculine"})
        self.assertEqual(result2, {"word": "čambel", "part_of_speech": "verb", "gender": "other"})
        self.assertEqual(result3, {"word": "žila", "part_of_speech": "noun", "gender": "feminine"})
        self.assertEqual(result4, {"word": "arminakeri zumin / jarminakeri zumin", "part_of_speech": "other", "gender": "feminine"})
        self.assertEqual(result5, {"word": "grisoskeri zamiška", "part_of_speech": "other", "gender": "other"})

    def test_search_word_not_found(self):
        '''Test that search_word returns a string message for unknown words.'''
        result = search_word("xyzzy")
        self.assertIsInstance(result, str)
        self.assertIn("xyzzy", result)

    def test_search_word_empty(self):
        '''Test that an empty search term returns a helpful message.'''
        result = search_word("")
        self.assertIsInstance(result, str)

    def test_search_word_containing_word_substring(self):
        '''Regression: searching for a word that contains "word" as substring must not crash.'''
        result = search_word("keyword")
        # Should be a not-found string, NOT raise TypeError
        self.assertIsInstance(result, str)


class TestLanguageProcessor(unittest.TestCase):
    '''Test cases for the language_processor module.'''

    def test_generate_obliquus(self):
        '''Test the generate_obliquus function.'''
        csv_path = os.path.join(_HERE, 'tests', 'obliquus_test.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                input_word = row['input_word']
                input_gender = row['input_gender']
                expected_output = (
                    row['expected_obl_sg'],
                    row['expected_obl_pl'],
                    row['expected_gender'],
                    row['expected_noun_type'],
                )
                with self.subTest(word=input_word):
                    result = generate_obliquus(input_word, input_gender)
                    self.assertEqual(result, expected_output)

    def test_generate_noun_paradigms(self):
        '''Test the generate_noun_paradigms function.'''
        csv_path = os.path.join(_HERE, 'tests', 'paradigms_test.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                input_word = row['input_word']
                input_gender = row['input_gender']
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

                with self.subTest(word=input_word):
                    result = generate_noun_paradigms(input_word, input_gender, input_animacy)
                    self.assertEqual(result, expected_outputs)


if __name__ == '__main__':
    unittest.main()

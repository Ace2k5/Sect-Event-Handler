import unittest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from . import arknights, limbus
from .. import utils

class TestLimbusScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = limbus.LimbusScraper()
    
    def test_find_events_with_none_soup(self):
        '''Test that None soup returns None'''
        result = self.scraper.find_events(None, "lcbtable2", "Limbus Company", "February 2026")
        self.assertIsNone(result)
    
    def test_find_events_with_wrong_game(self):
        '''Test that wrong game name returns None'''
        mock_soup = Mock()
        result = self.scraper.find_events(mock_soup, "lcbtable2", "Arknights", "February 2026")
        self.assertIsNone(result)
    
    def test_format_events_with_none(self):
        '''Test that None input returns None'''
        result = self.scraper.format_events(None)
        self.assertIsNone(result)
    
    def test_format_events_with_valid_data(self):
        '''Test formatting with proper 3-element rows'''
        row_data = [
            ['Hell\'s Chicken', 'April 20th, 2023', 'May 4th, 2023'],
            ['Hell\'s Chicken', 'April 20th, 2023', 'May 4th, 2023']  # Duplicate to test dedup
        ]
        result = self.scraper.format_events(row_data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # Should deduplicate to 1
        self.assertIn("Hell's Chicken", result[0])
    
    def test_format_events_with_empty_strings(self):
        '''Test that empty strings are trimmed'''
        row_data = [
            ['', 'New Manager Attendance Check Event', 'April 20th, 2023', 'May 4th, 2023']
        ]
        result = self.scraper.format_events(row_data)
        self.assertIsNotNone(result)
        self.assertIn("New Manager Attendance Check Event", result[0])
    
    def test_format_events_with_insufficient_columns(self):
        '''Test that rows with < 3 elements are skipped'''
        row_data = [
            ['Event Name'],  # Only 1 element
            ['Event Name', 'Start Date'],  # Only 2 elements
        ]
        result = self.scraper.format_events(row_data)
        self.assertIsNone(result)  # No valid events
    
    def test_format_events_mixed_valid_invalid(self):
        '''Test with mix of valid and invalid rows'''
        row_data = [
            ['Event Name'],  # Invalid
            ['Hell\'s Chicken', 'April 20th, 2023', 'May 4th, 2023'],  # Valid
            ['Incomplete Event', 'Start Date']  # Invalid
        ]
        result = self.scraper.format_events(row_data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # Only 1 valid event


class TestArkScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = arknights.ArkScraper()
    
    def test_find_events_with_none_soup(self):
        '''Test that None soup returns None'''
        result = self.scraper.find_events(None, "mrfz-wtable flex-table", "Arknights", ["2026-02"])
        self.assertIsNone(result)
    
    def test_find_events_with_wrong_game(self):
        '''Test that wrong game name returns None'''
        mock_soup = Mock()
        result = self.scraper.find_events(mock_soup, "mrfz-wtable flex-table", "Limbus Company", ["2026-02"])
        self.assertIsNone(result)
    
    def test_format_events_with_none(self):
        '''Test that None input returns None'''
        result = self.scraper.format_events(None)
        self.assertIsNone(result)
    
    def test_format_events_with_valid_data(self):
        '''Test formatting with proper event data'''
        row_data = [
            ['Side Story – Carnival', 'Global:2026/01/16 – 2026/02/06(asArknightsGlobal\'s 6th Anniversary event)']
        ]
        result = self.scraper.format_events(row_data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertIn("Side Story – Carnival", result[0])
        self.assertNotIn("(asArknights", result[0])  # Parentheses should be removed
    
    def test_format_events_removes_parentheses(self):
        '''Test that parenthetical text is removed'''
        row_data = [
            ['Event Name', 'Global:2026/01/16 – 2026/02/06(some annotation)']
        ]
        result = self.scraper.format_events(row_data)
        self.assertIsNotNone(result)
        self.assertNotIn("(some annotation)", result[0])
        self.assertIn("Global:2026/01/16 – 2026/02/06", result[0])
    
    def test_format_events_without_global_prefix(self):
        '''Test handling of rows without Global: prefix'''
        row_data = [
            ['Event Name', '2026/01/16 – 2026/02/06']
        ]
        result = self.scraper.format_events(row_data)
        self.assertIsNotNone(result)


class TestUtils(unittest.TestCase):
    def test_deduplication_with_duplicates(self):
        '''Test that duplicates are removed'''
        row_data = [
            ['Event A', 'Date 1'],
            ['Event A', 'Date 1'],  # Duplicate
            ['Event B', 'Date 2']
        ]
        result = utils.deduplication(row_data)
        self.assertEqual(len(result), 2)
    
    def test_deduplication_with_none(self):
        '''Test deduplication handles exceptions gracefully'''
        result = utils.deduplication(None)
        self.assertIsNone(result)
    
    def test_trim_empty_strings(self):
        '''Test that empty strings are removed'''
        list_events = [
            ['', 'Event Name', 'Date 1', ''],
            ['Event B', '', 'Date 2']
        ]
        result = utils.trimEmptyString(list_events)
        self.assertEqual(result[0], ['Event Name', 'Date 1'])
        self.assertEqual(result[1], ['Event B', 'Date 2'])
    
    def test_trim_empty_strings_all_empty(self):
        '''Test with all empty strings'''
        list_events = [['', '', '']]
        result = utils.trimEmptyString(list_events)
        self.assertEqual(result[0], [])


if __name__ == '__main__':
    unittest.main()
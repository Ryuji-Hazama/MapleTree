"""
Unit tests for MapleJson module.
Tests reading, writing, and encryption/decryption of JSON files.
"""

import os
import base64
import unittest
from src.maplex import MapleJson

class TestMapleJson(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.test_file = "test_maplejson.json"
        self.test_data = {
            "name": "Test",
            "value": 123,
            "items": [1, 2, 3]
        }

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_write_and_read_json(self):
        """Test writing and reading JSON data."""
        maple_json = MapleJson(self.test_file, encrypt=False)
        maple_json.write(self.test_data)
        read_data = maple_json.read()
        self.assertEqual(self.test_data, read_data)

    def test_encryption_and_decryption(self):
        """Test encryption and decryption of JSON data."""
        maple_json = MapleJson(self.test_file)
        maple_json.setEncryption(True, key=maple_json.generateKey())
        maple_json.write(self.test_data)
        read_data = maple_json.read()
        self.assertEqual(self.test_data, read_data)

    def test_invalid_file_read(self):
        """Test reading from a non-existent file."""
        maple_json = MapleJson("non_existent_file.json", encrypt=False)
        with self.assertRaises(Exception):
            maple_json.read()

if __name__ == "__main__":
    unittest.main()
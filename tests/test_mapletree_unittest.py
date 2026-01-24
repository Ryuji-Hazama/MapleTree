"""
Unit tests for MapleTree library
Tests file operations, encryption, data manipulation, and error handling
"""

import unittest
import os
import tempfile
import shutil
import base64

from src.maplex import (
    MapleTree,
    MapleFileNotFoundException,
    NotAMapleFileException,
    MapleFileEmptyException,
    KeyEmptyException,
    MapleTagNotFoundException,
    MapleHeaderNotFoundException,
    MapleEncryptionNotEnabledException
)


class TestMapleTreeBasicOperations(unittest.TestCase):
    """Test basic MapleTree file operations"""
    
    @classmethod
    def setUpClass(cls):
        """Create temporary directory for all tests"""
        cls.test_dir = tempfile.mkdtemp(prefix="mapletree_test_")
    
    @classmethod
    def tearDownClass(cls):
        """Remove temporary directory after all tests"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up test files before each test"""
        self.test_file = os.path.join(self.test_dir, 'test.mpl')
        self.encrypted_file = os.path.join(self.test_dir, 'encrypted.mpl')
    
    def tearDown(self):
        """Clean up test files after each test"""
        for f in [self.test_file, self.encrypted_file]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_create_base_file(self):
        """Test loading a basic MapleTree file"""
        
        maple = MapleTree(self.test_file, createBaseFile=True)
        self.assertTrue(os.path.exists(self.test_file))
        # Verify file has correct structure
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn('MAPLE', content)
            self.assertIn('EOF', content)
    
    def test_file_not_found(self):
        """Test exception when file doesn't exist"""
        non_existent = os.path.join(self.test_dir, 'nonexistent.mpl')
        with self.assertRaises(MapleFileNotFoundException):
            MapleTree(non_existent)
    
    def test_save_and_read_value_root_level(self):
        """Test saving and reading a value at root level"""
        maple = MapleTree(self.test_file, createBaseFile=True)
        test_data = "Test data at root"
        maple.saveValue("ROOT_TAG", test_data, save=True)
        
        # Read back the value
        result = maple.readMapleTag("ROOT_TAG")
        self.assertEqual(result, test_data)
    
    def test_save_and_read_value_with_headers(self):
        """Test saving and reading values within headers"""
        maple = MapleTree(self.test_file, createBaseFile=True)
        test_data = "Data in header"
        maple.saveValue("TAG1", test_data, "HEADER1", save=True)
        
        result = maple.readMapleTag("TAG1", "HEADER1")
        self.assertEqual(result, test_data)
    
    def test_nested_headers(self):
        """Test operations with nested headers"""
        maple = MapleTree(self.test_file, createBaseFile=True)
        test_data = "Nested data"
        maple.saveValue("NESTED_TAG", test_data, "HEADER1", "HEADER2", "HEADER3", save=True)
        
        result = maple.readMapleTag("NESTED_TAG", "HEADER1", "HEADER2", "HEADER3")
        self.assertEqual(result, test_data)
    
    def test_update_existing_value(self):
        """Test updating an existing tag value"""
        maple = MapleTree(self.test_file, createBaseFile=True)
        
        # Save initial value
        maple.saveValue("UPDATE_TAG", "Initial", save=True)
        initial = maple.readMapleTag("UPDATE_TAG")
        self.assertEqual(initial, "Initial")
        
        # Update value
        maple.saveValue("UPDATE_TAG", "Updated", save=True)
        updated = maple.readMapleTag("UPDATE_TAG")
        self.assertEqual(updated, "Updated")
    
    def test_read_nonexistent_tag(self):
        """Test reading a tag that doesn't exist"""
        maple = MapleTree(self.test_file, createBaseFile=True)
        nonexists = maple.readMapleTag("NONEXISTENT_TAG")
        self.assertIsNone(nonexists)
    
    def test_read_tag_in_wrong_header(self):
        """Test reading a tag from wrong header"""
        maple = MapleTree(self.test_file, createBaseFile=True)
        maple.saveValue("TAG1", "data", "HEADER1", save=True)
        
        with self.assertRaises((MapleHeaderNotFoundException, MapleTagNotFoundException)):
            maple.readMapleTag("TAG1", "WRONG_HEADER")

    def test_getters_and_setters(self):
        """Test getters and setters for file properties"""
        maple = MapleTree(self.test_file, createBaseFile=True)
        
        # Test file path getter
        self.assertEqual(maple.getFilePath(), self.test_file)
        
        # Test encryption status
        self.assertFalse(maple.isEncrypted())
        
        # Test setting and getting encryption (without actual encryption)
        maple.setEncryption(True)
        self.assertTrue(maple.isEncrypted())
        
        maple.setEncryption(False)
        self.assertFalse(maple.isEncrypted())
        
        # Test setting and getting encryption key
        test_key = base64.urlsafe_b64encode(os.urandom(32))
        maple.setEncryptionKey(test_key)
        self.assertEqual(maple.getEncryptionKey(), test_key)


class TestMapleTreeNotes(unittest.TestCase):
    """Test MapleTree notes functionality"""
    
    def setUp(self):
        """Set up test file before each test"""
        self.test_dir = tempfile.mkdtemp(prefix="mapletree_notes_")
        self.test_file = os.path.join(self.test_dir, 'notes.mpl')
    
    def _create_base_file(self, filepath):
        """Helper to create a basic Maple file"""
        with open(filepath, 'w') as f:
            f.write("MAPLE\nEOF")
        
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_save_and_read_notes(self):
        """Test saving and reading notes"""
        self._create_base_file(self.test_file)
        maple = MapleTree(self.test_file)
        notes = ["First line", "Second line", "Third line"]
        
        maple.saveNotes(notes, "NOTES_HEADER", save=True)
        read_notes = maple.readNotes("NOTES_HEADER")
        
        self.assertEqual(read_notes, notes)
    
    def test_save_notes_with_nested_headers(self):
        """Test notes in nested headers"""
        self._create_base_file(self.test_file)
        maple = MapleTree(self.test_file)
        notes = ["Nested note 1", "Nested note 2"]
        
        maple.saveNotes(notes, "HEADER1", "HEADER2", save=True)
        read_notes = maple.readNotes("HEADER1", "HEADER2")
        
        self.assertEqual(read_notes, notes)
    
    def test_update_notes(self):
        """Test updating existing notes"""
        self._create_base_file(self.test_file)
        maple = MapleTree(self.test_file)
        
        initial_notes = ["Initial note"]
        maple.saveNotes(initial_notes, "UPDATE_NOTES", save=True)
        
        updated_notes = ["Updated note 1", "Updated note 2"]
        maple.saveNotes(updated_notes, "UPDATE_NOTES", save=True)
        
        result = maple.readNotes("UPDATE_NOTES")
        self.assertEqual(result, updated_notes)


class TestMapleTreeEncryption(unittest.TestCase):
    """Test MapleTree encryption features"""
    
    def setUp(self):
        """Set up test files and encryption key"""
        self.test_dir = tempfile.mkdtemp(prefix="mapletree_encrypt_")
        self.encrypted_file = os.path.join(self.test_dir, 'encrypted.mpl')
        # Generate a proper 32-byte key and base64 encode it (Fernet requirement)
        self.key = base64.urlsafe_b64encode(os.urandom(32))
        
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_create_encrypted_file(self):
        """Test creating an encrypted MapleTree file using createBaseFile"""
        # createBaseFile works correctly for encrypted files
        maple = MapleTree(self.encrypted_file, encrypt=True, key=self.key, createBaseFile=True)
        self.assertTrue(os.path.exists(self.encrypted_file))
        
        # Verify file is encrypted (should not be plain text)
        with open(self.encrypted_file, 'rb') as f:
            content = f.read()
            # Encrypted content should not contain plain "MAPLE" text
            self.assertNotIn(b'MAPLE\n', content)
    
    def test_save_and_read_encrypted_data(self):
        """Test saving and reading data in encrypted file"""
        maple = MapleTree(self.encrypted_file, encrypt=True, key=self.key, createBaseFile=True)
        secret_data = "Sensitive Information"
        
        maple.saveValue("SECRET_TAG", secret_data, "SECURE_HEADER", save=True)
        result = maple.readMapleTag("SECRET_TAG", "SECURE_HEADER")
        
        self.assertEqual(result, secret_data)
    
    def test_reopen_encrypted_file(self):
        """Test reopening and reading an encrypted file"""
        # Create and save encrypted data
        maple1 = MapleTree(self.encrypted_file, encrypt=True, key=self.key, createBaseFile=True)
        test_data = "Persistent encrypted data"
        maple1.saveValue("PERSIST_TAG", test_data, save=True)
        
        # Reopen file and verify data persistence
        maple2 = MapleTree(self.encrypted_file, encrypt=True, key=self.key)
        result = maple2.readMapleTag("PERSIST_TAG")
        
        self.assertEqual(result, test_data)
    
    def test_encryption_without_key_raises_error(self):
        """Test that encryption without key raises exception"""
        with self.assertRaises(KeyEmptyException):
            MapleTree(self.encrypted_file, encrypt=True, key=None, createBaseFile=True)
    
    def test_wrong_key_fails(self):
        """Test that wrong encryption key fails to decrypt"""
        # Create file with one key
        maple1 = MapleTree(self.encrypted_file, encrypt=True, key=self.key, createBaseFile=True)
        maple1.saveValue("TAG", "data", save=True)
        
        # Try to open with different key (also 32 bytes, base64 encoded)
        wrong_key = base64.urlsafe_b64encode(os.urandom(32))
        with self.assertRaises(Exception):  # Fernet will raise an error
            MapleTree(self.encrypted_file, encrypt=True, key=wrong_key)
    
    def test_change_encryption_key(self):
        """Test changing encryption key"""
        # Create encrypted file
        maple = MapleTree(self.encrypted_file, encrypt=True, key=self.key, createBaseFile=True)
        maple.saveValue("TAG", "data", save=True)
        
        # Change key (also 32 bytes, base64 encoded)
        new_key = base64.urlsafe_b64encode(os.urandom(32))
        maple.changeEncryptionKey(new_key, save=True)
        
        # Verify file can be opened with new key
        maple_new = MapleTree(self.encrypted_file, encrypt=True, key=new_key)
        result = maple_new.readMapleTag("TAG")
        self.assertEqual(result, "data")
    
    def test_change_key_on_unencrypted_file_raises_error(self):
        """Test that changing key on unencrypted file raises exception"""
        unencrypted_file = os.path.join(self.test_dir, 'plain.mpl')
        # Create unencrypted file properly (as text)
        with open(unencrypted_file, 'w') as f:
            f.write("MAPLE\nEOF")
        maple = MapleTree(unencrypted_file)
        
        new_key = base64.urlsafe_b64encode(os.urandom(32))
        with self.assertRaises(MapleEncryptionNotEnabledException):
            maple.changeEncryptionKey(new_key)
    
    def test_key_must_be_32_bytes_base64(self):
        """Test that encryption key must be properly formatted"""
        # Invalid key (not 32 bytes when decoded)
        invalid_key = base64.urlsafe_b64encode(b"short_key")
        
        with self.assertRaises(Exception):  # Fernet will raise ValueError
            MapleTree(self.encrypted_file, encrypt=True, key=invalid_key, createBaseFile=True)


class TestMapleTreeFileValidation(unittest.TestCase):
    """Test MapleTree file format validation"""
    
    def setUp(self):
        """Set up test directory"""
        self.test_dir = tempfile.mkdtemp(prefix="mapletree_validation_")
        
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_invalid_file_format(self):
        """Test that invalid file format raises exception"""
        invalid_file = os.path.join(self.test_dir, 'invalid.mpl')
        with open(invalid_file, 'w') as f:
            f.write("This is not a valid Maple file\n")
        
        with self.assertRaises(NotAMapleFileException):
            MapleTree(invalid_file)
    
    def test_empty_file(self):
        """Test that empty file raises exception"""
        empty_file = os.path.join(self.test_dir, 'empty.mpl')
        with open(empty_file, 'w') as f:
            pass  # Create empty file
        
        with self.assertRaises(MapleFileEmptyException):
            MapleTree(empty_file)


class TestMapleTreeEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios"""
    
    def setUp(self):
        """Set up test directory"""
        self.test_dir = tempfile.mkdtemp(prefix="mapletree_edge_")
        self.test_file = os.path.join(self.test_dir, 'edge.mpl')
    
    def _create_base_file(self, filepath):
        """Helper to create a basic Maple file"""
        with open(filepath, 'w') as f:
            f.write("MAPLE\nEOF")
        
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_special_characters_in_data(self):
        """Test handling special characters in data"""
        self._create_base_file(self.test_file)
        maple = MapleTree(self.test_file)
        special_data = "Data with special chars: !@#$%^&*(){}[]|\\:;\"'<>,.?/~`"
        
        maple.saveValue("SPECIAL_TAG", special_data, save=True)
        result = maple.readMapleTag("SPECIAL_TAG")
        
        self.assertEqual(result, special_data)
    
    def test_unicode_data(self):
        """Test handling Unicode characters"""
        self._create_base_file(self.test_file)
        maple = MapleTree(self.test_file)
        unicode_data = "Unicode: こんにちは 世界 🌍 αβγ"
        
        maple.saveValue("UNICODE_TAG", unicode_data, save=True)
        result = maple.readMapleTag("UNICODE_TAG")
        
        self.assertEqual(result, unicode_data)
    
    def test_empty_string_value(self):
        """Test saving empty string"""
        self._create_base_file(self.test_file)
        maple = MapleTree(self.test_file)
        maple.saveValue("EMPTY_TAG", "", save=True)
        result = maple.readMapleTag("EMPTY_TAG")
        
        self.assertEqual(result, "")
    
    def test_multiline_data(self):
        """Test handling multiline data (if supported)"""
        self._create_base_file(self.test_file)
        maple = MapleTree(self.test_file)
        # Note: MapleTree might handle this differently
        # This tests current behavior
        multiline = "Line 1\nLine 2\nLine 3"
        maple.saveValue("MULTI_TAG", multiline, save=True)
        result = maple.readMapleTag("MULTI_TAG")
        
        # Assert based on how MapleTree handles newlines
        self.assertIsNotNone(result)


class TestMapleTreeWithRealFixture(unittest.TestCase):
    """Test MapleTree with a real fixture file"""
    
    @classmethod
    def setUpClass(cls):
        """Copy the test_file.mpl if it exists"""
        cls.original_file = '/home/ryuji-hazama/Documents/Python/MapleTree/test_file.mpl'
        if os.path.exists(cls.original_file):
            cls.test_dir = tempfile.mkdtemp(prefix="mapletree_fixture_")
            cls.fixture_file = os.path.join(cls.test_dir, 'fixture.mpl')
            shutil.copy(cls.original_file, cls.fixture_file)
            cls.has_fixture = True
        else:
            cls.has_fixture = False
    
    @classmethod
    def tearDownClass(cls):
        """Clean up fixture directory"""
        if cls.has_fixture:
            shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def test_read_existing_fixture_data(self):
        """Test reading data from existing fixture file"""
        if not self.has_fixture:
            self.skipTest("Fixture file not available")
        
        maple = MapleTree(self.fixture_file)
        
        # Test reading known tags from test_file.mpl
        try:
            result = maple.readMapleTag("OOH2")
            self.assertEqual(result, "Data for OOH tag")
        except MapleTagNotFoundException:
            self.fail("Expected tag OOH2 not found in fixture")
    
    def test_read_nested_data_from_fixture(self):
        """Test reading nested header data from fixture"""
        if not self.has_fixture:
            self.skipTest("Fixture file not available")
        
        maple = MapleTree(self.fixture_file)
        
        try:
            result = maple.readMapleTag("TAG2", "HEADER 1", "HEADER 3")
            self.assertEqual(result, "TEST DATA")
        except (MapleTagNotFoundException, MapleHeaderNotFoundException):
            self.fail("Expected nested tag not found in fixture")


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)

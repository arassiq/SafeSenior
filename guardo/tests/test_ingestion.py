"""
Tests for the data ingestion module.
"""
import unittest
import tempfile
import os
from pathlib import Path

from src.ingestion import DataIngestion
from src.config import Config


class TestDataIngestion(unittest.TestCase):
    """Test cases for DataIngestion class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        self.config.DATA_PATH = Path(self.temp_dir)
        self.ingestion = DataIngestion(self.config)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_scam_phrases_success(self):
        """Test successful loading of scam phrases."""
        # Create test data file
        scam_file = self.config.DATA_PATH / "scam_phrases.txt"
        test_phrases = [
            "You have won a prize!",
            "Act now or lose forever",
            "Verify your account immediately"
        ]
        
        with open(scam_file, 'w') as f:
            f.write('\n'.join(test_phrases))
        
        # Test loading
        phrases = self.ingestion.load_scam_phrases()
        
        self.assertEqual(len(phrases), 3)
        self.assertIn("You have won a prize!", phrases)
        self.assertIn("Act now or lose forever", phrases)
    
    def test_load_scam_phrases_file_not_found(self):
        """Test loading when file doesn't exist."""
        phrases = self.ingestion.load_scam_phrases()
        self.assertEqual(phrases, [])
    
    def test_load_scam_phrases_empty_file(self):
        """Test loading from empty file."""
        scam_file = self.config.DATA_PATH / "scam_phrases.txt"
        with open(scam_file, 'w') as f:
            f.write("")
        
        phrases = self.ingestion.load_scam_phrases()
        self.assertEqual(phrases, [])
    
    def test_load_all_data(self):
        """Test loading all data sources."""
        # Create test data
        scam_file = self.config.DATA_PATH / "scam_phrases.txt"
        with open(scam_file, 'w') as f:
            f.write("Test scam phrase\nAnother scam phrase")
        
        data = self.ingestion.load_all_data()
        
        self.assertIn('scam_phrases', data)
        self.assertEqual(len(data['scam_phrases']), 2)
    
    def test_validate_data_success(self):
        """Test data validation with valid data."""
        data = {'scam_phrases': ['phrase1', 'phrase2']}
        result = self.ingestion.validate_data(data)
        self.assertTrue(result)
    
    def test_validate_data_failure(self):
        """Test data validation with invalid data."""
        data = {'scam_phrases': []}
        result = self.ingestion.validate_data(data)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

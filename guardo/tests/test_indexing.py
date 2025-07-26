"""
Tests for the indexing module.
"""
import unittest
from pathlib import Path
import tempfile

from src.indexing import ScamIndexer
from src.config import Config
from src.ingestion import DataIngestion


class TestScamIndexer(unittest.TestCase):
    """Test cases for ScamIndexer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        self.config.DATA_PATH = Path(self.temp_dir)
        self.config.INDEX_PATH = Path(self.temp_dir) / "indexes"
        self.ingestion = DataIngestion(self.config)
        self.indexer = ScamIndexer(self.config)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_create_documents(self):
        """Test creation of documents from scam phrases."""
        phrases = ["Scam phrase 1", "Scam phrase 2"]
        documents = self.indexer.create_documents(phrases)
        
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0].text, "Scam phrase 1")
        self.assertEqual(documents[1].text, "Scam phrase 2")
    
    def test_build_index(self):
        """Test building of index from data."""
        # Create test data file
        scam_file = self.config.DATA_PATH / "scam_phrases.txt"
        test_phrases = [
            "You have won a prize!",
            "Act now or lose forever",
            "Verify your account immediately"
        ]
        
        with open(scam_file, 'w') as f:
            f.write('\n'.join(test_phrases))
        
        data = self.ingestion.load_all_data()
        index = self.indexer.build_index(data)
        
        self.assertIsNotNone(index)
        self.assertEqual(len(index.nodes), 3)
    
    def test_save_index(self):
        """Test saving of index to disk."""
        scam_file = self.config.DATA_PATH / "scam_phrases.txt"
        with open(scam_file, 'w') as f:
            f.write("Sample scam phrase")
        
        data = self.ingestion.load_all_data()
        self.indexer.build_index(data)
        result = self.indexer.save_index()
        
        self.assertTrue(result)
        self.assertTrue((self.config.INDEX_PATH / "index_store.json").exists())
    
    def test_load_index(self):
        """Test loading of index from disk."""
        # Save index first
        scam_file = self.config.DATA_PATH / "scam_phrases.txt"
        with open(scam_file, 'w') as f:
            f.write("Sample scam phrase")
        
        data = self.ingestion.load_all_data()
        self.indexer.build_index(data)
        self.indexer.save_index()
        
        # Load index
        loaded_index = self.indexer.load_index()
        self.assertIsNotNone(loaded_index)


if __name__ == '__main__':
    unittest.main()


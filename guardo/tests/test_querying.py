"""
Tests for the querying module.
"""
import unittest
from pathlib import Path
import tempfile

from src.querying import ScamDetector
from src.indexing import ScamIndexer
from src.config import Config
from src.ingestion import DataIngestion


class TestScamDetector(unittest.TestCase):
    """Test cases for ScamDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        self.config.DATA_PATH = Path(self.temp_dir)
        self.config.INDEX_PATH = Path(self.temp_dir) / "indexes"
        
        # Create test data and index
        scam_file = self.config.DATA_PATH / "scam_phrases.txt"
        test_phrases = [
            "You have won a prize!",
            "Act now or lose forever",
            "Verify your account immediately",
            "Your warranty is about to expire"
        ]
        
        with open(scam_file, 'w') as f:
            f.write('\n'.join(test_phrases))
        
        # Build index
        ingestion = DataIngestion(self.config)
        indexer = ScamIndexer(self.config)
        data = ingestion.load_all_data()
        self.index = indexer.build_index(data)
        
        self.detector = ScamDetector(self.config, self.index)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_detect_scam_positive(self):
        """Test scam detection with a scam text."""
        test_text = "Congratulations! You have won a $1000 prize! Act now!"
        result = self.detector.detect_scam(test_text)
        
        self.assertIn('text', result)
        self.assertIn('is_scam', result)
        self.assertIn('risk_score', result)
        self.assertIn('confidence', result)
        self.assertEqual(result['text'], test_text)
    
    def test_detect_scam_negative(self):
        """Test scam detection with legitimate text."""
        test_text = "Hello, this is your doctor's office calling to confirm your appointment."
        result = self.detector.detect_scam(test_text)
        
        self.assertEqual(result['text'], test_text)
        self.assertIsInstance(result['is_scam'], bool)
        self.assertIsInstance(result['risk_score'], float)
    
    def test_calculate_risk_score(self):
        """Test risk score calculation."""
        similarities = [0.8, 0.7, 0.6]
        text = "Act now to win a prize!"
        
        risk_score = self.detector._calculate_risk_score(similarities, text)
        
        self.assertIsInstance(risk_score, float)
        self.assertLessEqual(risk_score, 1.0)
        self.assertGreaterEqual(risk_score, 0.0)
    
    def test_batch_detect(self):
        """Test batch detection of multiple texts."""
        test_texts = [
            "You have won a lottery!",
            "Hello, how are you today?",
            "Your account needs immediate verification"
        ]
        
        results = self.detector.batch_detect(test_texts)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIn('text', result)
            self.assertIn('is_scam', result)
            self.assertIn('risk_score', result)
    
    def test_extract_similar_phrases(self):
        """Test extraction of similar phrases from response."""
        # This test would need a mock response object
        # For now, test that the method doesn't crash
        class MockResponse:
            def __init__(self):
                self.source_nodes = []
        
        response = MockResponse()
        similar_phrases = self.detector._extract_similar_phrases(response)
        
        self.assertIsInstance(similar_phrases, list)


if __name__ == '__main__':
    unittest.main()

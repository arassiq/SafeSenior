"""
Indexing module for creating and managing LlamaIndex indexes.
"""
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core.storage import StorageContext
from llama_index.core.node_parser import SimpleNodeParser

from .config import Config
from .utils import setup_logger

logger = setup_logger(__name__)


class ScamIndexer:
    """Creates and manages indexes for scam detection."""
    
    def __init__(self, config: Config):
        self.config = config
        self.index_path = Path(config.INDEX_PATH)
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.index: Optional[VectorStoreIndex] = None
    
    def create_documents(self, scam_phrases: List[str]) -> List[Document]:
        """Convert scam phrases into LlamaIndex documents."""
        documents = []
        
        for i, phrase in enumerate(scam_phrases):
            doc = Document(
                text=phrase,
                metadata={
                    "doc_id": f"scam_phrase_{i}",
                    "category": "scam_phrase",
                    "source": "scam_phrases.txt"
                }
            )
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} documents from scam phrases")
        return documents
    
    def build_index(self, data: Dict[str, Any]) -> VectorStoreIndex:
        """Build vector index from data."""
        try:
            # Create documents from scam phrases
            documents = self.create_documents(data['scam_phrases'])
            
            # Parse documents into nodes
            parser = SimpleNodeParser.from_defaults()
            nodes = parser.get_nodes_from_documents(documents)
            
            # Create vector index
            self.index = VectorStoreIndex(nodes)
            
            logger.info(f"Built index with {len(nodes)} nodes")
            return self.index
        
        except Exception as e:
            logger.error(f"Error building index: {e}")
            raise
    
    def save_index(self) -> bool:
        """Save index to disk."""
        if not self.index:
            logger.error("No index to save")
            return False
        
        try:
            self.index.storage_context.persist(persist_dir=str(self.index_path))
            logger.info(f"Index saved to {self.index_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            return False
    
    def load_index(self) -> Optional[VectorStoreIndex]:
        """Load index from disk."""
        try:
            if not (self.index_path / "index_store.json").exists():
                logger.warning("No saved index found")
                return None
            
            storage_context = StorageContext.from_defaults(
                persist_dir=str(self.index_path)
            )
            self.index = VectorStoreIndex.load_index_from_storage(storage_context)
            
            logger.info("Index loaded successfully")
            return self.index
        
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return None

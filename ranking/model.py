import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SearchRankingModel(nn.Module):
    """
    Cross-encoder ranking model for search relevance.
    Uses BERT-based architecture for query-document relevance scoring.
    """
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(768, 1)  # Relevance score (0-1)
        
    def forward(self, input_ids, attention_mask):
        # Encode the query+document pairs
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        pooled = outputs.pooler_output
        pooled = self.dropout(pooled)
        score = torch.sigmoid(self.classifier(pooled))
        return score.squeeze()

class RankingService:
    """Service for ranking search results using ML models"""
    
    def __init__(self, model_path: str = None):
        self.model = SearchRankingModel()
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        logger.info(f"Ranking service initialized on {self.device}")
    
    def rank(self, query: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank candidate documents by relevance to the query.
        Combines neural relevance score with traditional features.
        """
        if not candidates:
            return []
        
        scored_results = []
        
        for doc in candidates:
            # Get neural relevance score
            neural_score = self._neural_relevance(query, doc.get('content', ''))
            
            # Compute traditional ranking features
            freshness = self._freshness_score(doc.get('last_modified', None))
            engagement = self._engagement_score(doc.get('clicks', 0), doc.get('shares', 0))
            pagerank = doc.get('pagerank_score', 0.0)
            
            # Combine scores with weights
            final_score = (
                0.40 * neural_score +
                0.25 * pagerank +
                0.20 * engagement +
                0.15 * freshness
            )
            
            scored_results.append({
                **doc,
                'score': final_score,
                'relevance_score': neural_score,
                'combined_score': final_score
            })
        
        # Sort by score descending
        scored_results.sort(key=lambda x: x['combined_score'], reverse=True)
        return scored_results
    
    def _neural_relevance(self, query: str, document: str) -> float:
        """Compute relevance using the cross-encoder model"""
        if not query or not document:
            return 0.0
        
        # Truncate document to avoid token limits
        max_length = 512
        document = document[:1000]  # Roughly 250 tokens
        
        # Tokenize query + document
        inputs = self.tokenizer(
            query,
            document,
            return_tensors="pt",
            truncation=True,
            max_length=max_length,
            padding=True
        )
        
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            score = self.model(**inputs).item()
        
        return float(score)
    
    def _freshness_score(self, last_modified: str) -> float:
        """Compute freshness score based on document age"""
        if not last_modified:
            return 0.5  # Neutral if no date
        
        try:
            # Handle both string and datetime
            if isinstance(last_modified, str):
                last_modified = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
            
            age_hours = (datetime.now(datetime.UTC) - last_modified).total_seconds() / 3600
            # Score decays over time: 1.0 (new) to 0.0 (very old)
            return max(0, 1.0 - (age_hours / (24 * 30)))  # 30-day half-life
        except Exception as e:
            logger.warning(f"Error computing freshness: {e}")
            return 0.5
    
    def _engagement_score(self, clicks: int, shares: int) -> float:
        """Compute engagement score from user interactions"""
        # Normalize engagement signals
        click_score = min(1.0, clicks / 100)
        share_score = min(1.0, shares / 50)
        
        return 0.6 * click_score + 0.4 * share_score

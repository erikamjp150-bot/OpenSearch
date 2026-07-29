import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

class SearchRankingModel(nn.Module):
    """Re-ranking model using BERT-based cross-encoder for relevance scoring"""
    
    def __init__(self, model_name="distilbert-base-uncased"):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        self.classifier = nn.Linear(768, 1)  # Relevance score (0-1)
        
    def forward(self, query_tokens, doc_tokens):
        # Concatenate query and document for cross-encoding
        combined = torch.cat([query_tokens, doc_tokens], dim=1)
        outputs = self.encoder(combined)
        pooled = outputs.pooler_output
        score = torch.sigmoid(self.classifier(pooled))
        return score

class RankingService:
    """Feature-based ranking with ML model"""
    
    def __init__(self):
        self.model = SearchRankingModel()
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        
    def rank(self, query: str, candidate_docs: list) -> list:
        """Re-rank candidate documents based on relevance"""
        scored_docs = []
        for doc in candidate_docs:
            # Combine multiple ranking features
            bert_score = self._bert_relevance(query, doc['content'])
            engagement_score = self._engagement_score(doc.get('clicks', 0), doc.get('share_count', 0))
            freshness_score = self._freshness_score(doc.get('publish_date'))
            
            # Final score: weighted combination
            total_score = 0.5 * bert_score + 0.3 * engagement_score + 0.2 * freshness_score
            scored_docs.append({**doc, 'score': total_score})
        
        # Sort by score descending
        return sorted(scored_docs, key=lambda x: x['score'], reverse=True)
    
    def _bert_relevance(self, query, content):
        # Cross-encoder relevance (simplified)
        inputs = self.tokenizer(query, content, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            score = self.model(inputs['input_ids'], inputs['attention_mask'])
        return score.item()

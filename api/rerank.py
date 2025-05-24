from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class CrossEncoderReranker:
    def __init__(self, model_name='cross-encoder/ms-marco-MiniLM-L-6-v2', device=None):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(self.device)

    def rerank(self, query, docs, top_k=3):
        pairs = [(query, doc) for doc in docs]
        inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt').to(self.device)
        with torch.no_grad():
            scores = self.model(**inputs).logits.squeeze(-1)
        sorted_indices = torch.argsort(scores, descending=True)
        reranked = [docs[i] for i in sorted_indices[:top_k]]
        return reranked

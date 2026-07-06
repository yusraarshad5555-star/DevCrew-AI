import math
import re
from typing import List, Dict, Tuple, Any

# A small set of standard English stopwords to improve matching relevance
STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could',
    'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from', 'further',
    'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here', 'heres',
    'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in', 'into', 'is',
    'isnt', 'it', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of',
    'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same',
    'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats',
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd', 'theyll',
    'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasnt',
    'we', 'wed', 'well', 'were', 'weve', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which',
    'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll',
    'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves'
}

def tokenize(text: str) -> List[str]:
    """Tokenize a string: lowercase, remove punctuation, split by word and filter stopwords."""
    text = text.lower()
    # Replace non-alphanumeric chars with space
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

class PurePythonTFIDF:
    def __init__(self, corpus: List[str]):
        self.corpus = corpus
        self.doc_count = len(corpus)
        self.tokenized_corpus = [tokenize(doc) for doc in corpus]
        
        # Calculate Term Document Frequency (how many documents contain a term)
        self.doc_freq: Dict[str, int] = {}
        for doc_tokens in self.tokenized_corpus:
            unique_tokens = set(doc_tokens)
            for token in unique_tokens:
                self.doc_freq[token] = self.doc_freq.get(token, 0) + 1
                
        # Calculate IDF for each term
        self.idf: Dict[str, float] = {}
        for term, df in self.doc_freq.items():
            # Standard IDF formula with smoothing to avoid division by zero
            self.idf[term] = math.log((1 + self.doc_count) / (1 + df)) + 1

    def _get_vector(self, tokens: List[str]) -> Dict[str, float]:
        """Convert a list of tokens to a TF-IDF weight vector (stored as sparse dict)."""
        tf: Dict[str, int] = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
            
        vector: Dict[str, float] = {}
        doc_len = len(tokens)
        if doc_len == 0:
            return vector
            
        for term, freq in tf.items():
            if term in self.idf:
                # Term Frequency (normalized by doc length) * Inverse Document Frequency
                vector[term] = (freq / doc_len) * self.idf[term]
        return vector

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two sparse TF-IDF vectors."""
        if not vec1 or not vec2:
            return 0.0
            
        # Dot product
        dot_product = 0.0
        for term, weight in vec1.items():
            if term in vec2:
                dot_product += weight * vec2[term]
                
        # Norms
        norm1 = math.sqrt(sum(w ** 2 for w in vec1.values()))
        norm2 = math.sqrt(sum(w ** 2 for w in vec2.values()))
        
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
            
        return dot_product / (norm1 * norm2)

    def query(self, query_text: str, top_k: int = 3) -> List[Tuple[int, float]]:
        """Query the corpus, returning list of tuples (doc_index, similarity_score)."""
        if self.doc_count == 0:
            return []
            
        query_tokens = tokenize(query_text)
        if not query_tokens:
            # Fallback: if query has no tokens after filter, return empty or index match
            return []
            
        query_vec = self._get_vector(query_tokens)
        
        scores: List[Tuple[int, float]] = []
        for idx, doc_tokens in enumerate(self.tokenized_corpus):
            doc_vec = self._get_vector(doc_tokens)
            score = self._cosine_similarity(query_vec, doc_vec)
            scores.append((idx, score))
            
        # Sort by similarity score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

def search_local_memories(query_text: str, memories: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Search list of dicts (each having a 'text' key) and return the top_k most similar ones.
    Enriches each matched dict with a 'score' key.
    """
    if not memories:
        return []
        
    corpus = [m['text'] for m in memories]
    tfidf = PurePythonTFIDF(corpus)
    matches = tfidf.query(query_text, top_k=top_k)
    
    results = []
    for idx, score in matches:
        # Include matches with even a small similarity score
        if score > 0.01:
            matched_memory = dict(memories[idx])
            matched_memory['score'] = score
            results.append(matched_memory)
            
    return results

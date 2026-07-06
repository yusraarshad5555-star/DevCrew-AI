import unittest
from devcrew_ai.memory.local_similarity import PurePythonTFIDF, search_local_memories

class TestLocalMemorySimilarity(unittest.TestCase):
    def setUp(self):
        self.corpus = [
            "DevCrew AI supports pluggable local LLM models using Ollama.",
            "SQLite database is used to store agent task logs and project state.",
            "The architecture design separates the backend API from the Streamlit frontend UI.",
            "Developers write SOLID code with type hints and robust exception handling."
        ]
        self.memories = [
            {"id": idx + 1, "text": text, "category": "info"} for idx, text in enumerate(self.corpus)
        ]

    def test_tokenization_and_tfidf(self):
        tfidf = PurePythonTFIDF(self.corpus)
        # Check doc count
        self.assertEqual(tfidf.doc_count, 4)
        # Verify terms exist in idf
        self.assertIn("ollama", tfidf.idf)
        self.assertIn("sqlite", tfidf.idf)
        self.assertIn("solid", tfidf.idf)
        # Stopwords should not be indexed
        self.assertNotIn("is", tfidf.idf)
        self.assertNotIn("the", tfidf.idf)

    def test_query_matching(self):
        tfidf = PurePythonTFIDF(self.corpus)
        # Query for Ollama-related terms
        results = tfidf.query("pluggable models ollama", top_k=2)
        # Should return index 0 as highest score
        self.assertEqual(results[0][0], 0)
        self.assertGreater(results[0][1], 0.0)

    def test_search_local_memories_helper(self):
        matches = search_local_memories("sqlite logs", self.memories, top_k=2)
        self.assertGreater(len(matches), 0)
        # First match should be the SQLite memory (index 1)
        self.assertEqual(matches[0]["id"], 2)
        self.assertIn("score", matches[0])

if __name__ == "__main__":
    unittest.main()

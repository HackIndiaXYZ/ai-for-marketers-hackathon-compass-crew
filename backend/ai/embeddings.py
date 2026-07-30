"""
Embedding Utility
-----------------

Responsibilities:

- Convert customer reviews into semantic vectors
- Detect similar reviews
- Support duplicate detection
- Enable future clustering and RAG retrieval

Model:
Sentence Transformers
(all-MiniLM-L6-v2)

This runs locally and does not require API calls.
"""

from __future__ import annotations

from typing import List, Dict, Any

import numpy as np

from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    """
    Manages semantic embeddings for customer intelligence.

    Workflow:

    Customer Reviews

          ↓

    Embedding Model

          ↓

    Vector Representation

          ↓

    Similarity Search / Clustering
    """

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )


    # ======================================================
    # Create Single Embedding
    # ======================================================

    def create_embedding(
        self,
        text: str
    ) -> List[float]:
        """
        Convert one review into embedding vector.
        """

        vector = self.model.encode(
            text
        )

        return vector.tolist()


    # ======================================================
    # Create Multiple Embeddings
    # ======================================================

    def create_embeddings(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Convert multiple reviews into vectors.
        """

        vectors = self.model.encode(
            texts,
            show_progress_bar=False
        )

        return vectors.tolist()


    # ======================================================
    # Cosine Similarity
    # ======================================================

    def similarity(
        self,
        vector1: List[float],
        vector2: List[float]
    ) -> float:
        """
        Calculate semantic similarity.

        Range:

        0   = unrelated

        1   = identical meaning
        """

        vector1 = np.array(vector1)

        vector2 = np.array(vector2)


        score = np.dot(
            vector1,
            vector2
        ) / (
            np.linalg.norm(vector1)
            *
            np.linalg.norm(vector2)
        )


        return float(score)


    # ======================================================
    # Duplicate / Similar Review Detection
    # ======================================================

    def find_similar_reviews(
        self,
        reviews: List[str],
        threshold: float = 0.85
    ) -> List[Dict[str, Any]]:
        """
        Find semantically similar reviews.

        Example:

        "Nobody answers calls"

        "Phone support is useless"

        similarity = 0.91

        """

        if len(reviews) < 2:
            return []


        embeddings = self.create_embeddings(
            reviews
        )


        similar_reviews = []


        for i in range(len(reviews)):

            for j in range(
                i + 1,
                len(reviews)
            ):

                score = self.similarity(
                    embeddings[i],
                    embeddings[j]
                )


                if score >= threshold:

                    similar_reviews.append(

                        {
                            "review_1": reviews[i],

                            "review_2": reviews[j],

                            "similarity": round(
                                score,
                                3
                            )
                        }

                    )


        return similar_reviews


    # ======================================================
    # Search Most Similar Reviews
    # ======================================================

    def semantic_search(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve most relevant customer reviews.

        Future RAG support.

        Example:

        Query:

        "Why are customers leaving?"

        Returns:

        Reviews about:
        - delays
        - pricing
        - support
        """

        query_vector = self.create_embedding(
            query
        )


        document_vectors = self.create_embeddings(
            documents
        )


        results = []


        for index, vector in enumerate(document_vectors):

            score = self.similarity(
                query_vector,
                vector
            )


            results.append(

                {
                    "review": documents[index],

                    "similarity": round(
                        score,
                        3
                    )
                }

            )


        results.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )


        return results[:top_k]


    # ======================================================
    # Prepare Data For Clustering
    # ======================================================

    def prepare_clustering_vectors(
        self,
        reviews: List[str]
    ):
        """
        Returns numpy vectors.

        Compatible with:

        - KMeans
        - DBSCAN
        - FAISS
        """

        return np.array(

            self.create_embeddings(
                reviews
            )

        )



# Singleton Instance

embedding_manager = EmbeddingManager()
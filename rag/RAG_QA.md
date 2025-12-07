# RAG Interview Q&A (Comprehensive Guide)

This document contains a complete collection of RAG interview questions, ranging from fundamental concepts to expert-level system design.

---

## 🏗️ 1. Architecture

### Q: Explain RAG in your own words.
**A:** RAG (Retrieval-Augmented Generation) is a technique that gives an LLM access to external private data. Instead of relying only on what it learned during training, we first *retrieve* relevant documents from a database and then ask the LLM to generate an answer based *only* on those documents. It's like allowing a student to take an open-book exam instead of a closed-book one.

### Q: What problem does RAG solve?
**A:** It solves three main problems:
1.  **Hallucinations:** Prevents the model from making up facts by grounding it in real data.
2.  **Stale Knowledge:** LLMs are trained on data from the past. RAG allows access to live, up-to-the-minute data.
3.  **Private Data:** Enables LLMs to answer questions about proprietary company documents (PDFs, emails) that were not in its training set.

### Q: Difference between RAG and fine-tuning?
**A:**
*   **RAG:** Adds **Knowledge**. Best for factual recall, dynamic data, and avoiding hallucinations. It's cheaper and faster to update (just add a file to the DB).
*   **Fine-tuning:** Adjusts **Behavior**. Best for changing the *style* (e.g., talk like a pirate), learning a new language, or strictly following a complex format. It does *not* reliably teach new knowledge.

### Q: Explain the RAG pipeline.
**A:**
1.  **Ingestion:** Load documents -> Split into chunks -> Embed chunks -> Store in Vector DB.
2.  **Retrieval:** Embed User Query -> Find Top-K similar chunks in DB.
3.  **Generation:** Combine Query + Retrieved Chunks into a Prompt -> Feed to LLM -> Get Answer.

### Q: Why do we need chunking?
**A:** LLMs have a context window limit (e.g., 8k tokens). You cannot feed an entire 100-page book into the prompt. Chunking breaks the text into small, relevant pieces so we retrieve only the specific paragraphs needed to answer the question, reducing noise and cost.

### Q: What metadata is useful?
**A:**
*   `source`: Filename or URL (for citations).
*   `page_number`: To link the user back to the original spot.
*   `date`: To filter for "recent" news.
*   `category`/`department`: To implement security (RBAC) or narrow the search scope.

---

## 🧮 2. Embeddings & Indexing

### Q: What is an embedding?
**A:** An embedding is a list of floating-point numbers (a vector) that represents the **semantic meaning** of text. In this mathematical space, words with similar meanings (like "King" and "Queen") are positioned close to each other.

### Q: How does cosine similarity work?
**A:** It measures the angle between two vectors.
*   If the angle is 0 degrees (Cosine = 1), the vectors are identical (same meaning).
*   If the angle is 90 degrees (Cosine = 0), they are unrelated.
*   It is the standard metric for finding "nearest neighbors" in semantic search because it focuses on orientation (meaning) rather than magnitude (length).

### Q: What is the impact of embedding dimensionality?
**A:** Dimensionality is the length of the vector (e.g., 1536 for OpenAI, 384 for MiniLM).
*   **Higher dims:** Capture more nuance and complex relationships but require more storage and slower search.
*   **Lower dims:** Faster and cheaper but may lose subtle semantic distinctions.

### Q: What is vector normalization?
**A:** Scaling a vector so its length (magnitude) is 1. When vectors are normalized, "Cosine Similarity" becomes mathematically equivalent to the "Dot Product". This allows for faster calculations in the database.

### Q: Why use semantic chunking?
**A:** Standard chunking cuts text blindly (e.g., every 500 chars), potentially breaking a sentence in half. Semantic chunking calculates the similarity between sentences and only breaks the chunk when the topic changes. This ensures every chunk is a complete, coherent thought.

### Q: Why use overlapping chunks?
**A:** To preserve context at the boundaries. If a relevant keyword is at the very end of Chunk A and the start of Chunk B, splitting without overlap might separate the keyword from its context. Overlap (e.g., 10%) ensures the edges are covered in at least one chunk.

---

## 🔎 3. Retrieval

### Q: What is dense retrieval?
**A:** Search using Embeddings (vectors). It matches **concepts**. It can find documents that don't have the exact keywords but mean the same thing (e.g., Query: "fix engine", Doc: "motor repair").

### Q: What is sparse retrieval (BM25)?
**A:** Search using Keywords (like TF-IDF). It matches **exact words**. It's crucial for finding specific IDs, names, or rare acronyms that embeddings might miss.

### Q: What is hybrid retrieval?
**A:** Combining Dense (Vector) and Sparse (Keyword) search. You take the results from both, weight them (e.g., `Score = 0.7*Vector + 0.3*BM25`), and merge them. It gives the "best of both worlds".

### Q: What is re-ranking?
**A:** A two-step process:
1.  **Retrieve:** Get top 50 results quickly using standard vector search (Bi-Encoder).
2.  **Re-rank:** Pass those 50 to a slower, high-precision model (Cross-Encoder) that reads the query and document together to score their relevance accurately. Pick the top 5.
*   *Why?* It drastically improves accuracy.

### Q: Explain Recall@k vs Precision@k.
**A:**
*   **Recall@k:** "Did the correct answer appear anywhere in the top k results?" (Crucial for RAG - if it's not retrieved, we fail).
*   **Precision@k:** "How many of the top k results were actually relevant?" (Less critical, but helps reduce noise).

### Q: What is nDCG?
**A:** Normalized Discounted Cumulative Gain. It measures the **quality of ranking**. It doesn't just ask "Did we find the doc?", it asks "Is the best doc at position #1?". It penalizes the system if the best document is at position #10 instead of #1.

---

## 💬 4. Prompting

### Q: Why use delimiters?
**A:** Using XML tags like `<context>` or `###` clearly separates the instruction ("Summarize this") from the data ("The text to summarize"). It prevents the LLM from getting confused about what constitutes the input data.

### Q: What is grounding?
**A:** The process of ensuring the LLM's answer is based *factually* on the provided source material. In RAG, we "ground" the model by forcing it to answer using provided context.

### Q: How to reduce hallucinations in prompts?
**A:**
1.  **Instruction:** "Answer using ONLY the provided context."
2.  **Negative Constraint:** "If the answer is not in the context, say 'I don't know'."
3.  **Citations:** "Cite the source ID for every sentence."

### Q: What is context overflow?
**A:** When the retrieved documents + user query exceed the LLM's maximum token limit (e.g., 4096 tokens). The prompt gets truncated, and the LLM loses instructions or data.

---

## 🧠 5. Generation

### Q: Why use temperature=0 for RAG?
**A:** Temperature controls randomness. High temperature (1.0) is creative; Low temperature (0) is deterministic and factual. In RAG, we want facts, not creativity, so we strictly use 0.

### Q: How do larger models improve accuracy?
**A:** Larger models (GPT-4) have better **reasoning** capabilities and **instruction following**. They are better at ignoring irrelevant noise in the retrieved chunks and extracting the correct answer, whereas smaller models might get distracted by the noise.

---

## 🎯 6. Accuracy Improvements

### Q: List ways to improve RAG accuracy.
**A:**
1.  **Better Data:** Clean the text, remove html tags, fix formatting.
2.  **Hybrid Search:** Combine Keywords + Vectors.
3.  **Re-ranking:** Use a Cross-Encoder.
4.  **Metadata Filtering:** Narrow search scope (e.g., year=2024).
5.  **Query Transformation:** Rewrite vague user queries into better search terms.

### Q: Why does re-ranking help?
**A:** Vector search is fast but "fuzzy". It often returns documents that are *kind of* related but not exact. Re-ranking actually "reads" the document against the query to verify relevance, filtering out the "fuzzy" matches that confuse the LLM.

### Q: Why does hybrid retrieval help?
**A:** Vectors are bad at exact matches (like serial numbers "XJ-900"). Keywords are bad at concepts ("device not working"). Hybrid covers both weaknesses.

### Q: What is contextual compression?
**A:** Instead of returning 5 full pages of text, use a small LLM to extract only the 3 sentences relevant to the query from those pages *before* sending them to the main LLM. This saves tokens and reduces noise.

---

## 🚀 7. Advanced RAG

### Q: What is Multi-Vector RAG?
**A:** Decoupling the search vector from the content.
*   **Method:** You index a *Summary* of the document (better for searching high-level concepts), but when retrieved, you return the *Full Document* to the LLM.

### Q: What is GraphRAG?
**A:** Combining Knowledge Graphs with Vector/Text search.
*   **Use Case:** Multi-hop reasoning. "Concept A is related to B" might be in Doc 1, and "B is related to C" in Doc 2. GraphRAG traverses these links to find the answer, which vector search assumes are unrelated.

### Q: What is Fusion RAG?
**A:** Generating multiple search queries from one user prompt (e.g., "Code for python", "Python programming examples"), running them all, and fusing the results using an algorithm like Reciprocal Rank Fusion (RRF) to find the most consistently high-ranked documents.

### Q: What is Retrieval Fine-Tuning?
**A:** Fine-tuning the *Embedding Model* itself on your specific domain data so it understands that "Apple" means the tech company, not the fruit, within your dataset.

### Q: What is query rewriting in RAG?
**A:** Users ask vague questions ("How much is it?"). We use an LLM to rewrite this into a standalone query ("What is the price of the Enterprise Plan?") before searching definitions.

---

## 📊 8. Evaluation

### Q: How do you evaluate retrieval?
**A:** Using "Golden Datasets" (Question-Answer pairs). We check metrics like Recall@5 (did the right doc appear in top 5?).

### Q: What is a grounding score?
**A:** A metric (often 0-1) calculated by an LLM-Judge that measures "How much of the answer is supported by the retrieved chunks?". A score of 0 means pure hallucination.

### Q: What is LLM-as-a-judge evaluation?
**A:** Using a strong model (GPT-4) to read the Question, Context, and Answer, and grade the quality. It scales better than human review.

### Q: What is Faithfulness?
**A:** The metric measuring if the answer contradicts the context.

### Q: What is Completeness?
**A:** The metric measuring if the answer fully addresses the user's question.

---

## 🔧 9. Troubleshooting

### Q: Why does retrieval return irrelevant chunks?
**A:**
1.  **Poor embeddings:** Domain mismatch.
2.  **Bad chunking:** Chunks are too small (no context) or too large (too much noise).
3.  **Vague query:** User asked brief question; needs query expansion.

### Q: What to do if model ignores context?
**A:**
1.  **Prompt Engineering:** Emphasize the instruction. Put instructions *after* the context (Recency bias).
2.  **Reduce Noise:** Give fewer, more relevant chunks.

### Q: What to do if model hallucinates despite RAG?
**A:** Add a "Verification" step. Ask the LLM to output Citations. If it cannot cite a source, suppress the answer.

### Q: Why is chunk size important?
**A:**
*   **Too Small:** Loses meaning (e.g., "It was bad." - What was bad?).
*   **Too Large:** Dilutes the embedding (the distinct concept gets lost in a sea of words).

### Q: Why might embeddings be poor quality?
**A:** General purpose models (OpenAI) might not understand specific industry jargon (e.g., medical drug names).

---

## 💻 10. Implementation

### Q: Explain FAISS.
**A:** Facebook AI Similarity Search. A library for efficient similarity search of dense vectors. It implements algorithms like HNSW and IVF to make searching billions of vectors fast.

### Q: Explain Pinecone/Weaviate/Chroma.
**A:**
*   **Pinecone:** Managed, closed-source SaaS. Easy to scale.
*   **Weaviate:** Open-source, supports hybrid search and objects/classes.
*   **Chroma:** Open-source, runs locally (in-memory or file), great for prototyping.

### Q: What is a vector index?
**A:** A data structure that allows fast lookup. Instead of comparing the query to every single document (O(N)), it uses graphs or clusters (O(log N)) to find neighbors quickly.

### Q: What is an ANN search algorithm?
**A:** Approximate Nearest Neighbor. It trades a tiny bit of accuracy (finding the *absolute* closest match) for massive speed (finding *very close* matches). HNSW is the most popular ANN algorithm.

---

## 🌐 11. Practical Questions

### Q: How big can a RAG dataset be?
**A:** Theoretically limits are only storage/cost. FAISS handles billions of vectors. However, as the distinct concepts grow, "collision" (irrelevant things looking similar) increases, requiring better re-ranking.

### Q: How do you scale RAG?
**A:**
1.  **Database:** Use a distributed vector DB (Milvus, Pinecone).
2.  **Read Replicas:** Scale retrieval throughput.
3.  **Caching:** Cache frequent queries (Semantic Cache).

### Q: How do you speed up retrieval?
**A:**
1.  **Approximation:** Lower the `ef_search` parameter in HNSW.
2.  **Quantization:** Compress vectors (e.g., int8).
3.  **Metadata filtering:** Filter *before* searching to reduce the search space.

### Q: How often update embeddings?
**A:** Only when the underlying content changes. Embeddings are static. If your embedding *model* changes, you must re-index everything.

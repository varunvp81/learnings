# Retrieval-Augmented Generation (RAG) – Expert Q&A (100+ Questions)

This file contains **100+ expert-level RAG questions and answers**, covering theory, architecture, implementation, evaluation, troubleshooting, and advanced concepts. Ready for study, interviews, and GitHub reference.

---

## **Architecture & Basics**

**1. Explain RAG in your own words.**  
*Answer:* RAG combines a retriever and a generator to produce grounded, factual answers using external documents.

**2. What problem does RAG solve?**  
*Answer:* Reduces hallucinations, stale knowledge, and domain-specific gaps in LLMs.

**3. Difference between RAG and fine-tuning?**  
*Answer:* RAG retrieves information at inference time, whereas fine-tuning modifies model weights.

**4. Explain the RAG pipeline.**  
*Answer:* Query → Embedding → Retrieve top-k chunks → Build prompt → LLM → Answer.

**5. Why do we need chunking?**  
*Answer:* Smaller chunks improve retrieval relevance and reduce token overflow.

**6. What metadata is useful?**  
*Answer:* Document name, section ID, tags, timestamps, source.

---

## **Embeddings & Indexing**

**7. What is an embedding?**  
*Answer:* A numerical vector representing the semantic meaning of text.

**8. How does cosine similarity work?**  
*Answer:* Measures similarity between two vectors by computing the cosine of the angle between them.

**9. What is the impact of embedding dimensionality?**  
*Answer:* Higher dimensions capture more semantic nuance but increase computation and storage.

**10. What is vector normalization?**  
*Answer:* Scaling vectors to unit length to ensure consistent similarity comparisons.

**11. Why use semantic chunking?**  
*Answer:* Preserves contextually meaningful sections for accurate retrieval.

**12. Why use overlapping chunks?**  
*Answer:* Prevents splitting important context across chunks.

---

## **Retrieval**

**13. What is dense retrieval?**  
*Answer:* Uses vector embeddings and similarity search to retrieve documents.

**14. What is sparse retrieval (BM25)?**  
*Answer:* Uses term frequency and inverse document frequency for keyword-based search.

**15. What is hybrid retrieval?**  
*Answer:* Combines dense and sparse retrieval for better accuracy.

**16. What is re-ranking?**  
*Answer:* Using a stronger model to reorder retrieved documents to improve relevance.

**17. Explain Recall@k vs Precision@k.**  
*Answer:* Recall@k measures coverage of relevant documents in top-k; Precision@k measures proportion of relevant docs in top-k.

**18. What is nDCG?**  
*Answer:* Normalized Discounted Cumulative Gain, measures ranking quality considering position of relevant items.

---

## **Prompting**

**19. Why use delimiters?**  
*Answer:* Helps LLM distinguish between context and question.

**20. What is grounding?**  
*Answer:* Ensuring the generated answer is supported by retrieved documents.

**21. How to reduce hallucinations in prompts?**  
*Answer:* Explicitly instruct the model to use only provided context.

**22. What is context overflow?**  
*Answer:* When too many tokens exceed the LLM’s maximum context length.

---

## **Generation**

**23. Why use temperature=0 for RAG?**  
*Answer:* Reduces randomness, producing more factual outputs.

**24. How do larger models improve accuracy?**  
*Answer:* Better comprehension and reasoning over retrieved context.

---

## **Accuracy Improvements**

**25. List ways to improve RAG accuracy.**  
*Answer:* Better embeddings, semantic chunking, overlapping chunks, hybrid retrieval, re-ranking, prompt engineering.

**26. Why does re-ranking help?**  
*Answer:* Ensures the most relevant documents are used in generation.

**27. Why does hybrid retrieval help?**  
*Answer:* Combines semantic understanding and keyword precision.

**28. What is contextual compression?**  
*Answer:* Summarizing retrieved context before feeding to LLM to reduce token load.

---

## **Advanced RAG**

**29. What is Multi-Vector RAG?**  
*Answer:* Multiple embeddings per chunk (title, summary, keywords) to improve recall.

**30. What is GraphRAG?**  
*Answer:* Combines vector retrieval with knowledge graph traversal for entity-centric queries.

**31. What is Fusion RAG?**  
*Answer:* Retrieves from multiple sources/models and fuses results for improved coverage.

**32. What is Retrieval Fine-Tuning?**  
*Answer:* Fine-tuning retriever or LLM on retrieval-augmented data for higher accuracy.

**33. What is query rewriting in RAG?**  
*Answer:* Reformulating queries to improve retrieval results.

---

## **Evaluation**

**34. How do you evaluate retrieval?**  
*Answer:* Recall@k, Precision@k, nDCG, Mean Reciprocal Rank.

**35. What is grounding score?**  
*Answer:* Percentage of generated content supported by retrieved documents.

**36. What is LLM-as-a-judge evaluation?**  
*Answer:* Using an LLM to score factuality/coherence of generated answers.

**37. What is Faithfulness?**  
*Answer:* Whether the generated content matches source context accurately.

**38. What is Completeness?**  
*Answer:* Extent to which the generated answer covers the query fully.

---

## **Troubleshooting**

**39. Why does retrieval return irrelevant chunks?**  
*Answer:* Poor embeddings, wrong chunking, or vector DB misconfiguration.

**40. What to do if model ignores context?**  
*Answer:* Use explicit delimiters and grounding instructions.

**41. What to do if model hallucinates despite RAG?**  
*Answer:* Filter/re-rank retrieved chunks and enforce context-only instructions.

**42. Why is chunk size important?**  
*Answer:* Too small loses context, too large reduces retrieval precision.

**43. Why might embeddings be poor quality?**  
*Answer:* Wrong embedding model, out-of-domain text, or inconsistent preprocessing.

---

## **Implementation**

**44. Explain FAISS.**  
*Answer:* Facebook AI Similarity Search, a library for fast similarity search of vectors.

**45. Explain Pinecone.**  
*Answer:* Cloud-native vector DB for scalable vector retrieval.

**46. Explain Weaviate.**  
*Answer:* Open-source vector DB with semantic search and GraphQL support.

**47. What is a vector index?**  
*Answer:* Data structure storing embeddings for fast similarity search.

**48. What is an ANN search algorithm?**  
*Answer:* Approximate Nearest Neighbor, reduces computation time for large vector spaces.

---

## **Practical Questions**

**49. How big can a RAG dataset be?**  
*Answer:* Millions of documents; depends on vector DB and ANN algorithm.

**50. How do you scale RAG?**  
*Answer:* Sharding vector DB, distributed retrieval, caching embeddings, optimizing top-k.

**51. How do you speed up retrieval?**  
*Answer:* ANN search, dimensionality reduction, indexing optimization.

**52. How often update embeddings?**  
*Answer:* Whenever documents are added/modified, or periodically to maintain relevance.

---

## **Continuation: Advanced Concepts & Implementation**

**53. What is multi-hop retrieval?**  
*Answer:* Chain retrieval across documents for complex questions.

**54. What is GraphRAG?**  
*Answer:* Combines retrieval from a knowledge graph and vector DB.

**55. What is Fusion-in-Decoder (FiD)?**  
*Answer:* Sends each retrieved doc to decoder separately, fuses at generation.

**56. Contextual Compression RAG?**  
*Answer:* Summarize retrieved docs before feeding to LLM.

**57. Retrieval-Augmented Fine-Tuning (RAFT)?**  
*Answer:* Fine-tune model using retrieval-augmented data.

**58. RAG-Sequence vs RAG-Token?**  
*Answer:* Sequence: generate per doc; Token: generate using all docs simultaneously.

**59. Choosing top-k for retrieval?**  
*Answer:* Tune based on recall and LLM input limits.

**60. Handling long documents?**  
*Answer:* Chunk and overlap, embed each chunk.

**61. Vector normalization importance?**  
*Answer:* Ensures cosine similarity is comparable.

**62. Handling updates in vector DB?**  
*Answer:* Incremental embedding or periodic refresh.

**63. Scaling to millions of docs?**  
*Answer:* ANN algorithms, sharding, distributed DBs.

**64. What is hybrid search?**  
*Answer:* Dense + sparse retrieval combination.

**65. Prevent token overflow?**  
*Answer:* Limit chunks, compress context, summarize docs.

**66. Debugging a RAG pipeline?**  
*Answer:* Check embeddings, similarity scores, top-k results, prompts, LLM outputs.

**67. Re-ranking benefits?**  
*Answer:* Increases probability top documents are used for generation.

**68. Measure factuality?**  
*Answer:* Compare with reference, check context support.

**69. Grounding accuracy?**  
*Answer:* % of generated content supported by retrieved docs.

**70. Automatic metrics?**  
*Answer:* BLEU, ROUGE, F1, EM, FactCC, LLM-based fact-checking.

**71. Human evaluation metrics?**  
*Answer:* Coherence, relevance, factuality, completeness, readability.

**72. Evaluate retrieval independently?**  
*Answer:* Recall@k, Precision@k, nDCG, MRR.

**73. Trade-off retrieval size vs generation quality?**  
*Answer:* More context improves completeness but risks token overflow.

**74. Model ignores retrieved context?**  
*Answer:* Use explicit delimiters and grounding instructions.

**75. Model hallucinates despite RAG?**  
*Answer:* Filter/re-rank retrieved chunks, enforce context-only.

**76. Poor embeddings relevance?**  
*Answer:* Wrong embedding model, chunking, vector DB misconfig.

**77. Reduce retrieval latency?**  
*Answer:* ANN, caching, lower-dim embeddings.

**78. Multi-language retrieval?**  
*Answer:* Multilingual embeddings, normalize encoding.

**79. RAG in QA systems?**  
*Answer:* Retrieve supporting docs, LLM answers using them.

**80. RAG in summarization?**  
*Answer:* Retrieve relevant context to summarize accurately.

**81. RAG in chatbots?**  
*Answer:* Maintain history + retrieve knowledge for grounded answers.

**82. RAG in coding assistants?**  
*Answer:* Retrieve code/docs to generate accurate completions.

**83. Popular embedding models?**  
*Answer:* OpenAI text-embedding-3-large, BGE-M3, SentenceTransformers, Cohere embed-v3.

**84. Popular vector databases?**  
*Answer:* FAISS, Milvus, Pinecone, Chroma, Weaviate, Vespa.

**85. What is ANN search?**  
*Answer:* Approximate Nearest Neighbor, faster vector search with minor accuracy trade-off.

**86. Updating RAG with changed documents?**  
*Answer:* Re-embed and update vector DB.

**87. Multiple data sources in RAG?**  
*Answer:* Fusion-RAG: retrieve from all sources, re-rank.

**88. Ensure RAG answers are auditable?**  
*Answer:* Include citations to retrieved documents.

**89. Test RAG pipelines automatically?**  
*Answer:* QA test sets, factuality metrics, retrieval recall tests, LLM evaluation.

**90. Managing token limits?**  
*Answer:* Compress context, summarize chunks, reduce top-k, use larger-context LLMs.

**91. Query expansion?**  
*Answer:* Reformulate queries with synonyms or related terms.

**92. Pseudo-relevance feedback?**  
*Answer:* Improve query embedding using initially retrieved results.

**93. Multi-turn RAG?**  
*Answer:* Maintain chat history, retrieve per turn, summarize previous turns.

**94. Handling confidential data?**  
*Answer:* Secure DB, encrypt embeddings, isolate private indices.

**95. Reduce hallucinations?**  
*Answer:* Ground generation, enforce prompt instructions, cite sources.

**96. Evaluate long-form answers?**  
*Answer:* Coverage, factuality, coherence; human/LLM-as-judge evaluation.

**97. RAG vs knowledge-enhanced LLMs?**  
*Answer:* Knowledge-enhanced fine-tunes model; RAG retrieves dynamically.

**98. Choosing embedding dimensionality?**  
*Answer:* Higher = more detail; typical 768–1536.

**99. Late fusion in RAG?**  
*Answer:* Combine multiple generation outputs after generation.

**100. Monitor RAG in production?**  
*Answer:* Track retrieval recall, grounding accuracy, latency, hallucinations, user feedback, token usage.

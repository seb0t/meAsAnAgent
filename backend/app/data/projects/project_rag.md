# Title: RAG
## Role: AI Engineer
## Period: 2024-03
## Technologies:
- **Python** (LangChain, LlamaIndex)
- **Vector Databases** (Chroma, Weaviate, Pinecone)
- **LLMs** (OpenAI, Hugging Face Transformers)
- **Embeddings** (Sentence Transformers, OpenAI Embeddings)
## Summary:
Questo progetto sviluppa una pipeline avanzata di Retrieval Augmented Generation (RAG) per migliorare la qualità delle risposte AI attraverso retrieval contestuale da database vettoriali. Utilizzando **LangChain** o **LlamaIndex** per orchestrazione, integra modelli di embedding (**Sentence Transformers**) per convertire documenti in vettori, stored in database come **Chroma** o **Weaviate** per similarità efficiente. La pipeline include preprocessing documenti, chunking intelligente, retrieval top-k rilevanti, e generazione finale con LLM (**OpenAI GPT** o modelli locali). Supporta fonti multiple (PDF, web, database), con evaluation metrics per accuracy e rilevanza. È un foundation per applicazioni AI conversazionali, dimostrando come RAG riduce hallucination e aumenta factualità.
## Achievements:
- Implementazione pipeline RAG con accuracy >90% su benchmark
- Supporto per 5+ fonti dati eterogenee
- Ottimizzazione latency per real-time responses
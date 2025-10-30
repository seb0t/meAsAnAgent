# Title: meAsAnAgent
## Role: Full-Stack Developer & AI Engineer
## Period: 2024-10
## Technologies:
- **Python** (FastAPI, LangChain, ChromaDB, Neo4j)
- **JavaScript/TypeScript** (Next.js, React)
- **AI/ML** (OpenAI API, Vector Databases)
- **Deployment** (Docker, Uvicorn)
## Summary:
Questo progetto implementa un agente AI virtuale progettato per rispondere a domande di recruiter basandosi su una knowledge base personale strutturata. Utilizza una pipeline RAG (Retrieval Augmented Generation) che combina retrieval da un database a grafo (**Neo4j**) per relazioni semantiche e da un database vettoriale (**ChromaDB**) per similarità semantica, generando risposte accurate e contestualizzate tramite modelli LLM (**OpenAI**). L'architettura include un backend in **Python** con **FastAPI** per API RESTful, un frontend in **React/Next.js** per un'interfaccia chat interattiva, e supporto per deployment containerizzato con **Docker**. Il sistema è modulare, con servizi separati per graph retriever, vector retriever e pipeline RAG, permettendo espansione futura e integrazione con altri LLM locali.
## Achievements:
- Implementazione completa di knowledge base ibrida (graph + vector) per retrieval efficiente
- Pipeline RAG con citazione fonti per risposte trasparenti e verificabili
- Interfaccia web responsive con gestione stato real-time per conversazioni fluide
- Architettura scalabile con configurazione via **.env** e logging per monitoraggio
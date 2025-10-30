# Copilot Project Instructions — AI Personal Career Agent

## Missione
Sviluppare un agente AI che risponda automaticamente a recruiter e tecnici fornendo informazioni accurate sulla carriera, esperienza e competenze del candidato (Sebastiano). Il progetto deve dimostrare competenze avanzate in: LLM, RAG, Vector DB, Graph DB, agentica, deployment cloud.

## Obiettivi principali

1. Knowledge Base personale del candidato
   - Progetti, competenze, formazione, risultati
   - Stored su: Neo4j (graph DB) + Vector DB (Chroma/Weaviate)

2. RAG Pipeline
   - Interpretazione della query
   - Retrieval dal graph e vector DB
   - Generazione risposta con citazione delle fonti

3. Interfaccia Web
   - Chatbot in React/Next.js
   - Visualizzazione fonti + nodi coinvolti

4. Deployment
   - Docker + servizi cloud
   - Logging domande per miglioramento

## Architettura tecnica

User ─▶ Web Chat UI (React)
        └▶ Backend Python FastAPI
            ├▶ Graph Retriever: Neo4j
            ├▶ Vector Retriever: Chroma/Weaviate
            └▶ LLM (OpenAI/Local)

## Requisiti di coding

- Usare Python 3.10+
- LLM integrato tramite LangChain o LlamaIndex
- Clean architecture & modularità
- Config in .env e variabili ben gestite
- Tutto versionato su GitHub

## Cosa evitare

- Codice monolitico o non commentato
- Salvare dati personali sensibili non utili al portfolio
- Usare database non previsti nello stack

## Roadmap

- v0.1: Versione CLI con RAG base (solo vector DB)
- v0.2: Aggiunta graph DB Neo4j e schema completo
- v0.3: Interfaccia web per interazione
- v1.0: Personalizzazione risposte + tracking domande

## Stile di risposta dell’agente

- Modalità recruiter: chiara, sintetica, orientata ai risultati
- Modalità tecnico: dettagliata, architetture, stack usato
- Citare fonti interne (progetti, esperienze)


# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
What GPA/GRE stats actually get CS MS applicants admitted?

This knowledge is valuable because prospective CS master's applicants need realistic 
benchmarks to decide which programs to apply to, but universities only publish vague 
admission statistics that do not reflect actual admit profiles. The real data — specific 
GPA, GRE scores, and whether someone got in or rejected — only exists in student-generated 
posts on Reddit and Gradcafe, making it impossible to find through any official university 
channel.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit r/gradadmissions | MSCS admit/reject results thread with GPA and GRE stats from 2024 applicants | reddit.com/r/gradadmissions |
| 2 | Reddit r/gradadmissions | Discussion thread on minimum GPA and GRE scores needed for top CS master's programs | reddit.com/r/gradadmissions |
| 3 | Gradcafe — Carnegie Mellon | ~20 crowdsourced CMU MSCS admission results with GPA, GRE, and admit/reject outcomes | thegradcafe.com |
| 4 | Gradcafe — Georgia Tech | ~20 crowdsourced GT MSCS admission results with GPA, GRE, and admit/reject outcomes | thegradcafe.com |
| 5 | Gradcafe — UIUC | ~20 crowdsourced UIUC MCS admission results with GPA, GRE, and admit/reject outcomes | thegradcafe.com |
| 6 | Gradcafe — Stanford | ~20 crowdsourced Stanford MSCS admission results with GPA, GRE, and admit/reject outcomes | thegradcafe.com |
| 7 | Reddit r/OMSCS | Student posts about getting admitted to Georgia Tech OMSCS with low GPA and advice for applicants | reddit.com/r/OMSCS |
| 8 | Reddit r/csMajors | Undergrad experiences applying to CS master's programs with tips and final admission outcomes | reddit.com/r/csMajors |
| 9 | Reddit r/gradadmissions | Thread specifically about CS master's options for applicants with below 3.5 GPA | reddit.com/r/gradadmissions |
| 10 | Reddit r/cscareerquestions | Student and alumni opinions on whether an MS in CS improved career prospects and salary |
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** My documents are a mix of short Gradcafe entries (one admission result 
per line with GPA, GRE, and outcome) and medium-length Reddit posts (2–4 sentences per 
comment). A 300-character chunk keeps each Gradcafe entry intact in one chunk while 
still capturing a complete thought from Reddit comments. Overlap of 50 characters 
ensures that if a stat like "GPA: 3.7, admitted to CMU" spans a chunk boundary, at 
least one of the two chunks will contain the full context needed to answer a query.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** For a real deployment I would consider two tradeoffs. 
First, a domain-specific model like text-embedding-3-large (OpenAI) would better handle 
academic terminology and program names like "OMSCS" or "MCS" that all-MiniLM-L6-v2 may 
treat as out-of-vocabulary tokens. Second, since my users are English-only and documents 
are all in English, multilingual support is not a priority — but latency and cost would 
matter at scale, making a locally-hosted model like all-MiniLM-L6-v2 preferable over an 
API-hosted one despite the accuracy tradeoff.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What GPA do most admitted CMU MSCS students have? | Based on Gradcafe data, most admitted CMU MSCS students have a GPA between 3.7 and 4.0 |
| 2 | Can you get into Georgia Tech OMSCS with a GPA below 3.0? | Reddit posts indicate some students with sub-3.0 GPA have been admitted to OMSCS, especially with strong work experience |
| 3 | Do CS master's programs still require the GRE in 2024? | Most top programs have made GRE optional or dropped it entirely as of 2023–2024 |
| 4 | What GPA did rejected Stanford MSCS applicants typically report? | Gradcafe data shows many rejections even at 3.8+ GPA, indicating Stanford MSCS is highly competitive beyond just GPA |
| 5 | What options do CS applicants with a 3.3 GPA have for master's programs? | Reddit threads suggest OMSCS, UIUC MCS online, and state school programs as realistic targets for sub-3.5 GPA applicants |
---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Chunk boundary splitting stats:** Gradcafe entries often list GPA, GRE, and outcome 
on a single line. If a chunk boundary falls mid-entry (e.g., "GPA: 3.8 | GRE: 165 |" 
in one chunk and "Admitted | CMU MSCS" in the next), neither chunk alone can answer 
"what stats did admitted CMU students have?" — the retrieval will return incomplete 
context. The 50-character overlap is designed to mitigate this but may not fully solve it.

2. **Program name abbreviations:** Students use shorthand like "OMSCS", "MCS", "MSCS", 
"MCIT" inconsistently across sources. The embedding model may not recognize these as 
referring to the same or related programs, causing retrieval to miss relevant chunks 
when a query uses the full program name but documents use the abbreviation, or vice versa.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Raw .txt files (Reddit threads + Gradcafe entries)
            │
            ▼
    [Document Ingestion]
    load_documents.py
    — reads all .txt files from documents/
    — attaches source filename as metadata
            │
            ▼
        [Chunking]
    chunk_text() in ingest.py
    — 300-char chunks, 50-char overlap
    — filters empty chunks
            │
            ▼
      [Embedding]
    sentence-transformers
    all-MiniLM-L6-v2 (local, no API key)
            │
            ▼
     [Vector Store]
       ChromaDB
    — stored locally in ./chroma_db
    — metadata: source filename, chunk index
            │
            ▼
       [Retrieval]
    retrieve() in retrieve.py
    — top-5 semantic similarity search
    — returns chunks + source names
            │
            ▼
      [Generation]
    Groq API — llama-3.3-70b-versatile
    — grounded system prompt
    — answer + source citations
            │
            ▼
    Gradio web UI (app.py)
    http://localhost:7860
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** I will give Claude this planning.md (Documents section + Chunking Strategy section) and 
ask it to implement load_documents() and chunk_text() in ingest.py matching my 300-char 
chunk size and 50-char overlap. I will verify the output by running python ingest.py and 
printing 5 random chunks — each must be readable and self-contained.

**Milestone 4 — Embedding and retrieval:** I will give Claude my Architecture diagram and Retrieval Approach section and ask it to 
implement embed.py (loads chunks, embeds with all-MiniLM-L6-v2, stores in ChromaDB with 
source metadata) and retrieve.py (query function returning top-5 chunks with distances). 
I will verify by running 3 test queries and checking that distance scores are below 0.5 
and returned chunks are visibly relevant.

**Milestone 5 — Generation and interface:** I will give Claude my grounding requirement (answer only from retrieved context, cite 
sources) and ask it to implement generate.py with the Groq API and app.py with a Gradio 
interface showing answer and sources separately. I will verify grounding by asking a 
question my documents don't cover — the system must decline rather than hallucinate.

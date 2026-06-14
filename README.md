# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system covers unofficial student-reported admission statistics for Computer Science 
Master's programs, including GPA, GRE scores, and admit/reject outcomes at top universities 
like CMU, Stanford, Georgia Tech, and UIUC. This knowledge is valuable because prospective 
applicants need realistic benchmarks to decide where to apply, but universities never publish 
actual admit profiles — only vague averages that hide the full picture. The real data — 
specific GPA, GRE scores, and whether someone got in or rejected — only exists in 
student-generated posts on Reddit and Gradcafe, making it impossible to find through any 
official university channel.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit r/gradadmissions | Reddit thread | reddit.com/r/gradadmissions |
| 2 | Reddit r/gradadmissions | Reddit thread | reddit.com/r/gradadmissions |
| 3 | Gradcafe — Carnegie Mellon | Admission results | thegradcafe.com |
| 4 | Gradcafe — Georgia Tech | Admission results | thegradcafe.com |
| 5 | Gradcafe — UIUC | Admission results | thegradcafe.com |
| 6 | Gradcafe — Stanford | Admission results | thegradcafe.com |
| 7 | Reddit r/OMSCS | Reddit thread | reddit.com/r/OMSCS |
| 8 | Reddit r/csMajors | Reddit thread | reddit.com/r/csMajors |
| 9 | Reddit r/gradadmissions | Reddit thread | reddit.com/r/gradadmissions |
| 10 | Reddit r/cscareerquestions | Reddit thread | reddit.com/r/cscareerquestions |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**
My documents are a mix of short Gradcafe entries (one admission result per line with GPA, 
GRE, and outcome) and medium-length Reddit comments (2–4 sentences per comment). A 
300-character chunk keeps each Gradcafe entry intact in one chunk while still capturing 
a complete thought from Reddit comments. Overlap of 50 characters ensures that if a stat 
like "GPA: 3.7, admitted to CMU" spans a chunk boundary, at least one of the two chunks 
will contain the full context needed to answer a query. Before chunking, I preprocessed 
each document by stripping extra blank lines and whitespace using a clean_text() function.

**Final chunk count:** 160 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (local, no API key required)

**Production tradeoff reflection:**
For a real deployment I would consider two tradeoffs. First, a domain-specific model like 
text-embedding-3-large (OpenAI) would better handle academic terminology and program 
abbreviations like "OMSCS" or "MCS" that all-MiniLM-L6-v2 may treat as out-of-vocabulary 
tokens — this directly caused retrieval failures in my evaluation. Second, since my users 
are English-only and all documents are in English, multilingual support is not a priority. 
However, latency and cost at scale would favor a locally-hosted model like all-MiniLM-L6-v2 
over an API-hosted one, despite the accuracy gap on domain-specific abbreviations.

---

## Grounded Generation

**System prompt grounding instruction:**
"You are a helpful assistant for students researching CS Master's program admissions. 
Answer ONLY using the information provided in the context documents below. Do NOT use 
your general training knowledge. If the context does not contain enough information to 
answer the question, say exactly: 'I don't have enough information in my documents to 
answer that.' Always end your response by citing which source document(s) your answer 
draws from."

**How source attribution is surfaced in the response:**
Source filenames are programmatically extracted from the metadata of each retrieved chunk 
in ChromaDB and returned as a separate list alongside the LLM's answer. The Gradio 
interface displays them in a dedicated "Sources" field below the answer, guaranteeing 
attribution even if the LLM forgets to cite inline. This is a structural guarantee — 
not dependent on the LLM remembering to cite.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What GPA do most admitted CMU MSCS students have? | GPA between 3.7–4.0 based on Gradcafe data | "I don't have enough information in my documents to answer that" | Partially relevant | Inaccurate |
| 2 | Can you get into Georgia Tech OMSCS with a GPA below 3.0? | Yes, with strong work experience | Correctly said yes, cited 2.8 GPA example with 5 years experience | Relevant | Accurate |
| 3 | Do CS master's programs still require the GRE in 2024? | Most programs made GRE optional | "I don't have enough information in my documents to answer that" | Partially relevant | Inaccurate |
| 4 | What GPA did rejected Stanford MSCS applicants typically report? | Many rejections at 3.8+ GPA | Could not give a clear answer; cited isolated examples (3.90 ME PhD reject, 3.67 MSCS reject) but noted data was inconclusive | Partially relevant | Partially accurate |
| 5 | What options do CS applicants with a 3.3 GPA have? | OMSCS, UIUC MCS, state schools | Gave general advice (coursework, work experience, recs) but did not name specific programs like OMSCS or UIUC MCS | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**
"What GPA do most admitted CMU MSCS students have?"

**What the system returned:**
"I don't have enough information in my documents to answer that." — despite 
cmu_gradcafe.txt containing multiple entries with GPA values of 3.85, 4.00, and 3.95 
for admitted students.

**Root cause (tied to a specific pipeline stage):**
The failure occurred at the retrieval stage. The query asked for a "typical" or "most 
common" GPA — a summary-level question — but the Gradcafe chunks are structured as 
individual admission entries ("GPA: 3.85, Accepted"). The embedding model could not 
bridge the semantic gap between a query asking for a pattern ("what GPA do most students 
have") and chunks containing individual data points ("GPA: 3.85"). This produced distance 
scores of 0.67–0.77, above the reliable threshold, so the LLM correctly declined rather 
than hallucinating from weak context.

**What you would change to fix it:**
Add a manually written summary chunk at the top of each Gradcafe file that aggregates 
the data: "CMU MSCS admitted students in Fall 2024 had GPAs ranging from 3.7 to 4.0, 
with most above 3.8." This gives the embedding model a summary statement to match 
against pattern-seeking queries, rather than forcing it to infer a pattern from 
individual data points.

---

## Spec Reflection

**One way the spec helped you during implementation:**
Writing the Anticipated Challenges section in planning.md before coding helped me predict 
the chunk boundary problem for Gradcafe entries. Because I anticipated this risk, I 
deliberately chose a 50-character overlap to keep GPA and decision fields in the same 
chunk. This decision was validated during retrieval testing when I confirmed that 
Gradcafe entries were returning mostly intact, with GPA and outcome in the same chunk.

**One way your implementation diverged from the spec, and why:**
My planning.md specified that retrieval distance scores should be below 0.5 for reliable 
results. In practice, even my best CMU MSCS query returned scores of 0.67, well above 
that threshold. This revealed that structured tabular data like Gradcafe entries requires 
a summary layer on top of raw entries to achieve low distance scores on pattern-seeking 
queries. If I rebuilt this system I would add summary chunks to each Gradcafe file before 
embedding, which was not part of the original spec.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My Documents section and Chunking Strategy section from 
  planning.md, and asked Claude to implement load_documents() and chunk_text() in 
  ingest.py with 300-character chunks and 50-character overlap.
- *What it produced:* A complete ingest.py with load_documents(), clean_text(), 
  chunk_text(), and ingest_all() functions that matched my spec exactly.
- *What I changed or overrode:* I ran python ingest.py and inspected 5 random chunks 
  to verify they were self-contained. I confirmed the chunk count of 160 was within 
  the acceptable 50–2000 range before moving on.

**Instance 2**

- *What I gave the AI:* My Architecture diagram and Retrieval Approach section from 
  planning.md, and asked Claude to implement embed.py (storing chunks in ChromaDB with 
  source metadata) and retrieve.py (returning top-5 chunks with distance scores).
- *What it produced:* embed.py that embeds all 160 chunks using all-MiniLM-L6-v2 and 
  stores them in ChromaDB with source filename and chunk index as metadata, and 
  retrieve.py with a retrieve() function returning chunks and distance scores.
- *What I changed or overrode:* I tested retrieval with 3 evaluation questions and 
  observed that the OMSCS query returned a distance of 0.542 (acceptable) while the 
  CMU GPA query returned 0.67+ (weak). I kept the implementation but documented the 
  CMU failure as my failure case rather than tuning parameters to hide it.
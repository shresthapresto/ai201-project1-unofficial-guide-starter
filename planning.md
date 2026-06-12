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
admission statistics that do not reflect actual admit profiles. The real data specific 
GPA, GRE scores, and whether someone got in or rejected, only exists in student-generated 
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
| 10 | Reddit r/cscareerquestions | Student and alumni opinions on whether an

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
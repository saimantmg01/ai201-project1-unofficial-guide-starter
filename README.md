# Hunter College Housing and Commuting Guide

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This project is an unofficial guide to housing and commuting for Hunter College
students. It is designed to help students compare Hunter-affiliated housing,
off-campus housing, and commuting by answering practical questions about
availability, neighborhoods, roommates, transit routes, rental safety, and
tenant rights.

The information is valuable but difficult to find in one place. Official Hunter
College and MTA pages explain residences, campus locations, and transit routes,
while students' experiences with waitlists, housing costs, roommate searches,
summer closures, and long commutes are scattered across discussion threads.
NYC rental protections and safety guidance are published separately by city
agencies.

### Run the Guide

Create `.env` from `.env.example`, add a Groq API key, and build the local
vector index once:

```bash
python retrieval.py --index
python app.py
```

Open `http://127.0.0.1:7860`, enter a housing or commuting question, and select
**Ask**. The answer and retrieved source links appear in separate panels.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Hunter College Housing | Official college housing page | https://www.hunter.cuny.edu/students/campus-life/residence-life/ |
| 2 | Hunter College 68th Street Campus | Official campus directions | https://www.hunter.cuny.edu/about/campus-information/68th-street-campus/ |
| 3 | CUNY Residence Life | Official CUNY housing resource | https://www.cuny.edu/about/administration/offices/student-affairs/programs-services/housing-residence-life/ |
| 4 | MTA 6 Train Line Map | Official transit page | https://www.mta.info/maps/subway-line-maps/6-line |
| 5 | MTA Maps | Official transit maps | https://www.mta.info/maps |
| 6 | "Best way to go about housing while at Hunter?" | Reddit student discussion | https://www.reddit.com/r/HunterCollege/comments/1d4s1es/ |
| 7 | "Off campus student housing" | Reddit student discussion | https://www.reddit.com/r/HunterCollege/comments/1ggxot5/ |
| 8 | "51st midtown dorms, 79th dorms, and outside housing" | Reddit student discussion | https://www.reddit.com/r/HunterCollege/comments/1jq6ewe/ |
| 9 | "Best option for housing as a very low income student?" | Reddit student discussion | https://www.reddit.com/r/HunterCollege/comments/1imttmj/ |
| 10 | "How is commute to Hunter" | Reddit student discussion | https://www.reddit.com/r/HunterCollege/comments/1h0sblm/ |
| 11 | NYC Tenant Bill of Rights | Official NYC tenant guidance | https://www.nyc.gov/site/hpd/services-and-information/tenant-bill-of-rights.page |
| 12 | Spot an Illegal Conversion | Official NYC rental-safety guidance | https://www.nyc.gov/site/buildings/tenant/spot-illegal-conversion.page |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 250 characters

**Overlap:** 40 characters

**Why these choices fit your documents:** The corpus contains short student
discussions and compact official guidance. A custom boundary-aware splitter
targets 250 characters while preferring paragraph breaks, newlines, sentence
endings, and word boundaries. Initial retrieval tests at 200 characters found
the correct sources but sometimes missed the sentence containing the answer,
so the target was increased to preserve more context. The 40-character overlap
reduces context loss at boundaries. Before chunking, the loader separates the
title, source type, and URL into metadata, excludes `documents/README.txt`,
removes the reliability note from the content, and collapses excessive blank
lines.

**Final chunk count:** 54 chunks across 12 source documents.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` from `sentence-transformers`. It runs
locally, requires no API key, and is fast enough to embed this small
English-language corpus. The 54 chunk embeddings are stored in a persistent
ChromaDB collection using cosine distance. Each record includes the source
filename, title, URL, source type, and position within the source document.

**Production tradeoff reflection:** For a production system, I would compare
larger local and API-hosted embedding models for retrieval accuracy, latency,
cost, context length, and multilingual support. A larger model could better
represent nuanced housing and tenant-rights language, while a multilingual
model would serve more of Hunter's student population. The current model is a
reasonable project choice because the documents and questions are short and
written in English.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The system prompt tells the model:
"Answer the user's question using only the supplied source excerpts. Do not use
outside knowledge or make assumptions. If the excerpts do not contain enough
information, reply exactly: I don't have enough information on that." It also
requires bracketed source citations and asks the model to distinguish official
information from individual student experiences. Before the LLM is called, the
pipeline rejects a query when its best cosine distance is above `0.50`.

**How source attribution is surfaced in the response:** Retrieved chunks are
numbered in the prompt so the model can cite them as `[Source 1]`, `[Source 2]`,
and so on. Independently of the generated answer, the application constructs a
deduplicated source list from ChromaDB metadata and displays each source's
title, type, URL, and retrieval distance. This guarantees that attribution is
shown even if the model omits an inline citation.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | Actual system response | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which subway line stops directly at Hunter College's main 68th Street campus? | The 6 train stops at 68 St-Hunter College. | "The 6 subway line stops directly at Hunter College's main 68th Street campus, at the 68 St-Hunter College station [Source 1, Source 2, Source 3]." | Relevant | Accurate |
| 2 | Is Hunter-affiliated housing guaranteed to students? | No; space is limited and students must reapply. | "According to [Source 3], Hunter-affiliated housing is not guaranteed to students, as the application process is highly competitive and there are only a limited number of housing spaces available." | Relevant | Accurate |
| 3 | What alternatives do students discuss when Hunter housing is unavailable or too expensive? | Roommates, sublets, third-party housing, and housing along a convenient transit route. | "According to student discussions [Source 1, Source 2, Source 3], alternatives include an off-campus sublet or shared apartment with roommates, third-party student housing, and housing along a commute route." | Relevant | Accurate |
| 4 | What should a student consider before choosing a long commute instead of housing near Hunter? | Compare cost, travel time, transfers, reliability, schedule, and the burden of commuting. | "A student should consider their starting location, the impact of a long commute on daily life, the cost of housing near Hunter compared with commuting, and whether financial assistance is available [Source 1, Source 2, Source 3]." | Relevant | Partially accurate |
| 5 | What rental warning signs can indicate an illegal or unsafe NYC apartment? | Unusually low prices, unsafe basement or attic rooms, inadequate exits or windows, unpermitted walls, and informal rental arrangements. | "Warning signs include a price far below comparable apartments, basement or attic listings without adequate exits, rooms without proper windows, unpermitted flex walls, suspicious utility arrangements, and missing safety features [Source 1, Source 2, Source 3, Source 4]." | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What should a student consider before choosing a long
commute instead of housing near Hunter?

**What the system returned:** It correctly discussed starting location, the
burden of a four-hour commute, housing costs, and asking the financial-aid
office for guidance. It did not explicitly mention transfers, transit
reliability, or class schedule demands.

**Root cause (tied to a specific pipeline stage):** Retrieval returned relevant
student-experience chunks, but the corpus does not contain one chunk that
combines every commute tradeoff in the expected answer. With `top-k=4`, the
generation stage could only synthesize the factors present in those excerpts.

**What you would change to fix it:** Add a source specifically comparing NYC
commute time, transfers, reliability, and class schedules, or retrieve more
adjacent chunks for broad comparison questions.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped me during implementation:** The spec forced me to
define the document types, chunk size, overlap, embedding model, top-k value,
and expected answers before connecting the components. That made debugging more
systematic: when retrieval returned the correct source but omitted the answer
sentence, I could identify chunking as the likely cause instead of changing the
embedding model or prompt at random. The five evaluation questions also gave me
a stable test set for comparing each pipeline revision.

**One way my implementation diverged from the spec, and why:** The original
plan used 200-character chunks, but retrieval testing showed that those chunks
sometimes ended before the decisive sentence. I increased the target to 250
characters while retaining 40 characters of overlap; this reduced the corpus
from 66 to 54 chunks and improved answer retrieval while staying above
the suggested minimum. I also added a `0.50` cosine-distance gate
before generation, which was not in the initial architecture but was necessary
to make unsupported questions decline reliably.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1: Document ingestion and chunking**

- *What I gave the AI:* I provided the Documents and Chunking Strategy
  sections from `planning.md`, the 12 local text files, and the Milestone 3
  requirements for cleaning, metadata, overlap, chunk inspection, and count.
- *What it produced:* Claude helped implement `ingest.py`, including metadata
  parsing, content cleaning, a custom boundary-aware chunker, and diagnostic
  output for a cleaned document and five random chunks.
- *What I changed or overrode:* I chose a custom splitter instead of adding
  LangChain solely for chunking. After retrieval tests exposed incomplete
  200-character chunks, I directed the chunk size change to 250 characters and
  updated the plan and README to reflect the measured 54-chunk result.

**Instance 2: Retrieval, grounding, and interface**

- *What I gave the AI:* I provided the Retrieval Approach, five evaluation
  questions, Groq grounding requirements, ChromaDB metadata requirements, and
  the Milestone 5 Gradio interface expectations.
- *What it produced:* Codex helped implement `retrieval.py`, `query.py`, and
  `app.py`, including MiniLM embeddings, persistent cosine search, a
  context-only Groq prompt, and a Gradio answer-and-sources interface.
- *What I changed or overrode:* I required source attribution to be generated
  programmatically from ChromaDB metadata instead of trusting the LLM to cite
  correctly. I also added and tested a `0.50` relevance threshold so an
  unsupported dining question is rejected before Groq is called.

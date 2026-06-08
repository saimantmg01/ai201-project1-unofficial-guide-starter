# The Unofficial Guide — Project 1

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

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

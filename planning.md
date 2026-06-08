# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This project is an unofficial guide to housing and commuting for Hunter College
students, especially students deciding between Hunter-affiliated housing,
off-campus housing, and commuting from another part of New York City. It will
help answer practical questions about housing availability, neighborhoods,
roommates, transit routes, commute tradeoffs, rental safety, and tenant rights.

This knowledge is difficult to find in one place. Hunter College and the MTA
publish authoritative information about residences, campus locations, and
transit routes, but they do not capture students' firsthand experiences with
long commutes, housing waitlists, roommate searches, summer closures, or the
tradeoffs between cost and convenience. Those details are scattered across
official pages, Reddit threads, and New York City housing resources.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Hunter College Housing | Official overview of Hunter-affiliated residences, limited availability, and the housing application process. | https://www.hunter.cuny.edu/students/campus-life/residence-life/ |
| 2 | Hunter College 68th Street Campus | Official campus location and directions by subway and bus, including the direct entrance from the 68th Street station. | https://www.hunter.cuny.edu/about/campus-information/68th-street-campus/ |
| 3 | CUNY Residence Life | CUNY-wide residence options, eligibility information, and housing resources available to students. | https://www.cuny.edu/about/administration/offices/student-affairs/programs-services/housing-residence-life/ |
| 4 | MTA 6 Train Line Map | Official list of 6 train stops and transfer points, including 68 St-Hunter College. | https://www.mta.info/maps/subway-line-maps/6-line |
| 5 | MTA Maps | Official subway, accessibility, late-night, and borough bus maps for comparing possible commutes. | https://www.mta.info/maps |
| 6 | "Best way to go about housing while at Hunter?" | Hunter student discussion about moving closer to campus, residence photos, and how to begin a housing search. | https://www.reddit.com/r/HunterCollege/comments/1d4s1es/ |
| 7 | "Off campus student housing" | Student experiences with Hunter housing, third-party student housing, apartment costs, and finding roommates. | https://www.reddit.com/r/HunterCollege/comments/1ggxot5/ |
| 8 | "51st midtown dorms, 79th dorms, and outside housing" | Discussion comparing Hunter residences with outside housing, including summer availability and roommate-search options. | https://www.reddit.com/r/HunterCollege/comments/1jq6ewe/ |
| 9 | "Best option for housing as a very low income student?" | Student discussion of financial aid, housing costs, roommates, and the burden of a two-hour commute. | https://www.reddit.com/r/HunterCollege/comments/1imttmj/ |
| 10 | "How is commute to Hunter" | Firsthand comments about commute length, the 6 train, and studying during longer trips. | https://www.reddit.com/r/HunterCollege/comments/1h0sblm/ |
| 11 | NYC Tenant Bill of Rights | Official guidance on application fees, security deposits, leases, housing quality, evictions, and landlord harassment. | https://www.nyc.gov/site/hpd/services-and-information/tenant-bill-of-rights.page |
| 12 | Spot an Illegal Conversion | Official NYC warning signs for unsafe or illegally converted rental units. | https://www.nyc.gov/site/buildings/tenant/spot-illegal-conversion.page |

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
| 1 | Which subway line stops directly at Hunter College's main 68th Street campus? | The 6 train stops at 68 St-Hunter College, and the station has an entrance directly into the college. |
| 2 | Is Hunter-affiliated housing guaranteed to students? | No. Hunter has limited housing for a student population of more than 22,000, so housing is competitive, not guaranteed, and students must reapply each year. |
| 3 | What alternatives do students discuss when Hunter housing is unavailable or too expensive? | Students commonly discuss sharing an off-campus apartment with roommates, searching roommate groups or services, and considering third-party student housing. |
| 4 | What should a student consider before choosing a long commute instead of housing near Hunter? | They should compare rent and housing costs with total travel time, transit reliability, transfers, schedule demands, and the academic and personal burden of spending several hours commuting each day. |
| 5 | What rental warning signs can indicate an illegal or unsafe NYC apartment? | Warning signs include a suspiciously low price, basement or attic rooms with inadequate exits or windows, unpermitted flex walls, cash-only arrangements, no written lease, and a landlord unwilling to place utilities in the tenant's name. |

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

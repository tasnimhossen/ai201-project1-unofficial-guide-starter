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

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

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


# Evaluation Results

| Question                                      | Expected Answer                                                        | Actual Response                                                                                                                                                     | Accuracy   |
| --------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| What is ISYE 6501 known for?                  | Broad introduction to analytics methods and foundational OMSA concepts | The system retrieved course review information describing ISYE 6501 as a foundational OMSA course covering regression, classification, clustering, and forecasting. | Accurate   |
| What do students say about CSE 6242 workload? | Heavy workload, large projects, and significant time commitment        | The system retrieved reviews discussing project-heavy coursework, team projects, and substantial workload requirements.                                             | Accurate   |
| Why do students recommend CSE 6040?           | Python programming skills and preparation for later OMSA courses       | The system retrieved reviews emphasizing Python programming, computational problem solving, and preparation for advanced OMSA coursework.                           | Accurate   |
| What skills help OMSA students succeed?       | Python, statistics, probability, and linear algebra                    | The system retrieved FAQ content identifying Python, statistics, probability, and linear algebra as useful skills.                                                  | Accurate   |
| What is the best dining hall at Georgia Tech? | Not covered by the corpus                                              | The system returned weakly related OMSA content because no dining hall information exists in the document collection.                                               | Inaccurate |

# Failure Case Analysis

One failure occurred when asking about Georgia Tech dining halls. The corpus only contains OMSA course reviews, Reddit discussions, curriculum information, and FAQ documents. Because the retrieval system always returns the nearest available chunks, it retrieved OMSA-related content even though the query was outside the scope of the dataset.

The failure occurred during retrieval rather than generation. The embedding model returned the closest educational content available despite the question being unrelated to OMSA coursework. A future improvement would be implementing a similarity threshold so the system can reject low-confidence retrieval results and explicitly state that it lacks sufficient information.

# Spec Reflection

The planning specification helped guide implementation by requiring chunking decisions, retrieval choices, evaluation questions, and architecture design before coding. This made implementation more structured and reduced uncertainty during development.

One area where implementation differed from the original specification was chunking. During testing, larger chunks produced too few retrievable segments for the small corpus. The chunk size and overlap were adjusted to increase the number of chunks and improve retrieval performance.

# AI Usage

## Example 1

I used ChatGPT to help implement the ingestion and chunking pipeline. I provided my planned chunking strategy and document structure. The generated code loaded text files, cleaned content, and produced overlapping chunks. After inspecting the output, I modified the chunk size and overlap to better fit the corpus.

## Example 2

I used ChatGPT to help implement embeddings and retrieval using SentenceTransformers and ChromaDB. The generated code provided a starting point for embedding storage and semantic search. I adjusted file paths, retrieval parameters, and debugging logic to match the project structure and improve retrieval quality.


Question 1:
What is ISYE6501 known for?

Based on the retrieved documents:

[Source: isye6501_reviews.txt]
ISYE 6501 is considered one of the foundational OMSA courses. Students describe it as a broad survey of analytics methods including regression, classi

[Source: isye6740_reviews.txt]
Review 1: ISYE 6740 is one of the most mathematically rigorous courses in OMSA. Students should be comfortable with linear algebra and probability con

[Source: reddit_course_difficulty.txt]
during the first few weeks. User C: I would recommend taking ISYE 6501 and CSE 6040 before attempting some of the more advanced courses. Those classe

Question 2:
What do students say about CSE 6242 workload?

Based on the retrieved documents:

[Source: reddit_cse6242.txt]
Discussion: Is CSE 6242 Really That Bad? User A: The workload is definitely significant, but I learned more practical skills in this class than in man

[Source: cse6242_reviews.txt]
mention large team projects, challenging assignments, and significant time commitments. Many reviews describe the workload as heavy. Several students

[Source: isye6501_reviews.txt]
s including regression, classification, clustering, and forecasting. Most reviews mention a moderate workload and weekly assignments. Many students re

Question 3:
Based on the retrieved documents:

[Source: reddit_course_difficulty.txt]
t on background. Students with software engineering experience often find CSE 6040 easy but may struggle with the mathematical aspects of machine lear

[Source: reddit_cse6242.txt]
Discussion: Is CSE 6242 Really That Bad? User A: The workload is definitely significant, but I learned more practical skills in this class than in man

[Source: cse6040_reviews.txt]
. Review 5: Many advanced OMSA courses assume familiarity with Python, making CSE 6040 a valuable foundation course.


Question 4:
What skills help OMSA students succeed?

Based on the retrieved documents:

[Source: omsa_curriculum.txt]
The OMSA curriculum consists of foundational courses, advanced analytics courses, and electives. Students are expected to develop skills in programmin

[Source: reddit_isye6740.txt]
lt, many students consider it one of the most valuable technical courses in OMSA.

[Source: cse6242_reviews.txt]
Review 1: CSE 6242 Data and Visual Analytics is frequently described as one of the most demanding OMSA courses. Students mention large team projects,


Question 5:
What is the best dining hall at Georgia Tech?


[Source: cse6242_reviews.txt]
enges. Students consistently recommend maintaining regular contact with project partners.

[Source: reddit_isye6740.txt]
lt, many students consider it one of the most valuable technical courses in OMSA.

[Source: cse6242_reviews.txt]
many hours of work each week. Review 2: Students often comment that the course teaches valuable real-world analytics skills. Team projects require co


## Failure Case Analysis

One partial failure occurred when asking: "What is the best dining hall at Georgia Tech?" The system still returned an answer instead of clearly rejecting the question. This happened because the retrieval system always returns the nearest available chunks from ChromaDB, even when the question is outside the OMSA course-review domain.

The answer was not grounded in dining hall documents because the corpus does not contain campus dining information. This failure occurred during retrieval: the vector store found the closest available OMSA-related chunks, but there was no relevance threshold to determine that the query was out of scope. A future improvement would be adding a distance threshold so that if the top retrieval score is too weak, the system responds with "I don't have enough information in the provided documents to answer that."


# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- My chosen domain is Georgia Tech OMSA/MSDS course reviews, student experiences, and program guidance. This knowledge is valuable because students need practical information about course difficulty, workload, professors, exams, projects, and recommended course sequencing before registering. Official Georgia Tech pages explain requirements, but they do not fully capture student experience, workload reality, or which courses are manageable while working or interning. -->

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #  | Source                               | Description                                                       | URL or location                                                               |
| -- | ------------------------------------ | ----------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1  | OMSCentral - ISYE 6501 Reviews       | Student reviews discussing workload, difficulty, and course value | https://www.omscentral.com/courses/introduction-to-analytics-modeling/reviews |
| 2  | OMSCentral - CSE 6040 Reviews        | Reviews focused on Python programming and data analysis skills    | https://www.omscentral.com/courses/computing-for-data-analysis/reviews        |
| 3  | OMSCentral - CSE 6242 Reviews        | Student opinions on Data & Visual Analytics workload and projects | https://www.omscentral.com/courses/data-and-visual-analytics/reviews          |
| 4  | OMSCentral - ISYE 6740 Reviews       | Reviews of the Machine Learning course and its difficulty         | https://www.omscentral.com/courses/machine-learning/reviews                   |
| 5  | OMSCentral - ISYE 6644 Reviews       | Student experiences with Simulation and modeling coursework       | https://www.omscentral.com/courses/simulation/reviews                         |
| 6  | Reddit OMSA Community                | General OMSA discussions, course recommendations, and advice      | https://www.reddit.com/r/OMSA/                                                |
| 7  | Reddit Course Difficulty Discussions | Student rankings and comparisons of OMSA course difficulty        | https://www.reddit.com/r/OMSA/search/?q=course+difficulty                     |
| 8  | Reddit CSE 6242 Discussions          | Student experiences specifically about CSE 6242                   | https://www.reddit.com/r/OMSA/search/?q=CSE+6242                              |
| 9  | Reddit ISYE 6740 Discussions         | Student experiences specifically about ISYE 6740                  | https://www.reddit.com/r/OMSA/search/?q=ISYE+6740                             |
| 10 | Georgia Tech OMSA Curriculum         | Official program requirements and course structure                | https://pe.gatech.edu/degrees/analytics/curriculum                            |
| 11 | Georgia Tech MS Analytics Catalog    | Official course descriptions and degree requirements              | https://catalog.gatech.edu/programs/analytics-ms/                             |
| 12 | Georgia Tech OMSA FAQ                | Official answers regarding program policies and expectations      | https://pe.gatech.edu/degrees/analytics/faqs                                  |
| 13 | CSE 6040 Course Syllabus             | Official syllabus covering assignments, grading, and schedule     | Local PDF or course website                                                   |
| 14 | ISYE 6501 Course Syllabus            | Official syllabus covering assignments, grading, and schedule     | Local PDF or course website                                                   |
| 15 | OMSA Student Guides / FAQs           | Community-created guides for course planning and success          | Local documents or community resources                                        |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size: 750 characters **

**Overlap: 100 characters**

**Reasoning:
My document collection consists primarily of OMSCentral course reviews, Reddit discussions, course syllabi, and Georgia Tech OMSA information pages. Most reviews and Reddit comments are relatively short and often contain a complete opinion or recommendation within a few sentences. A chunk size of approximately 750 characters is large enough to preserve the context of a review while remaining small enough for precise retrieval.

I will use a 100-character overlap between chunks to prevent important information from being split across chunk boundaries. This is particularly useful for longer documents such as course syllabi and FAQ pages where details about assignments, exams, grading policies, or prerequisites may span multiple paragraphs.

If chunks are too small, retrieval may return isolated fragments that lack enough context to answer a question accurately. If chunks are too large, retrieval may include irrelevant information and reduce the quality of search results. The selected chunk size balances context preservation and retrieval precision for a corpus that contains both short reviews and longer informational documents. 
**

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` using the `sentence-transformers` library

**Top-k:** 4 chunks per query

**Production tradeoff reflection:**

For this project, I will use `all-MiniLM-L6-v2` because it is lightweight, fast, easy to run locally, and strong enough for a small RAG system over course reviews and student discussions. I will retrieve the top 4 chunks per query because that should provide enough context without overwhelming the generation step with too much irrelevant information.

If this were deployed for real users and cost was not a constraint, I would compare larger embedding models with better semantic accuracy and longer context support. I would also consider whether the model handles informal student language well, since Reddit posts and course reviews often use abbreviations, slang, and subjective wording. The main tradeoffs would be retrieval accuracy, latency, cost, context length, and whether the model performs well on education-related and review-style text.

---

## Evaluation Plan

| # | Question                                                                                  | Expected answer                                                                                                                                                                                |
| 1 | What do students commonly say about the workload in CSE 6242 Data and Visual Analytics?   | Students commonly describe CSE 6242 as workload-heavy, project-intensive, and difficult to take with multiple other demanding courses.                                                         |
| 2 | Is CSE 6040 considered useful for building Python and data analysis skills?               | Yes. Student reviews generally describe CSE 6040 as useful for strengthening Python, data manipulation, and computational problem-solving skills.                                              |
| 3 | What is ISYE 6501 mainly known for in the OMSA program?                                   | ISYE 6501 is mainly known as an introductory analytics modeling course that exposes students to a broad range of modeling techniques.                                                          |
| 4 | Why should official Georgia Tech curriculum pages be included along with student reviews? | Official pages provide reliable degree requirements and course structure, while student reviews provide practical information about workload, difficulty, and student experience.              |
| 5 | What type of student would benefit from OMSCentral and Reddit course discussions?         | OMSA students choosing courses or planning schedules would benefit because these sources discuss workload, difficulty, professors, projects, and whether courses are manageable while working. |

---

## Anticipated Challenges

1. Student reviews and Reddit comments may be noisy, subjective, or contradictory. One student may describe a course as easy because they have strong programming or math experience, while another student may describe the same course as extremely difficult.

2. Source attribution may be difficult if chunks lose metadata during ingestion or chunking. Each chunk needs to preserve the original source URL, course name, and title so the generated answer can cite where the information came from.

3. Some Reddit discussions mention multiple courses in the same thread. This could cause off-topic retrieval where the system returns a relevant-looking chunk, but the chunk is actually discussing a different course.

4. Longer documents such as syllabi or FAQs may split important information across chunk boundaries. The overlap helps reduce this risk, but I will still need to check whether chunks preserve headings and context.

---

## Architecture

## Architecture

```mermaid
flowchart LR

A[Document Ingestion
Python Requests
BeautifulSoup
Local Files]

--> 

B[Chunking
chunk_text()
750 chars
100 overlap]

-->

C[Embedding + Vector Store
all-MiniLM-L6-v2
Sentence Transformers
ChromaDB]

-->

D[Retrieval
Semantic Search
Top-k = 4]

-->

E[Generation
LLM Response
Source Citations]
```


---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**

I plan to use ChatGPT or Claude to help implement document ingestion and chunking. I will give the AI the Documents section, Chunking Strategy section, and project requirement that every chunk should preserve metadata. I expect it to produce Python code that loads text from URLs and local files, cleans the text, and implements a `chunk_text(text, chunk_size=750, overlap=100)` function. I will verify the output by printing the number of chunks, checking sample chunks manually, and confirming that source URL, title, and course name are preserved in the metadata.

**Milestone 4 — Embedding and retrieval:**

I plan to use ChatGPT or Claude to help implement embeddings and vector storage. I will give the AI the Retrieval Approach section and ask it to use `sentence-transformers/all-MiniLM-L6-v2` with ChromaDB. I expect it to produce code that embeds all chunks, stores them in a local vector database, and implements a `retrieve(query, top_k=4)` function. I will verify the output by running my five evaluation questions and checking whether the retrieved chunks actually come from relevant course reviews, Reddit discussions, or official pages.

**Milestone 5 — Generation and interface:**

I plan to use ChatGPT or Claude to help implement the final question-answering function and a simple interface. I will provide the AI with my Architecture, Retrieval Approach, and Evaluation Plan sections. I expect it to produce code that takes a user question, retrieves the top 4 chunks, passes them to an LLM, and generates an answer using only the retrieved context with source citations. I will verify the output by comparing system answers to the expected answers in my evaluation plan and checking that the response does not make unsupported claims.

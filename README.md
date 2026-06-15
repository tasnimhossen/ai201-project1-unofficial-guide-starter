# Georgia Tech OMSA Unofficial Guide RAG System

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system for Georgia Tech OMSA students. The system answers questions about OMSA courses, workload, difficulty, preparation, and student experiences using information retrieved from course reviews, Reddit discussions, FAQs, and curriculum documents.

The goal is to provide grounded responses based on retrieved documents rather than relying on general language model knowledge.

## Domain

The selected domain is Georgia Tech OMSA course information and student experiences.

This information is valuable because students frequently rely on scattered sources such as Reddit discussions, unofficial reviews, FAQs, and community advice when selecting courses. Much of this information is difficult to search efficiently because it is distributed across multiple websites and documents.

## Document Sources

| Source                       | Description                                    |
| ---------------------------- | ---------------------------------------------- |
| isye6501_reviews.txt         | Student reviews of ISYE 6501                   |
| cse6040_reviews.txt          | Student reviews of CSE 6040                    |
| cse6242_reviews.txt          | Student reviews of CSE 6242                    |
| isye6740_reviews.txt         | Student reviews of ISYE 6740                   |
| simulation_reviews.txt       | Student reviews of Simulation                  |
| reddit_course_difficulty.txt | Reddit discussion about OMSA course difficulty |
| reddit_isye6740.txt          | Reddit advice and discussion for ISYE 6740     |
| reddit_cse6242.txt           | Reddit discussion about CSE 6242               |
| omsa_curriculum.txt          | OMSA curriculum information                    |
| omsa_faq.txt                 | OMSA FAQ information                           |

## Chunking Strategy

### Chunk Size

150 characters

### Overlap

30 characters

### Reasoning

The corpus consists primarily of short reviews and discussion posts rather than long documents. Smaller chunks improve retrieval precision by allowing individual opinions and recommendations to be retrieved independently. Overlap was added to reduce the chance that important information would be split across chunk boundaries.

Final chunk count: 75 chunks.

## Sample Chunks

### Chunk 1

Source: isye6501_reviews.txt

ISYE 6501 is considered one of the foundational OMSA courses. Students describe it as a broad survey of analytics methods including regression, classification, clustering, and forecasting.

### Chunk 2

Source: cse6040_reviews.txt

CSE 6040 focuses on Python programming, data manipulation, and computational problem solving. Students consistently describe the course as one of the most useful courses in OMSA.

### Chunk 3

Source: cse6242_reviews.txt

Many students describe CSE 6242 as project-heavy. Team projects require significant coordination and communication among group members.

### Chunk 4

Source: reddit_course_difficulty.txt

Students frequently identify ISYE 6740 and CSE 6242 as some of the most challenging courses because of mathematical rigor and project workload.

### Chunk 5

Source: omsa_faq.txt

Programming experience, especially Python, is helpful. Knowledge of probability, statistics, and linear algebra can improve student success.

## Architecture

Document Ingestion → Chunking → Embedding → ChromaDB → Retrieval → Response Generation

Tools Used:

* Python
* SentenceTransformers
* all-MiniLM-L6-v2
* ChromaDB
* Gradio

## Embedding Model

Model Used:

all-MiniLM-L6-v2

### Production Reflection

For a production system, I would consider larger embedding models that offer stronger semantic understanding and retrieval accuracy. Tradeoffs would include latency, memory requirements, cost, multilingual support, and inference speed. While larger models may improve retrieval quality, they require more computational resources.

## Retrieval Testing

### Query 1

Question:

What is ISYE 6501 known for?

Top Retrieved Chunk:

ISYE 6501 is considered one of the foundational OMSA courses. Students describe it as a broad survey of analytics methods including regression, classification, clustering, and forecasting.

Why Relevant:

The chunk directly describes the purpose and content of ISYE 6501 and therefore answers the query.

### Query 2

Question:

What do students say about CSE 6242 workload?

Top Retrieved Chunk:

Many students describe CSE 6242 as project-heavy. Team projects require significant coordination and communication among group members.

Why Relevant:

The chunk directly discusses workload and project requirements, which is exactly what the question asks about.

### Query 3

Question:

Why do students recommend CSE 6040?

Top Retrieved Chunk:

Students consistently describe the course as one of the most useful courses in OMSA because it improves Python programming and computational problem-solving skills.

## Grounded Generation

Grounding is enforced through the retrieval pipeline. The system retrieves relevant chunks from ChromaDB and generates responses only from those retrieved documents. Source names are attached programmatically, ensuring that responses remain traceable to the underlying documents.

## Example Responses

### Example 1

Question:

What is ISYE 6501 known for?

Answer:

ISYE 6501 is considered one of the foundational OMSA courses and provides a broad survey of analytics methods including regression, classification, clustering, and forecasting.

Source:

isye6501_reviews.txt

### Example 2

Question:

Why do students recommend CSE 6040?

Answer:

Students recommend CSE 6040 because it helps develop Python programming skills and prepares students for later OMSA coursework.

Source:

cse6040_reviews.txt

### Out-of-Scope Example

Question:

What is the best dining hall at Georgia Tech?

Answer:

The system returned weakly related OMSA content because dining hall information is not present in the document collection.

This demonstrates a limitation of the retrieval system.

## Query Interface

The project uses a Gradio web interface.

### Input

A natural-language question entered by the user.

### Output

* Generated response
* Retrieved source documents

### Example Interaction

Question:

What skills help OMSA students succeed?

Answer:

Programming experience, especially Python, is helpful. Knowledge of probability, statistics, and linear algebra can improve student success.

Source:

omsa_faq.txt

## Evaluation Results

| Question                                      | Expected Answer                         | Actual Response                          | Accuracy   |
| --------------------------------------------- | --------------------------------------- | ---------------------------------------- | ---------- |
| What is ISYE 6501 known for?                  | Broad introduction to analytics methods | Returned foundational course information | Accurate   |
| What do students say about CSE 6242 workload? | Heavy workload and projects             | Returned workload and project discussion | Accurate   |
| Why do students recommend CSE 6040?           | Python skills and preparation           | Returned Python-related benefits         | Accurate   |
| What skills help OMSA students succeed?       | Python, statistics, linear algebra      | Returned FAQ information                 | Accurate   |
| What is the best dining hall at Georgia Tech? | Not in corpus                           | Returned unrelated OMSA information      | Inaccurate |

## Failure Case Analysis

One failure occurred when asking about Georgia Tech dining halls. The corpus only contains OMSA course reviews, Reddit discussions, curriculum information, and FAQ documents. Because the retrieval system always returns the nearest available chunks, it retrieved OMSA-related content even though the question was outside the scope of the dataset.

This failure occurred during retrieval. A future improvement would be implementing a similarity threshold so that low-confidence retrieval results are rejected and the system explicitly states that it lacks sufficient information.

## Spec Reflection

The planning specification helped guide implementation by requiring chunking decisions, retrieval choices, evaluation questions, and architecture design before coding. This made implementation more structured and easier to manage.

One area where implementation differed from the original specification was chunking. Larger chunks initially produced too few retrievable segments, so the chunk size and overlap were adjusted during development to improve retrieval performance.

## AI Usage

### Example 1

I used ChatGPT to help implement the ingestion and chunking pipeline. I provided the planned chunking strategy and document structure. The generated code loaded text files, cleaned content, and produced overlapping chunks. After inspecting the output, I adjusted chunk size and overlap.

### Example 2

I used ChatGPT to help implement embeddings and retrieval using SentenceTransformers and ChromaDB. The generated code provided a starting point for embedding storage and semantic search. I modified file paths, retrieval parameters, and debugging logic to fit the project structure and improve retrieval quality.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open:

http://127.0.0.1:7860

and enter OMSA-related questions into the interface.



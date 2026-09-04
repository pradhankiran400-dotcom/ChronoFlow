# ChronoFlow – Complete Project Documentation

## 1. Project Overview

**ChronoFlow** is an interactive, AI-powered topic timeline platform that helps users explore the evolution of topics, events, ideas, and technologies over time.

Traditional information platforms usually display articles as simple lists. ChronoFlow organizes related events chronologically and presents them through an interactive timeline. Users can explore a topic, search for information, apply filters, open detailed articles, and ask AI-powered questions based on the stored knowledge base.

### Example

A user selects **Artificial Intelligence** and sees important developments across time:

```text
2020          2021          2022          2023          2024
 |             |             |             |             |
 ●             ●             ●             ●             ●
 GPT-3       DALL·E       ChatGPT       GPT-4       New AI Models
```

The user can click an event to read its details or ask:

> How did Artificial Intelligence evolve during 2023?

The system retrieves relevant stored articles and generates an answer with source references.

---

# 2. Main Objectives

ChronoFlow aims to:

- Organize information chronologically.
- Help users understand the evolution of a topic.
- Provide interactive timeline exploration.
- Support article and event management.
- Enable search and filtering.
- Provide semantic search using AI.
- Answer user questions using relevant stored information.
- Show the sources used for AI-generated answers.

---

# 3. Technology Stack

## Frontend

- React
- Vite
- Tailwind CSS

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

## Database

- PostgreSQL
- pgvector

## AI/ML

- Embedding model/API
- LLM API
- RAG architecture

> Redis is not used in this project.

---

# 4. System Architecture

```text
                        USER
                          |
                          v
                  React Frontend
                          |
                          | HTTP Requests
                          v
                    FastAPI Backend
                     /           \
                    /             \
                   v               v
            PostgreSQL          AI/ML Layer
                 |                 |
                 |          +------+------+
                 |          |             |
                 v          v             v
             Articles   Embeddings       LLM
                 |          |
                 +----------+
                     |
                     v
                  pgvector
```

---

# 5. Main User Flow

```text
User
 |
 v
Browse Topics
 |
 v
Select a Topic
 |
 v
Explore Interactive Timeline
 |
 +--> Search Articles
 |
 +--> Filter by Date
 |
 +--> Filter by Tags
 |
 v
Click an Event
 |
 v
View Article Details
 |
 +--> Ask AI Questions
          |
          v
     Get Answer + Sources
```

---

# 6. Core Features

## 6.1 Topic Management

The application supports multiple topics.

Examples:

- Artificial Intelligence
- Space Exploration
- Climate Change
- Blockchain
- Robotics

Each topic contains related articles and events.

### Features

- Create a topic
- View all topics
- View a single topic
- Update a topic
- Delete a topic

---

## 6.2 Article Management

Articles represent important events or pieces of information.

Each article contains:

- Title
- Summary
- Full content
- Source URL
- Publication date
- Topic
- Tags

### Features

- Create article
- View articles
- Update article
- Delete article
- Assign topic
- Assign multiple tags

---

## 6.3 Interactive Timeline

The timeline is the main visualization feature of ChronoFlow.

Articles are displayed according to their publication dates.

Example:

```text
2022
 |
 ● Launch of ChatGPT
 |
 ● Growth of Generative AI

2023
 |
 ● GPT-4 Release
 |
 ● AI Regulation Discussions

2024
 |
 ● New Multimodal Models
```

### Timeline Features

- Chronological ordering
- Topic-based timeline
- Date range filtering
- Tag filtering
- Search
- Event detail view
- Responsive design

---

## 6.4 Search

Users can search for articles using keywords.

The system searches through:

- Article title
- Article summary
- Article content

Example:

```text
Search: ChatGPT
```

Possible results:

```text
Launch of ChatGPT
ChatGPT Adoption
ChatGPT and Education
```

---

## 6.5 Filters

Users can filter timeline events by:

### Topic

```text
Artificial Intelligence
```

### Date Range

```text
Start Date: 2022-01-01
End Date: 2024-12-31
```

### Tags

```text
AI
LLM
Technology
```

---

# 7. Database Design

## 7.1 Topics

### Table: `topics`

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | Topic name |
| description | Text | Topic description |
| created_at | DateTime | Creation time |

### Relationship

```text
One Topic
    |
    +---- Many Articles
```

---

## 7.2 Articles

### Table: `articles`

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| title | String | Article title |
| summary | Text | Short description |
| content | Text | Full content |
| source_url | String | Original source |
| published_date | Date | Article/event date |
| topic_id | Integer | Foreign key |
| created_at | DateTime | Creation time |
| updated_at | DateTime | Update time |

### AI Field

The following field can be added for semantic search:

| Column | Type | Description |
|---|---|---|
| embedding | Vector | Semantic representation of article |

---

## 7.3 Tags

### Table: `tags`

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | String | Tag name |

---

## 7.4 Article Tags

Articles and tags have a many-to-many relationship.

### Table: `article_tags`

| Column | Type |
|---|---|
| article_id | Integer |
| tag_id | Integer |

Relationship:

```text
Article A -----> AI
          -----> LLM

Article B -----> AI
          -----> Technology
```

---

# 8. Entity Relationship Overview

```text
                 TOPICS
                    |
                    | One-to-Many
                    v
                 ARTICLES
                    |
                    | Many-to-Many
                    v
              ARTICLE_TAGS
                    |
                    v
                   TAGS
```

---

# 9. API Standards

All APIs should:

- Use JSON.
- Validate input using Pydantic.
- Return meaningful HTTP status codes.
- Return clear error messages.
- Keep code modular and simple.
- Use database queries efficiently.

Base development URL:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 10. Health APIs

## Check API Health

### Endpoint

```http
GET /health
```

### Response

```json
{
  "status": "healthy"
}
```

---

# 11. Topic APIs

## Create Topic

```http
POST /topics
```

### Request

```json
{
  "name": "Artificial Intelligence",
  "description": "Important developments in artificial intelligence."
}
```

### Response

```json
{
  "id": 1,
  "name": "Artificial Intelligence",
  "description": "Important developments in artificial intelligence."
}
```

Status:

```text
201 Created
```

---

## Get All Topics

```http
GET /topics
```

---

## Get Topic by ID

```http
GET /topics/{topic_id}
```

Example:

```text
GET /topics/1
```

---

## Update Topic

```http
PUT /topics/{topic_id}
```

---

## Delete Topic

```http
DELETE /topics/{topic_id}
```

---

# 12. Article APIs

## Create Article

```http
POST /articles
```

### Request

```json
{
  "title": "Launch of ChatGPT",
  "summary": "ChatGPT was released for public use.",
  "content": "Detailed article content.",
  "source_url": "https://example.com/article",
  "published_date": "2022-11-30",
  "topic_id": 1,
  "tag_ids": [1, 2]
}
```

### Validation

- Title is required.
- Publication date is required.
- Topic must exist.
- Tag IDs must exist.

---

## Get All Articles

```http
GET /articles
```

---

## Get Article by ID

```http
GET /articles/{article_id}
```

The response should include:

- Article details
- Topic information
- Associated tags

---

## Update Article

```http
PUT /articles/{article_id}
```

---

## Delete Article

```http
DELETE /articles/{article_id}
```

---

# 13. Tag APIs

## Create Tag

```http
POST /tags
```

### Request

```json
{
  "name": "AI"
}
```

---

## Get All Tags

```http
GET /tags
```

---

## Update Tag

```http
PUT /tags/{tag_id}
```

---

## Delete Tag

```http
DELETE /tags/{tag_id}
```

---

# 14. Timeline API

The timeline endpoint provides chronological event data to the frontend.

## Get Timeline

```http
GET /timeline
```

### Supported Query Parameters

| Parameter | Description |
|---|---|
| topic_id | Filter by topic |
| start_date | Starting date |
| end_date | Ending date |
| tag_id | Filter by tag |
| search | Search keyword |

### Example

```text
GET /timeline?topic_id=1&start_date=2022-01-01&end_date=2024-12-31
```

### Suggested Response

```json
{
  "topic": {
    "id": 1,
    "name": "Artificial Intelligence"
  },
  "events": [
    {
      "id": 1,
      "title": "Launch of ChatGPT",
      "summary": "ChatGPT was released for public use.",
      "date": "2022-11-30",
      "tags": [
        "AI",
        "LLM"
      ]
    }
  ]
}
```

### Timeline Processing

```text
Receive User Filters
        |
        v
Build Database Query
        |
        v
Filter Articles
        |
        v
Sort by Date
        |
        v
Return Timeline Events
```

---

# 15. Search API

## Search Articles

```http
GET /search
```

### Query

```text
GET /search?q=chatgpt
```

Optional topic filter:

```text
GET /search?q=chatgpt&topic_id=1
```

### Search Targets

- Title
- Summary
- Content

### Response

```json
{
  "query": "chatgpt",
  "results": [
    {
      "id": 1,
      "title": "Launch of ChatGPT",
      "published_date": "2022-11-30"
    }
  ]
}
```

---

# 16. AI/ML System

ChronoFlow includes an AI-powered knowledge exploration feature.

The AI should answer questions based on relevant articles stored in the application.

This follows a **Retrieval-Augmented Generation (RAG)** approach.

---

# 17. RAG Workflow

```text
User Question
      |
      v
Generate Question Embedding
      |
      v
Search Similar Article Embeddings
      |
      v
Retrieve Relevant Articles
      |
      v
Send Question + Context to LLM
      |
      v
Generate Answer
      |
      v
Return Answer + Sources
```

Example question:

> How did Artificial Intelligence evolve in 2023?

The application:

1. Converts the question into an embedding.
2. Searches for semantically similar articles.
3. Retrieves the most relevant articles.
4. Sends the question and article context to the LLM.
5. Returns an answer with article sources.

---

# 18. AI APIs

## Ask AI

```http
POST /ai/ask
```

### Request

```json
{
  "question": "How did Artificial Intelligence evolve in 2023?",
  "topic_id": 1
}
```

### Response

```json
{
  "answer": "Artificial Intelligence experienced significant development in generative AI during 2023.",
  "sources": [
    {
      "article_id": 10,
      "title": "Growth of Generative AI"
    }
  ]
}
```

---

## Semantic Search

```http
GET /ai/search
```

Example:

```text
GET /ai/search?q=important+AI+developments
```

The backend performs vector similarity search and returns semantically relevant articles.

---

# 19. AI/ML Folder

```text
ai_ml/
|
+-- embeddings/
|   +-- generate_embeddings.py
|
+-- rag/
|   +-- rag_service.py
|
+-- services/
|   +-- llm_service.py
|   +-- semantic_search.py
|
+-- schemas/
|   +-- ai_response.py
|
+-- config.py
+-- requirements.txt
+-- .env.example
```

### Responsibilities

#### Embeddings

```text
Article
   |
   v
Embedding Model
   |
   v
Numerical Vector
   |
   v
PostgreSQL + pgvector
```

#### Semantic Search

Finds articles with similar meanings instead of only matching exact keywords.

#### RAG Service

Combines:

- User question
- Relevant articles
- LLM

and produces a source-supported answer.

---

# 20. Backend Folder Structure

```text
backend/
|
+-- app/
    |
    +-- database/
    |   +-- connection.py
    |   +-- base.py
    |
    +-- models/
    |   +-- topic.py
    |   +-- article.py
    |   +-- tag.py
    |
    +-- schemas/
    |   +-- topic.py
    |   +-- article.py
    |   +-- tag.py
    |
    +-- routes/
    |   +-- topics.py
    |   +-- articles.py
    |   +-- tags.py
    |   +-- timeline.py
    |   +-- search.py
    |   +-- ai.py
    |
    +-- main.py
```

---

# 21. Complete API List

```text
GET     /health

POST    /topics
GET     /topics
GET     /topics/{id}
PUT     /topics/{id}
DELETE  /topics/{id}

POST    /articles
GET     /articles
GET     /articles/{id}
PUT     /articles/{id}
DELETE  /articles/{id}

POST    /tags
GET     /tags
PUT     /tags/{id}
DELETE  /tags/{id}

GET     /timeline
GET     /search

POST    /ai/ask
GET     /ai/search
```

---

# 22. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 400 | Bad request |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error |

---

# 23. Environment Variables

Sensitive values must be stored in a `.env` file.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/chronoflow
```

The actual `.env` file must not be uploaded to GitHub.

An `.env.example` file can be committed:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/chronoflow
```

---

# 24. Development Order

Recommended implementation sequence:

```text
1. FastAPI Setup
        |
        v
2. PostgreSQL Connection
        |
        v
3. SQLAlchemy Configuration
        |
        v
4. Topic Model + APIs
        |
        v
5. Article Model + APIs
        |
        v
6. Tag Model + APIs
        |
        v
7. Timeline API
        |
        v
8. Search API
        |
        v
9. React Frontend Integration
        |
        v
10. Interactive Timeline
        |
        v
11. Embeddings + pgvector
        |
        v
12. Semantic Search
        |
        v
13. RAG + LLM Integration
```

---

# 25. Project Completion Checklist

## Backend

- [ ] FastAPI running
- [ ] PostgreSQL connected
- [ ] SQLAlchemy configured
- [ ] Topic APIs complete
- [ ] Article APIs complete
- [ ] Tag APIs complete
- [ ] Timeline API complete
- [ ] Search API complete
- [ ] AI APIs complete

## Frontend

- [ ] React application
- [ ] API integration
- [ ] Topic browsing
- [ ] Interactive timeline
- [ ] Date filtering
- [ ] Tag filtering
- [ ] Search interface
- [ ] Article details
- [ ] Responsive design
- [ ] AI question interface

## AI/ML

- [ ] Article embeddings
- [ ] pgvector configured
- [ ] Semantic search
- [ ] RAG workflow
- [ ] LLM integration
- [ ] Source citations

---

# 26. Project Goal

ChronoFlow aims to transform chronological information into an interactive and intelligent exploration experience.

The complete user experience is:

```text
Topic
  |
  v
Timeline
  |
  +--> Filters
  |
  +--> Search
  |
  +--> Article Details
  |
  v
AI-Powered Questions
  |
  v
Answer with Relevant Sources
```

> **ChronoFlow: Explore the evolution of ideas, events, and topics through time.**

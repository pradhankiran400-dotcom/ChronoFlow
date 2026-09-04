# ⏳ ChronoFlow

## Interactive Topic Timeline Platform

ChronoFlow is an interactive platform that helps users explore the evolution of topics, events, and ideas over time.

Instead of displaying information as a simple list, ChronoFlow organizes articles and important events on an interactive timeline. Users can explore topics, search for events, apply filters, and understand how a topic has evolved across different time periods.

---

## 🚀 Features

### Round 1 – Core Platform

- Create and manage topics
- Add, edit, and delete articles
- Organize articles according to their publication dates
- Interactive timeline visualization
- Search articles
- Filter articles by:
  - Date range
  - Topic
  - Tags
- View detailed article information
- Responsive user interface
- PostgreSQL database integration

### Round 2 – AI Features

- AI-powered question answering
- Semantic article search
- Article embeddings
- RAG-based responses
- Source-based AI answers
- Relevant article citations
- pgvector similarity search

---

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Database

- PostgreSQL

### AI/ML (Round 2)

- LLM API
- Embeddings
- RAG
- pgvector

---

## 📁 Project Structure

```text
ChronoFlow/
│
├── frontend/                 # React frontend
│
├── backend/                  # FastAPI backend
│   └── app/
│       ├── database/         # Database configuration
│       ├── models/           # Database models
│       ├── routes/           # API routes
│       ├── schemas/          # Pydantic schemas
│       └── main.py           # FastAPI application
│
├── ai_ml/                    # AI/ML features (Round 2)
│
├── venv/                     # Virtual environment (ignored by Git)
│
├── .env                      # Environment variables (ignored by Git)
├── .gitignore
├── requirements.txt
└── README.md

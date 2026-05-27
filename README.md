# 🩺 Mana
**Your Trusted Health Companion** — Supports Persian & English

> *When patients Google their symptoms or ask ChatGPT about their medications, they get answers — but not always the right ones. Mana gives them the right ones.*

---

## About

Every day, patients search the internet for answers about their health. They get blog posts, forum opinions, and AI-generated text that sounds confident but isn't grounded in anything real. They leave more confused than when they started — or worse, make decisions based on information that was simply wrong.

Mana is different. It answers health questions directly from verified clinical guidelines — the same standards doctors rely on. Ask about your blood sugar target, your blood pressure medication, or what a lab result means. Mana finds the answer in the actual guideline and gives it to you clearly, in your language.

**If the answer isn't in the guidelines, Mana says so.** An honest "I don't know" is worth more than a confident wrong answer.

---

## How It Works

```
You ask a question
        ↓
Mana searches 2,600+ chunks from clinical guidelines
        ↓
Finds the 6 most relevant passages via semantic search
        ↓
Answers ONLY from those passages — nothing else
        ↓
Response in your language, grounded in the source
```

This is **RAG (Retrieval-Augmented Generation)** — the AI answers from the specific documents we've curated, not from general training data. Like an open-book exam where the book is the ADA Standards of Care.

---

## Clinical Guidelines

| Guideline | Organization | Year |
|-----------|-------------|------|
| Standards of Medical Care in Diabetes | ADA | 2026 |
| Hypertension Guidelines | AHA/ACC | 2025 |
| *(actively expanding)* | | |

---

## ## 🔗 [Try Mana → huggingface.co/spaces/NafisehS/Mana](https://huggingface.co/spaces/NafisehS/Mana)
*Currently in private beta*

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | GPT-4o-mini |
| Vector Database | ChromaDB |
| Embeddings | OpenAI Ada-002 |
| RAG Framework | LangChain |
| UI | Gradio |
| PDF Processing | PyPDF |
| Deployment | HuggingFace Spaces |
| Language | Python 3.11 |

---

## Project Structure

```
mana/
├── data/
│   ├── *.pdf              # Clinical guidelines
│   └── chroma_db/         # Vector database (auto-generated)
├── src/
│   ├── __init__.py
│   └── prompt.py          # Central prompt — single source of truth
├── app.py                 # Main application
├── ingest.py              # PDF processor & database builder
├── requirements.txt
└── .env                   # API keys (never committed)
```

---

## Setup

```bash
conda create -n mana python=3.11.9 -y
conda activate mana
pip install -r requirements.txt
```

Add your OpenAI key to `.env`:
```
OPENAI_API_KEY=sk-...
```

Build the knowledge base:
```bash
python ingest.py
```

Run:
```bash
python app.py
```

---

## Adding Guidelines

1. Drop any guideline PDF into `data/`
2. Run `python ingest.py`

The pipeline automatically filters junk pages, chunks text intelligently, tags each chunk with its source, and rebuilds the database. No code changes needed.

---

## Design Principles

**Honesty over helpfulness** — Mana will not answer outside its knowledge base.

**Traceability** — Every answer is grounded in a specific passage from a specific page.

**Accessibility** — Persian and English supported. Designed for patients, usable by clinicians.

**Single source of truth** — One prompt file, one database, one place to change anything.

---

## Roadmap

- [ ] GOLD (COPD), GINA (Asthma), ESC Cardiac guidelines
- [ ] Patient health profile with consent-based data collection
- [ ] Doctor-facing clinical mode
- [ ] Telegram bot
- [ ] Mobile app

---

## Disclaimer

Mana provides information from clinical guidelines for educational purposes only. It does not provide medical diagnosis or personalized medical advice. Always consult a qualified healthcare professional for medical decisions.

---

*© 2026 Mana Health — All rights reserved*